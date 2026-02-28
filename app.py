import warnings
# Suppress annoying warnings BEFORE other imports
warnings.filterwarnings("ignore", category=FutureWarning, message=".*pytree.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*Dropdown.*")

import torch
import torchaudio
import os
import soundfile as sf

# Aggressive torchaudio.load monkeypatch for PyTorch 2.10 Blackwell compatibility
def patched_torchaudio_load(filepath, *args, **kwargs):
    # Use soundfile directly to load the audio
    data, samplerate = sf.read(filepath)
    # Convert to torch tensor [channels, frames]
    tensor = torch.from_numpy(data)
    if tensor.ndim == 1:
        tensor = tensor.unsqueeze(0)
    else:
        tensor = tensor.t()
    return tensor.float(), samplerate

torchaudio.load = patched_torchaudio_load

# Patch torch.load to avoid weights_only error in PyTorch 2.6+
orig_load = torch.load
def hooked_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return orig_load(*args, **kwargs)
torch.load = hooked_load

import gradio as gr
import platform
import random
import json
from pathlib import Path

# --- MONKEY PATCH FOR TRANSFORMERS ---
# Fixes ImportError: cannot import name 'isin_mps_friendly' from 'transformers.pytorch_utils'
try:
    import transformers.pytorch_utils
    if not hasattr(transformers.pytorch_utils, "isin_mps_friendly"):
        # Fallback to 'isin' or a dummy function to prevent crash
        target = getattr(transformers.pytorch_utils, "isin", None)
        if target is None:
            # Absolute fallback to prevent TypeError if called
            def dummy_isin(tensor, values):
                import torch
                return torch.isin(tensor, torch.tensor(values).to(tensor.device))
            target = dummy_isin
        transformers.pytorch_utils.isin_mps_friendly = target
except Exception:
    pass
# -------------------------------------

# Note: The 'coqui-tts' package installs its code under the 'TTS' namespace.
# Even though the package name is 'coqui-tts', the import below MUST remain as 'TTS'.
from TTS.api import TTS
import uuid
import html

def is_mac_os():
    return platform.system() == 'Darwin'

params = {
    "activate": True,
    "autoplay": True,
    "show_text": False,
    "remove_trailing_dots": False,
    "voice": "Rogger.wav",
    "language": "English",
    "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
}

# SUPPORTED_FORMATS = ['wav', 'mp3', 'flac', 'ogg']
SAMPLE_RATE = 16000
device = None

# Improved device detection (support for CPU-only environments like VMs)
if is_mac_os():
    device = torch.device('cpu')
else:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(f"Using device: {device}")

# Load model
tts = TTS(model_name=params["model_name"]).to(device)

def update_speakers():
    # Strictly use files from the targets folder
    speakers = {p.stem: str(p) for p in list(Path('targets').glob("*.wav"))}
    return sorted(list(speakers.keys()))

def get_default_speaker():
    speakers = update_speakers()
    return speakers[0] if speakers else None

def update_dropdown(_=None, selected_speaker=None):
    choices = update_speakers()
    if not selected_speaker and choices:
        selected_speaker = choices[0]
    return gr.Dropdown(choices=choices, value=selected_speaker, label="Wybierz Mówcę")

def gen_voice(string, spk, speed, english):
    string = html.unescape(string)
    short_uuid = str(uuid.uuid4())[:8]
    fl_name='outputs/' + spk + "-" + short_uuid +'.wav'
    output_file = Path(fl_name)
    this_dir = str(Path(__file__).parent.resolve())
    tts.tts_to_file(
        text=string,
        speed=speed,
        file_path=output_file,
        speaker_wav=[f"{this_dir}/targets/" +spk + ".wav"],
        language=languages[english]
    )
    return output_file

def handle_recorded_audio(audio_data, speaker_dropdown, filename = "użytkownik"):
    if not audio_data:
        return speaker_dropdown
    
    sample_rate, audio_content = audio_data
    save_path = f"targets/{filename}.wav"

    # Write the audio content to a WAV file
    sf.write(save_path, audio_content, sample_rate)

    # Create a new Dropdown with the updated speakers list, including the recorded audio
    return update_dropdown(selected_speaker=filename)


# Load the language data
with open(Path('languages.json'), encoding='utf8') as f:
    languages = json.load(f)

# Custom CSS to hide the interactive icons (fullscreen, download, share) specifically on the avatar
css = """
#avatar button { display: none !important; }
#avatar [data-testid="download-button"] { display: none !important; }
#avatar .icon-button { display: none !important; }
"""

# Gradio Blocks interface
with gr.Blocks(title="XTTS-2 UI Klonowanie Głosu", css=css) as app:
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Image("info/avatar.jpg", elem_id="avatar", show_label=False, width=80, height=80, container=False, interactive=False)
        with gr.Column(scale=9):
            gr.Markdown("# Klonowanie głosu oparte na Coqui XTTS-2")
            gr.Markdown("### Technologia: Coqui-TTS (Fork) | Created by Alkemiik")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(lines=3, label="Tekst do przetworzenia", value="To determinuje twoją żółć i moje wszędobylstwo. Zastanowić się można czy szaszłyki to dobre posiłki.")
            speed_slider = gr.Slider(label='Prędkość', minimum=0.1, maximum=1.99, value=1.3, step=0.01)
            language_dropdown = gr.Dropdown(list(languages.keys()), label="Język / Akcent", value="Polish")

            gr.Markdown("### Wybór mówcy i klonowanie głosu")
            
            with gr.Row():
                with gr.Column():
                    speaker_dropdown = update_dropdown()
                    refresh_button = gr.Button("Odśwież Głosy")
                with gr.Column():
                    filename_input = gr.Textbox(label="Dodaj nowego mówcę", placeholder="Wpisz nazwę dla swojego nagrania")
                    save_button = gr.Button("Zapisz nagranie")
                
            refresh_button.click(fn=update_dropdown, inputs=[], outputs=speaker_dropdown)

            with gr.Row():
                record_button = gr.Audio(label="Nagraj swój głos (ok. 10 sekund)")
                
            save_button.click(fn=handle_recorded_audio, inputs=[record_button, speaker_dropdown, filename_input], outputs=speaker_dropdown)
            record_button.stop_recording(fn=handle_recorded_audio, inputs=[record_button, speaker_dropdown, filename_input], outputs=speaker_dropdown)
            record_button.upload(fn=handle_recorded_audio, inputs=[record_button, speaker_dropdown, filename_input], outputs=speaker_dropdown)
            
            submit_button = gr.Button("Generuj Głos", variant="primary")

        with gr.Column():
            audio_output = gr.Audio(label="Wygenerowany Dźwięk")

    submit_button.click(
        fn=gen_voice,
        inputs=[text_input, speaker_dropdown, speed_slider, language_dropdown],
        outputs=audio_output
    )

if __name__ == "__main__":
    app.launch(inbrowser=True)