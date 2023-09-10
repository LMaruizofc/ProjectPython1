import discord

from discord import option, slash_command
from discord.ext import commands
from db.event import addp, addp2, rmvp, rmvp2, points


class eventosVerPt(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name='ver_pontos_evento', description='mostra os pontos de evento de um membro')
    @option(name='membro', description='mencione o membro')
    async def verpontos(self, interaction: discord.Interaction, membro: discord.Member = None):

        if points.count_documents({"_id": interaction.guild.id})[f"{membro.id}"] == 1:

            pt = points.find_one({"_id": interaction.guild.id})[f"{membro.id}"]

            embed = discord.Embed(title='Pontos')

            embed.add_field(name=f'Pontos de {membro.name}', value=pt[f"{membro.id}"]['pontos'])

            vali = 1

            while True:

                embed.add_field(name=f'Ponto{vali}', value=pt[f'ponto{vali}'], inline=False)

                if vali == pt['pontos']:

                    break

                else:

                    vali += 1

            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await interaction.response.send_message('Esse membro não está nos meus registros', ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(eventosVerPt(bot))
