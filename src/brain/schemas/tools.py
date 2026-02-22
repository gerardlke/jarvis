from abc import ABC, abstractmethod


class Tool(ABC):
    name: str

    @abstractmethod
    def execute(self, **kwargs) -> dict:
        raise NotImplementedError


class SearchTool(Tool):
    def __init__(self):
        return
    
    def execute(self):
        return


class SpotifyTool(Tool):
    def __init__(self):
        return
    
    def execute(self):
        return
    

TOOLS = {
    "respond": None,
    "google_search": SearchTool(),
    "spotify_play": SpotifyTool(),
    "spotify_pause": SpotifyTool(),
}