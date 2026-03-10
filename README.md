# Dorwal AI 🤖

**Dorwal AI** is an offline intelligent desktop assistant inspired by JARVIS.  
Built with Python and Tkinter, it supports voice commands, note-taking, reminders, and AI-driven responses — all without an internet connection.

---

## ✨ Features

| Feature | Status |
|---|---|
| 🎤 Voice input (microphone) | ✅ Working |
| 💬 Text input | ✅ Working |
| 🧠 Rule-based AI responses | ✅ Working |
| 📝 Notes (add / view / delete) | ✅ Working |
| ⏰ Reminders (add / view / delete) | ✅ Working |
| 📁 File / folder commands | ✅ Working |
| 🔊 Text-to-speech (TTS) | 🔜 Planned |
| 🧬 Local LLM integration | 🔜 Planned |

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| Python 3.8+ | Core language |
| Tkinter | GUI (built into Python) |
| SpeechRecognition | Microphone input |
| PyAudio | Microphone hardware access |
| pyttsx3 | Offline text-to-speech (future) |
| JSON | Local storage for notes & reminders |

---

## 📁 Project Structure

```
desktop-file-manager/
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore
├── README.md
├── core/
│   ├── __init__.py
│   ├── gui.py           # Tkinter GUI
│   ├── voice.py         # Microphone → text transcription
│   ├── ai.py            # Rule-based AI response engine
│   └── commands.py      # Command parser + notes/reminders logic
├── data/
│   ├── notes.json       # Persisted notes
│   └── reminders.json   # Persisted reminders
└── models/              # Future: local AI model files (e.g., Vosk)
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/desktop-file-manager.git
cd desktop-file-manager
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note for Linux users:** You may need to install PortAudio first:
> ```bash
> sudo apt-get install portaudio19-dev python3-pyaudio
> ```

> **Note for macOS users:**
> ```bash
> brew install portaudio
> ```

### 4. Run the app

```bash
python main.py
```

---

## 💬 Supported Commands

| What you say / type | What happens |
|---|---|
| `hello` / `hi` | Greeting response |
| `what time is it` | Current time |
| `what's today's date` | Current date |
| `tell me a joke` | Random developer joke |
| `motivate me` | Motivational quote |
| `add note Buy groceries` | Saves a note |
| `show notes` | Lists all notes |
| `delete note 0` | Deletes note at index 0 |
| `remind me to call Mom` | Saves a reminder |
| `show reminders` | Lists all reminders |
| `delete reminder 0` | Deletes reminder at index 0 |
| `list files` | Lists files in home directory |
| `open folder C:\Users` | Opens folder in file explorer |
| `help` | Shows all capabilities |

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Dorwal AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

> **Status:** 🚧 Under Active Development
