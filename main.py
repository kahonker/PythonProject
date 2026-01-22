import discord
from discord.ext import commands
import logging
import threading
from fastapi import FastAPI, Request
from fastapi.dependencies.utils import request_body_to_args

from server_management import check_server_status
from dotenv import load_dotenv
import os
import uvicorn
Minecraft_Log = r"C:\Users\yuhao\Documents\server\server.log"

"hey Alexy, look here look here look here look here look here look here look here look here look here look here look here"
"replace the path in the Log variable above to the \"latest_log\" in your minecraft server"


GUILD_ID = "1462632241585979394"
LOG_CHANNEL_ID = "1462636342881161237"
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
ServerIsOn = False
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # REQUIRED

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

    if "shit" in message.content.lower() or "fuck" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - dont use that word!")

    await bot.process_commands(message)

@bot.command()
async def dm(ctx, user: discord.User, *, msg):
    try:
        await user.send(msg)
        await ctx.send("DM sent!")
    except discord.Forbidden:
        await ctx.send("I can't DM that user.")

@bot.command()
async def check_status(ctx): # renamed LaunchCheck to check_status for python conventions
    status = check_server_status()
    if status:
        await ctx.send("🟩 The server is on")
    else:
        await ctx.send("🟥 The server is off, or there was a problem connecting to it") # changed the messages

@bot.command()
async def UserSpeaker(member):
    await member.send(f"Hi")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

app = FastAPI()


@app.post("/log_message")
async def send_log_message(request: Request):
    body = request.get("message")
    await bot.get_guild(GUILD_ID).get_channel(LOG_CHANNEL_ID).send(body)

# text = read_log()

def run_bot():
    bot.run(token, log_handler=handler, log_level=logging.DEBUG)


if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    uvicorn.run(app, host="127.0.0.1", port=8000)