import os
import random
import discord
import NewFunctionsPYC

from discord.ext import commands
from db.economy import update_bank, economy, update_inv
from discord import SlashCommandGroup, option, slash_command
from economy.crafts import crafts
from economy.frutosdomar import on_frutos
from economy.recursos import on_recursos
from economy.utilitarios import on_utilitarios
from classes.economy.selectMenus import selectCraft, MercadoVer


class economia(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    economy = SlashCommandGroup("economy")

    @economy.command(name="rolar",
                     description="Voce pode ganhar de 0 a 2000 ReCoins"
                     )
    @commands.cooldown(5, 7200, commands.BucketType.user)
    async def rolar(self,
                    interaction: discord.Interaction
                    ):

        rand: int = random.randint(0, 10)

        match rand:

            case 10:

                update_bank(interaction.user, + 2000)

                await interaction.response.send_message(f"Parabens {interaction.user.name}, você ganhou 2000 ReCoins")

            case 8 | 9:

                r: int = random.randint(100, 900)

                update_bank(interaction.user, r)

                await interaction.response.send_message(f"{interaction.user.name}, você ganhou {r} ReCoins")

            case 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7:

                r: int = random.randint(1, 100)

                update_bank(interaction.user, + r)

                await interaction.response.send_message(f"{interaction.user.name}, você ganhou {r} ReCoins")

    @economy.command(name="carteira", description="Mostra a quantidade monetaria")
    @option(name="membro", description="Escolha um membro")
    async def balance(self,
                      interaction: discord.Interaction,
                      membro: discord.Member = None
                      ):

        if membro is None:
            membro = interaction.user

        try:
            economy.find_one({"_id": membro.id})["REcoins"]
        except Exception:
            update_bank(membro, 0)

        bal = economy.find_one({"_id": membro.id})

        em = discord.Embed(title=f"{membro.name} REcoins", color=discord.Color.red())
        em.add_field(name="REcoins", value=f"{bal['REcoins']:,}")

        await interaction.response.send_message(embed=em)

    @economy.command(name="transferir", description="Transfere REcoins para outra pessoa")
    @option(name="membro", description="Escolha um membro")
    @option(name="recoins", description="Escolha a quantidade")
    async def Transferir(self,
                         interaction: discord.Interaction,
                         membro: discord.Member,
                         recoins: int
                         ):

        try:
            economy.find_one({"_id": interaction.user.id})
        except Exception:
            update_bank(interaction.user, 0)

        bal = economy.find_one({"_id": interaction.user.id})

        if recoins > bal["REcoins"]:
            return await interaction.response.send_message(f"Você não tem dinheiro suficiente", ephemeral=True)
        elif recoins == 0:
            return await interaction.response.send_message("A quantia tem que ser maior que zero", ephemeral=True)
        elif recoins < 0:
            return await interaction.response.send_message(f"A quantia deve ser positiva", ephemeral=True)

        update_bank(interaction.user, - recoins)
        update_bank(membro, + recoins)
        await interaction.response.send_message(f"Voce transferiu {recoins} REcoins para {membro.mention}")

    @economy.command(name="loteria", description="Aposta na loteria")
    @option(name="recoins", description="Escolha a quantidade de REcoins")
    async def loteria(self,
                      interaction: discord.Interaction,
                      recoins: int
                      ):

        try:
            economy.find_one({"_id": interaction.user.id})
        except Exception:
            update_bank(interaction.user, 0)

        bal = economy.find_one({"_id": interaction.user.id})

        if recoins > bal["REcoins"]:
            return await interaction.response.send_message(f"Você não tem dinheiro suficiente", ephemeral=True)
        elif recoins <= 0:
            return await interaction.response.send_message("A quantia deve ser maior que 0", ephemeral=True)

        final = []
        for i in range(3):
            final.append(random.choice([":pineapple:", ":grapes:", ":kiwi:", ":melon:"]))
        await interaction.response.defer()
        await interaction.followup.send(f"| {str(final[0])} | {str(final[1])} | {str(final[2])} |")
        if final[0] == final[1] and final[2] == final[0]:
            update_bank(interaction.user, 4 * recoins)
            await interaction.followup.send(f"Você ganhou {4 * recoins} REcoins!!")
        else:
            update_bank(interaction.user, - recoins)
            await interaction.followup.send(f"Você perdeu {recoins} REcoins")

    @economy.command(name="cara_ou_coroa_apostado")
    @option(name="recoins", description="Escolha a quantidade de REcoins")
    @option(name="escolha", description="Escolha cara ou coroa", choices=["cara", "coroa"])
    async def Caraoucoroaap(self,
                            interaction: discord.Interaction,
                            recoins: int,
                            escolha: str
                            ):

        try:
            economy.find_one({"_id": interaction.user.id})
        except Exception:
            update_bank(interaction.user, 0)

        bal = economy.find_one({"_id": interaction.user.id})

        if recoins > bal["REcoins"]:
            return await interaction.response.send_message(f"Você não tem dinheiro suficiente para apostar")
        elif recoins < 0:
            return await interaction.response.send_message(f"A quantia deve ser positiva")
        
        choice = ["cara", "coroa"]
        if escolha == "cara":
            choice.append("coroa")
        if escolha == "coroa":
            choice.append("cara")

        random1 = random.choice(choice)

        if random1 == escolha:
            await interaction.response.send_message(f"Caiu {escolha}\nParabens, você ganhou {recoins * 2} REcoins")
            return update_bank(interaction.user, + recoins * 2)
        await interaction.response.send_message(f"Caiu {random1}\nSad, você perdeu {recoins} REcoins")
        update_bank(interaction.user, - recoins)

    @economy.command(name="recoins_top", description="Envia os 5 mais ricos")
    async def REcoinstop(self,
                         interaction: discord.Interaction
                         ):
        i = 1
        embed = discord.Embed(title=f"***Top 5 mais ricos***")
        for x in economy.find().sort("REcoins", -1):
            embed.add_field(name=f"{i}: {x['Nome']}", value=f"{x['REcoins'][:,]}", inline=False)
            if i == 5:
                break
            else:
                i += 1

        embed.set_footer(text=f"{interaction.guild}", icon_url=f"{interaction.guild.icon.url}")
        await interaction.response.send_message(embed=embed)

    @economy.command(guild_only=True, name="inventario", description="Mostra seu inventario")
    async def inv(self,
                  interaction: discord.Interaction
                  ):

        await interaction.response.defer(ephemeral=True)

        try:
            os.remove("./tempinv.txt")
        except:
            pass

        e = NewFunctionsPYC.EmbedBuilder()
        e.set_title(f"Inventario de {interaction.user.name}")

        for i in await on_frutos(self.bot):
            try:
                iv = economy.find_one({"_id": interaction.user.id})["inventario"][i["name"].lower()]
                with open("tempinv.txt", "a", encoding="UTF-8") as f:
                    f.write(f"\n{i['name']}: {iv}")
            except Exception as error:
                pass

        for i in crafts:
            try:
                iv = economy.find_one({"_id": interaction.user.id})["inventario"][i["name"].lower()]
                with open("tempinv.txt", "a", encoding="UTF-8") as f:
                    f.write(f"\n{i['name']}: {iv}")
            except Exception as error:
                pass

        for i in await on_recursos(self.bot):
            try:
                iv = economy.find_one({"_id": interaction.user.id})["inventario"][i["name"].lower()]
                with open("tempinv.txt", "a", encoding="UTF-8") as f:
                    f.write(f"\n{i['name']}: {iv}")
            except Exception as error:
                pass

        for i in await on_utilitarios(self.bot):
            try:
                iv = economy.find_one({"_id": interaction.user.id})["inventario"][i["name"].lower()]
                with open("tempinv.txt", "a", encoding="UTF-8") as f:
                    f.write(f"\n{i['name']}: {iv}")
            except Exception as error:
                pass

        try:
            with open("tempinv.txt", "r", encoding="UTF-8") as f:
                invs = f.read()
            e.set_description(invs)
            await interaction.followup.send(embed=e.build(), ephemeral=True)
        except:
            await interaction.followup.send("Você não possue inventario", ephemeral=True)

    @economy.command(guild_only=True, name="mercado", description="Mostra o mercado")
    @option(name="opção", description="Escolha a opção de comprar ou vender", choices=["comprar", "vender", "ver"])
    @option(name="item", description="Diga o item a comprar")
    @option(name="quantidade", description="Quantos itens")
    async def Shop(self,
                   interaction: discord.Interaction,
                   opção: str = None,
                   item: str = None,
                   quantidade: int = None
                   ):

        global price
        embed = discord.Embed(title="Mercado", description="Escolha a categoria")

        try:
            economy.find_one({"_id": interaction.user.id})
        except Exception:
            update_bank(interaction.user, 0)

        bal = economy.find_one({"_id": interaction.user.id})

        match opção:

            case None | "ver":
                await interaction.response.send_message(embed=embed, view=MercadoVer(self.bot, interaction.user))

            case "comprar":

                if item is None:
                    return await interaction.response.send_message("Você precisa dizer o item a comprar")

                if quantidade is None:
                    quantidade = 1

                item_name = item.capitalize()

                for it in await on_recursos(self.bot):
                    if it["name"] == item_name:
                        price = it["compra"]
                        break

                for it in await on_frutos(self.bot):
                    if it["name"] == item_name:
                        price = it["compra"]
                        break

                for it in await on_utilitarios(self.bot):
                    if it["name"] == item_name:
                        price = it["compra"]
                        break

                if price is None or price == "Null" or price == "None" or price == 0:
                    return await interaction.response.send_message("Esse item não possue valor de compra",
                                                                   ephemeral=True)

                cost = price * quantidade

                if bal["REcoins"] < cost:
                    return await interaction.response.send_message("Você não tem ReCoins suficientes")

                q = "unidade"
                if quantidade > 1:
                    q = "unidades"

                await interaction.response.send_message(f"Você comprou {quantidade} {q} de {item} por {cost} ReCoins")
                update_bank(interaction.user, - cost)
                update_inv(interaction.user, item_name, quantidade)

            case "vender":

                if item is None:
                    return await interaction.response.send_message("Você precisa dizer o item a vender", ephemeral=True)

                if quantidade is None:
                    return await interaction.response.send_message("Você precisa dizer a quantidade", ephemeral=True)

                item_name = item.capitalize()

                for it in await on_recursos(self.bot):
                    if it["name"] == item_name:
                        price = it["venda"]
                        break

                for it in await on_frutos(self.bot):
                    if it["name"] == item_name:
                        price = it["venda"]
                        break

                for it in await on_utilitarios(self.bot):
                    if it["name"] == item_name:
                        price = it["venda"]
                        break

                if price is None or price == "Null" or price == "None" or price == 0:
                    return await interaction.response.send_message("Esse item não possue valor de venda",
                                                                   ephemeral=True)

                cost = price * quantidade

                if bal["inventario"][item.lower()] < 1:
                    await interaction.response.send_message("Você não tem esse item para vender")
                else:

                    q = "unidade"
                    if quantidade > 1:
                        q = "unidades"

                    await interaction.response.send_message(
                        f"Você vendeu {quantidade} {q} de {item} por {cost} REcoins")
                    update_bank(interaction.user, + cost)
                    update_inv(interaction.user, item_name, - quantidade)

    @economy.command(guild_only=True, name="craft", description="Craft dos itens")
    @option(name="opt", description="Opção do que fazer", choices=["Ver Crafts", "Craftar"])
    async def craft(self,
                    interaction: discord.Interaction,
                    opt: str = "Ver Crafts"
                    ):

        e = NewFunctionsPYC.EmbedBuilder()

        match opt:

            case "Ver Crafts":

                e.set_title("Ver Crafts")

                for i in crafts:
                    name = i["name"]
                    compra = i["R1"]
                    venda = i["R2"]
                    e.add_field(name=name, value=f" {compra}\n {venda}")

                await interaction.response.send_message(embed=e.build())

            case "Craftar":

                await interaction.response.send_message("Qual item você vai craftar",
                                                        view=selectCraft(user=interaction.user.id))

    @economy.command(name='minerar', description='Minera, tem chance de vir minerios')
    @option(name="picareta", description="Seleciona a picareta",
            choices=["Picareta de ferro", "Picareta de ouro", "Picareta de diamante"])
    @commands.cooldown(20, 1800, commands.BucketType.user)
    async def minerar(self, interaction: discord.Interaction, picareta: str = "picareta de ferro"):

        try:
            economy.find_one({"_id": interaction.user.id})["inventario"][picareta.lower()]
        except Exception:
            update_inv(interaction.user, picareta.lower(), 0)

        if economy.find_one({"_id": interaction.user.id})["inventario"][picareta.lower()] < 1:
            return await interaction.response.send_message(f"Você não tem {picareta.lower()}", ephemeral=True)

        r1 = random.choice(
            [
                "none",
                "none1",
                "none2",
                "none3",
                "none4",
                "none5",
                "none",
                "none1",
                "none2",
                "none3",
                "none4",
                "none5",
                "dima",
                "ouro",
                "ferro",
                "ferro",
                "ferro"
            ]
        )
        r2 = random.randint(1, 5)
        r3 = random.randint(100, 200)
        r4 = random.randint(1, 10)

        q = ""
        if r2 > 1:
            q = "s"

        match picareta.lower():

            case "picareta de ferro":

                if r4 == 3 or r4 == 5:
                    await interaction.response.send_message("Sad, sua picareta de ferro quebrou")
                    return update_inv(interaction.user, "picareta de ferro", - 1)

            case "picareta de ouro":

                if r4 == 7:
                    await interaction.response.send_message("Sad, sua picareta de ouro quebrou")
                    return update_inv(interaction.user, "picareta de ouro", - 1)

        match r1:

            case "ouro":

                await interaction.response.send_message(f"Parabens, você achou 1 ouro")
                update_inv(interaction.user, "ouro", 1)

            case "dima":

                await interaction.response.send_message(f"Parabens, você achou 1 diamante")
                update_inv(interaction.user, "diamante", 1)

            case "ferro":

                await interaction.response.send_message(f"Parabens, você achou {r2} ferro{q}")
                update_inv(interaction.user, "ferro", r2)

            case "none" | "none1" | "none2" | "none3" | "none4" | "none5":

                await interaction.response.send_message(f"Você não achou nada mas ganhou {r3} edinhos")
                update_bank(interaction.user, r3)


def setup(bot: commands.Bot):
    bot.add_cog(economia(bot))
