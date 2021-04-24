#Setting Up the Bot
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
from discord.ext.commands import has_permissions
from replit import db
import random
import json
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
async def kick(ctx, member : discord.Member, *, reason="None"):
  await member.send("You have been kicked in " + ctx.guild.name + " for: " + reason + ". You can rejoin if you obtain an invite.")
  await member.kick(reason = reason)
  await ctx.send("Kicked **" + member.name + "** for: " + reason + ". They can join if they manage to obtain an invite.")

#+ban
@bot.command(name='ban', description = 'Ban a troublesome user.')
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason="None"):
  await member.send("You have been banned in " + ctx.guild.name + " for: " + reason + ". You cannot rejoin unless unbanned.")
  await member.ban(reason=reason)
  await ctx.send("**" + member.name + "** has been banned for: " + reason + ". They cannot join the server unless unbanned.")

#+info
@bot.command(name='info', description='Information about airplane.')
async def info(ctx):
  await ctx.send("airplane is a Discord bot by The Cheese-Blood Prince#0505\nContributors:\nhttps://github.com/TheCheese-BloodPrince")

#+afk
@bot.command(name='afk', description='Sets the user to afk.')
async def afk(ctx, *, reason="AFK"):
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
async def back(ctx):
  await ctx.send("**"+ctx.author.name+"** is back! *attempts to smile*")
  await ctx.author.edit(nick=db[str(ctx.author.id)+"_nick"])
  

#+purge
@bot.command(name='purge', description="Purges a certain amount of messages.")
@has_permissions(manage_messages=True)
async def purge(ctx, amount):
  await ctx.channel.purge(limit=int(amount))

#+dev
@bot.command(name='dev', description="Gives people the link to the GitHub so they can help build the bot.")
async def dev(ctx):
  await ctx.send("Thank you for your interest in helping airplane! You can help the airplane project here: https://github.com/TheCheese-BloodPrince/airplane")

#+mute
@bot.command(name='mute', description="Mutes a user SHUT THE HELL UP")
@has_permissions(manage_messages=True)
async def mute(ctx, member : discord.Member, *, reason="None"):
  muted = discord.utils.get(ctx.guild.roles, name="Muted")
  await member.add_roles(muted)
  await member.send("You have been muted in " + ctx.guild.name + " for: " + reason + ". You cannot talk there until unmuted.")
  await ctx.send("Muted **"+member.name+"**")

#+unmute
@bot.command(name='unmute', description="Unmuted the user they have served their sentence.")
@has_permissions(manage_messages=True)
async def unmute(ctx, member : discord.Member):
  muted = discord.utils.get(ctx.guild.roles, name="Muted")
  await member.remove_roles(muted)
  await member.send("You have been unmuted in " + ctx.guild.name + ". You can now talk there.")
  await ctx.send("**"+member.name+"** has been unmuted.")

#+unban
@bot.command(name='unban', description="Allows you to unban a user maybe they were good boi after all")
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  for banned_entry in banned_users:
    user = banned_entry.user
  
  if(user.name)==(member):
    await ctx.guild.unban(user)
    await ctx.send("**"+user.name+"** has been unbanned! Maybe they were good boi after all")
    return
  await ctx.send("Member not found")

#+tempban
@bot.command(name='tempban', description="Allows you to ban and then immediatly unban a user to delete all their messages in the past 24 hours.")
@has_permissions(kick_members=True)
async def tempban(ctx, member : discord.Member):
  await member.send("You have been temporarily banned in " + ctx.guild.name + " to wipe all your messages in the past 24 hours. Ask an admin to give you an invite as you have now been unbanned.")
  await ctx.guild.ban(member)
  banned_users = await ctx.guild.bans()
  for banned_entry in banned_users:
    user = banned_entry.user
  
  if(user.name)==(member.name):
    await ctx.guild.unban(user)
  await ctx.send("**"+member.name+"**'s messages in the past 24 hours have been deleted.'")

#+warn
@bot.command(name='warn', description="Allows you to warn a user.")
@has_permissions(kick_members=True)
async def warn(ctx, member : discord.Member , *, reason="None"):
  db_keys = db.keys()
  key = (str(ctx.guild.id)+"_"+str(member.id)+"_warnings")
  warning = ("Reason: " + reason + " Moderator: " + ctx.author.name + "\n")
  if key in db_keys:
    prevwarnings=db[key]
    currwarnings=prevwarnings+warning
    db[key]=currwarnings
    await ctx.send(db[key])
  else:
    db[key]=warning
    await ctx.send(db[key])
  await member.send("You have been warned in **" + ctx.guild.name + "** for **" + reason + "** by **" + ctx.author.name + "**")

#+warnings
@bot.command(name='warnings', description="Checks the warnings of a user")
@has_permissions(kick_members=True)
async def warnings(ctx, member : discord.Member):
  key=(str(ctx.guild.id)+"_"+str(member.id)+"_warnings")
  await ctx.send(member.name + "'s warnings: " + db[key])

#+clearwarn
@bot.command(name='clearwarn', description='Clears a users warnings')
@has_permissions(kick_members=True)
async def clearwarn(ctx, member : discord.Member):
  key=(str(ctx.guild.id)+"_"+str(member.id)+"_warnings")
  del db[key]
  await ctx.send("Cleared **" + member.name + "**'s warnings")

#+avatar
@bot.command(name='avatar', description="Sends a user's avatar")
async def avatar(ctx):
  await ctx.send(ctx.author.avatar_url)

#+membercount
@bot.command(name='membercount', description="Sends the amount of members in the guild.")
async def membercount(ctx):
  await ctx.send("Members in **"+ctx.guild.name+"**: " + str(ctx.guild.member_count))




#+register
@bot.command(name='register', description="Registers you for a currency account in airplane. Remember this wipes all of your progress if you have already used the currency system before. If you want to be careful, run +balance and if nothing is outputted, it is safe to run this.")
async def register(ctx):
  db[str(ctx.author.id)+"_bank"]=int(0)
  db[str(ctx.author.id)+"_networth"]=int(200)
  db[str(ctx.author.id)+"_revenue"]=int(20)
  db[str(ctx.author.id)+"_laptop"]=int(0)
  await ctx.send("Registered **" + ctx.author.name + "** for a currency account.")

#+balance
@bot.command(name='balance', description="Sends a user's balance.")
async def balance(ctx):
  userid = (str(ctx.author.id)+"_bank")
  await ctx.send("**" + ctx.author.name + "** has " + str(db[userid]) + " coins.")

#+give
@bot.command(name='give', description="Allows a user to give another user money.")
async def give(ctx, member : discord.Member, amount):
  if int(amount) >= 0:
    if db[str(ctx.author.id)+"_bank"] <= int(amount):
      await ctx.send("You don't have that much money!")
    else:
      db[str(member.id)+"_bank"] += int(amount)
      db[str(ctx.author.id)+"_bank"] -= int(amount)
      await ctx.send("**" + ctx.author.name + "** has given **" + member.name + "** **" + str(amount) + "** coins.")
  else:
    await ctx.send("Did you really try that?")
  
#+shop
@bot.command(name='shop', description="Shows all the items on market. Run +shop laptops to see available laptops.")
async def shop(ctx, *, item):
  if item == "laptops":
    await ctx.send("These are the laptops in stock:\nCheap Cheesett-Packard: $210; ID=1\nCheap CheesePad: $250; ID=2\nCheap Cheese-Soft: $400; ID=3\nCheap Cheesy-Goldstar: $800; ID=4\nCheeseBook Air: $1000; ID=5\nProfessional Cheese-Soft: $1400; ID=6\nProfessional Cheesett-Packard: $1670; ID=7\nProfessional Cheesy-Goldstar: $1900; ID=8\nCheeseBook Pro: $2400; ID=9\nProfessional Bell: $4110; ID=10\nProfessional Cheeser: $4300; ID=11\nProfessional CheesePad: $4660; ID=12")
  elif item == "collectibles":
    await ctx.send("These are the collectibles in stock:\nModel Train: $35; ID=13\nAirplane: $4500000")
  else:
    await ctx.send("Sorry, this item is not in stock.")

#+profile
@bot.command(name='profile', description="Allows you to view your profile.")
async def profile(ctx):
  await ctx.send("Name: **"+ctx.author.name+"**\nNetworth: **"+str(db[str(ctx.author.id)+"_networth"])+"**\nLaptop ID: **"+str(db[str(ctx.author.id)+"_laptop"])+"**")

#+buy
@bot.command(name='buy', description='Allows you to buy an item. Example: +buy 9')
async def buy(ctx, *, item):
  networth_key=(str(ctx.author.id)+"_networth")
  laptop_key=(str(ctx.author.id)+"_laptop")
  revenue_key=(str(ctx.author.id)+"_revenue")
  bank_key = (str(ctx.author.id)+"_bank")
  if item == "1":
    if int(db[bank_key])<=210:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 1
      db[revenue_key] = 21
      db[networth_key] = int(db[networth_key]) + int(210)
      db[bank_key] -= 210
      await ctx.send("**"+ctx.author.name+"** has bought the Cheap Cheesett-Packard.")
  elif item == "2":
    if int(db[bank_key])<=250:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 2
      db[revenue_key] = 24
      db[networth_key] = int(db[networth_key]) + int(250)
      db[bank_key] -= 250
      await ctx.send("**"+ctx.author.name+"** has bought the Cheap CheesePad.")
  elif item == "3":
    if int(db[bank_key])<=400:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 3
      db[revenue_key] = 40
      db[networth_key] = int(db[networth_key]) + int(400)
      db[bank_key] -= 400
      await ctx.send("**"+ctx.author.name+"** has bought the Cheap Cheese-Soft.")
  elif item == "4":
    if int(db[bank_key])<=800:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 4
      db[revenue_key] = 80
      db[networth_key] = int(db[networth_key]) + int(800)
      db[bank_key] -= 800
      await ctx.send("**"+ctx.author.name+"** has bought the Cheap Cheesy-Goldstar")
  elif item == "5":
    if int(db[bank_key])<=1000:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 5
      db[revenue_key] = 100
      db[networth_key] = int(db[networth_key]) + int(1000)
      db[bank_key] -= 1000
      await ctx.send("**"+ctx.author.name+"** has bought the CheeseBook Air")
  elif item == "6":
    if int(db[bank_key])<=1400:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 6
      db[revenue_key] = 140
      db[networth_key] = int(db[networth_key]) + int(1400)
      db[bank_key] -= 1400
      await ctx.send("**"+ctx.author.name+"** has bought the Professional Cheese-Soft")
  elif item == "7":
    if int(db[bank_key])<=1670:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 7
      db[revenue_key] = 167
      db[networth_key] = int(db[networth_key]) + int(1670)
      db[bank_key] -= 1670
      await ctx.send("**"+ctx.author.name+"** has bought the Professional Cheesett-Packard")
  elif item == "8":
    if int(db[bank_key])<=1900:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 8
      db[revenue_key] = 190
      db[networth_key] = int(db[networth_key]) + int(1900)
      db[bank_key] -= 1900
      await ctx.send("**"+ctx.author.name+"** has bought the Professional Cheesy-Goldstar")
  elif item == "9":
    if int(db[bank_key])<=2400:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 9
      db[revenue_key] = 240
      db[networth_key] = int(db[networth_key]) + int(2400)
      db[bank_key] -= 2400
      await ctx.send("**"+ctx.author.name+"** has bought the CheeseBook Pro")
  elif item == "10":
    if int(db[bank_key])<=4110:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 10
      db[revenue_key] = 411
      db[networth_key] = int(db[networth_key]) + int(4110)
      db[bank_key] -= 4100
      await ctx.send("**"+ctx.author.name+"** has bought the Professional Bell")
  elif item == "11":
    if int(db[bank_key])<=4300:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 11
      db[revenue_key] = 430
      db[networth_key] = int(db[networth_key]) + int(4300)
      db[bank_key] -= 4300
      await ctx.send("**"+ctx.author.name+"** has bought the Professional Cheeser")
  elif item == "12":
    if int(db[bank_key])<=4660:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[laptop_key] = 12
      db[revenue_key] = 466
      db[networth_key] = int(db[networth_key]) + int(4660)
      db[bank_key] -= 4660
      await ctx.send("**"+ctx.author.name+"** has bought the Professional CheesePad")
  elif item == "13":
    if int(db[bank_key])<=35:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
    else:
      db[networth_key] = int(db[networth_key]) + int(35)
      db[bank_key] -= 35
      await ctx.send("**"+ctx.author.name+"** has bought a model train.")
  elif item == "14":
    if int(db[bank_key])<=4500000:
      await ctx.send("You don't have enough money to buy that! Run +code to code to earn money.")
  else:
    await ctx.send("That item is not in stock.")

#+code
@bot.command(name='code', description="Allows you to code to earn money. The better laptop you have, the more money you earn.")
@commands.cooldown(1,60,commands.BucketType.user)
async def code(ctx):
  await ctx.send("Coding...")
  pay = random.randint(0, db[str(ctx.author.id)+"_revenue"])
  data = ["an operating system!\n", "a reading app!\n", "a team planning app!\n", "a video game!\n", "a chatting app!\n", "a Discord bot!\n", "a video chatting app!\n", "a GPS app!\n", "a coding platform!\n", "a web browser!\n", "a search engine!\n", "a website!\n", "a video editor!\n", "a music platform!\n", "a news platform!\n", "a note taking app!\n", "a coding language!\n", "a stock tracker!\n"]
  await ctx.send("You made " + random.choice(data) + "You earnt " + str(pay) + " coins!")
  db[str(ctx.author.id)+"_bank"] += pay

#+roll
@bot.command(name='roll', description="Rolls a die.")
async def roll(ctx):
  await ctx.send(str(random.randint(1,6)))

#+rps
@bot.command(name='rps', description="Plays rock paper scissors with the bot.")
async def rps(ctx, choice):
  botoptions=["rock", "paper", "scissors"]
  botchoice=random.choice(botoptions)
  if choice.lower() == "rock" and botchoice == "rock":
    await ctx.send("The member chose rock and the bot chose rock. It is a tie.")
  elif choice.lower() == "rock" and botchoice == "paper":
    await ctx.send("The member chose rock and the bot chose paper. The bot wins.")
  elif choice.lower() == "rock" and botchoice == "scissors":
    await ctx.send("The member chose rock and the bot chose scissors. The member wins.")
  elif choice.lower() == "paper" and botchoice == "rock":
    await ctx.send("The member chose paper and the bot chose rock. The member wins.")
  elif choice.lower() == "paper" and botchoice == "paper":
    await ctx.send("The member chose paper and the bot chose paper. It is a tie.")
  elif choice.lower() == "paper" and botchoice == "scissors":
    await ctx.send("The member chose paper and the bot chose scissors. The bot wins.")
  elif choice.lower() == "scissors" and botchoice == "rock":
    await ctx.send("The member chose scissors and the bot chose rock. The bot wins.")
  elif choice.lower() == "scissors" and botchoice == "paper":
    await ctx.send("The member chose scissors and the bot chose paper. The member wins.")
  elif choice.lower() == "scissors" and botchoice == "scissors":
    await ctx.send("The member chose scissors and the bot chose scissors. It is a tie.")
  else:
    await ctx.send("You need to send 'rock', 'paper', or 'scissors'")

#+github
@bot.command(name='github', description="Sends a GitHub profile/repository\n+github TheCheese-BloodPrince\n+github TheCheese-BloodPrince/airplane")
async def github(ctx, repo):
  await ctx.send("https://github.com/"+repo)





#Running the Bot
keep_alive()
bot.run(TOKEN)
