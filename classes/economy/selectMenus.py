import discord
import NewFunctionsPYC

from discord.ext import pages, commands
from db.economy import economy, update_inv
from economy.frutosdomar import on_frutos
from economy.recursos import on_recursos
from economy.utilitarios import on_utilitarios


class MercadoVer(discord.ui.View):

    def __init__(self, bot: commands.Bot, user: discord.Member):

        self.bot = bot
        self.user = user
        self.paginator: list = []

        super().__init__(timeout=300)

    def get_pages(self):
        return self.paginator

    @discord.ui.select(
        placeholder="Mercado",
        options=[
            discord.SelectOption(
                label="Recursos",
                description="Menu de recursos",
                value="REC"
            ),
            discord.SelectOption(
                label="Frutos do mar",
                description="Menu de frutos do mar",
                value="FRUTOS"
            ),
            discord.SelectOption(
                label="Utilitarios",
                description="Menu de utilitarios",
                value="UTILI"
            ),
        ]
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):

        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("Isso não te pertence", ephemeral=True)

        e = NewFunctionsPYC.EmbedBuilder()

        match select.values[0]:

            case "REC":

                e.set_title("Recursos")

                for i in await on_recursos(self.bot):
                    e.add_field(name=i["name"], value=f"Compra: {i['compra']}\nVenda: {i['venda']}")
                    if e.build().fields.__len__() == 10:
                        self.paginator.append(e.build())
                        e.detonarn()
                        e = NewFunctionsPYC.EmbedBuilder()
                        e.set_title("Recursos")

                if self.paginator.__len__() > 0:
                    await interaction.response.defer()

                    await interaction.followup.edit_message(interaction.message.id,
                                                            view=MercadoVer(self.bot, self.user))

                    e.set_title("Recursos")

                    self.paginator.append(e.build())

                    pagi = pages.Paginator(self.get_pages())

                    return await pagi.respond(interaction, ephemeral=True)

                await interaction.response.edit_message(embed=e.build(), view=MercadoVer(self.bot, self.user))

            case "FRUTOS":

                e.set_title("Frutos do mar")

                for i in await on_frutos(self.bot):
                    e.add_field(name=i["name"], value=f"Compra: {i['compra']}\nVenda: {i['venda']}")
                    if e.build().fields.__len__() == 10:
                        self.paginator.append(e.build())
                        e.detonarn()
                        e = NewFunctionsPYC.EmbedBuilder()
                        e.set_title("Frutos do mar")

                if self.paginator.__len__() > 0:
                    await interaction.response.defer()

                    await interaction.response.edit_message(view=MercadoVer(self.bot, self.user))

                    e.set_title("Frutos do mar")

                    self.paginator.append(e.build())

                    pagi = pages.Paginator(self.get_pages())

                    return await pagi.respond(interaction, ephemeral=True)

                await interaction.response.edit_message(embed=e.build(), view=MercadoVer(self.bot, self.user))

            case "UTILI":

                e.title = "Utilitarios"

                for i in await on_utilitarios(self.bot):
                    e.add_field(name=i["name"], value=f"Compra: {i['compra']}\nVenda: {i['venda']}")
                    if e.build().fields.__len__() == 10:
                        self.paginator.append(e.build())
                        e.detonarn()
                        e = NewFunctionsPYC.EmbedBuilder()
                        e.set_title("Utilitarios")

                if self.paginator.__len__() > 0:
                    await interaction.response.defer()

                    await interaction.followup.edit_message(interaction.message.id,
                                                            view=MercadoVer(self.bot, self.user))

                    e.set_title("Utilitarios")

                    self.paginator.append(e.build())

                    pagi = pages.Paginator(self.get_pages())

                    return await pagi.respond(interaction, ephemeral=True)

                await interaction.response.edit_message(embed=e.build(), view=MercadoVer(self.bot, self.user))


class selectCraft(discord.ui.View):

    def __init__(self, **kwargs):

        self.user = kwargs.get("user")

        super().__init__(timeout=180)

    @discord.ui.select(
        placeholder="Item",
        options=[
            discord.SelectOption(
                label="Picareta de Ferro",
                description="Cria a picareta de ferro",
                value="PICFERRO"
            ),
            discord.SelectOption(
                label="Picareta de Ouro",
                description="Cria a picareta de ouro",
                value="PICOURO"
            ),
            discord.SelectOption(
                label="Picareta de diamante",
                description="Cria a picareta de diamante",
                value="PICDIAMANTE"
            )
        ]
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):

        if interaction.user.id != interaction.guild.get_member(self.user).id:
            return await interaction.response.send_message("Esse select menu não é seu", ephemeral=True)

        for i in ["madeira", "ferro", "ouro", "diamante"]:
            try:
                economy.find_one({"_id": interaction.user.id})["inventario"][i]
            except:
                update_inv(interaction.user, i, 0)

        inv = inv = economy.find_one({"_id": interaction.user.id})["inventario"]

        try:
            match select.values[0]:

                case "PICFERRO":

                    if inv["madeira"] < 1:
                        await interaction.response.send_message('Você não tem madeira suficiente', ephemeral=True)
                        return await interaction.message.edit(view=selectCraft(user=self.user))

                    elif inv["ferro"] < 3:
                        await interaction.response.send_message('Você não tem ferro suficiente', ephemeral=True)
                        return await interaction.message.edit(view=selectCraft(user=self.user))

                    update_inv(interaction.user, "madeira", -1)
                    update_inv(interaction.user, "ferro", -3)
                    update_inv(interaction.user, "picareta de ferro", 1)
                    await interaction.response.send_message("Item craftado com sucesso", ephemeral=True)
                    await interaction.message.edit(view=selectCraft(user=self.user))

                case "PICOURO":

                    if inv["madeira"] < 1:
                        await interaction.response.send_message('Você não tem madeira suficiente', ephemeral=True)
                        return await interaction.message.edit(view=selectCraft(user=self.user))

                    elif inv["ouro"] < 3:
                        await interaction.response.send_message('Você não tem ouro suficiente', ephemeral=True)
                        return await interaction.message.edit(view=selectCraft(user=self.user))

                    update_inv(interaction.user, "madeira", -1)
                    update_inv(interaction.user, "ouro", -3)
                    update_inv(interaction.user, "picareta de ouro", 1)
                    await interaction.response.send_message("Item craftado com sucesso", ephemeral=True)
                    await interaction.message.edit(view=selectCraft(user=self.user))

                case "PICDIAMANTE":

                    if inv["madeira"] < 1:
                        await interaction.response.send_message('Você não tem madeira suficiente', ephemeral=True)
                        return await interaction.message.edit(view=selectCraft(user=self.user))

                    elif inv["diamante"] < 6:
                        await interaction.response.send_message('Você não tem diamante suficiente', ephemeral=True)
                        return await interaction.message.edit(view=selectCraft(user=self.user))

                    update_inv(interaction.user, "madeira", -1)
                    update_inv(interaction.user, "diamante", -6)
                    update_inv(interaction.user, "picareta de diamante", 1)
                    await interaction.response.send_message("Item craftado com sucesso", ephemeral=True)
                    await interaction.message.edit(view=selectCraft(user=self.user))
        except:
            await interaction.response.send_message("Iventario adicionado, selecione novamente", ephemeral=True)
            await interaction.message.edit(view=selectCraft(user=self.user))
