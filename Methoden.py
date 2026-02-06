import asyncio
import discord
from typing import Optional
import re
from dataBase import *
from main import connection

def CheckServerExists(serverID):
    """
    Prüft ob Server in der Datenbank existiert, wenn nicht wird er hinzugefügen
    """
    exists = checkServerExists(connection, serverID)
    if exists == False:
        insertServer(connection, serverID)


def CheckServerExistsInSettings(serverID):
    """
    Prüft ob ServerSettings in der Datenbank existiert, wenn nicht wird er hinzugefügen
    """
    exists = getServerSettings(connection, serverID)
    if exists == False:
        insertServerSettings(connection, serverID)


def UserExists(userID): 
    """
    Prüft ob User in der Datenbank existiert, wenn nicht wird er hinzugefügen
    """
    exists = checkUserExists(connection, userID)
    if exists is None:
        insertUser(connection, userID)

def CheckPossibleSparks(userID):
    UserExists(userID)
    possibleSparks = getPossibleSparks(connection, userID)
    if possibleSparks <= 0:
        return False 
    else:
        return True

def removePossibleSpark(userID):
    possibleSparks = getPossibleSparks(connection, userID)
    setPossibleSparks(connection, userID, possibleSparks - 1)  


async def CheckSparkChannel(connection, guildID, channelID, interaction):
    sparkChannel = getChannelSparkID(connection, guildID)
    if sparkChannel != channelID and sparkChannel != None:
        await interaction.followup.send("Du kannst hier keine Befehle nutzen! Nutze den vorgesehenen Channel dafür.", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.delete_original_response()
        raise Exception("Wrong Channel")
    


# :name: – aber NICHT, wenn davor "<" steht und NICHT, wenn direkt danach ":<digits>>" kommt
_COLON_NAME = re.compile(r"(?<!<):([A-Za-z0-9_]+):(?!\d+>)")

def replaceEmotes(text: str, guild: discord.Guild, bot: discord.Client) -> str:
    def pick_emoji(name: str) -> Optional[str]:
    # 1) zuerst im aktuellen Server
        for e in getattr(guild, "emojis", []):
            if e.name == name:
                return str(e)

        # 2) dann global suchen (inkl. current guild, falls oben nichts war)
        for g in bot.guilds:
            for e in g.emojis:
                if e.name == name:
                    return str(e)

        return None

    def repl(m: re.Match) -> str:
        name = m.group(1)
        chosen = pick_emoji(name)
        return chosen if chosen is not None else m.group(0)

    return _COLON_NAME.sub(repl, text)

async def getUserName(userID, bot):
    userName = await bot.fetch_user(userID)
    return userName