import asyncio
from dataclasses import dataclass
from typing import Optional


@dataclass
class SystemState:
    last_command: Optional[str] = None
    last_gesture: Optional[str] = None
    gesture_conf: Optional[float] = None
    mode: str = "IDLE"  # IDLE/EXECUTING

class EventManager:
    def __init__(self):
        self.state = SystemState()

        # Lock to prevent overlapping operations
        self.lock = asyncio.Lock()

    async def update_command(self, command):
        async with self.lock:
            self.state.last_command = command
            self.state.mode = "EXECUTING"

    async def update_gesture(self, gesture, confidence):
        async with self.lock:
            self.state.last_gesture = gesture
            self.state.gesture_conf = confidence
            if gesture:
                self.state.mode = "LISTENING"
            else:
                self.state.mode = "IDLE"

    async def set_mode(self, mode):
        async with self.lock:
            self.state.mode = mode

    async def get_state(self):
        async with self.lock:
            return self.state
