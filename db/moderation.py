import discord

from utils.loader import configData
from pymongo import MongoClient
from tinydb import TinyDB

cluster = MongoClient(configData["mongokey"])

db_temp_ticket = TinyDB('./db/ticket.json')

db = cluster["IVM"]
adv = db["adv"]
mod = db["mod"]
ausen = db["ausente"]

async def adcadvdb(membro: discord.Member, qnt, motivo):
    adv.update_one({"_id": membro.id}, {"$set": {f"Adv{qnt}": motivo}}, upsert=True)


async def rmvadvdb(membro: discord.Member, qnt, motivo):
    adv.update_one({"_id": membro.id}, {"$set": {f"Adv{qnt}": motivo}}, upsert=True)


async def ausendb(membro: discord.Member, motivo, data):
    ausen.update_one({"_id": membro.id},
                     {"$set": {f"Nome": membro.name, f"Motivo": motivo, f"Data": data, "Ausente?": True}}, upsert=True)

    if ausen.find_one({"_id": "validador"})["valor"] == 0:
        ausen.update_one({"_id": "validador"}, {"$set": {f"valor": 1}}, upsert=True)

async def desausendb(membro: discord.Member):
    ausen.update_one({"_id": membro.id},
                     {"$set": {f"Nome": membro.name, f"Motivo": "None", f"Data": "None", "Ausente?": False}},
                     upsert=True)

    if ausen.count_documents({"Ausente?": True}) == 0:
        ausen.update_one({"_id": "validador"}, {"$set": {f"valor": 0}}, upsert=True)


def adcLog(guild: discord.Guild, name: str, canal: discord.TextChannel):
    if mod.find_one({"_id": guild.id}) == 0:
        mod.update_one({"_id": guild.id}, {"$set": {f"name": guild.name}}, upsert=True)

    mod.update_one({"_id": guild.id}, {"$set": {f"logs.{name}": [canal.id]}}, upsert=True)


def adccargoticket(guild: discord.Guild, name: str, cargo: discord.Role):
    if mod.find_one({"_id": guild.id}) == 0:
        mod.update_one({"_id": guild.id}, {"$set": {f"name": guild.name}}, upsert=True)

    mod.update_one({"_id": guild.id}, {"$set": {f"roleticket.{name}": [cargo.id]}}, upsert=True)
