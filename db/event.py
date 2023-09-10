import discord

from utils.loader import  configData
from pymongo import MongoClient
from pytz import timezone
from datetime import datetime
#-----------------------------------------------------------------------------------------------------#
cluster = MongoClient(configData['mongokey'])

db = cluster['IVM']

points = db['points']
#-----------------------------------------------------------------------------------------------------#
async def addp(membro: discord.Member, pontos):

    points.update_one({"_id": membro.guild.id}, {"$inc": {f"{membro.id}.pontos": pontos}}, upsert = True)

async def addp2(membro: discord.Member, ctx, up):

    data_e_hora_atuais = datetime.now()

    fuso_horario = timezone('America/Sao_Paulo')

    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    
    dt = data_e_hora_sao_paulo.strftime('%d/%m/%Y')

    points.update_one({"_id": membro.guild.id}, {"$set": {f"{membro.id}.ponto{up}": f"adicionado {dt} por {ctx.name}"}}, upsert = True)
#-----------------------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------------------#
async def rmvp(membro: discord.Member, pontos):

    points.update_one({"_id": membro.guild.id}, {"$inc": {f"{membro.id}.pontos": pontos}}, upsert = True)

async def rmvp2(membro: discord.Member, up,rs):

    points.update_one({"_id": membro.guild.id}, {"$unset":{f"{membro.id}.ponto{up}": rs}}, upsert = True)
#-----------------------------------------------------------------------------------------------------#