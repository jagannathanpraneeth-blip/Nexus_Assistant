import asyncio
from typing import Callable, Dict, List, Awaitable
from .types import Event

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Event], Awaitable[None]]]] = {}

    def subscribe(self, event_name: str, callback: Callable[[Event], Awaitable[None]]):
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)

    async def publish(self, event: Event):
        if event.name in self.subscribers:
            # Run all callbacks concurrently
            await asyncio.gather(*[cb(event) for cb in self.subscribers[event.name]])
