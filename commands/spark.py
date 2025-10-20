import discord
import json
from discord.ext import commands
from discord import Interaction, Locale, app_commands
from main import localizations, connection, KuroID, translate
from commands.settings import CheckUserIsInSettings
from dataBase import *

with open("sparks.json", "r", encoding="utf8") as f:
    sparksData = json.load(f)
    softSparks = {key: value for key, value in sparksData.items() if value.get("Typ") == "Soft"}
    spicySparks = {key: value for key, value in sparksData.items() if value.get("Typ") == "Spicy"}

class Spark(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="sparknsfw", description="Send anonymous Sparks") #kann nicht dynamisch gesetzt werden
    async def sparkNSFW(self, interaction: discord.Interaction, user: discord.User):
        userID = str(interaction.user.id)
        targetID = str(user.id)
        targetName = user.name
        Language = interaction.locale

        CheckUserIsInSettings(userID)
        CheckUserIsInSettings(targetID)
        Sparktyp = getUserSparktypeSetting(connection, userID) #für später wichtig im Modal, um abzufragen welche Sparks angezeigt werden sollen
        await interaction.response.send_modal(SparkModal(targetName, Language, Sparktyp))




class SparkModal(discord.ui.Modal):
    def __init__(self, targetName: discord.User, locale: Locale, Sparktyp: str):
        super().__init__(title=translate(locale, "modal.spark.title", targetName=targetName))
        self.targetName = targetName
        self.Sparktyp = Sparktyp

        
        if Sparktyp == "Explicit":
            sparks = discord.ui.Label(
                text = translate(locale, "modal.spark.sparkSelect.text"),
                description = translate(locale, "modal.spark.sparkSelect.description"),
                component = discord.ui.Select(
                    options=[
                        discord.SelectOption(label=key, value=key)
                        for key in sparksData.keys()
                    ]
                )
            )
            self.add_item(sparks)
        elif Sparktyp == "Spicy":
            sparks = discord.ui.Label(
                text = translate(locale, "modal.spark.sparkSelect.text"),
                description = translate(locale, "modal.spark.sparkSelect.description"),
                component = discord.ui.Select(
                    options=[
                        discord.SelectOption(label=key, value=key)
                        for key in spicySparks.keys()
                    ]
                )
            )
            self.add_item(sparks)
        else:
            sparks = discord.ui.Label(
                text = translate(locale, "modal.spark.sparkSelect.text"),
                description = translate(locale, "modal.spark.sparkSelect.description"),
                component = discord.ui.Select(
                    options=[
                        discord.SelectOption(label=key, value=key)
                        for key in softSparks.keys()
                    ]
                )
            )
            self.add_item(sparks)


    async def on_submit(self, interaction: discord.Interaction):
        targetName = self.targetName
        await interaction.response.send_message(translate(interaction.locale, "modal.spark.onSubmit", targetName=targetName), ephemeral=True)




# Setup-Funktion für Cog
async def setup(bot):
    await bot.add_cog(Spark(bot))
    print("SparkCommand geladen ✅")