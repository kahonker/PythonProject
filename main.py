import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import time
Minecraft_Log = r"C:\Users\yuhao\Documents\server\server.log"

"hey Alexy, look here look here look here look here look here look here look here look here look here look here look here"
"replace the path in the Log variable above to the \"latest_log\" in your minecraft server"

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
ServerIsOn = False;
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


def read_log():
    with open(Minecraft_Log, "r", encoding="utf-8") as f:
        return f.read()

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - dont use that word!")

    await bot.process_commands(message)

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def LaunchCheck(ctx):
    await ctx.send(f"{ctx.author.mention}  the server is on: {ServerIsOn}")

@bot.command()
async def UserSpeaker(member):
    await member.send(f"Hi")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
text = read_log()