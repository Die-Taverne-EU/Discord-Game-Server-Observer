import os
import discord
from dotenv import load_dotenv

load_dotenv()

class ConnectButton(discord.ui.View):
    def __init__(self, addr, port):
        super().__init__(timeout=30)
        button = discord.ui.Button(label="Connect", style=discord.ButtonStyle.green, url=f"{os.getenv('STEAM_CONNECT_URL')}/{addr}/{port}")
        self.add_item(button)