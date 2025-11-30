from typing import List
from core.types import Task
from core.orchestrator import TaskOrchestrator
from .llm_interface import get_llm_provider

class Brain:
    def __init__(self, orchestrator: TaskOrchestrator):
        self.orchestrator = orchestrator
        self.llm = get_llm_provider()

    async def process_input(self, user_input: str):
        print(f"[BRAIN] Processing: {user_input}")
        print("[BRAIN] NLP Engine: Analyzing intent and context...")
        
        image_data = None
        # Capture screen for vision-related commands
        if any(word in user_input.lower() for word in ["screen", "look", "see", "what", "summarize", "describe", "read"]):
            print("[BRAIN] Capturing screen for vision analysis...")
            from integrations.system import SystemIntegration
            sys_int = SystemIntegration()
            image_data = await sys_int.capture_screen()
            if image_data:
                print(f"[BRAIN] Screen captured successfully ({len(image_data)} bytes)")
            else:
                print("[BRAIN] Warning: Screen capture failed")
            
        subtasks_data = await self.llm.analyze_task(user_input, image_data)
        
        print(f"[BRAIN] Created {len(subtasks_data)} tasks:")
        for i, task_data in enumerate(subtasks_data):
            print(f"  Task {i+1}: {task_data['description']} | Type: {task_data['metadata'].get('type')} | Action: {task_data['metadata'].get('action', 'N/A')}")
            
            task = Task(
                description=task_data["description"],
                metadata=task_data["metadata"]
            )
            
            # Handle scheduling
            if "scheduled_delay_seconds" in task_data["metadata"]:
                from datetime import datetime, timedelta
                delay = task_data["metadata"]["scheduled_delay_seconds"]
                task.scheduled_time = datetime.now() + timedelta(seconds=delay)
                
            await self.orchestrator.submit_task(task)
