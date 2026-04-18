import discord

class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
    
    @discord.ui.button(label="Ajuda", style=discord.ButtonStyle.primary, emoji="❓")
    async def ajuda(self, interaction:discord.Interaction, button:discord.ui.Button):
        embed = discord.Embed(
            title="Menu de Help",
            description="Aqui estão alguns comandos do Gezero.",
            color=discord.Color.blue()
        )
        embed.add_field(name="/ola-mundo", value="Mensagem de saudação", inline=False)
        embed.add_field(name="/soma", value="Soma dois números distintos", inline=False)
        embed.add_field(name="/versao", value="Mostra em qual versão atual do Gezero", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Ping", style=discord.ButtonStyle.success, emoji="🏓")
    async def ping(self, interaction:discord.Interaction, button:discord.ui.Button):
        latency = round(interaction.client.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! {latency}ms", ephemeral=True)
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger, emoji="🏓")
    async def fechar(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.edit_message(
            content="Menu fechado.",
            embed=None,
            view=None
        )