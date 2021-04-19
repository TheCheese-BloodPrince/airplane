#Setting Up the Bot
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
from discord.ext.commands import has_permissions
from replit import db
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

#+info
@bot.command(name='info', description='Information about airplane.')
async def info(ctx):
  ctx.send("airplane is an open-source Discord moderation/economy bot made by The Cheese-Blood Prince#0505.")

#+afk
@bot.command(name='afk', description='Sets the user to afk.')
async def afk(ctx, reason):
  if ctx.author.nick == None:
    await ctx.author.edit(nick=("["+reason+"]"+ctx.author.name))
    db[str(ctx.author.id)+"_nick"] = ctx.author.name
  else:
    previousNick = ctx.author.nick
    await ctx.author.edit(nick=("["+reason+"]"+previousNick))
    db[str(ctx.author.id)+"_nick"] = ctx.author.nick
  await ctx.send("**"+ctx.author.name+"** is AFK: " + reason)

#+back
@bot.command(name='back', description="Removes the user's afk.")
async def back(ctx):
  await ctx.author.edit(nick=db[str(ctx.author.id)+"_nick"])
  await ctx.send("**"+ctx.author.name+"** is back! *attempts to smile*")


#Running the Bot
keep_alive()
bot.run(TOKEN)
