#Setting Up the Bot
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json
from keep_alive import keep_alive
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix=';')

@bot.event
async def on_ready():
  print("airplane has started up; Can now execute commands.")


#Commands
#Running the Bot
keep_alive()
bot.run(TOKEN)
