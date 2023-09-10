import discord

from ..modalsMod import adivertenciaAdicionarModal, adivertenciaRemoverModal
from .adicionarcargosequipes import AdcCargos
from .removercargosequipes import RmvCargos


class adcrmvadivertência(discord.ui.View):

    def __init__(self, timeout=300):

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Advivertencia",
        options=[
            discord.SelectOption(
                label='Adicionar',
                description='Adiciona uma advertencia'
            ),
            discord.SelectOption(
                label='Remover',
                description='Remove uma advertencia'
            )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):

        if select.values[0] == 'Adicionar':
            await interaction.response.send_modal(adivertenciaAdicionarModal())
        elif select.values[0] == 'Remover':
            await interaction.response.send_modal(adivertenciaRemoverModal())


class adcrmvcargosequipes(discord.ui.View):

    def __init__(self, bot, timeout=300):

        self.bot = bot

        super().__init__(timeout=timeout)

    @discord.ui.select(
        placeholder="Ação",
        options=[
            discord.SelectOption(
                label='Adicionar',
                description='Adiciona o cargo'
            ),
            discord.SelectOption(
                label='Remover',
                description='Remove o cargo'
            )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):

        if select.values[0] == 'Adicionar':
            await interaction.response.send_message('De qual equipe?', ephemeral=True, view=AdcCargos(self.bot))

        elif select.values[0] == 'Remover':
            await interaction.response.send_message('De qual equipe?', ephemeral=True, view=RmvCargos(self.bot))
