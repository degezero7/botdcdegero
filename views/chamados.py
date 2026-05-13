import discord

STAFF_ROLE_ID = 889953705028378635 # Id do cargo da equipe
CATEGORY_NAME = "📂 CHAMADOS"

class FecharChamadoView(discord.ui.View):
    def __init__(self,):
        super().__init__(timeout=600)

    @discord.ui.button(label="Fechar Chamado", style=discord.ButtonStyle.danger, emoji="🔒")
    async def fechar_chamado(self, interaction:discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message("🔒 Fechando chamado...", ephemeral=True)
            await interaction.channel.delete(reason=f"Chamado fechado por {interaction.user}")
        except Exception as e:
            print(f"ERRO AO FECHAR CHAMADO: {e}")

class AbrirChamadoView(discord.ui.View):
    def __init__(self,):
        super().__init__(timeout=600)

    @discord.ui.button(label="Abrir Chamado", style=discord.ButtonStyle.primary, emoji="🎫")
    async def abrir_chamado(self, interaction: discord.Interaction, button:discord.ui.Button):

        try:
            guild = interaction.guild
            user = interaction.user

            staff_role = guild.get_role(STAFF_ROLE_ID)

            if staff_role is None:
                await interaction.response.send_message(
                    f"Cargo '{STAFF_ROLE_ID}' não encontrado.",
                    ephemeral=True)
                return
            
            category = discord.utils.get(
                guild.categories,
                name=CATEGORY_NAME
            )

            if category is None:
                category = await guild.create_category(
                    CATEGORY_NAME
                )

            existing_channel = discord.utils.get(
                guild.text_channels,
                name=f"chamado-{user.name.lower()}"
            )

            if existing_channel:
                await interaction.response.send_message(
                    f"Você já possui um chamado aberto: {existing_channel.mention}",
                    ephemeral=True
                )
                return

            # Membro do bot
            bot_member = guild.get_member(
                interaction.client.user.id
            )

            # Permmissão
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    view_channel=False
                    ),
                user: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                ),
                staff_role: discord.PermissionOverwrite(
                    view_channel=True, 
                    send_messages=True,
                    manage_channels=True
                    ),
                bot_member: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    manage_channels=True
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
        
            channel = await guild.create_text_channel(
                name=f"chamado-{user.name.lower()}",
                overwrites=overwrites,
                category=category,
                reason=f"Chamado aberto por {user}"
            )

            embed = discord.Embed(
                title="🎫 Chamado Aberto",
                description=(
                    f"Olá {user.mention}!\n\n"
                    "Explique com detalhes seu problema.\n"
                    "A equipe irá te responder em breve"
                    ),
                color=discord.Color.purple()
            )
            embed.add_field(
                name="Usuário", 
                value=user.mention, 
                inline=True
                )
            embed.add_field(
                name="Status", 
                value="Aberto ✅", 
                inline=True
                )

            await channel.send(
                content=f"{user.mention} {staff_role.mention}",
                embed=embed,
                view=FecharChamadoView()
            )

            await interaction.response.send_message(
                f"✅ Seu chamado foi criado: {channel.mention}",
                ephemeral=True
            )
        
        except Exception as e:
            print(f"ERRO CHAMADO: {e}")

            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"Erro '{e}'",
                    ephemeral=True
                    )