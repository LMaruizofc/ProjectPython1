import discord

from classes.Ticket import embedCreator
from discord import InvalidArgument, option, slash_command
from discord.ext import commands
from db.moderation import adccargoticket, db_temp_ticket
from tinydb import table

class ticketAdcCargo(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name="adc_cargos_ticket", description="Adiciona um cargo aos overwrites do ticket")
    @option(name="cargo", description="Mencione o cargo")
    @option(name="mention_cargo", description="Cargo para mencionar no ticket")
    async def adccargotck(self,
                          interaction: discord.Interaction,
                          cargo: discord.Role,
                          mention_cargo: discord.Role = None
                          ):

        await interaction.response.defer()

        await interaction.followup.send(f"{cargo.name} adicionado aos ticket")
        adccargoticket(interaction.guild, cargo.name, cargo)

        if mention_cargo != None:
            await interaction.followup.send(f"{mention_cargo.name} Adicionado as menções")
            adccargoticket(interaction.guild, "mentionable", mention_cargo)


def setup(bot: commands.Bot):
    bot.add_cog(ticketAdcCargo(bot))
