import discord

OWNER_ID = 1068747060729352364

class MenuView(discord.ui.View):
    def __init__(self, user:discord.User):
        super().__init__(timeout=120)
    
        if hasattr(user, "guild_permissions"):
            is_admin = user.guild_permissions.administrator
        else:
            is_admin = False

        is_owner = user.id == OWNER_ID

        if is_owner or is_admin:
            self.add_item(DesligarButton())

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
        embed.add_field(name="/desligar", value="Desliga o bot", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Ping", style=discord.ButtonStyle.success, emoji="🏓")
    async def ping(self, interaction:discord.Interaction, button:discord.ui.Button):
        latency = round(interaction.client.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! {latency}ms", ephemeral=True)
    
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.danger, emoji="⛔")
    async def fechar(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.edit_message(
            content="Menu fechado.",
            embed=None,
            view=None
        )

class DesligarButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Desligar Bot", style=discord.ButtonStyle.danger, emoji="🛑")

    async def callback(self, interaction:discord.Interaction):
        user = interaction.user

        is_owner = user.id == OWNER_ID
        is_admin = user.guild_permissions.administrator

        if not (is_owner or is_owner):
            await interaction.response.send_message(
                "❌ Você não tem permissão para desligar o bot.",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message("🛑 Desligando o bot...", ephemeral=True)
        await interaction.client.close()