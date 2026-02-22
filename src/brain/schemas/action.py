from typing import Dict, Any
from pydantic import BaseModel


class Action(BaseModel):
    action: str
    parameters: Dict[str, Any]
