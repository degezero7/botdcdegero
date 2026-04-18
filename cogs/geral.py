import discord
from discord import app_commands
from discord.ext import commands

class Geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="saudação",description="Comando de saudação")
    async def olamundo(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Olá {interaction.user.mention}")

    @app_commands.command(name="embed", description="Exemplo de Embed")
    async def embed(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Meu primeiro embed",
            description="Primeiro embed do Bot",
            color=discord.Color.blue()
        )
        embed.add_field(name="Usuário", value=interaction.user.mention, inline=False)
        embed.set_footer(text="Bot criado por David")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Geral(bot))