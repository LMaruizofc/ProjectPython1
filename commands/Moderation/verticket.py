import discord

from discord import SlashCommandGroup, option, slash_command
from discord.ext import commands
from classes.buttons import KickButtons
from utils.loader import configData
from db.moderation import adcLog


class ModerationVerTicket(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name='verticket', description='Mostra as mensagens do ultimo ticket de um membro')
    @option(name='membro', description='Mostra as mensagens o ultimo ticket da pessoa')
    async def verticket(self,
                        interaction: discord.Interaction,
                        membro: discord.Member
                        ):

        try:
            await interaction.response.send_message(
                file=discord.File(f'./tickets/{interaction.guild.id}{membro.id}.txt', f'Ticket de {membro.name}.txt'),
                ephemeral=True)
        except:
            await interaction.response.send_message('Esse membro ainda não abriu um ticket', ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(ModerationVerTicket(bot))
