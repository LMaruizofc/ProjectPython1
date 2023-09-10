import discord

from discord.ext import commands
from discord import slash_command

class GeraisConvidar(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot
    
    @slash_command(name = "convidar", description = "Envia o link para convidar a RE=L para seu servidor")
    async def convidar(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://discord.com/api/oauth2/authorize?client_id=1018958083764002919&permissions=8&scope=bot%20applications.commands",ephemeral = True)

    @slash_command(name="servers")
    async def servers(self, i: discord.Interaction):

        await i.response.send_message(f"{self.bot.guilds.__len__()}")
        
def setup(bot:commands.Bot):
    bot.add_cog(GeraisConvidar(bot))