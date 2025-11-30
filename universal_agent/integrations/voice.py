import speech_recognition as sr
import threading
import asyncio
from typing import Callable, Awaitable

class VoiceInterface:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Optimize for faster recognition
        self.recognizer.energy_threshold = 4000  # Higher threshold for better noise filtering
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5  # Shorter pause = faster response
        
        self.is_listening = False
        self.tts_available = False
        self.engine = None
        
        # Try to initialize TTS using Windows SAPI directly
        try:
            import win32com.client
            self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
            
            # Set faster speech rate (range: -10 to 10, default is 0)
            self.speaker.Rate = 2  # Faster speech
            
            # Try to use a different voice (usually David or Zira)
            voices = self.speaker.GetVoices()
            if voices.Count > 1:
                # Use second voice if available (usually male voice)
                self.speaker.Voice = voices.Item(1)
            
            self.tts_available = True
            print("[VOICE] Text-to-Speech initialized successfully (Windows SAPI).")
            print(f"[VOICE] Using voice: {self.speaker.Voice.GetDescription()}")
            print(f"[VOICE] Speech rate: {self.speaker.Rate}")
        except Exception as e:
            print(f"[VOICE] Text-to-Speech not available: {e}")
            print("[VOICE] Voice recognition will still work, but responses will be text-only.")
            self.speaker = None

    def speak(self, text: str):
        print(f"[VOICE] {text}")
        if self.tts_available:
            try:
                import pythoncom
                pythoncom.CoInitialize()
                if not self.speaker:
                    import win32com.client
                    self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
                    self.speaker.Rate = 2  # Faster
                
                # Use async speak for non-blocking
                self.speaker.Speak(text, 1)  # 1 = SVSFlagsAsync (non-blocking)
            except Exception as e:
                print(f"[VOICE] TTS error: {e}")

    def listen_once(self) -> str:
        with sr.Microphone() as source:
            # Quick ambient noise adjustment (only 0.3 seconds)
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            print("[VOICE] Listening...")
            try:
                # Reduced timeout for faster response
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                print(f"[VOICE] Heard: {text}")
                return text
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                print(f"[VOICE] Error: {e}")
                return ""

    async def start_listening_loop(self, callback: Callable[[str], Awaitable[None]]):
        self.is_listening = True
        print("[VOICE] Voice Loop Started. Say 'Nexus' or 'Hey Nexus' to activate.")
        print("[VOICE] Say 'Stop Listening' to pause.")
        
        while self.is_listening:
            # Run blocking listen in a thread to not block asyncio loop
            text = await asyncio.to_thread(self.listen_once)
            
            if text:
                text_lower = text.lower()
                
                # Check for stop command
                if "stop listening" in text_lower:
                    self.speak("Pausing voice interface.")
                    self.is_listening = False
                    break
                
                # Wake word detection
                if text_lower.startswith("nexus") or text_lower.startswith("hey nexus"):
                    # Remove wake word from command
                    command = text.replace("Nexus", "", 1).replace("nexus", "", 1).strip()
                    command = command.replace("Hey", "", 1).replace("hey", "", 1).strip()
                    
                    if command:
                        print(f"[VOICE] Wake word detected! Command: {command}")
                        # Don't say "Yes?" - just process immediately for speed
                        await callback(command)
                    else:
                        self.speak("How can I help?")
                else:
                    # Ignore commands without wake word
                    print(f"[VOICE] Ignored (no wake word): {text}")
