import discord
import json
from discord.ext import commands
from discord import Interaction, Locale, app_commands
from main import localizations, connection, KuroID, translate
from commands.settings import CheckUserIsInSettings
from dataBase import *

with open("sparks.json", "r", encoding="utf8") as f:
    sparks_data = json.load(f)

class Spark(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="sparknsfw", description="Send anonymous Sparks")
    async def sparkNSFW(self, interaction: discord.Interaction, user: discord.User):
        #await interaction.response.defer(ephemeral=True)
        userID = str(interaction.user.id)
        targetID = str(user.id)
        targetName = user.name
        Language = interaction.locale

        CheckUserIsInSettings(userID)
        Sparktyp = checkUserSparktypeSetting(connection, interaction.user.id) #für später wichtig im Modal, um abzufragen welche Sparks angezeigt werden sollen
        await interaction.response.send_modal(SparkModal(targetName, Language))




class SparkModal(discord.ui.Modal):
    sparks = discord.ui.Label(
        text = "Test",
        description = "Send anonym Sparks",
        component = discord.ui.Select(
            options=[
                discord.SelectOption(label=key, value=key)
                for key in sparks_data.keys()
            ]
        )
    )

    def __init__(self, targetName: discord.User, locale: Locale):
        super().__init__(title=translate(locale, "modals.spark.title") + f"{targetName}")
        self.targetName = targetName

    async def on_submit(self, interaction: discord.Interaction):
        targetName = self.targetName
        await interaction.response.send_message(f"Spark sent to {targetName}!", ephemeral=True)




# Setup-Funktion für Cog
async def setup(bot):
    await bot.add_cog(Spark(bot))
    print("SparkCommand geladen ✅")