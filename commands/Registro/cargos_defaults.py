import discord

from discord.ext import commands
from discord import option, slash_command
from db.register import addCargoReg


class registroCargosDefault(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name="cargos_defaults",
                   description="Adiciona os cargos defaults do registro")
    @option(name="cargo_default_reg", description="Cargo antes de registrar")
    @option(name="cargo_final_reg", description="Cargo que a depoid de registrado")
    async def cgdft(self,
                    interaction: discord.Interaction,
                    cargo_final_reg: discord.Role,
                    cargo_default_reg: discord.Role = None):

        if cargo_final_reg:
            addCargoReg(interaction.guild,
                        cargo_final_reg,
                        "defaults",
                        "finalreg")

        if cargo_default_reg:
            addCargoReg(interaction.guild,
                        cargo_default_reg,
                        "defaults",
                        "defaultreg")

        await interaction.response.send_message("Adicionado com sucesso", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(registroCargosDefault(bot))
