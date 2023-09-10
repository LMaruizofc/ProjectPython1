import discord

from discord.ui import Button
from db.register import regCargo


class ComandosStaff(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='Ausencia',
                style=discord.ButtonStyle.blurple,
                custom_id="ausencia"
            )
        )
        self.add_item(
            Button(
                label='Cargos',
                style=discord.ButtonStyle.green,
                custom_id="adcCargosEquipes"
            )
        )
        self.add_item(
            Button(
                label='Ban',
                style=discord.ButtonStyle.red,
                custom_id="banMember"
            )
        )
        self.add_item(
            Button(
                label='Advertencia',
                style=discord.ButtonStyle.red,
                custom_id="advertência"
            )
        )


class BanButtons(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='✅',
                style=discord.ButtonStyle.red,
                custom_id="confirmBan"
            )
        )
        self.add_item(
            Button(
                label='❎',
                style=discord.ButtonStyle.red,
                custom_id="deny"
            )
        )


class KickButtons(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='✅',
                style=discord.ButtonStyle.red,
                custom_id="confirmKick"
            )
        )
        self.add_item(
            Button(
                label='❎',
                style=discord.ButtonStyle.red,
                custom_id="deny"
            )
        )


class AdvAdcButtons(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='✅',
                style=discord.ButtonStyle.red,
                custom_id="confirmAdcAdv"
            )
        )
        self.add_item(
            Button(
                label='❎',
                style=discord.ButtonStyle.red,
                custom_id="deny"
            )
        )


class AdvRmvButtons(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='✅',
                style=discord.ButtonStyle.red,
                custom_id="confirmRmvAdv"
            )
        )
        self.add_item(
            Button(
                label='❎',
                style=discord.ButtonStyle.red,
                custom_id="deny"
            )
        )


class AdcCapEquipes(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='✅',
                style=discord.ButtonStyle.red,
                custom_id="confirmAdcCap"
            )
        )
        self.add_item(
            Button(
                label='❎',
                style=discord.ButtonStyle.red,
                custom_id="denyAdcCap"
            )
        )


class AdcCargoEquipes(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='✅',
                style=discord.ButtonStyle.red,
                custom_id="confirmAdcEquipe"
            )
        )
        self.add_item(
            Button(
                label='❎',
                style=discord.ButtonStyle.red,
                custom_id="deny"
            )
        )


class Ticket(discord.ui.View):

    def __init__(self, **kwargs):
        super().__init__()

        for i in range(0, int(kwargs.get("qnt"))):
            self.add_item(
                Button(
                    style=discord.ButtonStyle.blurple,
                    label=f"{kwargs.get('name_list')[i]}",
                    custom_id=f"abrirTicket{i}-{kwargs.get('idcategorias')[i]}"
                )
            )


class AdonTicket(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='🔒 Fechar ticket',
                style=discord.ButtonStyle.blurple,
                custom_id="closeTicket"
            )
        )


class AdonTicket2(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='🔓 Abrir ticket',
                style=discord.ButtonStyle.blurple,
                custom_id="openTicket"
            )
        )
        self.add_item(
            Button(
                label='🛑 Deletar Ticket',
                style=discord.ButtonStyle.blurple,
                custom_id="deleteTicket"
            )
        )


class jumpto(discord.ui.View):

    def __init__(self, url):
        super().__init__()

        self.add_item(
            Button(
                label='Atalho para o ticket',
                style=discord.ButtonStyle.url,
                url=url
            )
        )


class RmvCapEquipes(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='✅',
                style=discord.ButtonStyle.red,
                custom_id="confirmRmvCap"
            )
        )
        self.add_item(
            Button(
                label='❎',
                style=discord.ButtonStyle.red,
                custom_id="denyRmvCap"
            )
        )


class RmvCargoEquipes(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='✅',
                style=discord.ButtonStyle.red,
                custom_id="confirmRmvEquipe"
            )
        )
        self.add_item(
            Button(
                label='❎',
                style=discord.ButtonStyle.red,
                custom_id="deny"
            )
        )


class creatorButton(discord.ui.View):

    def __init__(self, **kwargs):

        super().__init__()

        match kwargs.get("type"):

            case "selectCatego":

                for i in regCargo.find_one({"_id": kwargs.get("guild_id")}):
                    if i != "_id":
                        if "defaults" not in i:
                            self.add_item(Button(
                                label=i,
                                custom_id=f"catego-{i}",
                                style=discord.ButtonStyle.blurple
                            )
                            )

            case "regCargoAdd":

                for i in regCargo.find_one({"_id": kwargs.get("guild_id")})[kwargs.get("categoria")]:
                    a = regCargo.find_one({"_id": kwargs.get("guild_id")})[kwargs.get("categoria")][i]



                    self.add_item(Button(
                        label=a["name"],
                        custom_id=f"regButton-{a['cargoid']}",
                        style=discord.ButtonStyle.blurple
                    )
                    )

                self.add_item(Button(
                    label="Rotornar",
                    custom_id="menureg",
                    style=discord.ButtonStyle.green
                )
                )

                self.add_item(Button(
                    label="Finalizar",
                    custom_id="finalreg",
                    style=discord.ButtonStyle.red
                )
                )
