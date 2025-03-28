import discord
from discord.ext import commands
import asyncpg
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

db_pool = None

@bot.event
async def on_ready():
    global db_pool
    db_pool = await asyncpg.create_pool(os.getenv("DATABASE_URI"))
    print(f'Logged in as {bot.user}')

    # Load Commands
    await bot.load_extension("commands")

TOKEN = os.getenv("MTM1NTA4MTE2NTQxMjg5Njg1OQ.GKpgWk.4IQNesyXMWwV4ep94TkSsQ5ergzcjk0Os37DCE")
bot.run(TOKEN)
