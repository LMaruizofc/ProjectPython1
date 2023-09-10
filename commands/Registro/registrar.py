import discord

from discord.ext import commands
from classes.buttons import creatorButton
from discord import option, slash_command, user_command


class registroRegistrar(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name="registrar", description="Registra um membro")
    @option(name="membro", description="Escolha um membro a registrar")
    async def regSlashCommand(self, interaction: discord.Interaction, membro: discord.Member):

        e = discord.Embed(title="Registro", description="Escolha a categoria que deseja")
        e.set_author(name=f"Registrado {membro.id}")
        e.set_footer(text=f"Registrador {interaction.user.id}")

        try:
            await interaction.response.send_message(
                embed=e,
                view=creatorButton(
                    type="selectCatego",
                    guild_id=interaction.guild.id
                )
            )
        except:
            await interaction.response.send_message(
                "Nenhum registro criado ainda",
                ephemeral=True
            )

    @user_command(guild_only=True, name="Registrar", description="Registra um membro")
    @option(name="membro", description="Escolha um membro a registrar")
    async def regUserCommand(self, interaction: discord.Interaction, membro: discord.Member):

        e = discord.Embed(title="Registro", description="Escolha a categoria que deseja")
        e.set_author(name=f"Registrado {membro.id}")
        e.set_footer(text=f"Registrador {interaction.user.id}")

        try:
            await interaction.response.send_message(
                embed=e,
                view=creatorButton(type="selectCatego",
                guild_id=interaction.guild.id
                )
            )
        except:
            await interaction.response.send_message(
                "Nenhum registro criado ainda", 
                ephemeral=True
            )


def setup(bot: commands.Bot):
    bot.add_cog(registroRegistrar(bot))
