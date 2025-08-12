import discord

class ConnectButton(discord.ui.View):
    def __init__(self, addr, port):
        super().__init__(timeout=30)
        button = discord.ui.Button(label="Connect", style=discord.ButtonStyle.green, url=f"https://connect.die-taverne.eu/{addr}/{port}")
        self.add_item(button)