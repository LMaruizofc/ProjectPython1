import discord

from discord import option, slash_command
from discord.ext import commands
from db.event import addp, addp2, rmvp, rmvp2, points


class eventosAdcPt(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name='adicionar_ponto_evento',
                    description='Adiciona um ponto de evento para um membro')
    @option(name='membro', description='mencione o membro')
    async def addpoints(self, interaction: discord.Interaction, membro: discord.Member):

        await addp(membro, + 1)

        pt = points.find_one({"_id": interaction.guild.id})

        pt2 = pt[f"{membro.id}"]['pontos']

        await addp2(membro, interaction.author, pt2)

        role = discord.utils.get(interaction.guild.roles, name=f'{pt2}🏆')

        if role not in interaction.guild.roles:

            role2 = await interaction.guild.create_role(name=f'{pt2}🏆', color=0xff8600)

            await membro.add_roles(role2)

            if discord.utils.get(interaction.guild.roles, name=f'{pt2 - 1}🏆') in interaction.guild.roles:
                await discord.utils.get(interaction.guild.roles, name=f'{pt2 - 1}🏆').edit(
                    color=discord.Colour.default())

            if discord.utils.get(interaction.guild.roles, name=f'{pt2 - 1}🏆') in membro.roles:
                await membro.remove_roles(discord.utils.get(interaction.guild.roles, name=f'{pt2 - 1}🏆'))

            await interaction.response.send_message(
                f'Ponto adicionado com sucesso e {role2.mention} adicionado com sucesso', ephemeral=True)

        else:

            await membro.add_roles(role)

            if discord.utils.get(interaction.guild.roles, name=f'{pt2 - 1}🏆') in membro.roles:
                await membro.remove_roles(discord.utils.get(interaction.guild.roles, name=f'{pt2 - 1}🏆'))

            await interaction.response.send_message(
                f'Ponto adicionado com sucesso e {role.mention} adicionado com sucesso', ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(eventosAdcPt(bot))
