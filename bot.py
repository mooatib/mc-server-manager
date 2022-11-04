import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

token: str = os.environ.get("CLIENT_ID")

description = """Minecraft Server Manager
Made by dib."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def start(ctx):
    """Start EC2 instance"""
    await ctx.send()


bot.run(token)
