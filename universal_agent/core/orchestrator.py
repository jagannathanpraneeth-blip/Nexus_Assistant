import asyncio
from typing import Dict, List, Optional
from .types import Task, TaskStatus, Event
from .event_bus import EventBus

from .database import Database

class TaskOrchestrator:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.db = Database()

    async def submit_task(self, task: Task):
        if task.scheduled_time:
            from datetime import datetime
            delay = (task.scheduled_time - datetime.now()).total_seconds()
            if delay > 0:
                print(f"[ORCHESTRATOR] Scheduling task for {task.scheduled_time} (in {delay:.1f}s): {task.description}")
                self.db.save_task(task)
                
                # Run in background thread that waits
                import threading
                def wait_and_run():
                    import time
                    time.sleep(delay)
                    
                    # Create new loop for execution
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self._execute_task(task))
                    loop.close()
                
                threading.Thread(target=wait_and_run, daemon=True).start()
                return

        print(f"[ORCHESTRATOR] Executing task immediately: {task.description}")
        self.db.save_task(task)
        await self.event_bus.publish(Event("task_submitted", {"task_id": task.id}))
        
        # Execute in a new thread with its own event loop
        import threading
        def run_task():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._execute_task(task))
            loop.close()
        
        threading.Thread(target=run_task, daemon=True).start()

    async def _execute_task(self, task: Task):
        task.status = TaskStatus.RUNNING
        self.db.save_task(task)
        await self.event_bus.publish(Event("task_started", {"task_id": task.id}))
        
        try:
            # Check for GUI Automation
            if task.metadata.get("type") == "gui_automation":
                from integrations.system import SystemIntegration
                sys_int = SystemIntegration()
                
                action = task.metadata.get("action")
                if action == "open":
                    app_name = task.metadata.get("app")
                    result = await sys_int.open_application(app_name)
                    
                    # Fallback: If app not found, open website
                    if "FAILED_TO_OPEN" in result:
                        print(f"[ORCHESTRATOR] App '{app_name}' not found. Falling back to web search.")
                        
                        # Notify user
                        await sys_int.show_notification("Nexus", f"Could not find {app_name}, opening website instead.")
                        
                        # Create web search task
                        from integrations.web_search import WebSearch
                        search = WebSearch()
                        # Search for "appname official site"
                        query = f"{app_name} official website"
                        results = await search.search(query)
                        
                        if results:
                            # Open the first result
                            url = results[0]['url']
                            await sys_int.run_command(f"start {url}")
                            result = f"App not found. Opened website: {url}"
                        else:
                            result = f"App not found and could not find website for {app_name}"

                elif action == "type":
                    text_to_type = task.metadata.get("text")
                    print(f"[ORCHESTRATOR] Typing text: '{text_to_type}'")
                    result = await sys_int.type_text(text_to_type)
                elif action == "press":
                    result = await sys_int.press_key(task.metadata.get("key"))
                elif action == "close":
                    result = await sys_int.close_application(task.metadata.get("app"))
                elif action == "install":
                    result = await sys_int.install_app(task.metadata.get("app"))
                elif action == "uninstall":
                    result = await sys_int.uninstall_app(task.metadata.get("app"))
                else:
                    result = "Unknown GUI action"
            
            elif task.metadata.get("type") == "web_search":
                from integrations.web_search import WebSearch
                from integrations.web_automation import WebAutomation
                
                query = task.metadata.get("query", "")
                
                # If it's a YouTube/music search, use web automation
                if "song" in query.lower() or "music" in query.lower() or "play" in task.description.lower():
                    web_auto = WebAutomation()
                    result = await web_auto.search_and_play(query)
                else:
                    search = WebSearch()
                    results = await search.search(query)
                    result = f"Search results for '{query}': {len(results)} found"

            elif task.metadata.get("type") == "reminder":
                from integrations.system import SystemIntegration
                sys_int = SystemIntegration()
                message = task.metadata.get("message", task.description)
                await sys_int.show_notification("Nexus Reminder", message)
                result = f"Reminder sent: {message}"

            elif task.metadata.get("type") == "shell":
                from integrations.system import SystemIntegration
                sys_int = SystemIntegration()
                cmd = task.metadata.get("command")
                stdout, stderr = await sys_int.run_command(cmd)
                result = f"Command executed. Output: {stdout}"
                if stderr:
                    result += f" Error: {stderr}"

            elif task.metadata.get("type") == "response":
                # Just return the text so it can be spoken
                result = task.metadata.get("text", task.description)
            
            else:
                # Simulate work or delegate to specific handlers
                duration = task.metadata.get("duration", 2)
                await asyncio.sleep(duration)
                result = f"Executed: {task.description}"
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            self.db.save_task(task)
            await self.event_bus.publish(Event("task_completed", {"task_id": task.id, "result": task.result}))
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            self.db.save_task(task)
            await self.event_bus.publish(Event("task_failed", {"task_id": task.id, "error": str(e)}))
