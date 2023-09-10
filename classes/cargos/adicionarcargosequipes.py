import discord

from discord.ext import commands
from utils.loader import configData
from ..buttons import AdcCargoEquipes, AdcCapEquipes


class AdcCargos(discord.ui.View):

    def __init__(self, bot: commands.Bot, timeout=300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Equipe",
        options=[
            discord.SelectOption(
                label='Eventos',
                description='Cargos da equipe de Eventos',
            ),
            discord.SelectOption(
                label='Call',
                description='Cargos da equipe de Call'
            ),
            discord.SelectOption(
                label='Chat',
                description='Cargos da equipe de Chat'
            ),
            discord.SelectOption(
                label='Registro',
                description='Cargos da equipe de Registro'
            )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):

        capeventos = discord.utils.get(interaction.guild.roles,
                                       id=configData['roles']['equipes']['equipeeventos']['chefeeventos'])
        capcall = discord.utils.get(interaction.guild.roles, id=configData['roles']['equipes']['equipecall']['submod'])
        capchat = discord.utils.get(interaction.guild.roles,
                                    id=configData['roles']['equipes']['equipechat']['liderchat'])
        admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])
        mod = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['mod'])
        chefreg = discord.utils.get(interaction.guild.roles, id=configData['roles']['equipes']['equipereg']['regchefe'])

        match select.values[0]:

            case 'Eventos':

                if capeventos in interaction.user.roles \
                        or admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Qual cargo vai adicionar?', ephemeral=True,
                                                            view=cargoevento(self.bot))

                    self.stop()

                else:

                    await interaction.response.send_message('Você não tem permissão para usar isto', ephemeral=True)

            case 'Call':

                if capcall in interaction.user.roles \
                        or admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Qual cargo vai adicionar?', ephemeral=True,
                                                            view=cargocall(self.bot))

                    self.stop()

                else:

                    await interaction.response.send_message('Você não tem permissão para usar isto', ephemeral=True)

            case 'Chat':

                if capchat in interaction.user.roles \
                        or admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Qual cargo vai adicionar?', ephemeral=True,
                                                            view=cargochat(self.bot))

                    self.stop()

                else:

                    await interaction.response.send_message('Você não tem permissão para usar isto', ephemeral=True)

            case 'Registro':

                if chefreg in interaction.user.roles \
                        or admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Qual cargo vai adicionar?', ephemeral=True,
                                                            view=cargoreg(self.bot))

                    self.stop()

                else:

                    await interaction.response.send_message('Você não tem permissão para usar isto', ephemeral=True)


class cargoevento(discord.ui.View):

    def __init__(self, bot, timeout=300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Cargos",
        options=[
            discord.SelectOption(
                label='Chefe de eventos',
                description='Adiciona o cargo de chefe de eventos',
            ),
            discord.SelectOption(
                label='Organizador',
                description='Adiciona o cargo de Organizador'
            ),
            discord.SelectOption(
                label='Ajudante',
                description='Adiciona o cargo de Ajudante'
            )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):

        admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])
        mod = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['mod'])
        capeventos = discord.utils.get(interaction.guild.roles,
                                       id=configData['roles']['equipes']['equipeeventos']['chefeeventos'])
        org = discord.utils.get(interaction.guild.roles,
                                id=configData['roles']['equipes']['equipeeventos']['apresentador'])
        ajud = discord.utils.get(interaction.guild.roles,
                                 id=configData['roles']['equipes']['equipeeventos']['auxiliar'])

        match select.values[0]:

            case 'Chefe de eventos':

                if admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                            ephemeral=True)

                    def check50(m):
                        return m.content and m.author.id == interaction.user.id

                    msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                    membro = interaction.guild.get_member(int(msg50.content))

                    await msg50.delete()

                    if capeventos in membro.roles:
                        return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                    e = discord.Embed(title='Adicionar cargo de Chefe de eventos')

                    e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')

                    e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                    e.add_field(name='Qual cargo vai ser adicionado ', value=capeventos.mention, inline=False)

                    e.set_footer(text=membro.id)

                    await interaction.channel.send(embed=e, view=AdcCapEquipes())

                    self.stop()

                else:

                    return await interaction.response.send_message('Você não tem permissão para usar isto',
                                                                   ephemeral=True)

            case 'Organizador':

                await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if org in membro.roles:
                    return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                e = discord.Embed(title='Adicionar cargo de Org. De eventos')

                e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')

                e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser adicionado ', value=org.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=AdcCargoEquipes())

                self.stop()

            case 'Ajudante':

                await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if ajud in membro.roles:
                    return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                e = discord.Embed(title='Adicionar cargo de Ajudante de Eventos')

                e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')

                e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser adicionado ', value=ajud.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=AdcCargoEquipes())

                self.stop()


class cargocall(discord.ui.View):

    def __init__(self, bot, timeout=300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Cargos",
        options=[
            discord.SelectOption(
                label='Chefe call',
                description='Adiciona o cargo de Chefe call',
            ),
            discord.SelectOption(
                label='Staff call',
                description='Adiciona o cargo de staff call'
            ),
            discord.SelectOption(
                label='Mov. call',
                description='Adiciona o cargo de Mov. call'
            )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):

        admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])
        mod = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['mod'])
        submod = discord.utils.get(interaction.guild.roles, id=configData['roles']['equipes']['equipecall']['submod'])
        staffcall = discord.utils.get(interaction.guild.roles,
                                      id=configData['roles']['equipes']['equipecall']['staffcall'])
        movi = discord.utils.get(interaction.guild.roles, id=configData['roles']['equipes']['equipecall']['movimenta'])

        match select.values[0]:

            case 'Chefe call':

                if admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                            ephemeral=True)

                    def check50(m):
                        return m.content and m.author.id == interaction.user.id

                    msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                    membro = interaction.guild.get_member(int(msg50.content))

                    await msg50.delete()

                    if submod in membro.roles:
                        return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                    e = discord.Embed(title='Adicionar cargo de Chefe call')

                    e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')
                    e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                    e.add_field(name='Qual cargo vai ser adicionado ', value=submod.mention, inline=False)

                    e.set_footer(text=membro.id)

                    await interaction.channel.send(embed=e, view=AdcCapEquipes())

                    self.stop()

                else:

                    return await interaction.response.send_message('Você não tem permissão para usar isto',
                                                                   ephemeral=True)

            case 'Staff call':

                await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if staffcall in membro.roles:
                    return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                e = discord.Embed(title='Adicionar cargo de Staff Call')

                e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')
                e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser adicionado ', value=staffcall.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=AdcCargoEquipes())

                self.stop()

            case 'Mov. call':

                await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if movi in membro.roles:
                    return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                e = discord.Embed(title='Adicionar cargo de Mov. call')

                e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')
                e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser adicionado ', value=movi.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=AdcCargoEquipes())

                self.stop()


class cargochat(discord.ui.View):

    def __init__(self, bot, timeout=300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Cargos",
        options=[
            discord.SelectOption(
                label='Chefe chat',
                description='Adiciona o cargo de Chefe chat',
            ),
            discord.SelectOption(
                label='Staff chat',
                description='Adiciona o cargo de Staff chat'
            ),
            discord.SelectOption(
                label='Mov. Chat',
                description='Adiciona o cargo de Mov. Chat'
            )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):

        admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])
        mod = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['mod'])
        liderchat = discord.utils.get(interaction.guild.roles,
                                      id=configData['roles']['equipes']['equipechat']['liderchat'])
        staffchat = discord.utils.get(interaction.guild.roles,
                                      id=configData['roles']['equipes']['equipechat']['staffchat'])
        movi = discord.utils.get(interaction.guild.roles, id=configData['roles']['equipes']['equipechat']['movimenta'])

        match select.values[0]:

            case 'Chefe chat':

                if admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                            ephemeral=True)

                    def check50(m):
                        return m.content and m.author.id == interaction.user.id

                    msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                    membro = interaction.guild.get_member(int(msg50.content))

                    await msg50.delete()

                    if liderchat in membro.roles:
                        return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                    e = discord.Embed(title='Adicionar cargo de Chefe chat')

                    e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')
                    e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                    e.add_field(name='Qual cargo vai ser adicionado ', value=liderchat.mention, inline=False)

                    e.set_footer(text=membro.id)

                    await interaction.channel.send(embed=e, view=AdcCapEquipes())

                    self.stop()

                else:

                    return await interaction.response.send_message('Você não tem permissão para usar isto',
                                                                   ephemeral=True)

            case 'Staff chat':

                await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if staffchat in membro.roles:
                    return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                e = discord.Embed(title='Adicionar cargo de Staff Chat')

                e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')
                e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser adicionado ', value=staffchat.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=AdcCargoEquipes())

                self.stop()

            case 'Mov. Chat':

                await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if movi in membro.roles:
                    return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                e = discord.Embed(title='Adicionar cargo de Mov. Chat')

                e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')
                e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser adicionado ', value=movi.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=AdcCargoEquipes())

                self.stop()

class cargoreg(discord.ui.View):

    def __init__(self, bot, timeout=300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Cargos",
        options=[
            discord.SelectOption(
                label='Reg. Chefe',
                description='Adiciona o cargo de Reg. Chefe',
            ),
            discord.SelectOption(
                label='Registrador',
                description='Adiciona o cargo de Registrador'
            ),
            discord.SelectOption(
                label='Ajudante',
                description='Adiciona o cargo de Ajudante'
            )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):

        admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])
        mod = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['mod'])
        regchefe = discord.utils.get(interaction.guild.roles,
                                     id=configData['roles']['equipes']['equipereg']['regchefe'])
        registrador = discord.utils.get(interaction.guild.roles,
                                        id=configData['roles']['equipes']['equipereg']['registrador'])
        regjunior = discord.utils.get(interaction.guild.roles,
                                      id=configData['roles']['equipes']['equipereg']['regjunior'])

        match select.values[0]:

            case 'Reg. Chefe':

                if admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                            ephemeral=True)

                    def check50(m):
                        return m.content and m.author.id == interaction.user.id

                    msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                    membro = interaction.guild.get_member(int(msg50.content))

                    await msg50.delete()

                    if regchefe in membro.roles:
                        return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                    e = discord.Embed(title='Adicionar cargo de Reg. Chefe')

                    e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')

                    e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                    e.add_field(name='Qual cargo vai ser adicionado ', value=regchefe.mention, inline=False)

                    e.set_footer(text=membro.id)

                    await interaction.channel.send(embed=e, view=AdcCapEquipes())

                    self.stop()

                else:

                    return await interaction.response.send_message('Você não tem permissão para usar isto',
                                                                   ephemeral=True)

            case 'Registrador':

                await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if registrador in membro.roles:
                    return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                e = discord.Embed(title='Adicionar cargo de Registrador')

                e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')

                e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser adicionado ', value=registrador.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=AdcCargoEquipes())

                self.stop()

            case 'Ajudante':

                await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if regjunior in membro.roles:
                    return await interaction.channel.send('Este membro já possue este cargo', delete_after=3)

                e = discord.Embed(title='Adicionar cargo de Reg. Junior')

                e.add_field(name='Quem vai ser adicionado o cargo', value=f'{membro.mention}')

                e.add_field(name='Quem adicionou ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser adicionado ', value=regjunior.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=AdcCargoEquipes())

                self.stop()
