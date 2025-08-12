from enum import Enum
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import Database.database as db
from modals import AddServerModal
from embeds import ServerEmbed
from buttons import ConnectButton
from GameQuery.a2s import a2sprotocol

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

SERVER_COUNT = 0

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
        self.db.create_tables()
        global SERVER_COUNT
        SERVER_COUNT = self.db.count_servers()
        await self.change_presence(activity=discord.Game(name=f"Observing {SERVER_COUNT} Servers"))
        self.check_servers.start()

    @tasks.loop(seconds=60)
    async def check_servers(self):
        """Periodically check the status of servers."""
        all_servers = self.db.get_all_servers()
        global SERVER_COUNT

        if len(all_servers) != SERVER_COUNT:
            SERVER_COUNT = len(all_servers)
            await self.change_presence(activity=discord.Game(name=f"Observing {SERVER_COUNT} Servers"))

        for server in all_servers:
            await query_server(server)
            # Here you would implement the logic to check the server status
            # For example, pinging the server or checking its availability
            

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = Client(command_prefix='.', intents=intents)

@client.tree.command(name='addgameserver', description='Adds a new server to the database', guild=GUILD)
@discord.app_commands.checks.has_permissions(administrator=True)
# @discord.app_commands.describe(gametype="Game type of the server (e.g., source)", address="IP address or hostname of the server", port="Port of the server", countrycode="Country code of the server (default: de)", channelid="Channel ID to send the server information (if non, the current channel will be used)")
async def addgameserver(interaction: discord.Interaction, channelid: str = None):
    """Command to add a server using a modal."""
    # await interaction.response.defer(ephemeral=True)
    if channelid is None:
        channelid = interaction.channel_id

    # await db.Database().insert_server(
    #     game_type=gametype,
    #     address=address,
    #     port=port,
    #     channel_id=channelid,
    #     country=countrycode,
    #     lang="en"
    # )

    # server = await db.Database().get_server_by_address_port(address, port)

    # await query_server(server)

    modal = AddServerModal(channelID=channelid)

    return await interaction.response.send_modal(modal)

    # await interaction.followup.send("Server added successfully!", ephemeral=True)

async def create_or_edit_server_embed(server_data):
    """Creates or edits a server embed."""
    channel = client.get_channel(server_data['channel_id'])
    if channel:
        embed = ServerEmbed(server_data)
        # button = ConnectButton(server_data['ip'], server_data['port'])
        message_id = server_data['message_id']
        if message_id:
            try:
                message = await channel.fetch_message(message_id)
                await message.edit(embed=embed)
            except discord.NotFound:
                message = await channel.send(embed=embed)

                db.Database().update_server_message_id(server_data['id'], message.id)
        else:
            message = await channel.send(embed=embed)
            # Update the database with the new message ID
            db.Database().update_server_message_id(server_data['id'], message.id)

async def query_server(server):
    gametype = server[1]
    addr = server[2]
    port = server[3]
    country = server[6] if len(server) > 6 else AllowedCountries.UNKNOWN.value
    name = server[8] if len(server) > 8 else 'Unknown'
    print(f"Checking {gametype} server at {addr}:{port}")
    match gametype:
        case AllowedGameTypes.SOURCE.value:
            status = await a2sprotocol(addr, port).get_info()
            if status:
                players = await a2sprotocol(addr, port).get_players()
                if status.server_name != name:
                    db.Database().update_server_name(server[0], status.server_name)
                print(f"Players: {players}")
                server_data = {
                    'id': server[0],
                    'status': 'Online',
                    'game': status.game,
                    'ip': addr,
                    'port': port,
                    'name': status.server_name,
                    'map': status.map_name,
                    'numplayers': status.player_count,
                    'maxplayers': status.max_players,
                    'country': country,
                    'channel_id': server[4],
                    'message_id': server[5],
                    'players': players
                }
            else:
                server_data = {
                    'id': server[0],
                    'status': 'Offline',
                    'game': 'Unknown',
                    'ip': addr,
                    'port': port,
                    'name': name,
                    'map': 'Unknown',
                    'numplayers': 0,
                    'maxplayers': 0,
                    'country': country,
                    'channel_id': server[4],
                    'message_id': server[5],
                    'players': []
                }
            print(f"Server Status: {status}")
            await create_or_edit_server_embed(server_data)

if __name__ == "__main__":
    if not TOKEN:
        print("No token found in .env file. Please set the TOKEN variable.")
    else:
        print("Starting Discord Bot...")
        client.run(TOKEN)

