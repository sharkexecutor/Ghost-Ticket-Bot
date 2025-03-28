import discord
from discord.ext import commands
import asyncpg
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # Slash commands are registered here

db_pool = None

@bot.event
async def on_ready():
    global db_pool
    db_pool = await asyncpg.create_pool(os.getenv("DATABASE_URI"))
    print(f'Logged in as {bot.user}')
    await tree.sync()  # Sync slash commands

@tree.command(name="new", description="Create a new support ticket")
async def new_ticket(interaction: discord.Interaction):
    guild = interaction.guild
    category = discord.utils.get(guild.categories, name="Tickets")
    
    if not category:
        category = await guild.create_category("Tickets")

    ticket_channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", category=category)
    await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
    await ticket_channel.set_permissions(guild.default_role, read_messages=False)
    
    await ticket_channel.send(f"{interaction.user.mention}, your ticket has been created!")
    await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)

@tree.command(name="close", description="Close the current ticket")
async def close_ticket(interaction: discord.Interaction):
    if interaction.channel.category and interaction.channel.category.name == "Tickets":
        await interaction.channel.delete()
        await interaction.response.send_message("Ticket closed!", ephemeral=True)
    else:
        await interaction.response.send_message("This is not a ticket channel!", ephemeral=True)

TOKEN = os.getenv("BOT_TOKEN")
bot.run(TOKEN)
