# Nexus Assistant 🤖

**Nexus** is a **conversational, "bro‑style" AI desktop assistant** built with Python. It listens, speaks, and helps you with desktop tasks in a casual, friendly tone.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/LLM-OpenAI%2FGemini-green.svg)](https://openai.com/)

## ✨ Features

- 🎤 **Listen & speak** – Windows SAPI TTS with casual "bro" persona
- 🖥️ **App Control** – Open, close, install, uninstall, and type into applications
- 🌐 **Web Integration** – Search the web and play YouTube videos (smart fallback to official site)
- 📸 **Screen Capture** – Capture and summarize your screen (vision-enabled)
- ⏰ **Reminders** – Set reminders with natural-language timing
- 🖱️ **Shell Commands** – Run arbitrary PowerShell commands for advanced tasks
- 💬 **Natural Chat** – Greetings, small talk, and casual conversation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows OS (for SAPI TTS support)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jagannathanpraneeth-blip/Nexus_Assistant.git
   cd Nexus_Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Includes: speechrecognition, pyautogui, aiohttp, openai, etc.*

3. **Configure environment variables**
   Create a `.env` file in the project root:
   ```bash
   # Choose your LLM provider
   OPENAI_API_KEY=your-openai-api-key-here   # or GOOGLE_API_KEY for Gemini
   LLM_PROVIDER=openai                       # options: openai | gemini | hybrid
   ```

### Running Nexus

```bash
python main.py
```

**Wake word:** Say "Nexus" or "Hey Nexus" to activate the assistant.

## 📖 Usage Examples

| Command | Action |
|---------|--------|
| `"Open Notepad and type hello world"` | Opens Notepad and types the text |
| `"Play never gonna give you up"` | Searches and plays the video on YouTube |
| `"Summarize my screen"` | Captures and summarizes current screen content |
| `"Remind me to drink water in 5 minutes"` | Sets a reminder with notification |
| `"Hey Nexus, how's it going?"` | Casual conversation with the assistant |
| `"Search for Python tutorials"` | Performs web search |

## 📁 Project Structure

```
Nexus_Assistant/
├── .env                    # Environment variables (git-ignored)
├── .gitignore             # Excludes .env, DB, cache files
├── main.py                # Entry point - starts orchestrator, brain, voice loop, GUI
├── core/
│   ├── orchestrator.py    # Task scheduler & executor
│   ├── types.py           # Task, Event, statuses
│   └── event_bus.py       # Simple pub/sub system
├── cognitive/
│   ├── brain.py           # Parses input, captures screen, creates tasks
│   └── llm_interface.py   # LLM wrappers (Mock, OpenAI, Gemini, Hybrid)
├── integrations/
│   ├── system.py          # OS actions (open app, type, screenshot, notifications)
│   ├── web_search.py      # DuckDuckGo HTML search (no API key)
│   ├── web_automation.py  # YouTube search & auto-play
│   └── voice.py           # Speech-to-text & text-to-speech
├── ui/
│   ├── desktop_gui.py     # Tkinter window for typed commands
│   └── templates/
│       └── index.html     # HTML UI (for web front-end expansion)
└── universal_agent.db     # SQLite DB for task logging
```

## 🎭 Customizing the Persona

The "bro" tone is defined in `cognitive/llm_interface.py` system prompt. 

To change the personality:

1. **Edit the prompt directly** in `llm_interface.py`
2. **Or use environment variable**:
   ```bash
   export NEXUS_FORMAL=true   # Changes to a more formal tone
   ```

## 🔧 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **pyautogui / cv2 import errors** | Run typing in a thread pool and catch import errors |
| **Screen summarization not working** | Currently uses mock response; replace with real vision model (e.g., OpenAI's GPT-4 Vision) |
| **Git secret exposure** | `.gitignore` excludes `.env` and SQLite DB - ensure sensitive files aren't committed |
| **Speech recognition issues** | Check microphone permissions and try different speech recognition backends |

### Development Notes

- **Mock Vision**: The screen summarization feature currently returns a mock response. Replace with actual vision API calls in the code.
- **Windows Focus**: Some automation features require appropriate window focus and permissions.
- **Thread Safety**: UI interactions and voice processing run in separate threads to prevent blocking.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and various open-source libraries
- Inspired by modern AI assistant architectures
- Thanks to the open-source community for excellent tools and libraries

## 📞 Contact

**Project Link:** [https://github.com/jagannathanpraneeth-blip/Nexus_Assistant](https://github.com/jagannathanpraneeth-blip/Nexus_Assistant)

**Enjoy the vibe, bro!** 🎧

If you run into any hiccups, just shout "Nexus" and ask for help.

---
