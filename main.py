#Setting Up the Bot
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
from keep_alive import keep_alive
from discord_slash import SlashCommand, SlashContext
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='e')

@bot.event
async def on_ready():
  print("airplane has started up; Can now execute commands.")




#Commands

#ekick
@bot.command(name='kick')
async def kick(ctx, user):
  await kick(user)


#Commands
#Running the Bot
keep_alive()
bot.run(TOKEN)
