from discord.ext import commands
from config import connection
from dataBase import *
from Methoden import *

class AdminCommands(commands.Cog):
    @commands.command(name="setNSFWChannel")
    @commands.has_permissions(administrator=True)
    async def setNSFWChannel(self, ctx):
        channel = ctx.channel
        serverID = ctx.guild.id
        CheckServerExists(serverID)
        await ctx.send(f"{channel} ist nun der Spark Channel!")
        setChannelSparkID(connection, serverID, channel.id)

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
    print("AdminCommands geladen ✅")