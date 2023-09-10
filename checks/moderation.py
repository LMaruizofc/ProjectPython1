import discord

from db.moderation import adv
from utils.loader import configData
from db.event import points

async def verfyadv(self, member: discord.Member) -> None:

    role1 = discord.utils.get(member.guild.roles, id = configData['roles']['adv']['adv1'])
    role2 = discord.utils.get(member.guild.roles, id = configData['roles']['adv']['adv2'])
    role3 = discord.utils.get(member.guild.roles, id = configData['roles']['adv']['adv3'])

    if adv.count_documents({ "_id": member.id}) == 1:

        ad = adv.find_one({"_id": member.id})

        adv1 = ad['Adv1']
        adv2 = ad['Adv2']
        adv3 = ad['Adv3']

        if adv3 != 'None':
            await  member.add_roles(role3)

        if adv2 != 'None':
            await  member.add_roles(role2)

        if adv1 != 'None':
            await  member.add_roles(role1)
#-----------------------------------------------------------------------------------------------------#
async def verfypoints(self, member: discord.Member) -> None:

    if points.count_documents({ "_id": member.id}) == 1:

        p = points.find_one({"_id": member.id})

        if discord.utils.get(member.guild.roles, name = f'{p["pontos"]}🏆') in member.guild.roles:

            await member.add_roles(discord.utils.get(member.guild.roles, name = f'{p["pontos"]}🏆'))