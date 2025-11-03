import logging
from dotenv import load_dotenv
import os
import discord
import json
from discord.ext import commands
from discord import Locale, app_commands
import asyncio
from dataBase import createConnection

load_dotenv()
logging.basicConfig(level=logging.WARNING)

BotToken = os.getenv("BotToken")
KuroID = os.getenv("KuroID")
Kurocord = os.getenv("Kurocord")
BotID = int(os.getenv("BotID"))
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="-", intents=intents)
connection = createConnection()


#Übersetzungen laden
localizations = {}
for language in ["de", "en"]:
    with open(os.path.join("localization", f"{language}.json"), encoding="utf-8") as f:
        localizations[language] = json.load(f)

#Mapping von Discord Locales zu den JSON-Keys
locale_map = {
    Locale.german: "de"
    #Alles andere ist Englisch
}

def translate(locale: Locale, path: str, **kwargs):

    """
    Übersetzt den Text anhand der übergebenen path aus den Lokalisierungsdateien.

    Falls der Wert ein String ist, wird dieser mit den übergebenen kwargs formatiert.
    Falls der Wert ein Dict ist, wird nach dem Schlüssel "_label" gesucht und dieser Wert
    zurückgegeben. 
    
    Wenn der Schlüssel nicht vorhanden ist, wird ein KeyError ausgelöst.
    Falls der Wert kein String oder Dict ist, wird er einfach als String zurückgegeben.
    """
    parts = path.split(".")
    lang = locale_map.get(locale, "en")  # fallback auf Englisch
    value = localizations[lang]
    for p in parts:
        value = value[p]

    if isinstance(value, dict):
        if "_label" in value:
            value = value["_label"]
        else:
            raise KeyError(f"Key '{path}' verweist auf ein Objekt ohne _label")

    # falls String → format anwenden
    if isinstance(value, str):
        return value.format(**kwargs)
    
    return str(value)


async def setBotActivity():
    await asyncio.sleep(10)  # Warte 10 Sekunden, um sicherzustellen, dass der Bot vollständig verbunden ist
    activity = discord.Streaming(
        name=f"{len(bot.guilds)} von 100 Server",
        url="https://www.twitch.tv/kurom0m0"
    )
    await bot.change_presence(activity=activity)



@bot.event
async def on_ready():
    print(f"Bot ist eingeloggt als {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash-Commands synchronisiert: {len(synced)} Befehle")
        #bot.add_view(WhatIsSparkButton())
    except Exception as e:
        print(f"Fehler beim Synchronisieren: {e}")
    #zeigt in Konsole an, auf welchen Servern der Bot ist
    for guild in bot.guilds:
        print(f'- {guild.name} (ID: {guild.id}) | {len(guild.members)} Mitglieder')
    await setBotActivity()


@bot.event
async def on_guild_join(guild):
    await setBotActivity()
    systemChannel = guild.system_channel
    await systemChannel.send("use -setNSFWChannel to make the bot work in this channel")

@bot.event
async def on_guild_remove(guild):
    await setBotActivity()



async def loadCommands():
    await bot.load_extension("commands.settings")
    await bot.load_extension("commands.spark")
    await bot.load_extension("commands.Test")
    await bot.load_extension("commands.adminCommands")
    await bot.load_extension("commands.kuroCommands")
    await bot.load_extension("commands.help")



async def main():
    await loadCommands()
    await bot.start(BotToken)

if __name__ == "__main__":
    asyncio.run(main())