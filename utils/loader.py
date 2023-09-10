import os
import discord
from discord import Bot as BotBase

class client(BotBase):

    def __init__(self):
        super().__init__(
            description="Um simples bot com funções para te ajudar no seu server",
            help_command=None,
            intents=discord.Intents(
                auto_moderation_configuration=False,
                auto_moderation_execution=False,
                bans=True,
                dm_messages=False,
                dm_reactions=False,
                dm_typing=False,
                emojis=True,
                emojis_and_stickers=True,
                guild_messages=True,
                guild_reactions=True,
                guild_typing=False,
                guilds=True,
                integrations=False,
                invites=False,
                members=True,
                message_content=True,
                messages=True,
                presences=False,
                reactions=True,
                scheduled_events=False,
                typing=False,
                voice_states=True,
                webhooks=True,
            ),
            owner_ids=[485801281621852175],
        )

    def __load_cogs__(self):

        pastaname = 'commands'
        for filename in os.listdir(f'./{pastaname}'):
            for commands in os.listdir(f'./{pastaname}/{filename}'):
                if commands.endswith('.py') and not commands.startswith('__'):
                    self.load_extension(f'{pastaname}.{filename}.{commands[:-3]}')

        for plugins in os.listdir("./plugins"):
            if plugins.endswith(".py") and not plugins.startswith("__"):
                self.load_extension("plugins.{}".format(plugins[:-3]))
    
    def __run__(self):
        self.__load_cogs__()
        self.run(configData["token"])
