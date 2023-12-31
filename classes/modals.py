import discord

from discord.ext import commands
from discord.ui import InputText, Modal
from .buttons import BanButtons, AdvAdcButtons, AdvRmvButtons, PuxarModal, Ticket
from .selectmenus import createSelect

class banModal(Modal):

    def __init__(self) -> None:

        super().__init__(title = "Ban", custom_id = "Modal")

        self.add_item(
            InputText(
                label = "ID",
                placeholder = "Id do membro a banir",
                required = True
            )
        ),
        self.add_item(
            InputText(
                label = "Motivo",
                placeholder = "Motivo de banir o membro",
                required = True
            )
        )
    async def callback(self, interaction: discord.Interaction):
        
        member = interaction.guild.get_member(int(self.children[0].value))
        
        embed = discord.Embed(title = "Ban")
        embed.add_field(name = "Name",value=member.name,inline = False)
        embed.add_field(name = "Author",value=interaction.user,inline = False)
        embed.add_field(name = "Motivo",value=self.children[1].value,inline = False)
        embed.set_footer(text = member.id)
        embed.set_thumbnail(url = member.display_avatar)

        await interaction.response.send_message(embed = embed, view = BanButtons())
        
class adivertenciaAdicionarModal(Modal):

    def __init__(self) -> None:

        super().__init__(title = "Adicionar adivertencia", custom_id = "Modal")

        self.add_item(
            InputText(
                label = "ID",
                placeholder = "Id do membro a adicionar a adivertencia",
                required = True
            )
        ),
        self.add_item(
            InputText(
                label = "Motivo",
                placeholder = "Motivo de advertir o membro",
                required = True
            )
        )
    async def callback(self, interaction: discord.Interaction):
        
        member = interaction.guild.get_member(int(self.children[0].value))
        
        embed = discord.Embed(title = "Adicionar Advertincia")
        embed.add_field(name = "Name",value=member.name,inline = False)
        embed.add_field(name = "Author",value=interaction.user.mention,inline = False)
        embed.add_field(name = "Motivo",value=self.children[1].value,inline = False)
        embed.set_footer(text = member.id)
        embed.set_thumbnail(url = member.display_avatar)

        await interaction.response.send_message(embed = embed, view = AdvAdcButtons())

class adivertenciaRemoverModal(Modal):

    def __init__(self) -> None:

        super().__init__(title = "Remover adivertencia", custom_id = "Modal")

        self.add_item(
            InputText(
                label = "ID",
                placeholder = "Id do membro a remover a adivertencia",
                required = True
            )
        ),
    async def callback(self, interaction: discord.Interaction):
        
        member = interaction.guild.get_member(int(self.children[0].value))
        
        embed = discord.Embed(title = "Ban")
        embed.add_field(name = "Name",value=member.name,inline = False)
        embed.add_field(name = "Author",value=interaction.user,inline = False)
        embed.set_footer(text = member.id)
        embed.set_thumbnail(url = member.display_avatar)

        await interaction.response.send_message(embed = embed, view = AdvRmvButtons())


class ticketModalStarterEmbed(Modal):

    def __init__(self, **kwargs) -> None:

        self.kwargs = kwargs

        super().__init__(title = "Embed ticket")

        self.add_item(
            InputText(
                label = "Titilo da embed",
                placeholder = "Titulo da embed",
                required = True
            )
        ),
        self.add_item(
            InputText(
                label = "Descrição da embed",
                placeholder = "Descrição da embed",
                required = True,
                style = discord.InputTextStyle.long
            )
        ),
        self.add_item(
            InputText(
                label = "Imagem",
                placeholder = "Url da imagem da embed",
                required = False
            )
        )
    async def callback(self, interaction: discord.Interaction):

        e = discord.Embed(
            title = self.children[0].value,
            description = self.children[1].value
        )
        try:
            e.set_image(url = self.children[2].value)
        except:
            pass

        await interaction.response.send_message(
            view=PuxarModal(
                name = "ticketModalSelect",
                embed = e,
                webhook_id = self.kwargs.get("webhook_id"),
                channel_id = self.kwargs.get("channel_id")
            ),
            ephemeral = True
        )

class ticketModalSelect(Modal):

    def __init__(self, **kwargs):

        self.kwargs = kwargs

        super().__init__(title = "Select")

        self.add_item(
            InputText(
                label = "Tipo",
                placeholder = "Selecione o tipo, DropDown/Button",
                required = True
            )
        ),
        self.add_item(
            InputText(
                label = "Quantidade",
                placeholder = "Quantidade de botão ou DropDown (Maximo 5)",
                required = True,
                value = 1,
                max_length=1
            )
        )
    async def callback(self, interaction: discord.Interaction):
        
        match self.children[0].value.lower():

            case "dropdown" | "dropview":

                await interaction.response.send_message(
                    view=PuxarModal(
                        type = "Select",
                        label = "Nome",
                        name = "modalCreator",
                        qnt = self.children[1].value,
                        embed = self.kwargs.get("embed"),
                        webhook_id = self.kwargs.get("webhook_id"),
                        channel_id = self.kwargs.get("channel_id"),
                        name_list = []
                    ),
                    ephemeral = True
                )

            case "button" | "botão" | "botao":

                await interaction.response.send_message(
                    view=PuxarModal(
                        type = "Button",
                        label = "Nome",
                        name = "modalCreator",
                        qnt = self.children[1].value,
                        embed = self.kwargs.get("embed"),
                        webhook_id = self.kwargs.get("webhook_id"),
                        channel_id = self.kwargs.get("channel_id"),
                        name_list = []
                    ),
                    ephemeral = True
                )

class modalCreator(Modal):

    def __init__(self, **kwargs):

        self.kwargs = kwargs

        self.bot = commands.Bot

        super().__init__(title = "Nome")

        for i in range(0, int(kwargs.get("qnt"))):

            self.add_item(
                InputText(
                    label = f"{kwargs.get('label')} {i}",
                    placeholder = f"{kwargs.get('label')} do DropDown"
                )
            ),
    async def callback(self, interaction: discord.Interaction):

        if self.kwargs.get("type") == "Select":

            if "Categoria" in self.children[0].label:
                
                w = []
                for i in range(0,int(self.kwargs.get("qnt"))):
                    w.append(self.children[i].value)

                if self.kwargs.get("webhook_id") != None:

                    for web in await interaction.guild.webhooks():
                        if web.id == int(self.kwargs.get("webhook_id")):
                            await web.send(
                                embed = self.kwargs.get("embed"), 
                                view = createSelect(
                                        name_list = self.kwargs.get("name_list"),
                                        qnt = self.kwargs.get("qnt"),
                                        idcategorias = w
                                    )
                                )
                            await interaction.response.send_message("Pronto", ephemeral = True)
                            return await web.delete()

                await interaction.response.send_message("Pronto", ephemeral = True)

                channel = interaction.guild.get_channel(int(self.kwargs.get("channel_id")))

                return await channel.send(
                        embed = self.kwargs.get("embed"), 
                        view = createSelect(
                                name_list = self.kwargs.get("name_list"),
                                qnt = self.kwargs.get("qnt"),
                                idcategorias = w
                            )
                    )
            
            w = []

            for i in range(0,int(self.kwargs.get("qnt"))):
                w.append(self.children[i].value)
            
            await interaction.response.send_message(
                        view=PuxarModal(
                            type = "Select",
                            label = "Categoria",
                            name = "modalCreator",
                            qnt = int(self.kwargs.get("qnt")),
                            embed = self.kwargs.get("embed"),
                            webhook_id = self.kwargs.get("webhook_id"),
                            channel_id = self.kwargs.get("channel_id"),
                            name_list = w
                        ),
                        ephemeral = True
                    )
        elif self.kwargs.get("type") == "Button":

            if "Categoria" in self.children[0].label:
                
                w = []
                for i in range(0,int(self.kwargs.get("qnt"))):
                    w.append(self.children[i].value)

                if self.kwargs.get("webhook_id") != None:

                    for web in await interaction.guild.webhooks():
                        if web.id == int(self.kwargs.get("webhook_id")):
                            await web.send(
                                embed = self.kwargs.get("embed"), 
                                view = Ticket(
                                        name_list = self.kwargs.get("name_list"),
                                        qnt = self.kwargs.get("qnt"),
                                        idcategorias = w
                                    )
                                )
                            await interaction.response.send_message("Pronto", ephemeral = True)
                            return await web.delete()

                await interaction.response.send_message("Pronto", ephemeral = True)

                channel = interaction.guild.get_channel(int(self.kwargs.get("channel_id")))

                return await channel.send(
                        embed = self.kwargs.get("embed"), 
                        view = Ticket(
                                name_list = self.kwargs.get("name_list"),
                                qnt = self.kwargs.get("qnt"),
                                idcategorias = w
                            )
                    )
            
            w = []

            for i in range(0,int(self.kwargs.get("qnt"))):
                w.append(self.children[i].value)
            
            await interaction.response.send_message(
                        view=PuxarModal(
                            type = "Button",
                            label = "Categoria",
                            name = "modalCreator",
                            qnt = int(self.kwargs.get("qnt")),
                            embed = self.kwargs.get("embed"),
                            webhook_id = self.kwargs.get("webhook_id"),
                            channel_id = self.kwargs.get("channel_id"),
                            name_list = w
                        ),
                        ephemeral = True
            )