import discord

from utils.loader import configData
from pymongo import MongoClient

cluster = MongoClient(configData["mongokey"])
db = cluster["IVM"]
economy = db["economy"]
mercado = db["mercado"]

def update_bank(membro: discord.User, REcoins: int):
    if membro is not None:

        if economy.count_documents({"_id": membro.id}) == 0:
            economy.insert_one({"_id": membro.id, "Nome": membro.name})

        economy.update_one(
            {"_id": membro.id},
            {"$inc": {
                "REcoins": REcoins
            }
            },
            upsert=True
        )


def update_inv(member, item: str, qnt: int):
    if member is not None:
        economy.update_one(
            {"_id": member.id},
            {"$inc": {
                f"inventario.{item.lower()}": qnt
            }
            },
            upsert=True
        )


def market_update(item: str, qual: str, valor: int):
    if item is not None:
        mercado.update_one(
            {"_id": "mercado"},
            {"$set": {
                f"{item.lower()}.{qual.lower()}": valor
            }
            },
            upsert=True
        )
