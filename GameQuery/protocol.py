import os
from abc import ABC, abstractmethod

class GameQueryProtocol(ABC):
    pre_query_required = False

    def __init__(self, kv:dict):
        self.kv = kv
        self.timeout = float(os.getenv("QUERY_TIMEOUT", 5.0))

    async def pre_query(self):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError("Subclasses must implement the 'name' property.")
    
    @abstractmethod
    async def query(self):
        raise NotImplementedError("Subclasses must implement the 'query' method.")