import discord
import os

from discord.ext import tasks, commands
from dotenv import load_dotenv

from cogs.timesheet import Timesheet

load_dotenv() # loads the .env file with variables

description = '''A self-hosted bot for tracking working hours and some extra useful work commands.'''

INTENTS = discord.Intents.default()

PREFIX=';;'
TOKEN=os.getenv('DISCORD_SECRET')

bot = commands.Bot(command_prefix=PREFIX, description=description, intents=INTENTS)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def ping(ctx):
    """Adds two numbers together."""
    await ctx.message.reply('pong')
    await ctx.message.channel.say()


@bot.command()
async def toggle_cog(ctx):
    """Hooks cog on and off"""
    if bot.get_cog('Timesheet'):
        await ctx.message.reply('Removed cog...')
        bot.remove_cog('Timesheet')
    else:
        bot.add_cog(Timesheet(bot))
        await ctx.message.reply('Added cog...')
    


bot.run(TOKEN)