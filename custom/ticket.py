import discord
import os

from datetime import datetime, timedelta
from pytz import timezone
from discord.ext import commands
from classes.buttons import AdonTicket, AdonTicket2, jumpto
from db.moderation import mod
from classes.selectmenus import createSelect

async def ticket_select(selfbot: commands.Bot, interaction: discord.Interaction):

    await interaction.response.defer(ephemeral=True)

    name_list = []
    idcategorias = []
    for i in interaction.to_dict()["message"]["components"][0]["components"][0]["options"]:
        name_list.append(i["label"])
        idcategorias.append(i["value"][3:])
    
    await interaction.followup.edit_message(
        interaction.message.id,
        view=createSelect(
            qnt = interaction.to_dict()["message"]["components"][0]["components"][0]["options"].__len__(),
            name_list = name_list,
            idcategorias = idcategorias
        )
    )

    await interaction.followup.send('Criando ticket', ephemeral=True)

    try:
        os.listdir("tickets")
    except:
        os.mkdir("tickets")

    for i in interaction.to_dict()["message"]["components"][0]["components"][0]["options"]:
        if interaction.to_dict()["data"]["values"][0] == i["value"]:
            ticket = f'{i["label"]}-{interaction.user.id}'
            break

    dt = datetime.now() - timedelta(hours=3)
    categoria: discord.CategoryChannel = None

    try:
        categoria: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=int(interaction.to_dict()["data"]["values"][0][3:].strip("-")))
    except Exception as error:
        return await interaction.followup.send(
            f"Não consegui criar o canal na categoria de id {interaction.to_dict()['data']['values'][0][3:]}",
            ephemeral = True
        )

    for i in categoria.text_channels:
        if ticket in i.name:
            return await interaction.followup.send('Ticket já existente, encerre o ultimo para criar outro', ephemeral=True)

    guild = interaction.guild
    member = interaction.user
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
    }

    try:
        for i in mod.find_one({"_id": guild.id})["roleticket"]:
            r = mod.find_one({'_id': guild.id})["roleticket"][i]
            overwrites[discord.utils.get(guild.roles, id=int(
                r[0]))] = discord.PermissionOverwrite(read_messages=True)
    except:
        pass

    for file in os.listdir("./tickets"):
        if file.endswith(".txt"):
            try:
                if file.startswith(f'{interaction.guild.id}_{ticket.removeprefix("ticket-")}'):
                    os.remove(
                        f"./tickets/{interaction.guild.id}_{ticket.removeprefix('ticket-')}.txt")
            except:
                pass

    with open(f'./tickets/{interaction.guild.id}_{ticket.removeprefix("ticket-")}.txt', 'a') as f:
        f.write(
            f'Ticket de {interaction.user.name} {dt.strftime("%d/%m/%Y")}')
        
    channel = await interaction.guild.create_text_channel(
        name=ticket,
        overwrites=overwrites,
        category=categoria
    )

    if interaction.message.author.discriminator == "0000":
        if interaction.message.author.avatar != None:
            web = await channel.create_webhook(name=interaction.message.author.name, avatar=await interaction.message.author.avatar.read())
        else:
            web = await channel.create_webhook(name=interaction.message.author.name)

    await interaction.followup.send('Ticket criado com sucesso', view=jumpto(f'https://discordapp.com/channels/{interaction.guild.id}/{channel.id}'), ephemeral=True)

    e = discord.Embed(
        title=f'Ticket de {interaction.user}',
        description=dt.strftime("Aberto as %H:%M de %d/%m/%Y")
    )
    e.set_footer(text=interaction.user.id)

    try:
        mentionRole = interaction.guild.get_role(int(mod.find_one({"_id": interaction.guild.id})["roleticket"]["mentionable"][0])).mention
    except:
        mentionRole = ""

    try:
        await web.send(content=f'{interaction.user.mention} {mentionRole}', embed=e, view=AdonTicket())
    except:
        await channel.send(content=f'{interaction.user.mention} {mentionRole}', embed=e, view=AdonTicket())

async def abrirTicket(selfbot: commands.Bot, interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send('Criando ticket', ephemeral=True)

    try:
        os.listdir("tickets")
    except:
        os.mkdir("tickets")

    dt = datetime.now() - timedelta(hours=3)
    ticket = f'ticket-{interaction.user.id}'
    categoria: discord.CategoryChannel = None

    try:
        categoria: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=int(interaction.custom_id[13:].strip("-")))
    except Exception as error:
        return await interaction.followup.send(
                f"Não consegui criar o canal na categoria de id {interaction.custom_id[13:]}",
                ephemeral = True
            )

    for i in categoria.text_channels:

        if ticket in i.name:
            return await interaction.followup.send('Ticket já existente, encerre o ultimo para criar outro', ephemeral=True)
        
    guild = interaction.guild
    member = interaction.user
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
    }

    try:
        for i in mod.find_one({"_id": guild.id})["roleticket"]:
            r = mod.find_one({'_id': guild.id})["roleticket"][i]
            overwrites[discord.utils.get(guild.roles, id=int(
                r[0]))] = discord.PermissionOverwrite(read_messages=True)
    except:
        pass

    for file in os.listdir("./tickets"):
        if file.endswith(".txt"):
            try:
                if file.startswith(f'{interaction.guild.id}_{ticket.removeprefix("ticket-")}'):
                    os.remove(
                        f"./tickets/{interaction.guild.id}_{ticket.removeprefix('ticket-')}.txt")
            except:
                pass

    with open(f'./tickets/{interaction.guild.id}_{ticket.removeprefix("ticket-")}.txt', 'a') as f:
        f.write(
            f'Ticket de {interaction.user.name} {dt.strftime("%d/%m/%Y")}')

    channel = await interaction.guild.create_text_channel(
        name=ticket,
        overwrites=overwrites,
        category = categoria
                
    )

    if interaction.message.author.discriminator == "0000":
        if interaction.message.author.avatar != None:
            web = await channel.create_webhook(name=interaction.message.author.name, avatar=await interaction.message.author.avatar.read())
        else:
            web = await channel.create_webhook(name=interaction.message.author.name)

    await interaction.followup.send('Ticket criado com sucesso', view=jumpto(f'https://discordapp.com/channels/{interaction.guild.id}/{channel.id}'), ephemeral=True)

    e = discord.Embed(
        title=f'Ticket de {interaction.user}',
        description=dt.strftime("Aberto as %H:%M de %d/%m/%Y")
    )
    e.set_footer(text=interaction.user.id)

    try:
        mentionRole = interaction.guild.get_role(int(mod.find_one({"_id": interaction.guild.id})["roleticket"]["mentionable"][0])).mention
    except:
        mentionRole = ""

    try:
        await web.send(content=f'{interaction.user.mention} {mentionRole}', embed=e, view=AdonTicket())
    except:
        await channel.send(content=f'{interaction.user.mention} {mentionRole}', embed=e, view=AdonTicket())

async def closeTicket(selfbot: commands.Bot, interaction: discord.Interaction):

    member = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))

    overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=False),
    }

    try:
        for i in mod.find_one({"_id": interaction.guild.id})["roleticket"]:
            r = mod.find_one({'_id': interaction.guild.id})["roleticket"][i]
            overwrites[discord.utils.get(interaction.guild.roles, id=int(
                r[0]))] = discord.PermissionOverwrite(read_messages=True)
    except:
        pass

    e = discord.Embed(
        description=f'🔒Ticket de {member} fechado por {interaction.user.mention} \nClique no 🔓 para abrir'
    )
    e.set_footer(text=member.id)
    await interaction.channel.edit(overwrites=overwrites)
    await interaction.message.delete()

    try:
        p = await interaction.channel.webhooks()
        web = await selfbot.fetch_webhook(p[0].id)
        await web.send(embed=e, view=AdonTicket2())
    except:
        await interaction.channel.send(embed=e, view=AdonTicket2())

async def openTicket(selfbot: commands.Bot, interaction: discord.Interaction):

    member = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))
    overwrites = {
        member: discord.PermissionOverwrite(read_messages=True),
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
    }

    try:
        for i in mod.find_one({"_id": interaction.guild.id})["roleticket"]:
            r = mod.find_one({'_id': interaction.guild.id})["roleticket"][i]
            overwrites[discord.utils.get(interaction.guild.roles, id=int(
                r[0]))] = discord.PermissionOverwrite(read_messages=True)
    except:
        pass

    await interaction.channel.edit(overwrites=overwrites)
    await interaction.message.delete()
    e = discord.Embed(title=f'Ticket de {member} aberto 🔓')
    e.set_footer(text=member.id)
    try:
        p = await interaction.channel.webhooks()
        web = await selfbot.fetch_webhook(p[0].id)
        await web.send(embed=e, view=AdonTicket2())
    except:
        await interaction.channel.send(embed=e, view=AdonTicket())

async def deleteTicket(selfbot: commands.Bot, interaction: discord.Interaction):

    member = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))
    dt = datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M')

    try:
        await interaction.guild.get_channel(
                int(mod.find_one({"_id": interaction.guild.id})["logs"]["tckLog"][0])).send(
                content=f"Ticket de {member.name} {dt}",
                file=discord.File('./tickets/{}_{}.txt'.format(
                        interaction.guild.id, member.id
                    ), 
                    f'Ticket de {member.name}.txt'
                )
        )
    except:
        pass

    await interaction.channel.delete()
