import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("A variável TOKEN não foi encontrada no ambiente.")

GUILD_ID = 817116003178774580
guild = discord.Object(id=GUILD_ID)

intents = discord.Intents.default()
intents.message_content = False

bot = commands.Bot(command_prefix="!", intents=intents)

synced = False

@bot.event
async def on_ready():
    global synced

    if not synced:
        #copia os comandos globais para essa guild e sincroniza só nela
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild = guild)
        synced = True
        print("Slash commands sincronizados!")

    print(f"O Bot {bot.user} ligado com sucesso!")

@bot.tree.command(name="teste-novo", description="Teste da nova versão")
async def testenovo(interaction:discord.Interaction):
    await interaction.response.send_message("Versão nova funcionando!")

@bot.tree.command(name="versao", description="Mostra a versão atual")
async def versao(interaction:discord.Interaction):
    await interaction.response.send_message("Estou na nova versão do bot")

async def load_extensions():
    await bot.load_extension("cogs.geral")
    await bot.load_extension("cogs.util")

async def main():
    async with bot:
        print("===NOVA VERSÃO BOT===")
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())