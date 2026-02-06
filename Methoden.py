import asyncio
from dataBase import *
from main import connection

def CheckServerExists(serverID):
    """
    Prüft ob Server in der Datenbank existiert, wenn nicht wird er hinzugefügen
    """
    exists = checkServerExists(connection, serverID)
    if exists == False:
        insertServer(connection, serverID)


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