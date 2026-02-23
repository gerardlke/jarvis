import asyncio
from dataclasses import dataclass, field
from typing import Optional, List

from .brain.schemas.logger import Logger


@dataclass
class SystemState:
    # State to persist throughout different parts of the system
    current_gesture: Optional[str] = None
    gesture_conf: Optional[float] = None

    last_command: Optional[str] = None

    last_response: Optional[str] = None
    
    command_history: List[str] = field(default_factory=list)
    response_history: List[str] = field(default_factory=list)

    mode: str = "IDLE"  # IDLE/EXECUTING/LISTENING


class EventManager:
    def __init__(self):
        self.state = SystemState()

        # Lock to prevent overlapping operations
        self.lock = asyncio.Lock()

        # Queues for commands
        self.command_queue = asyncio.Queue()

        # To track gesture changes
        self.last_gesture: Optional[str] = None

        Logger.info("Pipeline", "Event Manager initialised.")


    async def update_command(self, command):
        async with self.lock:
            Logger.debug("Event Manager", f"Command detected: {command}")

            self.state.last_command = command
            self.state.command_history.append(command)
            self.state.mode = "EXECUTING"

            await self.command_queue.put(command)


    async def get_next_command(self):
        async with self.lock:
            if self.command_queue.empty():
                return None
            
            command = await self.command_queue.get()
            Logger.info("Event Manager", f"New actionable command: {command}")
            return command 


    async def update_gesture(self, gesture, confidence):
        async with self.lock:
            if gesture:
                Logger.debug("Event Manager", f"Gesture detected: {gesture} ({int(confidence * 100)}%)")

                self.state.current_gesture = gesture
                self.state.gesture_conf = confidence

                self.state.mode = "LISTENING"  # To update later
            else:
                self.state.current_gesture = None
                self.state.gesture_conf = 0.0
                self.state.mode = "IDLE"


    async def get_next_gesture(self):
        async with self.lock:
            gesture = self.state.current_gesture

            if gesture and gesture != self.last_gesture:
                Logger.info("Event Manager", f"New actionable gesture: {gesture}")
                self.last_gesture = gesture
                return gesture
            
            return None
            

    async def update_response(self, response):
        async with self.lock:
            Logger.info("Event Manager", f"New response: {response}")
            self.state.last_response = response
            self.state.response_history.append(response)
            self.state.mode = "IDLE"


    async def set_mode(self, mode):
        async with self.lock:
            Logger.debug("Event Manager", f"Setting mode to: {mode}")
            self.state.mode = mode


    async def get_state(self):
        async with self.lock:
            Logger.debug("Event Manager", "Retrieving state.")
            return self.state
