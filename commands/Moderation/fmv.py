import discord

from discord import SlashCommandGroup, option, slash_command
from discord.ext import commands
from classes.buttons import KickButtons
from utils.loader import configData
from db.moderation import adcLog


class ModerationFmv(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name='fmv', description='Move um membro para uma outra call')
    @option(name='membro', description='Escolha o membro para mover para uma call')
    @option(name='canal', description='Escolha o canal para mover o membro')
    async def fmv(self,
                  interaction: discord.Interaction,
                  membro: discord.Member = None,
                  canal: discord.VoiceChannel = None
                  ):

        call = interaction.guild.get_channel(canal.id)

        if membro.voice is None:
            return await interaction.response.send_message(f'{membro.mention} não está em um canal de voz',
                                                           ephemeral=True)

        await membro.move_to(call)

        await interaction.response.send_message(f'{membro.mention} movido para {call}', ephemeral=True)

        cmdl = f'{interaction.user} usou o comando {interaction.command.name} e moveu o {membro.display_name} para o {canal.name}'

        cmdlc = self.bot.get_channel(configData['logs']['usocomandos'])

        await cmdlc.send(cmdl)

def setup(bot: commands.Bot):
    bot.add_cog(ModerationFmv(bot))
