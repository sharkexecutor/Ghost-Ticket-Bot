import discord
from discord.ext import commands
import asyncpg
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True  # Ensure members intent is enabled

bot = commands.Bot(command_prefix="!", intents=intents)

db_pool = None

@bot.event
async def on_ready():
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(os.getenv("DATABASE_URI"))
    print(f'Logged in as {bot.user}')

@bot.slash_command(name="new", description="Create a new support ticket")
async def new_ticket(ctx):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="Tickets")
    if not category:
        category = await guild.create_category("Tickets")

    ticket_channel = await guild.create_text_channel(f"ticket-{ctx.author.name}-{ctx.author.id}", category=category)
    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
    await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
    
    await ticket_channel.send(f"{ctx.author.mention}, your ticket has been created!")
    await ctx.respond(f"Ticket created: {ticket_channel.mention}", ephemeral=True)

@bot.slash_command(name="close", description="Close the current ticket")
async def close_ticket(ctx):
    if ctx.channel.category and ctx.channel.category.name == "Tickets":
        if ctx.channel.name.endswith(str(ctx.author.id)):  # Check if user owns the ticket
            await ctx.channel.delete()
            await ctx.respond("Ticket closed!", ephemeral=True)
        else:
            await ctx.respond("You can only close your own ticket!", ephemeral=True)
    else:
        await ctx.respond("This is not a ticket channel!", ephemeral=True)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables!")

bot.run(TOKEN)
