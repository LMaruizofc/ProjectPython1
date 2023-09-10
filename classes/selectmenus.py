import discord


class createSelect(discord.ui.View):

    def __init__(self, **kwargs):
        super().__init__()

        options = []

        for i in range(0, kwargs.get("qnt")):
            options.append(
                discord.SelectOption(
                    label=f"{kwargs.get('name_list')[i]}",
                    value=f"c{i}-{kwargs.get('idcategorias')[i]}",
                )
            )

        self.add_item(
            discord.ui.Select(
                placeholder="Abrir Ticket",
                options=options,
                custom_id="ticket_select",
                max_values=1,
                min_values=1,
            )
        )
