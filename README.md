# Coqui-TTS XTTSv2 Gradio Interface for RTX

Prosty interfejs dla technologii Coqui-TTS (XTTSv2) zoptymalizowany dla kart graficznych NVIDIA RTX, w tym najnowszej serii **50xx** (CUDA 12.8), a także systemów bez GPU (CPU).

## 🚀 Zalety i Instalacja

- **Ekstremalnie prosta instalacja**: Dzięki plikowi `INSTALL.bat` całe środowisko (Python, venv, sterowniki CUDA) konfiguruje się automatycznie.
- **Wsparcie RTX 50xx**: Pełna optymalizacja pod najnowsze jednostki NVIDIA dzięki wsparciu CUDA 12.8.
- **Gotowość do pracy**: Pierwsza instalacja konfiguruje wszystko, a każde kolejne uruchomienie odbywa się błyskawicznie poprzez `START_GRADIO.bat`.

### Instrukcja instalacji na Windows:

1. Zainstaluj **Git** w swoim systemie (pobierz z [git-scm.com](https://git-scm.com/)).
2. Otwórz terminal (CMD lub PowerShell), przejdź do folderu gdzie chcesz trzymać projekt i pobierz repozytorium:
   ```bash
   git clone https://github.com/alkemiik-coder/GRADIO-XTTSv2-PL.git
   cd GRADIO-XTTSv2-PL
   ```
3. Uruchom plik **`INSTALL.bat`** dwukrotnym kliknięciem.
4. Poczekaj na zakończenie procesu (może to zająć od 5 do 15 minut). Po wszystkim aplikacja uruchomi się automatycznie w przeglądarce pod adresem `http://127.0.0.1:7860`.

### 📂 Folder Wynikowy (Outputs)
Wszystkie wygenerowane pliki audio są automatycznie zapisywane w folderze **`outputs`** w głównym katalogu projektu. Każde nagranie ma unikalną nazwę, co ułatwia zarządzanie sesjami.

> [!IMPORTANT]
> Instalator automatycznie pobiera dedykowaną, przenośną wersję **Python 3.10.9**. Nie musisz posiadać zainstalowanego Pythona w systemie ani konfigurować zmiennych środowiskowych.

## ⚖️ Licencja Głosów (Użytek Komercyjny)

Wszystkie głosy zawarte w folderze `targets` są na licencji **"Madafaka Free"**. Zostały wygenerowane syntetycznie i są w pełni **gotowe do użytku komercyjnego**. Możesz ich używać w swoich filmach, grach czy prezentacjach bez żadnych opłat i bez konieczności podawania autora.

---

# Coqui-TTS XTTSv2 Gradio Interface for RTX (English)

A simple interface for Coqui-TTS (XTTSv2) technology, optimized for NVIDIA RTX graphics cards, including the latest **50xx series** (CUDA 12.8), as well as CPU-only systems.

## 🚀 Key Features & Installation

- **Dead Simple Installation**: Using the `INSTALL.bat` file, the entire environment (Python, venv, CUDA drivers) is configured automatically.
- **RTX 50xx Support**: Fully optimized for the latest NVIDIA hardware using CUDA 12.8.
- **Ready for Action**: The initial setup handles everything, and every subsequent launch is lightning-fast via `START_GRADIO.bat`.

### Installation Instructions for Windows:

1. Install **Git** on your system (get it from [git-scm.com](https://git-scm.com/)).
2. Open a terminal (CMD or PowerShell), navigate to your desired directory and clone the repository:
   ```bash
   git clone https://github.com/alkemiik-coder/GRADIO-XTTSv2-PL.git
   cd [FOLDER_NAME]
   ```
3. Run the **`INSTALL.bat`** file by double-clicking it.
4. Wait for the process to finish (it may take 5 to 15 minutes). Once complete, the application will open automatically in your browser at `http://127.0.0.1:7860`.

### 📂 Output Folder (Outputs)
All generated audio files are automatically saved in the **`outputs`** folder within the main project directory. Each recording is given a unique name for easy session management.

> [!IMPORTANT]
> The installer automatically downloads a dedicated, portable **Python 3.10.9** version. You don't need to have Python installed on your system or configure any environment variables.

## ⚖️ Voice License (Commercial Use)

All voices included in the `targets` folder are under the **"Madafaka Free"** license. They have been synthetically generated and are fully **ready for commercial use**. You can use them in your videos, games, or presentations with no fees and no attribution required.

---
*Ciesz się szybką generacją mowy! / Enjoy your fast speech generation!*


