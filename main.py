import asyncio
import os

import discord
from discord.ext import commands


cmd = "#"
bot = commands.Bot(command_prefix=cmd, description='Why is nothing working?!')
OWNER = os.getenv('OWNER')

say = bot.say
send = bot.send_message


async def status_task():
    while True:
        await bot.change_presence(game=discord.Game(name=f'on {len(bot.servers)} servers'))
        await asyncio.sleep(10)
        await bot.change_presence(game=discord.Game(name='in repl.it'))
        await asyncio.sleep(10)


@bot.event
async def on_ready():
  print("========")
  print("Logged in as: "+bot.user.name)
  print("========")
  bot.loop.create_task(status_task())


@bot.command()
async def roll(dice: str):
  """Rolls a dice in NdN format."""
  rolls, limit = dice.split('d')

  if not rolls.isdigit() and not limit.isdigit():
    await say('Format has to be in NdN!')
    return
  elif not rolls.isdigit():
    rolls = 1
  rolls = int(rolls)
  limit = int(limit)
  import random
  result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))

  await say(result)


async def isUser(id):
  "Checks is user has account, and returns it if True"
  user = User.exist(id)
  if not user:
    return False
  return user


async def game_embed():
  embed = discord.Embed(color=0xd33131)
  embed.add_field(name="Voice Panel", value="This is the board to maintain the mute panel.", inline=False)
  await say(embed=embed)
  for r in ['🔇', '🔊', '🚫']:
    await bot.add_reaction(msg, r)


token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)
