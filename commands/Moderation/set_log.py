import discord

from discord import SlashCommandGroup, option, slash_command
from discord.ext import commands
from classes.buttons import KickButtons
from utils.loader import configData
from db.moderation import adcLog


class ModerationSetL(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name="set_logs", description="Define o canal de logs")
    @option(name="log", description="Define as logs do bot", choices=["Log de Registro", "Log De Ticket"])
    @option(name="canal", description="A categoria do cargo de registro")
    async def setLog(self,
                     interaction: discord.Interaction,
                     log: str,
                     canal: discord.TextChannel
                     ):

        await interaction.response.send_message(f"Prontinho, {log} setado para {canal.mention}")

        match log:
            case "Log de Registro":
                log = "regLog"
            case "Log De Ticket":
                log = "tckLog"

        adcLog(interaction.guild, log, canal)

def setup(bot: commands.Bot):
    bot.add_cog(ModerationSetL(bot))
