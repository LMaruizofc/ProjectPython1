import discord

from discord import SlashCommandGroup, option, slash_command
from discord.ext import commands
from classes.buttons import KickButtons
from utils.loader import configData
from db.moderation import adcLog


class ModerationClear(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name='clear', description='Limpa o chat')
    @option(name='quantidade', type=int, description='Escolha a quantidade de mensagens a limpar')
    @commands.has_guild_permissions(manage_channels=True)
    async def clear(self,
                    interaction: discord.Interaction,
                    quantidade: int = 0
                    ):

        if quantidade > 100:
            return await interaction.response.send_message('O limite maximo é de 100 mensagens')

        elif quantidade == 0:
            return await interaction.response.send_message(
                'Você precisa escolher uma quantidade de mensagens, a quantidade maxima é 100 mensagens')

        purge = await interaction.channel.purge(limit=quantidade)

        await interaction.response.send_message(
            f"O chat teve {len(purge)} mensagens apagadas por {interaction.user.mention}")

        cmdl = f'''{interaction.user} usou o comando {interaction.command.name} e apagou {len(purge)} mensagens no {interaction.channel}'''

        cmdlc = self.bot.get_channel(configData['logs']['usocomandos'])

        await cmdlc.send(cmdl)

def setup(bot: commands.Bot):
    bot.add_cog(ModerationClear(bot))
