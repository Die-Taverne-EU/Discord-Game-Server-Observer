import discord
from discord import Embed

class ServerEmbed(Embed):
    def __init__(self, server_data):
        super().__init__(title=server_data['name'], color=discord.Color.blue())
        self.add_field(name="Status", value=":green_circle: Online" if server_data['status'] == 'Online' else ":red_circle: Offline", inline=True)
        self.add_field(name="Address:Port", value=f"{server_data['ip']}:{server_data['port']}", inline=True)
        self.add_field(name="Country", value=f":flag_{server_data['country']}:", inline=True)
        self.add_field(name="Game", value=server_data['game'], inline=True)
        self.add_field(name="Map", value=server_data['map'], inline=True)
        self.add_field(name="Players", value=f"{server_data['numplayers']}/{server_data['maxplayers']}", inline=True)
        self.set_footer(text=f"Server ID: {server_data['id']}")