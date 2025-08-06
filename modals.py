import discord
from discord.ui import Modal, TextInput
import Database.database as db

class AddServerModal(Modal):
    def __init__(self, channelID: discord.TextChannel):
        super().__init__(title="Add Server")
        self.game_type = TextInput(label="Game Type", placeholder="Enter game type (e.g., source)", required=True)
        self.country = TextInput(label="Country", placeholder="Enter country code (e.g., de, us)", required=True)
        self.ip = TextInput(label="IP Address / Hostname", placeholder="Enter server IP address or Hostname", required=True)
        self.port = TextInput(label="Port", placeholder="Enter server port", required=True)
        self.channel_id = channelID

        self.add_item(self.game_type)
        self.add_item(self.country)
        self.add_item(self.ip)
        self.add_item(self.port)

    async def on_submit(self, interaction: discord.Interaction):
        # Here you would handle the submission, e.g., save to the database
        await db.Database().insert_server(
            game_type=self.game_type.value,
            address=self.ip.value,
            port=int(self.port.value),
            channel_id=self.channel_id,
            country=self.country.value,
            lang="en"  # Default language, can be modified as needed
        )
        await interaction.response.send_message("Server added successfully!", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
        print(f"Error in AddServerModal: {error}")