from enum import Enum
from http import server
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import Database.database as db
from modals import AddServerModal
from embeds import ServerEmbed
from GameQuery.source import Source

class AllowedGameTypes(Enum):
    SOURCE = "source"

class AllowedCountries(Enum):
    UNKNOWN = "unknown"
    DE = "de"
    US = "us"

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = discord.Object(id=os.getenv('SERVER_ID'))

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        try:
            synced = await self.tree.sync(guild=GUILD)
            print(f'Synced {len(synced)} commands to the guild: {GUILD.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

        self.db = db.Database()
        await self.db.create_tables()
        await self.change_presence(activity=discord.Game(name="Observing Servers"))
        self.check_servers.start()

    @tasks.loop(seconds=60)
    async def check_servers(self):
        """Periodically check the status of servers."""
        all_servers = await self.db.get_all_servers()
        for server in all_servers:
            # Here you would implement the logic to check the server status
            # For example, pinging the server or checking its availability
            addr = server[2]
            port = server[3]
            # print(f"Server: {server}")
            print(f"Checking server: {addr}:{port}")
            print(f"Server Status: {await query_server(addr, port)}")


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = Client(command_prefix='.', intents=intents)

@client.tree.command(name='addgameserver', description='Adds a new server to the database', guild=GUILD)
@discord.app_commands.checks.has_permissions(administrator=True)
@discord.app_commands.describe(channelid="Channel ID to send the server information (if non, the current channel will be used)")
async def addgameserver(interaction: discord.Interaction, channelid: str = None):
    """Command to add a server using a modal."""

    if channelid is None:
        channelid = interaction.channel_id

    modal = AddServerModal(channelID=channelid)

    await interaction.response.send_modal(modal)

async def create_or_edit_server_embed(server_data, rcon_data=None):
    """Creates or edits a server embed."""
    channel = client.get_channel(server_data['channel_id'])
    if channel:
        embed = ServerEmbed(server_data)
        message_id = server_data['message_id']
        if message_id:
            try:
                message = await channel.fetch_message(message_id)
                await message.edit(embed=embed)
            except discord.NotFound:
                await channel.send(embed=embed)
        else:
            message = await channel.send(embed=embed)
            # Update the database with the new message ID
            await db.Database().update_server_message_id(server_data['id'], message.id)

async def query_server(server_address, server_port):
    query = Source(server_address, server_port)
    result = await query.query()
    return result

client.run(TOKEN)
