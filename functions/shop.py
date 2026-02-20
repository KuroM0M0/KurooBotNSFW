import discord
import math
import functions.emotes as E
from discord import ButtonStyle, ui
from functions.dataBase import *
from functions.items.items import ShopItem, PriceType



class ShopButtons(ui.View):
    def __init__(self, connection, site: int = 1, per_page: int = 1):
        super().__init__()
        self.site = site
        self.connection = connection
        self.per_page = per_page

        shop = Shop(connection)
        items = shop.getItemsOnPage(site, per_page=per_page)
        self.current_item = items[0] if items else None

        # Maximal mögliche Seiten berechnen
        max_pages = math.ceil(len(shop.items) / per_page)

        if site <= 1:
            self.back.disabled = True
        if site >= max_pages:
            self.next.disabled = True

    @ui.button(label="<", style=discord.ButtonStyle.secondary, row=0)
    async def back(self, interaction: discord.Interaction, button: ui.Button):
        self.site -= 1
        await interaction.response.edit_message(embed=ShopEmbed(self.site, interaction, self.connection), view=ShopButtons(self.connection, self.site))

    @ui.button(label=">", style=discord.ButtonStyle.secondary, row=0)
    async def next(self, interaction: discord.Interaction, button: ui.Button):
        self.site += 1
        await interaction.response.edit_message(embed=ShopEmbed(self.site, interaction, self.connection), view=ShopButtons(self.connection, self.site))

    @ui.button(label="Kaufen", style=discord.ButtonStyle.primary, row=1)
    async def ItemKauf(self, interaction: discord.Interaction, button: ui.Button):
        item = self.current_item
        if not item:
            await interaction.response.send_message("❌ Kein Item gefunden!", ephemeral=True)
            return

        userID = interaction.user.id
        userInventar = getUserItemID(self.connection, userID)

        # Prüfe, ob User genug Punkte hat
        if item.priceType == PriceType.VotePunkt:
            punkte = getVotePoints(self.connection, userID)
        else:
            punkte = getStreakPoints(self.connection, userID)

        if punkte < item.price:
            await interaction.response.send_message(
                f"❌ Du hast nicht genug {item.priceType.value} für **{item.name}**!",
                ephemeral=True)
            return

        #Punkte abziehen
        if item.priceType == PriceType.VotePunkt:
            updateVotePoints(self.connection, userID, -item.price) #- davor, weil die Datenbank Punkte + ? hat. also zb. 100 + -10 = 90
        else:
            updateStreakPunkte(self.connection, userID, -item.price)

        #Item hinzufügen
        if item.itemID in userInventar:
            updateUserInventar(self.connection, userID, item.itemID, 1)
            userInventar = getUserItemID(self.connection, userID)
        else:
            addItemToInventar(self.connection, userID, item.itemID, 1)
            userInventar = getUserItemID(self.connection, userID)

        await interaction.response.send_message(
            f"✅ Du hast **{item.name}** für {item.price} {item.priceType.value} gekauft!",
            ephemeral=True
        )


def ShopEmbed(site: int, interaction: discord.Interaction, connection) -> discord.Embed:
    userID = interaction.user.id
    #votepunkte = getVotePoints(connection, userID)
    streakpunkte = getStreakPoints(connection, userID)
    shop = Shop(connection)

    embed = discord.Embed(
        title="Shop", 
        description=f"Du hast: ",
        color=0x005b96)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1354078227903283251/1405245863852245033/Shop.png?ex=689ec972&is=689d77f2&hm=efb2c60ae90d11f746b1117fbe394e7045810515cf4fd616648ba8830a61d0f6&=")
    #embed.add_field(name="", value=f"**{votepunkte}** {E.VotePoint}", inline=True)
    embed.add_field(name="", value=f"**{streakpunkte}** {E.StreakPoint}", inline=True)
    embed.add_field(name="", value="", inline=True)
    embed.add_field(name="--------", value="", inline=False)

    items = shop.getItemsOnPage(site, per_page=1)
    if items:  # falls es ein Item gibt
        item = items[0]
        priceEmote = item.priceType.value
        if priceEmote == "VotePunkte":
            priceEmote = f"{E.VotePoint}"
        elif priceEmote == "StreakPunkte":
            priceEmote = f"{E.StreakPoint}"

        embed.set_image(url=item.image)

        embed.add_field(name=f"{item.name}", value=item.description, inline=True)
        embed.add_field(name="--------", value="", inline=False)
        embed.add_field(name="Preis:", value=f"{item.price} {priceEmote}", inline=False)
        embed.set_footer(text=f"Seite {site} von {len(shop.items)}")
    else:
        embed.add_field(name="Fehler", value="Kein Item auf dieser Seite gefunden.", inline=False)
    return embed


class Shop:
    def __init__(self, connection):
        self.connection = connection
        # Items aus der DB laden
        self.items = self.loadItems()

    def loadItems(self) -> list[ShopItem]:
        rows = getAllShopItems(self.connection)

        items = []
        for row in rows:
            try:
                item = ShopItem(
                    itemID=row[0],
                    name=row[1],
                    description=row[2],
                    price=row[3],
                    priceType=PriceType(row[4]),
                    image=row[5]
                )
                items.append(item)
            except Exception as e:
                print("Fehler beim Laden von Item:", row, e)
        return items

    def getItemByID(self, itemId: int) -> ShopItem | None:
        for item in self.items:
            if item.itemID == itemId:
                return item
        return None

    def getItemsOnPage(self, page: int, per_page: int = 1) -> list[ShopItem]:
        start = (page - 1) * per_page
        end = start + per_page
        return self.items[start:end]
    