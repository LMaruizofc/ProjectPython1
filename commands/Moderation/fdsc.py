import discord

from discord import SlashCommandGroup, option, slash_command
from discord.ext import commands
from classes.buttons import KickButtons
from utils.loader import configData
from db.moderation import adcLog


class ModerationFdsc(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name='fdsc', description='Desconecta uma pessoa da call')
    @option(name='membro', description='Escolha o membro para desconectar da call')
    async def fdsc(self,
                   interaction: discord.Interaction,
                   membro: discord.Member = None
                   ):

        if membro.voice is None:
            return await interaction.response.send_message(f'{membro.mention} não está em um canal de voz',
                                                           ephemeral=True)

        await membro.move_to(None)

        await interaction.response.send_message(f'{membro.mention} desconectado com sucesso', ephemeral=True)

        cmdl = f'{interaction.user} usou o comando {interaction.command.name} e desconectou o {membro.display_name}'

        cmdlc = self.bot.get_channel(configData['logs']['usocomandos'])

        await cmdlc.send(cmdl)

def setup(bot: commands.Bot):
    bot.add_cog(ModerationFdsc(bot))
