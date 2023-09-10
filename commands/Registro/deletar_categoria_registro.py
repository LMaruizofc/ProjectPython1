import discord

from discord.ext import commands
from discord import option, slash_command
from db.register import regCargo


class registrodelCatego(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot


    @slash_command(guild_only=True, name="deletar_categoria_registro",
                   description="Adiciona ou edita um cargo ao registro")
    @option(name="categoria", description="A categoria do cargo de registro")
    async def rmvCatego(self,
                        interaction: discord.Interaction,
                        categoria: str,
                        ):

        try:

            var = regCargo.find_one({"_id": interaction.guild.id})[categoria]
            for dbc in regCargo.find_one({"_id": interaction.guild.id}):
                if dbc == categoria:
                    for c in regCargo.find_one({"_id": interaction.guild.id})[categoria]:
                        regCargo.find_one_and_update(
                            {"_id": interaction.guild.id},
                            {"$unset": {f"{categoria}": c}}
                        )
            await interaction.response.send_message(
                f"Prontinho, categoria \"{categoria}\" removida",
                ephemeral=True
            )

        except:
            await interaction.response.send_message(
                f"Não encontrei a categoria \"{categoria}\" no meu banco de dados",
                ephemeral=True
            )

def setup(bot: commands.Bot):
    bot.add_cog(registrodelCatego(bot))
