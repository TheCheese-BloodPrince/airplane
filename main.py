#Setting Up the Bot
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
from discord.ext.commands import has_permissions
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='+')

@bot.event
async def on_ready():
  print("airplane has started up; Can now execute commands.")




#Commands

#+kick
@bot.command(name='kick', description='Kick a troublesome user.')
@has_permissions(kick_members=True)  
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason = reason)

#+ban
@bot.command(name='ban', description = 'Ban a troublesome user.')
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)

#Commands
#Running the Bot
keep_alive()
bot.run(TOKEN)
