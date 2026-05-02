import discord

STAFF_ROLE_ID = 889953705028378635 # Id do cargo da equipe

class FecharChamadoView(discord.ui.View):
    def __init__(self,):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fechar Chamado", style=discord.ButtonStyle.danger, emoji="🔒")
    async def fechar_chamado(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(reason=f"Chamado fechado por {interaction.user}")

class AbrirChamadoView(discord.ui.View):
    def __init__(self,):
        super().__init__(timeout=600)

    @discord.ui.button(label="Abrir Chamado", style=discord.ButtonStyle.primary, emoji="🎫")
    async def abrir_chamado(self, interaction: discord.Interaction, button:discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
        }

        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_messages=True,
                manage_channels=True
            )
        
        channel_name = f"chamado-{user.name}".lower().replace("","-")

        existing = discord.utils.get(guild.text_channels, name=channel_name)

        if existing:
            await interaction.response.send_message(
                f"⚠️ Você possui um chamado aberto: {existing.mention}",
                ephemeral=True
            )
            return
    
        channel = await guild.text_channel(
            name=channel_name,
            overwrites=overwrites,
            reason=f"Chamado aberto por {user}"
        )

        embed = discord.Embed(
            title="🎫 Chamado Aberto",
            description=f"Olá {user.mention}, explique com detalhes seu problema. \n\nA equipe irá te responder em breve",
            color=discord.Color.purple()
        )
        embed.add_field(name="Usuário", value=user.mention, inline=True)
        embed.add_field(name="Status", value="Aberto", inline=True)

        await channel.send(
            content=f"{user.mention}",
            embed=embed,
            view=FecharChamadoView()
        )

        await interaction.response.send_message(
            f"✅ Seu chamado foi criado: {channel.mention}",
            ephemeral=True
        )