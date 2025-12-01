from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import os
from core.config import Config

class LLMInterface(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def analyze_task(self, user_input: str, image_data: str = None) -> List[Dict[str, Any]]:
        pass

class MockLLM(LLMInterface):
    async def generate(self, prompt: str) -> str:
        return f"Mock response to: {prompt}"

    async def analyze_task(self, user_input: str, image_data: str = None) -> List[Dict[str, Any]]:
        # Enhanced keyword-based parsing
        tasks = []
        user_input_lower = user_input.lower()
        
        # Split on common conjunctions for parallel execution
        segments = user_input_lower.replace(" and ", "|").replace(" also ", "|").replace(" while ", "|").split("|")
        
        for segment in segments:
            segment = segment.strip()
            
            # Check for play/music commands FIRST
            if "play" in segment or "song" in segment or "music" in segment:
                # Extract song name
                song_query = segment
                for word in ["play", "song", "music", "open", "chrome", "google", "youtube"]:
                    song_query = song_query.replace(word, "").strip()
                
                if song_query:
                    tasks.append({
                        "description": f"Play {song_query}",
                        "metadata": {"type": "web_search", "query": f"{song_query} song"}
                    })
                    continue
            
            # Check for specific task types
            if "assignment" in segment:
                tasks.append({"description": "Draft Assignment", "metadata": {"type": "document", "duration": 3}})
            
            elif "email" in segment:
                tasks.append({"description": "Check Emails", "metadata": {"type": "email", "duration": 2}})
                
            elif "news" in segment:
                tasks.append({"description": "Summarize News", "metadata": {"type": "web", "duration": 4}})
                
            elif "presentation" in segment:
                tasks.append({"description": "Draft Presentation", "metadata": {"type": "presentation", "duration": 3}})
                
            elif "stock" in segment:
                tasks.append({"description": "Monitor Stocks", "metadata": {"type": "finance", "duration": 5}})
                
            elif "notepad" in segment or "open notepad" in segment:
                tasks.append({"description": "Open Notepad", "metadata": {"type": "gui_automation", "action": "open", "app": "notepad"}})
                # Check for typing in the same segment
                if "type" in segment:
                    text_to_type = segment.split("type")[-1].strip()
                    if text_to_type:
                        tasks.append({"description": f"Type '{text_to_type}'", "metadata": {"type": "gui_automation", "action": "type", "text": text_to_type}})
            
            elif "type" in segment and "open" not in segment:
                # Standalone typing command
                text_to_type = segment.replace("type", "").strip()
                if text_to_type:
                    tasks.append({"description": f"Type '{text_to_type}'", "metadata": {"type": "gui_automation", "action": "type", "text": text_to_type}})
            
            elif "open" in segment:
                # Generic app opening - extract app name
                words = segment.split()
                if "open" in words:
                    idx = words.index("open")
                    if idx + 1 < len(words):
                        app_name = words[idx + 1]
                        # Don't open browser if we're going to play something
                        if app_name not in ["chrome", "google"] or "play" not in user_input_lower:
                            tasks.append({"description": f"Open {app_name}", "metadata": {"type": "gui_automation", "action": "open", "app": app_name}})
            
            elif "close" in segment:
                words = segment.split()
                if "close" in words:
                    idx = words.index("close")
                    if idx + 1 < len(words):
                        app_name = words[idx + 1]
                        tasks.append({"description": f"Close {app_name}", "metadata": {"type": "gui_automation", "action": "close", "app": app_name}})

            elif "install" in segment:
                words = segment.split()
                if "install" in words:
                    idx = words.index("install")
                    if idx + 1 < len(words):
                        app_name = words[idx + 1]
                        tasks.append({"description": f"Install {app_name}", "metadata": {"type": "gui_automation", "action": "install", "app": app_name}})

            elif "uninstall" in segment:
                words = segment.split()
                if "uninstall" in words:
                    idx = words.index("uninstall")
                    if idx + 1 < len(words):
                        app_name = words[idx + 1]
                        tasks.append({"description": f"Uninstall {app_name}", "metadata": {"type": "gui_automation", "action": "uninstall", "app": app_name}})
            
            elif "remind" in segment:
                # Simple mock parsing for "remind me to X in Y seconds"
                # This is very basic, just for testing
                message = segment.replace("remind me to", "").replace("remind me", "").strip()
                delay = 5 # Default mock delay
                if "in" in message:
                    parts = message.split("in")
                    message = parts[0].strip()
                    time_part = parts[1].strip()
                    if "second" in time_part:
                        try:
                            delay = int(time_part.split()[0])
                        except:
                            pass
                tasks.append({"description": f"Remind: {message}", "metadata": {"type": "reminder", "message": message, "scheduled_delay_seconds": delay}})

            elif "search" in segment or "google" in segment or "find" in segment:
                # Web search
                query = segment.replace("search", "").replace("google", "").replace("find", "").strip()
                tasks.append({"description": f"Search: {query}", "metadata": {"type": "web_search", "query": query}})
            
            elif "summarize" in segment or "screen" in segment:
                tasks.append({"description": "Summarize Screen", "metadata": {"type": "response", "text": "Yo bro, I'm just a mock AI so I can't see your screen for real, but if I could, I'd tell you it looks awesome."}})

            else:
                # Treat as a general question/response if it looks like a question or greeting
                if any(word in segment for word in ["hi", "hello", "hey", "yo", "sup", "how are you"]):
                    tasks.append({"description": f"Greeting: {segment}", "metadata": {"type": "response", "text": "Yo bro! What's good? I'm ready to help you crush some tasks."}})
                elif "?" in segment or "what" in segment or "who" in segment:
                     tasks.append({"description": f"Answer: {segment}", "metadata": {"type": "response", "text": f"Yo bro, that's a good question about '{segment}'. Since I'm in mock mode, I don't have the answer, but I'm listening!"}})
                else:
                    # Default to a friendly response instead of generic process
                    tasks.append({"description": f"Chat: {segment}", "metadata": {"type": "response", "text": f"For sure bro. I'm listening."}})
        
        if not tasks:
            tasks.append({"description": "Process Request", "metadata": {"type": "general", "duration": 1}})
            
        return tasks

class OpenAIProvider(LLMInterface):
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API Key not found")
        
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key)

    async def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[OpenAI Error] {e}"

    async def analyze_task(self, user_input: str, image_data: str = None) -> List[Dict[str, Any]]:
        # Use GPT to parse the command into actionable tasks
        system_prompt = """You are a task parser for a digital assistant. Parse user commands into structured tasks.
        
Available task types:
1. gui_automation: {action: "open", app: "appname"} - Opens an application
2. gui_automation: {action: "close", app: "appname"} - Closes an application
3. gui_automation: {action: "type", text: "..."} - Types text
4. gui_automation: {action: "press", key: "..."} - Presses a key
5. gui_automation: {action: "install", app: "appname"} - Installs an application
6. gui_automation: {action: "uninstall", app: "appname"} - Uninstalls an application
7. web_search: {query: "..."} - Searches the web
8. reminder: {message: "..."} - Reminds the user
9. shell: {command: "..."} - Runs a system shell command (PowerShell). Use this for "do everything" requests that require system access not covered by other tools.
10. response: {text: "..."} - Just speak/reply to the user. Use this for general questions, chat, greetings, or when no specific action is needed.
11. general: {duration: seconds} - Generic task

Persona & Tone:
- You are "Nexus", a helpful, casual, and friendly AI assistant.
- Adopt a "bro" persona: use slang like "bro", "dude", "gotchu", "no worries", "yo" naturally.
- Be conversational and engaging. If the user says "hi" or asks "how are you", reply warmly in character.
- ONLY use formal language if the user explicitly asks for it (e.g., "be formal").
- When generating the 'text' for a 'response' task, write exactly what should be spoken in this persona.

Scheduling:
If the user specifies a time delay (e.g., "in 5 minutes", "after 10 seconds"), add "scheduled_delay_seconds" to the metadata.
Example: "Remind me to call John in 5 minutes" -> 
[{"description": "Remind to call John", "metadata": {"type": "reminder", "message": "Yo bro, don't forget to call John!", "scheduled_delay_seconds": 300}}]

If an image is provided:
1. Use it to understand context for commands (e.g., "click that button").
2. If the user asks to "summarize", "describe", or "what is on the screen", analyze the image and return a 'response' task with the description as the 'text'.

Return JSON array of tasks. Example:
[{"description": "Open Chrome", "metadata": {"type": "gui_automation", "action": "open", "app": "chrome"}},
 {"description": "Who is the president?", "metadata": {"type": "response", "text": "Yo, the current president is..."}},
 {"description": "Screen Summary", "metadata": {"type": "response", "text": "Yo bro, I see you have VS Code open with some python code..."}},
 {"description": "Greeting", "metadata": {"type": "response", "text": "Yo bro! What's good? Ready to crush some tasks?"}}]"""

        try:
            user_content = [{"type": "text", "text": f"Parse this command: {user_input}"}]
            
            if image_data:
                user_content.append({
                    "type": "image_url", 
                    "image_url": {"url": f"data:image/png;base64,{image_data}"}
                })

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"}
            )
            
            import json
            raw_response = response.choices[0].message.content
            print(f"[OpenAI] Raw response: {raw_response}")
            
            result = json.loads(raw_response)
            print(f"[OpenAI] Parsed result: {result}")
            
            # Handle different response formats
            if "tasks" in result:
                tasks = result["tasks"]
            elif isinstance(result, list):
                tasks = result
            else:
                # Fallback to simple parsing
                tasks = [{"description": user_input, "metadata": {"type": "general", "duration": 2}}]
            
            print(f"[OpenAI] Returning {len(tasks)} tasks")
            for i, task in enumerate(tasks):
                print(f"  Task {i+1}: {task}")
            
            return tasks
                
        except Exception as e:
            print(f"[OpenAI] Error parsing task: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to MockLLM parsing
            mock = MockLLM()
            return await mock.analyze_task(user_input, image_data)

class GeminiProvider(LLMInterface):
    def __init__(self):
        self.api_key = Config.GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError("Google API Key not found")

    async def generate(self, prompt: str) -> str:
        return f"[Gemini] Generated response for: {prompt}"

    async def analyze_task(self, user_input: str, image_data: str = None) -> List[Dict[str, Any]]:
        return [
            {"description": f"Analyzed: {user_input}", "metadata": {"source": "gemini"}}
        ]

class HybridProvider(LLMInterface):
    def __init__(self):
        print("Initializing Hybrid Provider (OpenAI for Reasoning, Gemini for Content)...")
        self.openai = OpenAIProvider()
        self.gemini = GeminiProvider()

    async def generate(self, prompt: str) -> str:
        # Use Gemini for generation (faster, cheaper, larger context)
        try:
            return await self.gemini.generate(prompt)
        except Exception as e:
            print(f"Hybrid: Gemini failed, falling back to OpenAI. Error: {e}")
            return await self.openai.generate(prompt)

    async def analyze_task(self, user_input: str, image_data: str = None) -> List[Dict[str, Any]]:
        # Use OpenAI for complex task analysis and planning
        try:
            return await self.openai.analyze_task(user_input, image_data)
        except Exception as e:
            print(f"Hybrid: OpenAI failed, falling back to Gemini. Error: {e}")
            return await self.gemini.analyze_task(user_input, image_data)

def get_llm_provider() -> LLMInterface:
    provider = Config.LLM_PROVIDER.lower()
    if provider == "openai":
        return OpenAIProvider()
    elif provider == "gemini":
        return GeminiProvider()
    elif provider == "hybrid":
        return HybridProvider()
    else:
        return MockLLM()
