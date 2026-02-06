import discord
from discord.ext import tasks, commands
import datetime
from dataBase import addPossibleSparksForAllUsers
from main import connection

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_update.start() # Startet den Loop beim Laden des Cogs

    def cog_unload(self):
        self.daily_update.cancel() # Stoppt den Loop, falls der Cog entladen wird

    @tasks.loop(time=datetime.time(hour=0, minute=0))
    async def daily_update(self):
        addPossibleSparksForAllUsers(connection)

    @daily_update.before_loop
    async def before_daily_update(self):
        await self.bot.wait_until_ready()

# Diese Funktion braucht discord.py, um den Cog zu laden
async def setup(bot):
    await bot.add_cog(Daily(bot))