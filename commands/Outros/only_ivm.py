import discord

from discord.ext import commands
from discord import slash_command, option
from classes.buttons import ComandosStaff
from utils.loader import configData
from db.moderation import adv, ausen


class only_ivm(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(
        guild_only=True, guild_ids=[configData["guild"]],
        name="buttonsstaff",
        description="Envia os botons de staff"
    )
    @option(name="channel", description="Escolha o chat para mandar")
    async def buttonstaff(self, interaction: discord.Interaction,channel: discord.TextChannel = None):

        if channel == None: channel = interaction.channel

        await interaction.response.send_message('Foi', ephemeral=True)

        await channel.send("", view=ComandosStaff())

    @slash_command(
        guild_only=True, 
        guild_ids=[configData["guild"]],
        name='say',
        description='Envia uma mensagem em um chat'
    )
    @option(name='canal', description='Escolha o canal que falar')
    @option(name='mensagem', description='Escreva oq deseja que eu fale')
    async def say(self,
                  interaction: discord.Interaction,
                  mensagem: str,
                  canal: discord.TextChannel = None
                  ):

        if canal is None:
            canal = interaction.channel

        cmdl = f'''{interaction.user} usou o comando {interaction.command.name} e falou {mensagem}'''

        cmdlc = self.bot.get_channel(configData['logs']['usocomandos'])

        await cmdlc.send(cmdl)

        await canal.send(mensagem)

    @slash_command(
        guild_only=True, 
        guild_ids=[configData["guild"]], 
        name='editmsg',
        description='edita uma mensagem já enviada'
    )
    @option(name='channel', description='envie o id do canal')
    @option(name='messageid', description='envie o id da mensagem')
    @option(name='msg', description='Escreva a mensagem á editar')
    @commands.has_guild_permissions(manage_channels=True)
    async def editmsg(self,
                      interaction: discord.Interaction,
                      msg: str,
                      messageid: str,
                      channel: discord.TextChannel = None
                      ):

        if channel is None:
            channel = interaction.channel

        mensagem = await channel.fetch_message(int(messageid))

        await mensagem.edit(content=msg)

        cmdl = f'''{interaction.user} usou o comando {interaction.command.name} e editou a mensagem {messageid} no chat {channel.mention}'''

        cmdlc = self.bot.get_channel(configData['logs']['usocomandos'])

        await cmdlc.send(cmdl)

    @slash_command(
        guild_only=True,
        guild_ids=[configData["guild"]],
        name="embed",
        description="Envia uma embed em um chat desejado"
    )
    @option(name="channel", description="Escolha o chat para enviar a embed")
    @option(name="title", description="Escreva o titulo da embed")
    @option(name="link_image", description="Escolha a imagem da embed")
    @option(name="mention", description="Mencione um cargo para mencionar na embed")
    @option(name="content", description="Escreva o conteudo da embed")
    @commands.has_guild_permissions(manage_channels=True)
    async def embed(self,
                    interaction: discord.Interaction,
                    channel: discord.TextChannel = None,
                    title=None,
                    img=None,
                    mention: discord.Role = None,
                    content=None
                    ):

        if channel is None:
            channel = interaction.channel
        if title is None:
            title = ""
        if img is None:
            img = ""
        if content is None:
            content = ""
        if mention is None:
            mention = ""

        e = discord.Embed(title=title, description=content, colour=0x4B0082)
        e.set_image(url=img)
        e.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon)
        await channel.send(mention, embed=e)
        await interaction.response.send_message("Enviado certinho", ephemeral=True)

        cmdl = f"""{interaction.user} usou o comando {interaction.command.name} e enviou uma embed no {channel.mention}"""
        cmdlc = self.bot.get_channel(configData["logs"]["usocomandos"])
        await cmdlc.send(cmdl)

    @slash_command(
        guild_only=True,
        guild_ids=[configData["guild"]],
        name='editembed',
        description='Edita uma embed já enviada'
    )
    @option(name='channel', description='Envie o id do canal')
    @option(name='embedid', description='Envie o id da embed')
    @option(name='title', description='Escreva o titulo da embed')
    @option(name='img', description='Escolha a imagem da embed')
    @option(name='mention', description='Mencione um cargo para mencionar na embed')
    @option(name='content', description='Escreva o conteudo da embed')
    @commands.has_guild_permissions(manage_channels=True)
    async def editembed(self,
                        interaction: discord.Interaction,
                        channel: discord.TextChannel = None,
                        embedid: int = None,
                        title: str = None,
                        img: str = None,
                        mention: discord.Role = None,
                        content: str = None
                        ):

        if channel is None:
            channel = interaction.channel
        if title is None:
            title = ''
        if img is None:
            img = ''
        if content is None:
            content = ''
        if mention is None:
            mention = ''

        mensagem = await channel.fetch_message(int(embedid))

        e = discord.Embed(title=title, description=content, colour=0x4B0082)

        e.set_image(url=img)

        e.set_footer(text=f'{interaction.guild.name} author: {interaction.user.name}', icon_url=interaction.guild.icon)

        await mensagem.edit(content=mention, embed=e)

        cmdl = f'{interaction.user} usou o comando {interaction.command.name} e edtou a embed {embedid} no canal {channel.mention}'

        cmdlc = self.bot.get_channel(configData['logs']['usocomandos'])

        await cmdlc.send(cmdl)

    @slash_command(
        guild_only=True,
        guild_ids=[configData["guild"]],
        name='veradv',
        description='Envia as advs de um membro'
    )
    @option(name='membro', description='Escolha o membro a remover a advertencia')
    async def veradv(self,
                     interaction: discord.Interaction,
                     membro: discord.Member
                     ):

        myquery = {"_id": membro.id}

        if adv.count_documents(myquery) == 1:

            cmdl = f'''{interaction.user} usou o comando {interaction.command.name} e viu as advertencias de {membro.display_name}'''

            cmdlc = self.bot.get_channel(configData['logs']['usocomandos'])

            await cmdlc.send(cmdl)

            ad = adv.find_one({"_id": membro.id})

            adv1 = ad['Adv1']

            adv2 = ad['Adv2']

            adv3 = ad['Adv3']

            if adv1 == 'None':
                return await interaction.response.send_message('Esse membro não Possui advertencia', ephemeral=True)

            if adv3 != 'None':
                e = discord.Embed(title=f'Advertencias de {membro.name}#{membro.discriminator}',
                                  description=f'Adv1: {adv1}\nAdv2: {adv2}\nAdv3: {adv3}')

                return await interaction.response.send_message(embed=e, ephemeral=True)

            if adv2 != 'None':
                e = discord.Embed(title=f'Advertencias de {membro.name}#{membro.discriminator}',
                                  description=f'Adv1: {adv1}\nAdv2: {adv2}')

                return await interaction.response.send_message(embed=e, ephemeral=True)

            if adv1 != 'None':
                e = discord.Embed(title=f'Advertencias de {membro.name}#{membro.discriminator}',
                                  description=f'Adv1: {adv1}')

                return await interaction.response.send_message(embed=e, ephemeral=True)

        await interaction.response.send_message('Esse membro não Possui advertencia', ephemeral=True)

        cmdl = f'''{interaction.user} usou o comando {interaction.command.name} e viu as advertencias de {membro.display_name}'''

        cmdlc = self.bot.get_channel(configData['logs']['usocomandos'])

        await cmdlc.send(cmdl)

    @slash_command(
        guild_only=True,
        guild_ids=[configData["guild"]],
        name='verausentes',
        description='Mostra todos os membros em estado de ausente'
    )
    async def verausente(self,
                         interaction: discord.Interaction
                         ):

        if ausen.find_one({"_id": 'validador'})['valor'] == 1:
            await interaction.response.send_message('Aqui está os ausentes', ephemeral=True)

            for x in ausen.find({'Ausente?': True}):
                await interaction.response.send_message(f"Nome: {x['Nome']}\nData: {x['Data']}\nMotivo: {x['Motivo']}",
                                                        ephemeral=True)

        else:
            await interaction.response.send_message('Ninguem está ausente no momento', ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(only_ivm(bot))
