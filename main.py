import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = discord.Object(id=os.getenv('SERVER_ID'))

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = Client(command_prefix='.', intents=intents)

client.run(TOKEN)
