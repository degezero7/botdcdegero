import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("A variável TOKEN não foi encontrada no ambiente.")

intents = discord.Intents.default()
intents.message_content = False

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"O Bot {bot.user} ligado com sucesso!")

async def load_extensions():
    await bot.load_extension("cogs.geral")
    await bot.load_extension("cogs.util")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())