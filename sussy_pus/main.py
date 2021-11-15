# main.py
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import keep_alive
import time

load_dotenv()
TOKEN = os.getenv('PUSSTOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="?", help_command=None)

bot.load_extension("cog_basic")
# bot.load_extension("passive_process")
bot.load_extension("cog_anime")
bot.load_extension("cog_management")

def __init__(self, bot):
  self.bot = bot


@bot.command(name="announce")
async def announce(ctx, arg1, arg2):
    """Announcement"""
    # await ctx.send('You passed {} and {}'.format(arg1, arg2))
    await ctx.message.delete()

    if arg1 == "primos-general":
      arg1 = 901408102321127464
    elif arg1 =="test-general":
      arg1 = 901142939365933171
    elif arg1 == "djas":
      arg1 = 902189685441437830
    else:
      arg1 = int(arg1)


    channel = bot.get_channel(arg1)
    await channel.send(arg2)




keep_alive.keep_alive()
bot.run(TOKEN)