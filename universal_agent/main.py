import asyncio
import threading
from core.event_bus import EventBus, Event
from core.orchestrator import TaskOrchestrator
from core.types import Task
from cognitive.brain import Brain

def main():
    try:
        print("=" * 50)
        print("  NEXUS - Universal Digital Agent")
        print("=" * 50)
        print()
        
        # Initialize Core (need to run in thread since we're not in async context)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        event_bus = EventBus()
        orchestrator = TaskOrchestrator(event_bus)

        # Subscribe to events for logging
        async def log_event(event: Event):
            print(f"[EVENT] {event.name}: {event.payload}")

        event_bus.subscribe("task_submitted", log_event)
        event_bus.subscribe("task_started", log_event)
        event_bus.subscribe("task_completed", log_event)
        event_bus.subscribe("task_failed", log_event)

        print("[INIT] Orchestrator initialized (immediate execution mode)")

        # Initialize Cognitive Layer
        print("[INIT] Initializing Brain...")
        brain = Brain(orchestrator)

        # Initialize Voice Interface
        print("[INIT] Initializing Voice Interface...")
        from integrations.voice import VoiceInterface
        voice = VoiceInterface()

        # Voice Feedback System
        async def voice_feedback(event: Event):
            if event.name == "task_completed":
                result = event.payload.get("result", "")
                # Don't speak long results, just summary
                if len(str(result)) > 100:
                    voice.speak("Task completed.")
                else:
                    voice.speak(f"Done. {result}")
            elif event.name == "task_failed":
                error = event.payload.get("error", "")
                voice.speak(f"I encountered an error: {error}")
            elif event.name == "task_started":
                # Optional: speak when starting? Might be too chatty.
                pass

        event_bus.subscribe("task_completed", voice_feedback)
        event_bus.subscribe("task_failed", voice_feedback)

        # Initialize Desktop GUI
        print("[INIT] Launching Desktop GUI...")
        from ui.desktop_gui import NexusGUI
        gui = NexusGUI(brain, voice)

        print("[READY] Nexus is ready!")
        print("[INFO] Voice: Say 'Nexus' to activate")
        print("[INFO] GUI: Type commands in the window")
        print()
        
        # Start Voice Loop in background thread
        def voice_thread():
            try:
                asyncio.run(voice.start_listening_loop(brain.process_input))
            except Exception as e:
                print(f"[VOICE ERROR] {e}")
        
        threading.Thread(target=voice_thread, daemon=True).start()

        # Run GUI (blocking)
        gui.run()
        
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
