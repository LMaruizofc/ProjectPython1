from db.economy import mercado
from discord.ext import commands


async def on_frutos(selfBot: commands.Bot):
    return [

        {
            "name": "Tilapia",
            "compra": mercado.find_one({"_id": "mercado"})["tilapia"]["compra"],
            "venda": mercado.find_one({"_id": "mercado"})["tilapia"]["venda"]
        },

        {
            "name": "Corvina",
            "compra": mercado.find_one({"_id": "mercado"})["corvina"]["compra"],
            "venda": mercado.find_one({"_id": "mercado"})["corvina"]["venda"]
        },

        {
            "name": "Camarão",
            "compra": mercado.find_one({"_id": "mercado"})["camarão"]["compra"],
            "venda": mercado.find_one({"_id": "mercado"})["camarão"]["venda"]
        },

        {
            "name": "Lula",
            "compra": mercado.find_one({"_id": "mercado"})["lula"]["compra"],
            "venda": mercado.find_one({"_id": "mercado"})["lula"]["venda"]
        },

        {
            "name": "Ostra",
            "compra": mercado.find_one({"_id": "mercado"})["ostra"]["compra"],
            "venda": mercado.find_one({"_id": "mercado"})["ostra"]["venda"]
        },

        {
            "name": "Lagosta",
            "compra": mercado.find_one({"_id": "mercado"})["lagosta"]["compra"],
            "venda": mercado.find_one({"_id": "mercado"})["lagosta"]["venda"]
        },

        {
            "name": "Caranguejo",
            "compra": mercado.find_one({"_id": "mercado"})["caranguejo"]["compra"],
            "venda": mercado.find_one({"_id": "mercado"})["caranguejo"]["venda"]
        },

        {
            "name": "Peixe",
            "compra": mercado.find_one({"_id": "mercado"})["peixe"]["compra"],
            "venda": mercado.find_one({"_id": "mercado"})["peixe"]["venda"]
        }

    ]
