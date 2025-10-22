import discord
import json
import random
from discord.ext import commands
from discord import Interaction, Locale, app_commands
from main import connection, translate
from commands.settings import CheckUserIsInSettings
from dataBase import *
from Methoden import *

with open("sparks.json", "r", encoding="utf8") as f:
    sparksData = json.load(f)
    softSparks = {key: value for key, value in sparksData.items() if value.get("Typ") == "Soft"}
    spicySparks = softSparks | {key: value for key, value in sparksData.items() if value.get("Typ") == "Spicy"} # | wird verwendet um dicts zu kombinieren

class Spark(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="sparknsfw", description="Send anonymous Sparks") #kann nicht dynamisch gesetzt werden
    async def sparkNSFW(self, interaction: discord.Interaction, user: discord.User):
        userID = str(interaction.user.id)
        targetID = str(user.id)
        target = user
        channelID = interaction.channel.id
        NSFWChannel = getChannelSparkID(connection, interaction.guild_id)

        if str(channelID) != NSFWChannel:
            await interaction.response.send_message(translate(interaction.locale, "command.sparknsfw.error"), ephemeral=True)
            return

        CheckUserIsInSettings(userID)
        CheckUserIsInSettings(targetID)
        CheckServerExists(interaction.guild_id)

        Sparktyp = getSparkIntensity(connection, targetID) #für später wichtig im Modal, um abzufragen welche Sparks angezeigt werden sollen
        await interaction.response.send_modal(SparkModal(target, interaction.locale, Sparktyp))




class SparkModal(discord.ui.Modal):
    def __init__(self, target: discord.User, locale: Locale, Sparktyp: str):
        super().__init__(title=translate(locale, "modal.spark.title", targetName=target.name))
        self.target = target
        self.targetName = target.name
        self.Sparktyp = Sparktyp

        
        if Sparktyp == "Explicit":
            self.select = discord.ui.Select(
                options=[
                        discord.SelectOption(label=key, value=key)
                        for key in sparksData.keys()])
            
            sparks = discord.ui.Label(
                text = translate(locale, "modal.spark.sparkSelect.text"),
                description = translate(locale, "modal.spark.sparkSelect.description"),
                component = self.select)
            self.add_item(sparks)

        elif Sparktyp == "Spicy":
            self.select = discord.ui.Select(
                options=[
                        discord.SelectOption(label=key, value=key)
                        for key in spicySparks.keys()])
            
            sparks = discord.ui.Label(
                text = translate(locale, "modal.spark.sparkSelect.text"),
                description = translate(locale, "modal.spark.sparkSelect.description"),
                component = self.select)
            self.add_item(sparks)

        else:
            self.select = discord.ui.Select(
                options=[
                        discord.SelectOption(label=key, value=key)
                        for key in softSparks.keys()])
            
            sparks = discord.ui.Label(
                text = translate(locale, "modal.spark.sparkSelect.text"),
                description = translate(locale, "modal.spark.sparkSelect.description"),
                component = self.select)
            self.add_item(sparks)

        self.anonym = discord.ui.Select(
            options=[
                discord.SelectOption(label=translate(locale, "yes"), value="yes"),
                discord.SelectOption(label=translate(locale, "no"), value="no")])
        
        anonym = discord.ui.Label(
            text = translate(locale, "modal.spark.anonym.text"),
            description = translate(locale, "modal.spark.anonym.description"),
            component = self.anonym)
        self.add_item(anonym)


    async def on_submit(self, interaction: discord.Interaction):
        targetName = self.targetName
        kompliment = self.select.values[0]
        serverID = interaction.guild_id
        UserExists(str(interaction.user.id))
        insertLogs(connection, datetime.now().isoformat(), interaction.user.id, self.target.id, serverID, kompliment, "Spark", 1)

        if self.anonym.values[0] == "yes":
            desc = translate(interaction.locale, f"sparks.{kompliment}.anonym")
        else:
            desc = translate(interaction.locale, f"sparks.{kompliment}.text", userName=interaction.user.name)
        embed = discord.Embed(
        title=translate(interaction.locale, f"sparks.{kompliment}.name"),
        description=f"{self.target.mention} {desc}",
        color=0x00FF00)

        embed.set_image(url=random.choice(sparksData[kompliment].get("link")))
        embed.set_thumbnail(url=self.target.display_avatar.url)
        embed.set_footer(text=f"Spark ID: {getSparkID(connection)}")
        await interaction.response.send_message(translate(interaction.locale, "modal.spark.onSubmit", targetName=targetName), ephemeral=True)
        await interaction.followup.send(embed=embed)




# Setup-Funktion für Cog
async def setup(bot):
    await bot.add_cog(Spark(bot))
    print("SparkCommand geladen ✅")