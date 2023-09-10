import discord

from classes.Ticket import embedCreator
from discord import InvalidArgument, option, slash_command
from discord.ext import commands
from db.moderation import adccargoticket, db_temp_ticket
from tinydb import table

class ticketSetup(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(guild_only=True, name="setup_ticket", description="Começa a configuração do ticket")
    @option(name='name_webhook', description="Nome da webhook para enviar a mensagem")
    @option(name='image_webhook', description="imagem da webhook para enviar a mensagem")
    @option(name='channel', description="Chat para enviar a mensagem")
    @option(name="category", description="Categoria para abrir os tickets")
    async def setupticket(self,
                          interaction: discord.Interaction,
                          name_webhook: str = None,
                          image_webhook: discord.Attachment = None,
                          channel: discord.TextChannel = None
                          ):
        
        await interaction.response.send_modal(embedCreator())

        if channel is None:
            channel = interaction.channel
        
        web = None

        if name_webhook is not None:

            if image_webhook is not None and "image/" not in image_webhook.content_type:
                return await interaction.followup.send(
                    "Arquivo não suportado não suportado, somente arquivos de imagem", ephemeral=True)

            if image_webhook is not None:
                try:
                    web = await channel.create_webhook(name=name_webhook, avatar=await image_webhook.read())
                except InvalidArgument as error:
                    return await interaction.followup.send(
                        "Arquivo de imagem não suportado, ERROR: {}".format(error),
                        ephemeral=True)
                web = web.id
            else:
                web = await channel.create_webhook(name=name_webhook)

                web = web.id

        try:
            insert = {
                "_id": interaction.guild.id,
                "channel_id": channel.id,
                "webhook_id": web
                }
            db_temp_ticket.insert(table.Document(insert, doc_id=interaction.guild.id))
        except Exception as e:
            if db_temp_ticket.contains(doc_id=interaction.guild.id):
                doc = db_temp_ticket.get(doc_id=interaction.guild.id)
                doc["channel_id"] = channel.id
                db_temp_ticket.update(doc, doc_ids=[interaction.guild.id])
                doc["webhook_id"] = web
                db_temp_ticket.update(doc, doc_ids=[interaction.guild.id])

def setup(bot: commands.Bot):
    bot.add_cog(ticketSetup(bot))
