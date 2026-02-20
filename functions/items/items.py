import discord
from dataclasses import dataclass
from enum import Enum
from discord import ui
from functions.dataBase import *
from config import connection
from functions.items.Brille import useBrille


class PriceType(Enum):
    VotePunkt = "VotePunkte"
    StreakPunkt = "StreakPunkte"


@dataclass
class ShopItem:
    itemID: int
    name: str
    description: str
    price: int
    priceType: PriceType 
    image: str

def checkUserHasItem(connection, userID, itemID):
    userInventar = getUserItems(connection, userID)
    for item, count in userInventar:
        if item == itemID and count > 0:
            return True
    return False



async def useMask(interaction, SparkID = None): #SparkID muss über Modal übergeben werden
    userID = str(interaction.user.id)
    itemID = getItemIDByName(connection, "🎭 Verborgene Maske")
    
    try:
        updateUserInventar(connection, userID, itemID, -1)
        #await checkStatCanBeDisabled(SparkID, userID, interaction)
    except Exception as e:
        await interaction.followup.send(f"Fehler: {e}", ephemeral=True)
        print(f"Fehler bei useMask: {e}")


async def useKrone(interaction):
    userID = str(interaction.user.id)
    itemID = getItemIDByName(connection, "👑 Premium-Krone")
    try:
        setPremium(connection, userID)
        updateUserInventar(connection, userID, itemID, -1)
        await interaction.followup.send("Eine unsichtbare Macht setzt dir die Premium-Krone auf. Ihr Licht durchdringt die Dunkelheit und weist dir nun exklusive Wege!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Fehler: {e}", ephemeral=True)
        print(f"Fehler bei useKrone: {e}")


ITEM_ACTIONS = {
    "🎭 Verborgene Maske": {"func": useMask, "needSparkID": True},
    "👑 Premium-Krone": {"func": useKrone, "needSparkID": False},
    "👓 Weisheitsbrille": {"func": useBrille, "needSparkID": True},
}