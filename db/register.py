import discord

from utils.loader import configData
from pymongo import MongoClient

# -----------------------------------------------------------------------------------------------------#
cluster = MongoClient(configData['mongokey'])

db = cluster['IVM']
regCargo = db["configReg"]
reg = db['registrador']


# -----------------------------------------------------------------------------------------------------#
def addpregistro(membro: discord.Member, pontos: int):
    reg.update_one({"_id": membro.id}, {"$inc": {"registros": pontos}}, upsert=True)


def addCargoReg(guild: discord.Guild, cargo: discord.Role, categoria: str, name: str):
    regCargo.update_one(
        {"_id": guild.id},
        {"$set": {
            f"{categoria}.{name}": {
                "name": name,
                "cargoid": cargo.id
            }
        }
        },
        upsert=True
    )


def rmvCargoReg(guild: discord.Guild, categoria: str, name: str):
    regCargo.update_one(
        {"_id": guild.id},
        {"$unset": {
            f"{categoria}.{name}": ["name", "cargoid"]
        }
        },
        upsert=True
    )
