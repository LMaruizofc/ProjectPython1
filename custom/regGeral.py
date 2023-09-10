import datetime

import discord

from discord.ext import commands

from classes.buttons import creatorButton
from db.moderation import mod
from db.register import regCargo


async def regButton(selfbot: commands.Bot, interaction: discord.Interaction, id: str):
    if interaction.user.id != int(interaction.message.embeds[0].footer.text.strip("Registrador")):
        return await interaction.response.send_message("Você não tem permissão para isso", ephemeral=True)

    if interaction.guild.get_role(int(id)) not in interaction.guild.get_member(
            int(interaction.message.embeds[0].author.name.strip("Registrado"))).roles:
        await interaction.guild.get_member(
            int(interaction.message.embeds[0].author.name.strip("Registrado"))).add_roles(
            interaction.guild.get_role(int(id)))
        await interaction.response.send_message("Cargo adicionado ao membro", ephemeral=True)
    else:
        await interaction.guild.get_member(
            int(interaction.message.embeds[0].author.name.strip("Registrado"))).remove_roles(
            interaction.guild.get_role(int(id)))
        await interaction.response.send_message("Cargo removido do membro", ephemeral=True)


async def finalreg(selfbot: commands.Bot, interaction: discord.Interaction):

    if interaction.user.id != int(
            interaction.message.embeds[0].footer.text.strip("Registrador")):
        return await interaction.response.send_message("Você não tem permissão para isso",
                                                       ephemeral=True)

    tempo = datetime.datetime.now() - datetime.timedelta(hours=3)
    Member = interaction.guild.get_member(
        int(interaction.message.embeds[0].author.name.strip("Registrado ")))
    Registrador = interaction.guild.get_member(
        int(interaction.message.embeds[0].footer.text.strip("Registrador ")))
    if interaction.user.id != Registrador.id:
        await interaction.response.send_message(
            "Você não possue permissão para isso", ephemeral=True)

    e = discord.Embed(title='Registro',
                      description=
                      f'''
    **Registrado:** {Member.mention}
    **Registrador:** {Registrador.mention}
    **Servidor:** {interaction.guild.name}
    **Data do Registro:** {tempo.strftime("%d/%m/%Y")}
                                ''')
    await interaction.message.delete()
    try:
        await interaction.guild.get_channel(
            int(mod.find_one({"_id": interaction.guild.id})["logs"]["regLog"][0])).send(embed=e)
        await interaction.guild.get_member(
            int(interaction.message.embeds[0].author.name.strip("Registrado"))).send(embed=e)
    except:
        await interaction.guild.get_member(
            int(interaction.message.embeds[0].author.name.strip("Registrado "))).send(
            embed=e)
        await interaction.channel.send(embed=e)
    else:
        pass

    try:
        await Member.remove_roles(interaction.guild.get_role(
            regCargo.find_one({"_id": interaction.guild.id})["defaults"]["dfaultreg"]["cargoid"]
        )
        )
        await Member.add_roles(interaction.guild.get_role(
            regCargo.find_one({"_id": interaction.guild.id})["defaults"]["finalreg"]["cargoid"]
        )
        )
    except:
        await Member.add_roles(interaction.guild.get_role(
            regCargo.find_one({"_id": interaction.guild.id})["defaults"]["finalreg"]["cargoid"]
        )
        )
        await Member.remove_roles(interaction.guild.get_role(
            regCargo.find_one({"_id": interaction.guild.id})["defaults"]["defaultreg"]["cargoid"]
        )
        )
    else:
        pass


async def menureg(selfbot: commands.Bot, interaction: discord.Interaction):

    if interaction.user.id != int(
            interaction.message.embeds[0].footer.text.strip("Registrador")):
        return await interaction.response.send_message("Você não tem permissão para isso",
                                                       ephemeral=True)

    e = discord.Embed(title="Registro", description="Escolha a categoria que deseja")
    e.set_author(name=f"{interaction.message.embeds[0].author.name}")
    e.set_footer(text=f"{interaction.message.embeds[0].footer.text}")

    await interaction.response.edit_message(embed=e, view=creatorButton(type="selectCatego",
                                                                        guild_id=interaction.guild.id))


async def categoriaRegistro(selfbot: commands.Bot, interaction: discord.Interaction):

    if interaction.user.id != int(
            interaction.message.embeds[0].footer.text.strip("Registrador")):
        return await interaction.response.send_message("Você não tem permissão para isso",
                                                       ephemeral=True)

    e = discord.Embed(title="Registro")

    for i in regCargo.find_one({"_id": interaction.guild.id})[
        str(interaction.custom_id).removeprefix("catego-")]:
        a = regCargo.find_one(
            {"_id": interaction.guild.id}
        )[interaction.custom_id.removeprefix("catego-")][i]
        e.add_field(
            name=a["name"],
            value=interaction.guild.get_role(
                int(a["cargoid"])
            ).mention
        )

    e.set_author(name=interaction.message.embeds[0].author.name)
    e.set_footer(text=interaction.message.embeds[0].footer.text)
    await interaction.response.edit_message(
        embed=e,
        view=creatorButton(
            type="regCargoAdd",
            guild_id=interaction.guild.id,
            categoria=str(interaction.custom_id).removeprefix("catego-")
        )
    )
