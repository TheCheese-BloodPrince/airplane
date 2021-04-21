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
@commands.cooldown(100,86400,commands.BucketType.guild)
async def kick(ctx, member : discord.Member, *, reason="None"):
  await member.send("You have been kicked in " + ctx.guild.name + " for: " + reason + ". You can rejoin if you obtain an invite.")
  await member.kick(reason = reason)
  await ctx.send("Kicked **" + member.name + "** for: " + reason + ". They can join if they manage to obtain an invite.")

#+ban
@bot.command(name='ban', description = 'Ban a troublesome user.')
@has_permissions(ban_members=True)
@commands.cooldown(100,86400,commands.BucketType.guild)
async def ban(ctx, member : discord.Member, *, reason="None"):
  await member.send("You have been banned in " + ctx.guild.name + " for: " + reason + ". You cannot rejoin unless unbanned.")
  await member.ban(reason=reason)
  await ctx.send("**" + member.name + "** has been banned for: " + reason + ". They cannot join the server unless unbanned.")

#+info
@bot.command(name='info', description='Information about airplane.')
@commands.cooldown(1,5,commands.BucketType.user)
async def info(ctx):
  await ctx.send("airplane is a Discord bot by The Cheese-Blood Prince#0505")
  await ctx.send("Contributors:")
  await ctx.send("https://github.com/TheCheese-BloodPrince")

#+afk
@bot.command(name='afk', description='Sets the user to afk.')
@commands.cooldown(1,30,commands.BucketType.user)
async def afk(ctx, *, reason):
  await ctx.send("**"+ctx.author.name+"** is AFK: " + reason)
  if ctx.author.nick == None:
    await ctx.author.edit(nick=("[AFK]"+ctx.author.name))
    db[str(ctx.author.id)+"_nick"] = ctx.author.name
  else:
    previousNick = ctx.author.nick
    await ctx.author.edit(nick=("[AFK]"+previousNick))
    db[str(ctx.author.id)+"_nick"] = ctx.author.nick
  

#+back
@bot.command(name='back', description="Removes the user's afk.")
@commands.cooldown(1,30,commands.BucketType.user)
async def back(ctx):
  await ctx.send("**"+ctx.author.name+"** is back! *attempts to smile*")
  await ctx.author.edit(nick=db[str(ctx.author.id)+"_nick"])
  

#+purge
@bot.command(name='purge', description="Purges a certain amount of messages.")
@has_permissions(manage_messages=True)
@commands.cooldown(1,60,commands.BucketType.guild)
async def purge(ctx, amount):
  await ctx.channel.purge(limit=int(amount))

#+dev
@bot.command(name='dev', description="Gives people the link to the GitHub so they can help build the bot.")
@commands.cooldown(1,5,commands.BucketType.user)
async def dev(ctx):
  await ctx.send("Thank you for your interest in helping airplane! You can help the airplane project here: https://github.com/TheCheese-BloodPrince/airplane")

#+mute
@bot.command(name='mute', description="Mutes a user SHUT THE HELL UP")
@has_permissions(manage_messages=True)
@commands.cooldown(100,86400,commands.BucketType.guild)
async def mute(ctx, member : discord.Member, *, reason="None"):
  muted = discord.utils.get(ctx.guild.roles, name="Muted")
  await member.add_roles(muted)
  await member.send("You have been muted in " + ctx.guild.name + " for: " + reason + ". You cannot talk there until unmuted.")
  await ctx.send("Muted **"+member.name+"**")

#+unmute
@bot.command(name='unmute', description="Unmuted the user they have served their sentence.")
@has_permissions(manage_messages=True)
@commands.cooldown(100,86400,commands.BucketType.guild)
async def unmute(ctx, member : discord.Member):
  muted = discord.utils.get(ctx.guild.roles, name="Muted")
  await member.remove_roles(muted)
  await member.send("You have been unmuted in " + ctx.guild.name + ". You can now talk there.")
  await ctx.send("**"+member.name+"** has been unmuted.")

#unban
@bot.command(name='unban', description="Allows you to unban a user maybe they were good boi after all")
@has_permissions(ban_members=True)
@commands.cooldown(100,86400,commands.BucketType.guild)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  for banned_entry in banned_users:
    user = banned_entry.user
  
  if(user.name)==(member):
    await ctx.guild.unban(user)
    await ctx.send("**"+user.name+"** has been unbanned! Maybe they were good boi after all")
    return
  await ctx.send("Member not found")

#tempban
@bot.command(name='tempban', description="Allows you to ban and then immediatly unban a user to delete all their messages in the past 24 hours.")
@has_permissions(kick_members=True)
@commands.cooldown(100,86400,commands.BucketType.guild)
async def tempban(ctx, member : discord.Member):
  await member.send("You have been temporarily banned in " + ctx.guild.name + " to wipe all your messages in the past 24 hours. Ask an admin to give you an invite as you have now been unbanned.")
  await ctx.guild.ban(member)
  banned_users = await ctx.guild.bans()
  for banned_entry in banned_users:
    user = banned_entry.user
  
  if(user.name)==(member.name):
    await ctx.guild.unban(user)
  await ctx.send("**"+member.name+"**'s messages in the past 24 hours have been deleted.'")

#warn
@bot.command(name='warn', description="Allows you to warn a user.")
@has_permissions(kick_members=True)
@commands.cooldown(100,86400,commands.BucketType.guild)
async def warn(ctx, member : discord.Member , *, reason="None"):
  db_keys = db.keys()
  key = (str(ctx.guild.id)+"_"+str(member.id)+"_warnings")
  warning = ("||Reason: " + reason + "; Moderator: " + ctx.author.name + "|| ** ** ** **")
  if key in db_keys:
    prevwarnings=db[key]
    currwarnings=prevwarnings+warning
    db[key]=currwarnings
    await ctx.send(db[key])
  else:
    db[key]=warning
    await ctx.send(db[key])
  await member.send("You have been warned in **" + ctx.guild.name + "** for **" + reason + "** by **" + ctx.author.name + "**")

#warnings
@bot.command(name='warnings', description="Checks the warnings of a user")
@has_permissions(kick_members=True)
@commands.cooldown(100,86400,commands.BucketType.guild)
async def warnings(ctx, member : discord.Member):
  key=(str(ctx.guild.id)+"_"+str(member.id)+"_warnings")
  await ctx.send(member.name + "'s warnings: " + db[key])

#clearwarn
@bot.command(name='clearwarn', description='Clears a users warnings')
@has_permissions(kick_members=True)
@commands.cooldown(100,86400,commands.BucketType.guild)
async def clearwarn(ctx, member : discord.Member):
  key=(str(ctx.guild.id)+"_"+str(member.id)+"_warnings")
  del db[key]
  await ctx.send("Cleared **" + member.name + "**'s warnings")

#avatar
@bot.command(name='avatar', description="Sends a user's avatar")
@commands.cooldown(1,5, commands.BucketType.member)
async def avatar(ctx):
  await ctx.send(ctx.author.avatar_url)

#membercount
@bot.command(name='membercount', description="Sends the amount of members in the guild.")
@commands.cooldown(1,5, commands.BucketType.member)
async def membercount(ctx):
  await ctx.send("Members in **"+ctx.guild.name+"**: " + str(ctx.guild.member_count))
#Running the Bot
keep_alive()
bot.run(TOKEN)
