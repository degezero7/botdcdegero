import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

#Token é o codigo confidencial do bot
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("A variável TOKEN não foi encontrada no ambiente.")

#Id do Usuário
OWNER_ID = 1068747060729352364

#Id do servidor
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
        # Copia os comandos para a guild de teste e remove o registro global
        # para evitar comandos de "/" duplicados dentro do servidor.
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        synced = True
        print("Slash commands sincronizados!")

    print(f"O Bot {bot.user} ligado com sucesso!")

@bot.tree.command(name="teste-novo", description="Teste da nova versão")
async def testenovo(interaction:discord.Interaction):
    await interaction.response.send_message("Versão nova funcionando!")

@bot.tree.command(name="versao", description="Mostra a versão atual")
async def versao(interaction:discord.Interaction):
    await interaction.response.send_message("Estou na nova versão do bot")

#Desligar o bot pelo discord
@bot.tree.command(name="desligar", description="Desligar o bot")
async def desligar(interaction: discord.Interaction):

    is_owner = interaction.user.id == OWNER_ID
    is_admin = interaction.user.guild_permissions.administrator
    
    if not (is_owner or is_admin):
        await interaction.response.send_message(
            "❌ Opa! Calma lá, apenas Administradores podem usar.",
            ephemeral=True
        )
        return

    await interaction.response.send_message("Desligando...", ephemeral=True)
    await bot.close()

async def load_extensions():
    await bot.load_extension("cogs.geral")
    await bot.load_extension("cogs.util")

async def main():
    async with bot:
        print("===BOT INICIANDO===")
        await load_extensions()
        await bot.start(TOKEN)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("⛔ Encerrando bot... ⛔")