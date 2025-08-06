from enum import Enum
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import Database.database as db

class AllowedGameTypes(Enum):
    SOURCE = "source"

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = discord.Object(id=os.getenv('SERVER_ID'))

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        self.db = db.Database()
        await self.db.create_tables()
        await self.change_presence(activity=discord.Game(name="Observing Servers"))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = Client(command_prefix='.', intents=intents)



client.run(TOKEN)
