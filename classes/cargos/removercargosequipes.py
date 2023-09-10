import discord

from discord.ext import commands
from utils.loader import configData
from ..buttons import RmvCapEquipes, RmvCargoEquipes


class RmvCargos(discord.ui.View):

    def __init__(self, bot: commands.Bot, timeout=300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Equipe",
        options=[
            discord.SelectOption(
                label='Eventos',
                description='Cargos da equipe de eventos',
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

                    await interaction.response.send_message('Qual cargo vai remover?', ephemeral=True,
                                                            view=cargoevento2(self.bot))

                    self.stop()

                else:

                    await interaction.response.send_message('Você não tem permissão para usar isto', ephemeral=True)

            case 'Call':

                if capcall in interaction.user.roles \
                        or admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Qual cargo vai remover?', ephemeral=True,
                                                            view=cargocall2(self.bot))

                    self.stop()

                else:

                    await interaction.response.send_message('Você não tem permissão para usar isto', ephemeral=True)

            case 'Chat':

                if capchat in interaction.user.roles \
                        or admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Qual cargo vai remover?', ephemeral=True,
                                                            view=cargochat2(self.bot))

                    self.stop()

                else:

                    await interaction.response.send_message('Você não tem permissão para usar isto', ephemeral=True)

            case 'Registro':

                if chefreg in interaction.user.roles \
                        or admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Qual cargo vai Remover?', ephemeral=True,
                                                            view=cargoreg2(self.bot))

                    self.stop()

                else:

                    await interaction.response.send_message('Você não tem permissão para usar isto', ephemeral=True)


# ------------------------------------------------------------------------------------------------------------#
class cargoevento2(discord.ui.View):

    def __init__(self, bot, timeout=300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Cargos",
        options=[
            discord.SelectOption(
                label='Chefe de eventos',
                description='Remove o cargo de chefe de eventos',
            ),
            discord.SelectOption(
                label='Org. de Eventos',
                description='Remove o cargo de Org. de Eventos'
            ),
            discord.SelectOption(
                label='Ajudante de evento',
                description='Remove o cargo de Ajudante de evento'
            )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):

        admin = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['admin'])
        mod = discord.utils.get(interaction.guild.roles, id=configData['roles']['staff']['mod'])
        capeventos = discord.utils.get(interaction.guild.roles,
                                       id=configData['roles']['equipes']['equipeeventos']['chefeeventos'])
        apresentador = discord.utils.get(interaction.guild.roles,
                                         id=configData['roles']['equipes']['equipeeventos']['apresentador'])
        auxiliar = discord.utils.get(interaction.guild.roles,
                                     id=configData['roles']['equipes']['equipeeventos']['auxiliar'])

        match select.values[0]:

            case 'Chefe de eventos':

                if admin in interaction.user.roles \
                        or mod in interaction.user.roles:

                    await interaction.response.send_message('Mande no chat o id da pessoa a remover o cargo',
                                                            ephemeral=True)

                    def check50(m):
                        return m.content and m.author.id == interaction.user.id

                    msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                    membro = interaction.guild.get_member(int(msg50.content))

                    await msg50.delete()

                    if capeventos not in membro.roles:
                        return await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                    e = discord.Embed(title='Remover cargo de Chefe de eventos')

                    e.add_field(name='Quem vai ser Removedo o cargo', value=f'{membro.mention}')

                    e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                    e.add_field(name='Qual cargo vai ser removido ', value=capeventos.mention, inline=False)

                    e.set_footer(text=membro.id)

                    await interaction.channel.send(embed=e, view=RmvCapEquipes())

                    self.stop()

                else:

                    return await interaction.response.send_message('Você não tem permissão para usar isto',
                                                                   ephemeral=True)

            case 'Org. de Eventos':

                await interaction.response.send_message('Mande no chat o id da pessoa a remover o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if apresentador not in membro.roles:
                    return await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                e = discord.Embed(title='Remover cargo de Org. de Eventos')

                e.add_field(name='Quem vai ser Removedo o cargo', value=f'{membro.mention}')

                e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser removido ', value=apresentador.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=RmvCargoEquipes())

                self.stop()

            case 'Ajudante de evento':

                await interaction.response.send_message('Mande no chat o id da pessoa a remover o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if auxiliar not in membro.roles:
                    await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                    return

                e = discord.Embed(title='Remover cargo de Ajudante de evento')

                e.add_field(name='Quem vai ser Removedo o cargo', value=f'{membro.mention}')

                e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser removido ', value=auxiliar.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=RmvCargoEquipes())

                self.stop()


class cargocall2(discord.ui.View):

    def __init__(self, bot, timeout=300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Cargos",
        options=[
            discord.SelectOption(
                label='Chefe call',
                description='Remove o cargo de Chefe call',
            ),
            discord.SelectOption(
                label='Staff call',
                description='Remove o cargo de staff call'
            ),
            discord.SelectOption(
                label='Mov. call',
                description='Remove o cargo de Mov. call'
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
                    await interaction.response.send_message('Mande no chat o id da pessoa a remover o cargo',
                                                            ephemeral=True)

                    def check50(m):
                        return m.content and m.author.id == interaction.user.id

                    msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                    membro = interaction.guild.get_member(int(msg50.content))

                    await msg50.delete()

                    if submod not in membro.roles:
                        return await interaction.channel.send('Este membro não possue este cargo', delete_after=5)

                    e = discord.Embed(title='Remover cargo de Chefe call')

                    e.add_field(name='Quem vai ser Removido o cargo', value=f'{membro.mention}')
                    e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                    e.add_field(name='Qual cargo vai ser removido ', value=submod.mention, inline=False)

                    e.set_footer(text=membro.id)

                    await interaction.channel.send(embed=e, view=RmvCapEquipes())

                    self.stop()

                else:

                    return await interaction.response.send_message('Você não tem permissão para usar isto',
                                                                   ephemeral=True)

            case 'Staff call':

                await interaction.response.send_message('Mande no chat o id da pessoa a remover o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if staffcall not in membro.roles:
                    return await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                e = discord.Embed(title='Remover cargo de staff call')

                e.add_field(name='Quem vai ser Removido o cargo', value=f'{membro.mention}')
                e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser removido ', value=staffcall.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=RmvCargoEquipes())

                self.stop()

            case 'Mov. call':

                await interaction.response.send_message('Mande no chat o id da pessoa a remover o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if movi not in membro.roles:
                    return await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                e = discord.Embed(title='Remover cargo de Mov. call')

                e.add_field(name='Quem vai ser Removido o cargo', value=f'{membro.mention}')
                e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser removido ', value=movi.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=RmvCargoEquipes())

                self.stop()


class cargochat2(discord.ui.View):

    def __init__(self, bot, timeout=300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Cargos",
        options=[
            discord.SelectOption(
                label='Chefe chat',
                description='Remove o cargo de Chefe chat',
            ),
            discord.SelectOption(
                label='Staff chat',
                description='Remove o cargo de Staff chat'
            ),
            discord.SelectOption(
                label='Mov. chat',
                description='Remove o cargo de Mov. chat'
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
                    await interaction.response.send_message('Mande no chat o id da pessoa a remover o cargo',
                                                            ephemeral=True)

                    def check50(m):
                        return m.content and m.author.id == interaction.user.id

                    msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                    membro = interaction.guild.get_member(int(msg50.content))

                    await msg50.delete()

                    if liderchat not in membro.roles:
                        return await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                    e = discord.Embed(title='Remover cargo de Chefe chat')

                    e.add_field(name='Quem vai ser Removedo o cargo', value=f'{membro.mention}')
                    e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                    e.add_field(name='Qual cargo vai ser removido ', value=liderchat.mention, inline=False)

                    e.set_footer(text=membro.id)

                    await interaction.channel.send(embed=e, view=RmvCapEquipes())

                    self.stop()

                else:

                    return await interaction.response.send_message('Você não tem permissão para usar isto',
                                                                   ephemeral=True)

            case 'Staff chat':

                await interaction.response.send_message('Mande no chat o id da pessoa a remover o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if staffchat not in membro.roles:
                    await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                    return

                e = discord.Embed(title='Remover cargo de Staff Chat')

                e.add_field(name='Quem vai ser Removido o cargo', value=f'{membro.mention}')
                e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser removido ', value=staffchat.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=RmvCargoEquipes())

                self.stop()

            case 'Mov. chat':

                await interaction.response.send_message('Mande no chat o id da pessoa a remover o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if movi not in membro.roles:
                    await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                    return

                e = discord.Embed(title='Remover cargo de Mov. chat')

                e.add_field(name='Quem vai ser Removido o cargo', value=f'{membro.mention}')
                e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser removido ', value=movi.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=RmvCargoEquipes())

                self.stop()


class cargoreg2(discord.ui.View):

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

                    if regchefe not in membro.roles:
                        return await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                    e = discord.Embed(title='Remover cargo de Reg. Chefe')

                    e.add_field(name='Quem vai ser removido o cargo', value=f'{membro.mention}')

                    e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                    e.add_field(name='Qual cargo vai ser removido ', value=regchefe.mention, inline=False)

                    e.set_footer(text=membro.id)

                    await interaction.channel.send(embed=e, view=RmvCapEquipes())

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

                if registrador not in membro.roles:
                    return await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                e = discord.Embed(title='Remover cargo de Registrador')

                e.add_field(name='Quem vai ser removido o cargo', value=f'{membro.mention}')

                e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser removido ', value=registrador.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=RmvCargoEquipes())

                self.stop()

            case 'Ajudante':

                await interaction.response.send_message('Mande no chat o id da pessoa a receber o cargo',
                                                        ephemeral=True)

                def check50(m):
                    return m.content and m.author.id == interaction.user.id

                msg50 = await self.bot.wait_for('message', check=check50, timeout=130)

                membro = interaction.guild.get_member(int(msg50.content))

                await msg50.delete()

                if regjunior not in membro.roles:
                    return await interaction.channel.send('Este membro não possue este cargo', delete_after=3)

                e = discord.Embed(title='Remover cargo de Reg. Junior')

                e.add_field(name='Quem vai ser removido o cargo', value=f'{membro.mention}')

                e.add_field(name='Quem removeu ', value=interaction.user.mention, inline=False)

                e.add_field(name='Qual cargo vai ser removido ', value=regjunior.mention, inline=False)

                e.set_footer(text=membro.id)

                await interaction.channel.send(embed=e, view=RmvCargoEquipes())

                self.stop()
