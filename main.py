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
    await ctx.author.edit(nick=("[AFK]"+ctx.author.name))
    db[str(ctx.author.id)+"_nick"] = ctx.author.name
  else:
    previousNick = ctx.author.nick
    await ctx.author.edit(nick=("[AFK]"+previousNick))
    db[str(ctx.author.id)+"_nick"] = ctx.author.nick
  await ctx.send("**"+ctx.author.name+"** is AFK: " + reason)

#+back
@bot.command(name='back', description="Removes the user's afk.")
async def back(ctx):
  await ctx.author.edit(nick=db[str(ctx.author.id)+"_nick"])
  await ctx.send("**"+ctx.author.name+"** is back! *attempts to smile*")

#+purge
@bot.command(name='purge', description="Purges a certain amount of messages.")
async def purge(ctx, amount):
  await ctx.channel.purge(limit=int(amount))

#+dev
@bot.command(name='dev', description="Gives people the link to the GitHub so they can help build the bot.")
async def dev(ctx):
  ctx.send("Thank you for your interest in helping airplane! You can help the airplane project here: https://github.com/TheCheese-BloodPrince/airplane")

#+mute
@bot.command(name='mute', description="Allows a moderator to mute a user.")
@commands.has_permissions(kick_members=True)
async def mute(ctx, member : discord.Member):
  muted_role = ctx.guild.get_role()
#Running the Bot
keep_alive()
bot.run(TOKEN)
