import discord
from discord.ext import commands
from main import connection
from dataBase import *
from Methoden import *


class KuroCommands(commands.Cog):
    @commands.command(name="insertItem")
    @commands.is_owner()
    async def insertItem(self, ctx, Name, Beschreibung, Preis, PreisTyp, ItemURL):
        insertItem(connection, Name, Beschreibung, Preis, PreisTyp, ItemURL)
        await ctx.send(f"{Name} wurde hinzugefügt!")


    @commands.command(name="PremiumAktivieren")
    @commands.is_owner()
    async def PremiumAktivieren(self, ctx, member: discord.Member, time: int):
        targetID = member.id
        UserExists(targetID)
        await ctx.send(f"{member} hat nun Premium!")
        setPremium(connection, targetID, time)


    @commands.command(name="PremiumDeaktivieren")
    @commands.is_owner()
    async def PremiumDeaktivieren(self, ctx, member: discord.Member):
        targetID = member.id
        await ctx.send(f"{member} hat nun kein Premium mehr!")
        resetPremium(connection, targetID)


async def setup(bot):
    await bot.add_cog(KuroCommands(bot))
    print("KuroCommands geladen ✅")