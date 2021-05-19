# Setting Up the Bot
import os
import discord
#from dotenv import load_dotenv
from keep_alive import keep_alive
#from replit import db
import random
#load_dotenv()
command_prefix = "="
#TOKEN = os.getenv('TOKEN')
class Client(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def on_ready(self):
        print("Airplane has started up; Can now execute commands.")
    
    async def on_message(self, message: discord.Message):
        if  message.content.startswith(command_prefix):
            print(message.content)
            command = message.content.split()[0].removeprefix(command_prefix)
            if command == "on_message" or command == "on_ready" or command == "__init__" or command == "run":
                await message.channel.send('Invalid command')
                return
            parameters = message.content.split()[1:]
            print(command)
            if hasattr(self, command):
                await getattr(self, command)(message, *parameters)
            else:
                await message.channel.send('Invalid command')
                return
            
    async def info(self, message):
        await message.channel.send("airplane is a Discord bot by The Cheese-Blood Prince#0505\nContributors:\nhttps://github.com/TheCheese-BloodPrince\nhttps://github.com/NeilShah2006")
    
    def run(self):
        super().run()

keep_alive()
x = Client()
x.run()
