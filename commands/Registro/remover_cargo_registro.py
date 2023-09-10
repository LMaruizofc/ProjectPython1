import discord

from discord.ext import commands
from discord import option, slash_command
from db.register import rmvCargoReg, regCargo


class registroRmvCargo(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    
    @slash_command(guild_only=True, name="remover_cargo_registro",
                   description="Adiciona ou edita um cargo ao registro")
    @option(name="categoria", description="A categoria do cargo de registro")
    @option(name="nome", description="Nome do cargo para remover")
    async def rmvCargoReg(self,
                          interaction: discord.Interaction,
                          categoria: str,
                          nome: str
                          ):

        try:

            var = regCargo.find_one({"_id": interaction.guild.id})[categoria][nome]
            for dbg in regCargo.find_one({"_id": interaction.guild.id}):
                if dbg == categoria:
                    for c in regCargo.find_one({"_id": interaction.guild.id})[categoria]:
                        regCargo.find_one_and_update(
                            {"_id": interaction.guild.id},
                            {"$unset": {f"{categoria}": c}}
                        )

            rmvCargoReg(interaction.guild, categoria, nome)
            await interaction.response.send_message(f"Prontinho, cargo {nome} removido da categoria {categoria}",
                                                    ephemeral=True)

        except:
            await interaction.response.send_message(
                f"Não encontrei o cargo \"{nome}\" na categoria \"{categoria}\"",
                ephemeral=True
            )


def setup(bot: commands.Bot):
    bot.add_cog(registroRmvCargo(bot))
