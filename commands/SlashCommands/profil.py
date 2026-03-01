import discord
from discord.ext import commands
from discord import app_commands
from functions.dataBase import *
from config import connection
from functions.emotes import StreakPoint

class Profil(commands.Cog):
    @app_commands.command(name="profil", description="Zeige dein Profil an")
    async def profil(self, interaction: discord.Interaction, user: discord.User = None):
        if user is None:
            user = interaction.user
        userID = user.id
        privacy = getProfilPrivateSetting(connection, userID)
        await interaction.response.defer(ephemeral=privacy)

        userName = user.display_name
        streak = getStreak(connection, userID)
        streakPoints = getStreakPoints(connection, userID)
        sparkCount = getSparkCount(connection, userID)
        sparkReceived = getSparkCountSelf(connection, userID)

        embed = discord.Embed(
            title=f"Profil von {userName}",
            description=f"\u200b**Sparks** \n Verschickt: **{sparkCount}**\n Erhalten: **{sparkReceived}**",
            color=0x005b96
        )
        #embed.add_field(name="\u200b", value="\u200b", inline=True) #leerzeile
        embed.add_field(name="Streak: ", value=f"**{streak}** Tage", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="StreakPunkte: ", value=f"**{streakPoints}** {StreakPoint}", inline=True)
        #embed.add_field(name="\u200b", value="\u200b", inline=False) #leerzeile
        #embed.add_field(name="gesparkt", value=sparkCount, inline=True)
        #embed.add_field(name="gesparkt von dir", value=sparkReceived, inline=True)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text="3 Tage Streak = 1 Punkt", icon_url="https://discord.com/channels/475295112453423125/1354078227903283251/1477768167379042324")

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Profil(bot))
    print("Profil geladen ✅")