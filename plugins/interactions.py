import discord
import custom
import pytz
import datetime

from discord.ext import commands
from custom import categoriaRegistro


class interactions(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):

        match interaction.to_dict()["type"]:
            case 1:
                return
            case 2:
                return
            case 3:
                match interaction.to_dict()["data"]["component_type"]:
                    case 1:
                        return
                    case 2:

                        if "catego" in interaction.custom_id:
                            await categoriaRegistro(self.bot, interaction)

                        elif "regButton" in interaction.custom_id:
                            await getattr(custom, "regButton")(self.bot, interaction,
                                                               str(interaction.custom_id).removeprefix("regButton-"))

                        elif "abrirTicket" in interaction.custom_id:
                            await getattr(custom, f"abrirTicket")(self.bot, interaction)

                        else:
                            try:
                                await getattr(custom, f"{interaction.custom_id}")(self.bot, interaction)
                            except Exception as error:
                                print(error)
                    case 3:
                        try:
                            await getattr(custom, f"{interaction.custom_id}")(self.bot, interaction)
                        except:
                            pass
                    case 4:
                        return
                    case 5:
                        return
            case 4:
                return
            case 5:
                return


def setup(bot: commands.Bot):
    bot.add_cog(interactions(bot))


# {
#     'id': 1081985965427531816,
#     'application_id': 1064938979406921738,
#     'type': 3,
#     'token': 'aW50ZXJhY3Rpb246MTA4MTk4NTk2NTQyNzUzMTgxNjoyRWw2aWhFWmd0WTVSUnBCT2s1M0FCOFJoRnpNcHFrblMzYWtJWmMxMW03cjJQT25CalpDQXBrd09DTEFGUWZyUXNTekNIb2xTeG1SakJJWnhoelB1TlRuTVFZOGZDSWYxdnVRb3RweUN5R1Y5RkVqakpLeFBlOHM5bE1YbWhLSg',
#     'version': 1,
#     'data': {
#         'values': ['ergrgerg'],
#         'custom_id': 'ticket-select',
#         'component_type': 3
#     },
#     'guild_id': 929181582571503658,
#     'channel_id': 1044742020830339082,
#     'locale': 'pt-BR',
#     'guild_locale': 'en-US',
#     'message': {
#         'type': 0,
#         'tts': False,
#         'timestamp': '2023-03-05T16:56:36.044000+00:00',
#         'pinned': False,
#         'mentions': [],
#         'mention_roles': [],
#         'mention_everyone': False,
#         'id': '1081983614767616052',
#         'flags': 0,
#         'embeds': [
#             {
#                 'type': 'rich',
#                 'title': 'egrergeqrgger',
#                 'description': 'ergergergfg'
#             }
#         ],
#         'edited_timestamp': None,
#         'content': '',
#         'components': [
#             {
#                 'type': 1,
#                 'components': [
#                     {
#                         'type': 3,
#                         'placeholder': 'Abrir Ticket',
#                         'options': [
#                             {
#                                 'value': 'ergrgerg',
#                                 'label': 'ergrgerg',
#                             },
#                             {
#                                 'value': 'ergergerg',
#                                 'label': 'ergergerg',
#                             },
#                             {
#                                 'value': 'arrgaga',
#                                 'label': 'arrgaga',
#                             }
#                         ],
#                         'min_values': 1,
#                         'max_values': 1,
#                         'custom_id': 'ticket-select'
#                     }
#                 ]
#             }
#         ],
#         'channel_id': '1044742020830339082',
#         'author': {
#             'username': 'RE=L Canary',
#             'public_flags': 0,
#             'id': '1064938979406921738',
#             'display_name': None,
#             'discriminator': '5115',
#             'bot': True,
#             'avatar_decoration': None,
#             'avatar': 'c71f00920235905eda75729dbd4299ab'
#         },
#         'attachments': []
#     }
# }
