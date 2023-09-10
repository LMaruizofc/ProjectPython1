from datetime import datetime, timedelta
import discord

from discord.ext import commands
from discord import option, slash_command
from db.register import addCargoReg, regCargo
from db.dono import modDono, Premium


class registroAdcCargo(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name="adicionar_cargo_registro",
                   description="Adiciona ou edita um cargo ao registro")
    @option(name="categoria", description="A categoria do cargo de registro")
    @option(name="nome", description="Nome do que vai aparecer no botão")
    @option(name="cargo", description="Cargo para adicionar")
    async def adcCargoReg(self,
                          interaction: discord.Interaction,
                          categoria: str,
                          nome: str,
                          cargo: discord.Role
                          ):
        try:
            modDono.find_one({"_id": interaction.guild.id})["premium"]["enable"]
        except:
            Premium(interaction.guild, datetime.now() + timedelta(seconds=5), False)
        qntcargoctg = 0
        qntcategoria = 0
        idrpt = False
        infoidrpt = {}
        for c in regCargo.find_one({"_id": interaction.guild.id}):
            if c == categoria:
                for r in regCargo.find_one({"_id": interaction.guild.id})[c]:
                    cgId = regCargo.find_one({"_id": interaction.guild.id})[c][r]["cargoid"]
                    if r:
                        qntcargoctg += 1
                    if cargo.id == cgId:
                        idrpt = True
                        infoidrpt = {
                            "name": r,
                            "id": cgId
                        }

        for c in regCargo.find_one({"_id": interaction.guild.id}):
            if "_id" not in c:
                qntcategoria += 1

        if qntcargoctg == 4 and not modDono.find_one({"_id": interaction.guild.id})["premium"]["enable"]:
            return await interaction.response.send_message(
                "Limite maximos de categorias alcançado gratis alcançado",
                ephemeral=True
            )

        if qntcategoria == 20:
            return await interaction.response.send_message("Limite maximos de categorias alcançado",
                                                           ephemeral=True)
        
        if qntcargoctg == 8 and not modDono.find_one({"_id": interaction.guild.id})["premium"]["enable"]:
            return await interaction.response.send_message(
                "Limite maximos de botão por categoria alcançado",
                ephemeral=True
            )

        if qntcargoctg == 18:
            return await interaction.response.send_message("Limite maximos de botão por categoria alcançado",
                                                           ephemeral=True)

        if idrpt:
            return await interaction.response.send_message(
                f"Id de cargo repetido\nCargo de conflito:\nNome: {infoidrpt['name']}\nId: {infoidrpt['id']}",
                ephemeral=True)

        addCargoReg(interaction.guild, cargo, categoria, nome)

        await interaction.response.send_message(
            f"Prontinho, cargo {cargo.name} adicionado na categoria {categoria}",
            ephemeral=True
        )

def setup(bot: commands.Bot):
    bot.add_cog(registroAdcCargo(bot))
