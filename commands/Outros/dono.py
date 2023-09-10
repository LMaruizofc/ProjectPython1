import discord

from datetime import datetime, timedelta
from discord.ext import commands
from discord import SlashCommandGroup, option
from db.economy import update_bank, market_update, update_inv
from db.dono import Premium, modDono
from utils.loader import configData


class Dono(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    dono = SlashCommandGroup("dono", guild_ids=[configData["guild"]])

    @dono.command(guild_only=True, name="adc_ivmcoins", description="Adiciona IVM coins a um membro")
    @commands.is_owner()
    @option(name="membro", description="Mencione o membro")
    @option(name="ivmcoins", description="Coloque a quantidade de ivmcoins")
    async def Set(self, interaction: discord.Interaction, membro: discord.User, ivmcoins: int):

        update_bank(membro, + ivmcoins)

        await interaction.guild.get_member(485801281621852175).send(
            f"Foram dados {ivmcoins} IVM coins para {membro.mention} por {interaction.user}")

        await interaction.response.send_message(f"Foram dados {ivmcoins} IVM coins para {membro.mention}",
                                                ephemeral=True)

    @dono.command(guild_only=True, name="rmv_ivmcoins", description="Remove IVM coins de um membro")
    @commands.is_owner()
    @option(name="membro", description="Mencione o membro")
    @option(name="ivmcoins", description="Coloque a quantidade de ivmcoins")
    async def Rmv(self, interaction: discord.Interaction, membro: discord.User, ivmcoins: int):

        update_bank(membro, - ivmcoins)

        await interaction.guild.get_member(self.bot.owner_id).send(
            f"Foram removidos {ivmcoins} IVM coins para {membro.mention} por {interaction.user}")

        await interaction.response.send_message(f"Foram removidos {ivmcoins} IVM coins de {membro.mention}", ephemeral=True)

    @dono.command(guild_only=True, name="update_market", description="Atualiza um item do mercado")
    @commands.is_owner()
    @option(name="item", description="Nome do item no mercado")
    @option(name="opção", description="Dizer se é compra ou venda", choices=["compra", "venda"])
    @option(name="valor", description="Valor que vai ficar")
    async def mku(self, interaction: discord.Interaction, item: str, opção: str, valor: str):

        if valor.lower() == "none" or valor.lower() == "null":
            market_update(item, opção, None)
        else:
            market_update(item, opção, int(valor))

        await interaction.response.send_message(
            f"Valor de {opção} de {item} modificado para {valor.lower()} por {interaction.user}")

        await interaction.guild.get_member(485801281621852175).send(
            f"Valor de {opção} de {item} modificado para {valor} por {interaction.user}")

    @dono.command(guild_only=True, name="remove_item", description="Remove um item de um membro")
    @commands.is_owner()
    @option(name="item", description="Nome do item")
    @option(name="qnt", description="Quantidade a ser removida")
    @option(name="membro", description="Valor que vai ficar")
    async def ritem(self, interaction: discord.Interaction, item: str, qnt: int, membro: discord.User):

        update_inv(membro, item, - qnt)

        await interaction.response.send_message(
            f"O item {item} foi removido de {membro} por {interaction.user} com a quantidade {qnt}", ephemeral=True)

        await interaction.guild.get_member(self.bot.owner_id).send(
            f"O item {item} foi removido de {membro} por {interaction.user} com a quantidade {qnt}")

    @dono.command(guild_only=True, name="give_item", description="Adiciona um item ao membro")
    @commands.is_owner()
    @option(name="item", description="Nome do item")
    @option(name="qnt", description="Quantidade a ser adicionada")
    @option(name="membro", description="Valor que vai ficar")
    async def gitem(self, interaction: discord.Interaction, item: str, qnt: int, membro: discord.User):

        update_inv(membro, item, + qnt)

        await interaction.response.send_message(
            f"O item {item} foi adicionado a {membro} por {interaction.user} com a quantidade {qnt}", ephemeral=True)

        await interaction.guild.get_member(485801281621852175).send(
            f"O item {item} foi adicionado a {membro} por {interaction.user} com a quantidade {qnt}")
    
    @dono.command(guild_only=True, name="adc_premium", description="Adiciona Premium a um servidor")
    @commands.is_owner()
    @option(name="tempo", description="Tempo de premium")
    @option(name="idserver", description="Id do servidor")
    async def gitem(self, interaction: discord.Interaction, tempo: int, idserver: discord.Guild):

        try:
            t = datetime.fromtimestamp(modDono.find_one({"_id": idserver.id})["premium"]["data"]) + timedelta(days=30)
        except:
            t = datetime.utcnow() + timedelta(days=30)

        Premium(idserver, t, True)

        await interaction.response.send_message(f"Adicionado {tempo} dias de premium pro servidor {idserver.name}")


def setup(bot: commands.Bot):
    bot.add_cog(Dono(bot))
