import a2s
from datetime import timedelta

class a2sprotocol:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def get_info(self):
        try:
            return await a2s.ainfo((self.host, self.port), timeout=5)
        except Exception as e:
            print(f"Error getting server info: {e}")
            return None

    async def get_players(self):
        try:
            return await a2s.aplayers((self.host, self.port), timeout=5)
        except Exception as e:
            print(f"Error getting player list: {e}")
            return None
