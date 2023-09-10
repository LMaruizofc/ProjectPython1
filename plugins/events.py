import discord

from discord.ext import commands
from checks.moderation import verfyadv, verfypoints
from db.moderation import adv, mod
from functions.defs import better_time


class eventsPL(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction, error):

        errorEmoji: discord.Emoji = self.bot.get_emoji(1044750438978818049)

        if isinstance(error, commands.CommandOnCooldown):

            cd = round(error.retry_after)

            if cd == 0:
                cd = 1

            await interaction.response.send_message(f'{errorEmoji} || {better_time(cd)}', ephemeral=True)

        # if isinstance(error, NoVote):

        #     await interaction.response.send_message(f"{errorEmoji} || {error}", ephemeral = True)

        if isinstance(error, commands.BotMissingPermissions):
            await interaction.response.send_message(
                f'{errorEmoji} || Eu não tenho permissão de {error.args} para utilizar isso')

        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message(
                f"{errorEmoji} || Você não tem permissão de {error.args} para utilizar isso", ephemeral=True)

        if isinstance(error, commands.MemberNotFound):
            await interaction.response.send_message(f'{errorEmoji} || Não encontrei esse membro')

        if isinstance(error, commands.NotOwner):
            await interaction.response.send_message(f'{errorEmoji} || Você não é meu dono')

        if error:
            print(error)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):

        for i in range(0, guild.text_channels.__len__()):
            try:
                await guild.text_channels[i].send(
                    content="A Re=L não vem com nenhuma limitação de permição nos comandos então eu(O Criador) recomendo você ir nas configurações e ir nessas opções para definir os comandos",
                    files=[
                        discord.File('./prints/image.png'),
                        discord.File('./prints/image2.png'),
                        discord.File('./prints/image3.png')
                    ]
                )
                break
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):

        mod.find_one_and_delete({"_id": guild.id})

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        if member.guild.id != 1003002386706612354:
            return

        await verfyadv(self.bot, member)

        await verfypoints(self.bot, member)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, member: discord.User):

        if guild.id != 1003002386706612354:
            return

        if adv.count_documents({"_id": member.id}) == 1:
            adv.find_one_and_delete({"_id": member.id})

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author == self.bot.user:
            return
        elif message.author.bot:
            return
        elif message.mention_everyone:
            return

        if "ticket-" in message.channel.name:
            with open(f"./tickets/{message.guild.id}_{message.channel.name.removeprefix('ticket-')}.txt", "a",
                      encoding="UTF-8") as f:
                f.write(f"\n{message.author.name}: {message.content}")

    @commands.Cog.listener()
    async def on_ready(self):

        print("Eu entrei como {}".format(self.bot.user))


def setup(bot: commands.Bot):
    bot.add_cog(eventsPL(bot))
