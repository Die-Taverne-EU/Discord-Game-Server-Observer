import discord
from discord import Embed

class ServerEmbed(Embed):
    def __init__(self, server_data):
        super().__init__(title=server_data['name'], color=discord.Color.blue())
        self.add_field(name="IP Address", value=server_data['ip'], inline=False)
        self.add_field(name="Port", value=server_data['port'], inline=False)
        self.add_field(name="Game Type", value=server_data['game_type'], inline=False)
        self.add_field(name="Country", value=server_data['country'], inline=False)
        self.set_footer(text=f"Server ID: {server_data['id']}")