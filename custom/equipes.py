import discord

from utils.loader import configData
from classes.cargos.selectmenus import adcrmvcargosequipes


async def adcCargosEquipes(selfbot, interaction):
    if discord.utils.get(interaction.guild.roles,
                         id=configData['roles']['staff']['admin']) in interaction.user.roles \
            or discord.utils.get(interaction.guild.roles,
                                 id=configData['roles']['staff']['mod']) in interaction.user.roles \
            or discord.utils.get(interaction.guild.roles, id=configData['roles']['equipes']['equipeeventos'][
        'chefeeventos']) in interaction.user.roles \
            or discord.utils.get(interaction.guild.roles,
                                 id=configData['roles']['equipes']['equipecall']['submod']) in interaction.user.roles \
            or discord.utils.get(interaction.guild.roles,
                                 id=configData['roles']['equipes']['equipechat']['liderchat']) in interaction.user.roles:

        await interaction.response.send_message('Oque ira fazer?', ephemeral=True, view=adcrmvcargosequipes(selfbot))

    else:

        await interaction.response.send_message('Você não tem permissão para usar isto', ephemeral=True)


async def confirmAdcCap(selfbot, interaction):
    member = interaction.guild.get_member(
        int(interaction.message.embeds[0].footer.text)
    )
    author = interaction.guild.get_member(
        int(interaction.message.embeds[0].fields[1].value.strip('<@>'))
    )
    cargo = discord.utils.get(
        interaction.guild.roles,
        id=int(interaction.message.embeds[0].fields[2].value.strip('<@&>'))
    )

    channel = interaction.guild.get_channel(configData['logs']['cargos'])

    admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])

    e = discord.Embed(title='Adição cargo')

    e.add_field(name='Qual cargo adicionado', value=cargo.mention)

    e.add_field(name='Quem adicionou', value=author.mention, inline=False)

    e.add_field(name='Foi adicionado a', value=member.mention)

    e.add_field(name='Aprovado por', value=interaction.user.mention, inline=False)

    if admin in interaction.user.roles:

        await member.add_roles(cargo)

        await interaction.message.delete()

        await channel.send(embed=e)

    else:

        await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral=True)


async def confirmAdcEquipe(selfbot, interaction):
    member = interaction.guild.get_member(
        int(interaction.message.embeds[0].footer.text)
    )
    author = interaction.guild.get_member(
        int(interaction.message.embeds[0].fields[1].value.strip('<@>'))
    )
    cargo = discord.utils.get(
        interaction.guild.roles,
        id=int(interaction.message.embeds[0].fields[2].value.strip('<@&>'))
    )
    channel = interaction.guild.get_channel(configData['logs']['cargos'])
    admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])
    mod = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['mod'])

    e = discord.Embed(title='Adição cargo')

    e.add_field(name='Qual cargo adicionado', value=cargo.mention)

    e.add_field(name='Quem adicionou', value=author.mention, inline=False)

    e.add_field(name='Foi adicionado a', value=member.mention)

    e.add_field(name='Aprovado por', value=interaction.user.mention, inline=False)

    if admin in interaction.user.roles \
            or mod in interaction.user.roles:

        await member.add_roles(cargo)

        await interaction.message.delete()

        await channel.send(embed=e)

    else:

        await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral=True)


async def confirmRmvCap(selfbot, interaction):
    member = interaction.guild.get_member(
        int(interaction.message.embeds[0].footer.text)
    )
    author = interaction.guild.get_member(
        int(interaction.message.embeds[0].fields[1].value.strip('<@>'))
    )
    cargo = discord.utils.get(
        interaction.guild.roles,
        id=int(interaction.message.embeds[0].fields[2].value.strip('<@&>'))
    )

    channel = interaction.guild.get_channel(configData['logs']['cargos'])

    admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])

    e = discord.Embed(title='Adição cargo')

    e.add_field(name='Qual cargo removido', value=cargo.mention)

    e.add_field(name='Quem removeu', value=author.mention, inline=False)

    e.add_field(name='Foi removido de', value=member.mention)

    e.add_field(name='Aprovado por', value=interaction.user.mention, inline=False)

    if admin in interaction.user.roles:

        await member.remove_roles(cargo)

        await interaction.message.delete()

        await channel.send(embed=e)

    else:

        await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral=True)


async def confirmRmvEquipe(selfbot, interaction):
    member = interaction.guild.get_member(
        int(interaction.message.embeds[0].footer.text)
    )
    author = interaction.guild.get_member(
        int(interaction.message.embeds[0].fields[1].value.strip('<@>'))
    )
    cargo = discord.utils.get(
        interaction.guild.roles,
        id=int(interaction.message.embeds[0].fields[2].value.strip('<@&>'))
    )
    channel = interaction.guild.get_channel(configData['logs']['cargos'])
    admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])
    mod = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['mod'])

    e = discord.Embed(title='Adição cargo')
    e.add_field(name='Qual cargo removido', value=cargo.mention)
    e.add_field(name='Quem removeu', value=author.mention, inline=False)
    e.add_field(name='Foi removido de', value=member.mention)
    e.add_field(name='Aprovado por', value=interaction.user.mention, inline=False)

    if admin in interaction.user.roles \
            or mod in interaction.user.roles:

        await member.remove_roles(cargo)
        await interaction.message.delete()
        await channel.send(embed=e)

    else:
        await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral=True)


async def denyAdcCap(selfbot, interaction):
    admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])

    if admin in interaction.user.roles:
        await interaction.message.delete()
    else:
        await interaction.response.send_message('Você não tem permissão para usar isso', ephemeral=True)
