# Nexus Assistant 🤖

**Nexus** is a **conversational, “bro‑style” AI desktop assistant** built with Python.  
It can:

- 🎤 **Listen & speak** (Windows SAPI TTS) with a casual tone.  
- 🖥️ **Open, close, install, uninstall, and type** into apps (e.g., Notepad).  
- 🌐 **Search the web** and **play YouTube videos** (smart fallback to the official site if the app isn’t installed).  
- 📸 **Capture & summarize the screen** (vision‑enabled).  
- ⏰ **Set reminders** with natural‑language timing.  
- 🖱️ **Run arbitrary shell commands** (PowerShell) for “do‑everything” requests.  
- 💬 **Chat naturally** – greetings, small talk, and casual replies using a “bro” persona.

## 🚀 Quick Start

1. **Clone the repo** (you already did)  
   ```bash
   git clone [https://github.com/jagannathanpraneeth-blip/Nexus_Assistant.git](https://github.com/jagannathanpraneeth-blip/Nexus_Assistant.git)
   cd Nexus_Assistant
   pip install -r requirements.txt
# you’ll need: speechrecognition, pyautogui, aiohttp, openai (or the provider you choose), etc.
OPENAI_API_KEY=your-openai-key   # or GOOGLE_API_KEY for Gemini
LLM_PROVIDER=openai               # openai | gemini | hybrid

Set environment variables (create a 
.env
 file)
dotenv
OPENAI_API_KEY=your-openai-key   # or GOOGLE_API_KEY for Gemini
LLM_PROVIDER=openai               # openai | gemini | hybrid
Run the assistant
python main.py
Say “Nexus” (or “Hey Nexus”) to wake it up.
Example commands:
Open Notepad and type hello world
Play never gonna give you up
Summarize my screen
Remind me to drink water in 5 minutes
Hey Nexus, how’s it going?
📂 Project Structure
Nexus_Assistant/
├─ .env                 # your secrets (git‑ignored)
├─ .gitignore           # excludes .env, DB, __pycache__, *.pyc
├─ main.py              # entry point – starts orchestrator, brain, voice loop, GUI
├─ core/
│   ├─ orchestrator.py  # task scheduler & executor
│   ├─ types.py         # Task, Event, statuses
│   └─ event_bus.py     # simple pub/sub system
├─ cognitive/
│   ├─ brain.py         # parses input, captures screen, creates tasks
│   └─ llm_interface.py # LLM wrappers (Mock, OpenAI, Gemini, Hybrid)
├─ integrations/
│   ├─ system.py        # OS actions (open app, type, screenshot, notifications)
│   ├─ web_search.py    # DuckDuckGo HTML search (no API key)
│   ├─ web_automation.py# YouTube search & auto‑play
│   └─ voice.py         # speech‑to‑text & text‑to‑speech
├─ ui/
│   ├─ desktop_gui.py   # simple Tkinter window for typed commands
│   └─ templates/
│       └─ index.html   # HTML UI (if you expand to a web front‑end)
└─ universal_agent.db   # tiny SQLite DB for task logging
🛠️ Customising the Persona
The “bro” tone is defined in 
cognitive/llm_interface.py
 system prompt.
If you want a more formal voice, just change the prompt or set the environment variable:
export NEXUS_FORMAL=true   # (or edit the prompt directly)
🔧 Known Issues & Fixes
pyautogui / cv2 import errors – resolved by running typing in a thread pool and catching the import error.
Screen‑summarisation – currently a mock response; replace the mock with a real vision model (e.g., OpenAI’s gpt‑4‑vision).
Git secret removal – 
.gitignore
 now excludes 
.env
 and the SQLite DB.
📜 License
MIT License – feel free to fork, tweak, and share!

Enjoy the vibe, bro!
If you run into any hiccups, just shout “Nexus” and ask for help. 🎧


Copy the whole block above into a new file named **README.md** at the root of your repository, commit, and push. Your repo will now have a nice landing page describing the project. Let me know if you’d like any tweaks!
