import discord

from utils.loader import configData
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient(configData["mongokey"])
db = cluster["IVM"]
modDono = db["mod"]

def Premium(guild: discord.Guild, tempo: datetime, value: bool):

    modDono.update_one(
        {"_id": guild.id}, {
            "$set": { 
                "premium":{
                    "data": tempo.timestamp(),
                    "enable": value
                }
            }
        },
        upsert=True
    )