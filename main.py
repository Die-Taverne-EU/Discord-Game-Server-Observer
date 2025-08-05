import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import database

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
        
        # Migrate the database schema
        database.migrate_database()
    
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = Client(command_prefix='.', intents=intents)

@client.tree.command(name='test', description='Test command to check if the bot is working.', guild=GUILD)
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message('Test command executed successfully!')

@client.tree.command(name='settings', description='View or modify bot settings.', guild=GUILD)
async def settings_command(interaction: discord.Interaction, key: str = None, value: str = None):
    if key is None:
        result = await database.get_all_settings()
        if not result:
            await interaction.response.send_message('No settings found.')
            return
        settings_list = '\n'.join([f'{k}: {v}' for k, v in result.items()])
        await interaction.response.send_message(f'Current settings:\n{settings_list}')
        return
    try:
        result = await database.get_setting(key)
        if result is None:
            await interaction.response.send_message(f'Setting "{key}" not found.')
            return
    except ValueError as e:
        await interaction.response.send_message(f'Error: {str(e)}')
        return
    if value is None:
        await interaction.response.send_message(f'Setting "{key}" has value: {result} (To update specify a value while calling the command)')
        return
    
    try:
        await database.update_setting(key, value)
    except ValueError as e:
        await interaction.response.send_message(f'Error updating setting: {str(e)}')
        return

    await interaction.response.send_message(f'Setting successfully set! Key: {key}, New value: {value}')

client.run(TOKEN)
