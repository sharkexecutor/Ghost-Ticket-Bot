import discord
from discord.ext import commands

class TicketCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="new", description="Create a new support ticket")
    async def new_ticket(self, ctx):
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")

        ticket_channel = await guild.create_text_channel(f"ticket-{ctx.author.name}", category=category)
        await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
        await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)

        await ticket_channel.send(f"{ctx.author.mention}, your ticket has been created!")
        await ctx.respond(f"Ticket created: {ticket_channel.mention}", ephemeral=True)

    @commands.slash_command(name="close", description="Close the current ticket")
    async def close_ticket(self, ctx):
        if ctx.channel.category and ctx.channel.category.name == "Tickets":
            await ctx.channel.delete()
            await ctx.respond("Ticket closed!", ephemeral=True)
        else:
            await ctx.respond("This is not a ticket channel!", ephemeral=True)

def setup(bot):
    bot.add_cog(TicketCommands(bot))
