import discord
from discord import app_commands
from discord.ext import commands
from config import connection
from functions.shop import Shop
from functions.dataBase import *
from functions.items.items import *


class Use(commands.Cog):
    @app_commands.command(name="use", description="Nutze deine Items aus dem /Inventar")
    async def use(self, interaction: discord.Interaction, item: str):
        actionData = ITEM_ACTIONS.get(item)
        hasItem = checkUserHasItem(connection, interaction.user.id, getItemIDByName(connection, item))
        if hasItem == False:
            await interaction.response.send_message(f"❌ Du hast das Item **{item}** nicht!", ephemeral=True)
            return
        if not actionData:
            await interaction.response.send_message(f"❌ Für **{item}** gibt es noch keine Funktion.", ephemeral=True)
            return

        func = actionData["func"]
    
        #await interaction.response.defer(ephemeral=True)
        # Direkt ausführen
        await func(interaction)
        

    @use.autocomplete("item")
    async def itemName_autocomplete(self, interaction: discord.Interaction, current: str):
        shop = Shop(connection)
        userItems = getUserItems(connection, interaction.user.id)  # [(itemID, count), ...]
        allItems = shop.loadItems()

        itemNameList = []
        for item in allItems:
            for userItem in userItems:
                if item.itemID == userItem[0] and userItem[1] > 0:  # Anzahl > 0
                    itemNameList.append(item.name)

        # Erstelle Choice-Objekte
        choices = [
            app_commands.Choice(name=name, value=name)
            for name in itemNameList
        ]

        # Filtere nach Suchbegriff
        return [
            choice for choice in choices
            if current.lower() in choice.name.lower()
        ]
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Use(bot))
    print("Use geladen ✅")