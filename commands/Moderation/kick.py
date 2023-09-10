import discord

from discord import SlashCommandGroup, option, slash_command
from discord.ext import commands
from classes.buttons import KickButtons
from utils.loader import configData
from db.moderation import adcLog


class ModerationKick(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name="kick", description="Expulsa um membro")
    @option(name="membro", description="Escolha o membro")
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self,
                   interaction: discord.Interaction,
                   membro: discord.Member,
                   motivo: str = None
                   ):

        if motivo is None:
            motivo = "Motivo não informado"

        e1 = discord.Embed(title="kick", description=f"Voce esta prestes a expulsar {membro.mention}")
        e1.set_footer(text=motivo)

        if membro == self.bot.user:
            return await interaction.response.send_message("Não posso expulsar a mim mesmo")

        elif membro == interaction.user:
            return await interaction.response.send_message("Você não pode expulsar a si mesmo")

        await interaction.response.send_message(embed=e1, view=KickButtons())

        cmdl = f"""{interaction.user} usou o comando {interaction.command.name} e expulsou o {membro.name}"""

        cmdlc = self.bot.get_channel(configData["logs"]["usocomandos"])

        await cmdlc.send(cmdl)

def setup(bot: commands.Bot):
    bot.add_cog(ModerationKick(bot))
