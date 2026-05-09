import discord
from discord import app_commands
from discord.ext import commands
from services.dragon_soul_service import buscar_item_por_nome

class Trade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@app_commands.command(name="valor", description="Consulta o valor de um item do Dragon Soul")
@app_commands.describe(item="Nome do item")
async def valor(self, interaction: discord.Interaction, item: str):
    await interaction.response.defer()

    resultado = await buscar_item_por_nome(item)

    if not resultado:
        await interaction.followup.send(
            f"Nenhum item encontrado com o nome '{item}'"
        )
        return
    
    nome = resultado.get("name", "Nome não informado")
    valor = resultado.get("value", "Valor não informado")
    demanda = resultado.get("demand", "Demanda não informada")
    tendencia = resultado.get("trend", "Tendência não informada")
    categoria = resultado.get("category", "Categoria não informada")

    embed = discord.Embed(
        title=f"📊 {nome}",
        description="Valor atualizado pelo sistema Dragon Soul Values.",
        color=discord.Color.gold()
    )

    embed.add_field(name="💰 Valor", value=str(valor), inline=True)
    embed.add_field(name="🔥 Demanda", value=str(demanda), inline=True)
    embed.add_field(name="🧭 Tendência", value=str(tendencia), inline=True)
    embed.add_field(name="📦 Categoria", value=str(categoria), inline=False)

    embed.set_footer(text="Fonte: Dragon Soul Values")

    await interaction.followup.send(embed=embed)

async def setup (bot):
    await bot.add_cog(Trade(bot))