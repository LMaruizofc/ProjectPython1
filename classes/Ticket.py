from datetime import datetime, timedelta
import discord
from discord.interactions import Interaction
from discord.ui import Modal, Select, View
from discord.ui.input_text import InputText
from classes.selectmenus import createSelect
from db.dono import modDono, Premium
from db.moderation import db_temp_ticket
from classes.buttons import Ticket


class embedCreator(Modal):

    def __init__(self) -> None:

        super().__init__(title = "Embed ticket")

        self.add_item(
            InputText(
                label = "Titilo da embed",
                placeholder = "Titulo da embed",
                required = False
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
        ejson = {
            "title": self.children[0].value,
            "description": self.children[1].value,
        }
        try:
            e.set_image(url = self.children[2].value)
            ejson["image"] = {
                "url": self.children[2].value
            }
        except:
            pass

        if db_temp_ticket.contains(doc_id=interaction.guild.id):
            doc = db_temp_ticket.get(doc_id=interaction.guild.id)
            doc["embed"] = ejson
            db_temp_ticket.update(doc, doc_ids=[interaction.guild.id])

        await interaction.response.send_message(view=View(ticketSelectType(), timeout=None), ephemeral = True)


class ticketSelectType(Select):

    def __init__(self) -> None:

        super().__init__(
            placeholder="Selecione o tipo",
            options=[
                discord.SelectOption(
                    label="Botão",
                    value="1",
                    description="O ticket vai ser por botão"
                ),
                discord.SelectOption(
                    label="Select Menu",
                    value="2",
                    description="O ticket vai ser por Menu de Seleção"
                )
            ]
        )
    async def callback(self, interaction: Interaction):
        
        await interaction.response.edit_message(view=View(selectQnt(interaction), timeout=None))

        if db_temp_ticket.contains(doc_id=interaction.guild.id):
            doc = db_temp_ticket.get(doc_id=interaction.guild.id)
            doc["type"] = self.values[0]
            db_temp_ticket.update(doc, doc_ids=[interaction.guild.id])


class selectQnt(Select):

    def __init__(self, interaction):

        try:
            modDono.find_one({"_id": interaction.guild.id})["premium"]["enable"]
        except:
            Premium(interaction.guild, datetime.now() + timedelta(seconds=5), False)

        opts = []
        for i in range(0, 20):
            if i > 2:
                if modDono.find_one({"_id": interaction.guild.id})["premium"]["enable"]:
                    lb = f"{i+1}"
                else:
                    lb = f"{i+1} ⭐Premium"
                opts.append(
                    discord.SelectOption(
                        label= lb,
                        value=f"{i}"
                    )
                )
            else:
                opts.append(
                    discord.SelectOption(
                        label=f"{i+1}",
                        value=f"{i}"
                    )
                )
        super().__init__(
            placeholder="Quantidade",
            options= opts
        )
    async def callback(self, interaction: Interaction):
        
        if int(self.values[0]) > 2:

            if modDono.find_one({"_id": interaction.guild.id})["premium"]["enable"]:
                qnt = int(self.values[0])+1
            else:
                return await interaction.response.send_message("Seu servidor não está na lista de premium", ephemeral=True)

        else:
            qnt = int(self.values[0])+1

        if db_temp_ticket.contains(doc_id=interaction.guild.id):
            doc = db_temp_ticket.get(doc_id=interaction.guild.id)
            doc["qnt"] = qnt
            db_temp_ticket.update(doc, doc_ids=[interaction.guild.id])

        
        await interaction.response.edit_message()
        
        nl= []
        for i in range(0,db_temp_ticket.get(doc_id=interaction.guild.id)["qnt"]):
            
            def check(m: discord.Message):
                return m.content and m.author == interaction.user

            await interaction.edit_original_response(content=f"Mande o nome do {i+1}°",view=None)

            msg = await interaction.client.wait_for("message", check=check, timeout=None)

            nl.append(msg.content)

            await msg.delete()
        
        idc=[]
        for i in range(0,db_temp_ticket.get(doc_id=interaction.guild.id)["qnt"]):
            
            def check(m: discord.Message):
                return m.content and m.author == interaction.user

            await interaction.edit_original_response(content=f"Mande o id da categoria do {i+1}°")

            msg = await interaction.client.wait_for("message", check=check, timeout=None)

            idc.append(msg.content)

            await msg.delete()
        
        e = discord.Embed.from_dict(db_temp_ticket.get(doc_id=interaction.guild.id)["embed"])

        if db_temp_ticket.get(doc_id=interaction.guild.id)["webhook_id"] == None or db_temp_ticket.get(doc_id=interaction.guild.id)["webhook_id"] == "null":
            if int(db_temp_ticket.get(doc_id=interaction.guild.id)["type"]) == 2:

                await interaction.guild.get_channel(
                    db_temp_ticket.get(doc_id=interaction.guild.id)["channel_id"]
                    ).send(
                    embed=e, 
                    view= createSelect(
                            qnt=db_temp_ticket.get(doc_id=interaction.guild.id)["qnt"],
                            name_list=nl, 
                            idcategorias=idc
                        )
                    )
            else:
                await interaction.guild.get_channel(
                    db_temp_ticket.get(doc_id=interaction.guild.id)["channel_id"]
                    ).send(
                    embed=e, 
                    view= Ticket(
                            qnt=db_temp_ticket.get(doc_id=interaction.guild.id)["qnt"],
                            name_list=nl, 
                            idcategorias=idc
                        )
                    )
        else:
            if int(db_temp_ticket.get(doc_id=interaction.guild.id)["type"]) == 2:
                for web in await interaction.guild.webhooks():
                    if web.id == int(db_temp_ticket.get(doc_id=interaction.guild.id)["webhook_id"]):
                        await web.send(
                            embed = e,
                            view= createSelect(
                                qnt=db_temp_ticket.get(doc_id=interaction.guild.id)["qnt"],
                                name_list=nl, 
                                idcategorias=idc
                            )
                        )
                        await web.delete()
            else:
                for web in await interaction.guild.webhooks():
                    if web.id == int(db_temp_ticket.get(doc_id=interaction.guild.id)["webhook_id"]):
                        await web.send(
                            embed = e,
                            view= Ticket(
                                qnt=db_temp_ticket.get(doc_id=interaction.guild.id)["qnt"],
                                name_list=nl, 
                                idcategorias=idc
                            )
                        )
                        await web.delete()
