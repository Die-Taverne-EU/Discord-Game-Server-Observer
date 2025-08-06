import asyncio
import time
import opengsq
from opengsq.responses.source import SourceInfo, GoldSourceInfo, Visibility

from GameQuery.protocol import GameQueryProtocol

class Source(GameQueryProtocol):
    name = "Source"
    game_type = "source"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.timeout = 60

    async def query(self):
        host, port = str(self.host), int(self.port)
        source = opengsq.Source(host, port, timeout=self.timeout)
        async def query_players():
            try:
                return await source.get_players()
            except Exception as e:
                print(f"Error querying players: {e}")
                return []
            
        start = time.time()
        
        info, players = await asyncio.gather(source.get_info(), query_players())

        if isinstance(info, SourceInfo):
            info: SourceInfo = info
            connect = f"{host}:{port}"
            game_id = info.game_id
            keywords = info.keywords
        elif isinstance(info, GoldSourceInfo):
            info: GoldSourceInfo = info
            connect = f"{host}:{port}"
            game_id = None
            keywords = None

        ping = int((time.time() - start) * 1000)
        players.sort(key=lambda x: x.duration, reverse=True)
        players, bots = players[info.bots :], players[:info.bots]

        query_result = {
            "name": info.name,
            "map": info.map,
            "password": info.visibility == Visibility.Private,
            "numplayers": info.players,
            "numbots": info.bots,
            "maxplayers": info.max_players,
            "players": [
                {
                    "name": player.name,
                    "raw": {"score": player.score, "time": player.duration},
                }
                for player in players
            ],
            "bots": [
                { "name": bot.name, "raw": {"score": bot.score, "time": bot.duration} }
                for bot in bots
            ],
            "connect": connect,
            "ping": ping,
            "raw": info.__dict__,
        }

        if keywords:
            query_result["raw"]["tags"] = str(keywords).split(",")

        return query_result

