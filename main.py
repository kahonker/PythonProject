import discord
from discord.ext import commands
import logging
import threading
from fastapi import FastAPI, Request
import asyncio
from server_management import check_server_status, server_start
from dotenv import load_dotenv
import os
import uvicorn
import re

Minecraft_Log = r"C:\Users\yuhao\Documents\server\server.log"

"hey Alexy, look here look here look here look here look here look here look here look here look here look here look here"
"replace the path in the Log variable above to the \"latest_log\" in your minecraft server"


GUILD_ID = "1462632241585979394"
LOG_CHANNEL_ID = 1462636342881161237
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
server_starting = False
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # REQUIRED

bot = commands.Bot(command_prefix='!', intents=intents)


app = FastAPI()

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

    if "shit" in message.content.lower() or "fuck" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - dont use that word!")

    await bot.process_commands(message)

@bot.event
async def InGameChatHadMentionedSomeOne(message):

@bot.command()
async def dm(ctx, user: discord.User, *, msg):
    try:
        await user.send(msg)
        await ctx.send("DM sent!")
    except discord.Forbidden:
        await ctx.send("I can't DM that user.")


@bot.command()
async def start_server(ctx):
    global server_starting
    if check_server_status() or server_starting:
        await ctx.send("The server is already started")
        return

    server_start()

    server_starting = True

    await ctx.send("Starting server")



@bot.command()
async def check_status(ctx): # renamed LaunchCheck to check_status for python conventions
    global server_starting
    status = check_server_status()
    if status:
        server_starting = False
        message = "🟩 The server is on "
        if status.players.sample is not None:
            message += "\nPlayers online:"
            for player in status.players.sample:
                message += "\n" + player.name
        await ctx.send(message)
    else:
        await ctx.send("🟥 The server is off, or there was a problem connecting to it") # changed the messages


@bot.command()
async def UserSpeaker(member):
    await member.send(f"Hi")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")



@app.post("/log_message")
async def send_log_message(request: Request):
    try:
        payload = await request.json()
        body = payload.get("data", "")
        channel = bot.get_channel(LOG_CHANNEL_ID)
        if re.search(r"(\[\d{2}:\d{2}:\d{2}\])\s*\[.*?/INFO\]:\s*(.*)", body):  # pattern == [HH:MM:SS][Server/Thread] wut ever
            time_part = match.group(1)
            message_part = match.group(2)
            if re.search(r"achievement \[(.*?)\]", message_part): #...achievement [title]
                messageToSend = time_part + "\n" + discord.Embed(
                    title="Achievement!",
                    description=match.group(2),
                    color=discord.Color.gold()
                )
            elif re.match(r'^<([^>]+)>\s*(.+)$', message): #<username> speech
                username = match.group(1)
                speech = match.group(2)
                messageToSend = time_part + f"\033[36m{username}\033[0m " +0xFFD700+ speech
                if
        else:
            messageToSend = body
        asyncio.run_coroutine_threadsafe(channel.send(body), bot.loop)
    except Exception as e:
        print(e)


# text = read_log()

def run_bot():
    bot.run(token, log_handler=handler, log_level=logging.DEBUG)


if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    uvicorn.run(app, host="192.168.12.176", port=8000)