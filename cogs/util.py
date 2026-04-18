import discord
from discord import app_commands
from discord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="soma", description="Some dois números distintos")
    @app_commands.describe(
        numero1="Primeiro número a somar",
        numero2="Segundo número a somar"
    )
    async def soma(self, interaction:discord.Interaction, numero1: int, numero2: int):
        resultado = numero1 + numero2
        await interaction.response.send_message(
            f"O número somado é {resultado}",
            ephemeral=True
        )

    @app_commands.command(name="ping", description="Mostra a Latência do Bot")
    async def ping(self, interaction:discord.Interaction):
        ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! {ms}ms")

async def setup(bot):
    await bot.add_cog(Util(bot))