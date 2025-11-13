import discord
from discord.ext import commands
from dataBase import *
from main import connection


class Settings(commands.Cog):
    @commands.command(name="settings")
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        embed = discord.Embed(title="Einstellungen", color=0x005b96)
        embed.add_field(
            name="🔒 Anonymität Auswahlmöglichkeiten",
            value=f">>> `Hug/Pat` → {getServerAnonymHug(connection, ctx.guild.id)}\n"
                  f"`Sparks` → {getServerAnonymSpark(connection, ctx.guild.id)}",
            inline=False
        )
        await ctx.send(embed=embed)