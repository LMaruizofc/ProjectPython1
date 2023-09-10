import discord

from discord import option, slash_command
from discord.ext import commands
from db.event import addp, addp2, rmvp, rmvp2, points


class eventosRmvPt(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name='remover_ponto_evento',
                    description='remove um ponto de evento para um membro')
    @option(name='membro', description='mencione o membro')
    async def rmvpoints(self, interaction: discord.Interaction, membro: discord.Member):

        await rmvp(membro, - 1)

        pt = points.find_one({"_id": interaction.guild.id})

        pt2 = pt[f"{membro.id}"]['pontos']

        if pt2 == -1:

            await addp(membro, + 1)

            await interaction.response.send_message('Esse membro não posue pontos', ephemeral=True)

            if discord.utils.get(interaction.guild.roles, name=f'{pt2 + 1}🏆') in membro.roles:
                await membro.remove_roles(discord.utils.get(interaction.guild.roles, name=f'{pt2 + 1}🏆'))

            return

        pt3 = pt[f"{membro.id}"][f'ponto{pt2 + 1}']

        if pt == 0:
            pt3 = pt[f"{membro.id}"][f'ponto{1}']

        if pt2 > 0:
            await rmvp2(membro, pt2 + 1, pt3)

        if pt2 == 0:
            await rmvp2(membro, 1, pt3)

        role = discord.utils.get(interaction.guild.roles, name=f'{pt2}🏆')

        if role in interaction.guild.roles:

            await membro.add_roles(role)

            if discord.utils.get(interaction.guild.roles, name=f'{pt2 + 1}🏆') in membro.roles:
                await membro.remove_roles(discord.utils.get(interaction.guild.roles, name=f'{pt2 + 1}🏆'))

            await interaction.response.send_message(
                f'Ponto removido com sucesso e {role.mention} adicionado com sucesso', ephemeral=True)

            return

        if discord.utils.get(interaction.guild.roles, name=f'{pt2 + 1}🏆') in membro.roles:
            await membro.remove_roles(discord.utils.get(interaction.guild.roles, name=f'{pt2 + 1}🏆'))

        await interaction.response.send_message(f'Ponto removido com sucesso e agora este membro não posue pontos',
                                                ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(eventosRmvPt(bot))
