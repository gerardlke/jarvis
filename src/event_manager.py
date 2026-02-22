import asyncio
from dataclasses import dataclass
from typing import Optional

from .brain.schemas.logger import Logger


@dataclass
class SystemState:
    last_command: Optional[str] = None
    last_gesture: Optional[str] = None
    gesture_conf: Optional[float] = None
    response: Optional[str] = None
    mode: str = "IDLE"  # IDLE/EXECUTING

class EventManager:
    def __init__(self):
        self.state = SystemState()

        # Lock to prevent overlapping operations
        self.lock = asyncio.Lock()

    async def update_command(self, command):
        async with self.lock:
            Logger.info("Event Manager", f"Command detected: {command}")
            self.state.last_command = command
            self.state.mode = "EXECUTING"

    async def update_gesture(self, gesture, confidence):
        async with self.lock:
            Logger.info("Event Manager", f"Gesture detected: {gesture} ({int(confidence * 100)}%)")
            self.state.last_gesture = gesture
            self.state.gesture_conf = confidence
            if gesture:
                self.state.mode = "LISTENING"
            else:
                self.state.mode = "IDLE"

    async def update_response(self, response):
        async with self.lock:
            Logger.info("Event Manager", f"New response: {response}")
            self.state.response = response
            self.state.mode = "IDLE"

    async def set_mode(self, mode):
        async with self.lock:
            Logger.info("Event Manager", f"Setting mode to: {mode}")
            self.state.mode = mode

    async def get_state(self):
        async with self.lock:
            Logger.info("Event Manager", "Retrieving state.")
            return self.state
