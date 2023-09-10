from db.economy import mercado
from discord.ext import commands


async def on_utilitarios(selfBot: commands.Bot):
    return [

        {
            "name": "Arma",
            "compra": mercado.find_one({"_id": "mercado"})["arma"]["compra"],
            "venda": mercado.find_one({"_id": "mercado"})["arma"]["venda"]
        },

        {
            "name": "Vara de pesca",
            "compra": mercado.find_one({"_id": "mercado"})["vara de pesca"]["compra"],
            "venda": mercado.find_one({"_id": "mercado"})["vara de pesca"]["venda"]
        }
    ]
