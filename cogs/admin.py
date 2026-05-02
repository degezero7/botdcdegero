import discord
from discord import app_commands
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="limpar", description="Apaga mensagens do canal")
    @app_commands.command(quantidade="Quantidade de mensagens para apagar")
    async def limpar(self, interaction: discord.Interaction, quantidade: int):
    
        #permissão
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "Você não tem permissão para usar esse comando.",
                ephemeral=True
            )
            return
        
        if quantidade <= 0 or quantidade > 100:
            await interaction.response.send_message(
            "Escolha um numero entre 1 e 100.",
            ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        deleted = await interaction.channel.purge(limit=quantidade)

        await interaction.followup.send(
            f"🧹 {len(deleted)} mensagens foram apagadas.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Admin(bot))