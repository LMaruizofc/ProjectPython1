import discord

from discord.ext import commands
from discord import option, SlashCommandGroup


class feedback(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    feedback = SlashCommandGroup("suporte")

    @feedback.command(name="sugestão",
                      description="Envia uma sugestão ao meu dono",
                      guild_only=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @option(name="sugest", description="Escreva a sugestão")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sugest(self, interaction: discord.Interaction, sugestão):
        channel: discord.TextChannel = self.bot.get_channel(int(1012123748637343756))
        emojiTicket: discord.Emoji = self.bot.get_emoji(1044752355163394119)

        embed: discord.Embed = discord.Embed(
            title="Sugest",
            description=f"""
**Enviado por:** \n {interaction.author}
**Sugestão:** \n {sugestão}
**No server:** \n {interaction.guild.name}
**ID:** {interaction.author.id}
                """
        )

        await interaction.response.send_message(f'{emojiTicket} Sugestão enviada com sucesso', ephemeral=True)

        await channel.send(embed=embed)

    @feedback.command(name="reportar",
                      description="Envia um report ao meu dono",
                      guild_only=True, )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @option(name="report", description="Escreva o report")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def report(self, interaction: discord.Interaction, report):
        channel: discord.TextChannel = self.bot.get_channel(int(1012123813070262312))
        emojiTicket: discord.Emoji = self.bot.get_emoji(1044752355163394119)

        embed: discord.Embed = discord.Embed(
            title="report",
            description=f"""
**Enviado por:** \n {interaction.author}
**Report:** \n {report}
**No server:** \n {interaction.guild.name}
**ID:** {interaction.author.id}
                    """
        )

        await interaction.response.send_message(f'{emojiTicket} Report enviado com sucesso', ephemeral=True)

        await channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(feedback(bot))
