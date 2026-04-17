import discord
from discord import app_commands

class PrimeiroBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="$",
            intents=intents
        )
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"O Bot {self.user} Ligado com Sucesso!")

bot = PrimeiroBot()

@bot.tree.command(name="ola-mundo",description="Comando de apresentação")
async def olamundo(interaction:discord.Interaction):
    await interaction.response.send_message(f"Olá {interaction.user.mention}")

@bot.tree.command(name="soma",description="Some dois números distintos")
@app_commands.describe(
    numero1="Primeiro número a somar",
    numero2="Segundo número a somar"
)
async def olamundo(interaction:discord.Interaction,numero1:int,numero2:int):
    numero_somado = numero1 + numero2
    await interaction.response.send_message(f"O número somado é {numero_somado}",ephemeral=True)

from dotenv import load_dotenv
import os

load_dotenv()

bot.run(os.getenv("TOKEN"))


