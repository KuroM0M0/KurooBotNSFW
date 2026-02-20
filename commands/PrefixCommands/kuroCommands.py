import discord
from discord.ext import commands
from config import connection
from functions.dataBase import *
from functions.Methoden import *


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


    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        bot = ctx.bot
        try:
            await bot.reload_extension(f"{extension}")
            await ctx.send(f"✅ Modul `{extension}` wurde neu geladen!")
        except Exception as e:
            await ctx.send(f"❌ Fehler: {e}")


    @commands.command()
    @commands.is_owner()
    async def setStreakPunkte(self, ctx, member: discord.Member, Punkte: int):
        targetID = member.id
        await ctx.send(f"{member} hat nun {Punkte} Streak Punkte!")
        setStreakPoints(connection, targetID, Punkte)


    @commands.command()
    @commands.is_owner()
    async def setVotePunkte(self, ctx, member: discord.Member, Punkte: int):
        targetID = member.id
        await ctx.send(f"{member} hat nun {Punkte} Vote Punkte!")
        setVotePoints(connection, targetID, Punkte)


async def setup(bot):
    await bot.add_cog(KuroCommands(bot))
    print("KuroCommands geladen ✅")