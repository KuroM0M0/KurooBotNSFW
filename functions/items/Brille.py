import discord
from discord import Locale
from config import connection
from functions.dataBase import *
from main import translate
from functions.Methoden import getUserName

async def useBrille(interaction):
    try:
        itemID = getItemIDByName(connection, "👓 Weisheitsbrille")
        await interaction.response.send_modal(BrilleModal(interaction.locale, itemID))
    except Exception as e:
        await interaction.followup.send(f"Fehler: {e}", ephemeral=True)
        print(f"Fehler bei useBrille: {e}")

class BrilleModal(discord.ui.Modal):
    def __init__(self, locale: Locale, itemID: int):
        super().__init__(title=translate(locale, "modal.brille.title"))
        self.locale = locale
        self.itemID = itemID

        self.SparkID = discord.ui.TextInput(
            label=translate(self.locale, "modal.brille.title"), 
            placeholder=translate(self.locale, "modal.brille.placeholder"),
            min_length=1,
            max_length=6,
            required=True)

        self.add_item(self.SparkID)

    async def on_submit(self, interaction: discord.Interaction):
        sparkID = self.SparkID.value
        userID = str(interaction.user.id)
        isRevealed = getIsRevealed(connection, sparkID)
        if isRevealed is False:
            await interaction.response.send_message("Gib eine Gültige ID ein!", ephemeral=True)
            return

        if userID != getSparkTargetID(connection, sparkID):
            await interaction.response.send_message("Du kannst nur Sparks aufdecken, die du selbst erhalten hast!", ephemeral=True)
            return

        result = getSparkReveal(connection, sparkID)
        if result is None:
            await interaction.response.send_message("Der Sender möchte Anonym bleiben.", ephemeral=True)
            return
        elif isRevealed == True:
            await interaction.response.send_message(f"Dieser Spark wurde bereits von dir aufgedeckt!", ephemeral=True)
            return
        else:
            userName = await interaction.client.fetch_user(result)
            await interaction.response.send_message(f"Die Wahrheitsbrille flackert auf, und ein Funken Klarheit brennt sich in dein Bewusstsein. \nDieser Spark wurde von **{userName}** gesendet.", ephemeral=True)
            updateUserInventar(connection, userID, self.itemID, -1)
            setIsRevealed(connection, sparkID)