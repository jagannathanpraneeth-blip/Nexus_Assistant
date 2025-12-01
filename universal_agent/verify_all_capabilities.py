import asyncio
from cognitive.llm_interface import MockLLM

async def verify_all():
    print("=== NEXUS CAPABILITY VERIFICATION ===")
    mock = MockLLM()
    
    test_cases = [
        ("Greeting", "Hey Nexus"),
        ("System Control", "Open Notepad"),
        ("Typing", "Type Hello World"),
        ("Web Search", "Search for Python tutorials"),
        ("Vision", "Summarize my screen"),
        ("Reminder", "Remind me to drink water in 5 minutes"),
        ("General Chat", "I am tired today")
    ]
    
    for category, command in test_cases:
        print(f"\n--- Testing {category} ---")
        print(f"User: {command}")
        tasks = await mock.analyze_task(command)
        for task in tasks:
            print(f"Nexus Action: {task['description']}")
            print(f"  Type: {task['metadata'].get('type')}")
            if 'text' in task['metadata']:
                print(f"  Response: {task['metadata']['text']}")
            if 'action' in task['metadata']:
                print(f"  Action: {task['metadata']['action']} {task['metadata'].get('app', '')} {task['metadata'].get('text', '')}")

if __name__ == "__main__":
    asyncio.run(verify_all())
