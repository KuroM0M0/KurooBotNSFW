import sqlite3
from datetime import datetime, timedelta
import json


def createConnection():
    try:
        connection = sqlite3.connect("data.db")
        print("Datenbankverbindung erfolgreich hergestellt.")
        return connection
    except sqlite3.Error as e:
        print(f"Fehler beim Herstellen der Datenbankverbindung: {e}")
        return None


try:
    with open("compliments.json", "r", encoding="utf8") as f:
        compliments = json.load(f)

except FileNotFoundError:
    compliments = {}




def closeConnection(connection):
    if connection:
        connection.close()
        print("Datenbankverbindung geschlossen.")





def getCompliments(connection, userID):
    """
    Liefert eine Dictionary mit den Komplimenten und der Anzahl
    der Nutzung pro Kompliment für einen bestimmten User aus der Compliments Tabelle

    Args:
        connection (sqlite3.Connection): Die Verbindung zur Datenbank.
        userID (int): Die ID des Users.

    Returns:
        dict: Ein Dictionary mit den Komplimenten und der Anzahl
            der Nutzung pro Kompliment.
    """
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''
                                SELECT Compliment, Typ, ID
                                FROM Logs
                                WHERE TargetID = ? AND Disabled = 0
                            ''', (userID,))
            results = cursor.fetchall()

            normal_types = {"Compliment", "Hug", "Pat"}

            stats = {
                "Normal": {},  # Dict[compliment] = count
                "Custom": {}   # Dict[compliment] = list of IDs
            }

            for compliment, cType, spark_id in results: #cType = Typ
                if cType in normal_types:
                    stats["Normal"][compliment] = stats["Normal"].get(compliment, 0) + 1
                elif cType == "Custom":
                    if compliment not in stats["Custom"]:
                        stats["Custom"][compliment] = []
                    stats["Custom"][compliment].append(spark_id)

            return stats
        
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen der Kompliment-Statistiken: {e}")
            return {}
    else:
        print("Keine Datenbankverbindung verfügbar.")
        return {}
    



def getServerCompliments(connection, userID, serverID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''
                                SELECT Compliment, Typ, ID
                                FROM Logs
                                WHERE TargetID = ? AND Disabled = 0 AND ServerID = ?
                            ''', (userID, serverID))
            results = cursor.fetchall()

            normal_types = {"Compliment", "Hug", "Pat"}

            stats = {
                "Normal": {},  # Dict[compliment] = count
                "Custom": {}   # Dict[compliment] = list of IDs
            }

            for compliment, cType, spark_id in results: #cType = Typ
                if cType in normal_types:
                    stats["Normal"][compliment] = stats["Normal"].get(compliment, 0) + 1
                elif cType == "Custom":
                    if compliment not in stats["Custom"]:
                        stats["Custom"][compliment] = []
                    stats["Custom"][compliment].append(spark_id)

            return stats
        
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen der Kompliment-Statistiken: {e}")
            return {}
    else:
        print("Keine Datenbankverbindung verfügbar.")
        return {}
    


def getCustomCompliments(connection, userID):
    """
    Liefert eine Liste mit allen Custom-Komplimenten für einen bestimmten User aus der Logs Tabelle

    Args:
        connection (sqlite3.Connection): Die Verbindung zur Datenbank.
        userID (int): Die ID des Users.

    Returns:
        list: Eine Liste mit allen Custom-Komplimenten des Users.
    """
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT Compliment
                                FROM Logs
                                WHERE UserID = ? AND Compliment = "Custom"''', 
                                (userID,))
            results = cursor.fetchall()

            if results:
                return [compliment for compliment, in results]
            else:
                return []
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen der Custom-Komplimente: {e}")
            return []
    else:
        print("Keine Datenbankverbindung verführbar.")
        return []




def insertCompliment(connection, userID, compliment, Count = 1):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  INSERT INTO Compliments
                                (UserID, Compliment, Count)
                                VALUES(?, ?, ?)''',
                                (userID, compliment, Count))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Einfügen des kompliments: {e}")
            return False
    else:
        print("Keine Datenbankverbindung verfügbar.")
        return False




def updateCompliment(connection, userID, compliment):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Compliments
                                SET Count = Count + 1
                                WHERE userID = ?
                                AND Compliment = ?''',
                                (userID, compliment))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Updaten der Compliments: {e}")
            return {}
    else:
        print("Keine Datenbankverbindung verfügbar")
        return {}




def updateStreak(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET Streak = Streak + 1
                                WHERE userID = ?''',
                                (userID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der Streak: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar.")
        return {}




def getStreak(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT Streak
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return None
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen der Streak: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar.")
        return {}
    



def resetStreak(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET Streak = 0
                                WHERE userID = ?''',
                                (userID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der Streak: {e}")
    else:
        print("Keine Datenbankverbindung verfühgbar.")
        return {}




def getSparkID(connection):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ID
                                FROM Logs
                                ORDER BY ID DESC
                                LIMIT 1''')
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen der ID: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar.")
        return {}




def getStreakPoints(connection, userID): #Bisher nicht verwendet
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT StreakPoints
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen der StreakPoints: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar.")
        return {}
    



def updateStreakPoints(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET StreakPoints = Streakpoints + 1
                                WHERE UserID = ?''',
                                (userID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen der StreakPoints: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar.")
        return {}
    



def setStreakPoints(connection, userID, Punkte):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET StreakPoints = ?
                                WHERE UserID = ?''',
                                (Punkte, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der StreakPunkte: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getPremium(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT PremiumTimeInMonths
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None or result[0] == 0:
                return False
            else:
                return True
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen von Premium: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")
        return {}
    



def getPremiumInMonths(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT PremiumTimeInMonths
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen von PremiumInMonths: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")
        return {}




def getPremiumTimestamp(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT PremiumTimestamp
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return False
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen von Premium: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")
        return {}




def setPremium(connection, userID, Months):
    if connection is not None:
        cursor = connection.cursor()
        time = datetime.now().isoformat()
        try:
            cursor.execute('''  UPDATE User
                                SET PremiumTimeInMonths = ?,
                                PremiumTimestamp = ?
                                WHERE UserID = ?''',
                                (Months, time, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Updaten von Premium: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def resetPremium(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET PremiumTimeInMonths = 0
                                WHERE UserID = ?''',
                                (userID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Updaten von Premium: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def insertLogs(connection, Timestamp, UserID, TargetID, ServerID, Spark, Typ, Anonym, isRevealed = 0):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  INSERT INTO Logs
                                (Timestamp, UserID, TargetID, ServerID, Spark, Typ, Anonym, isRevealed)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                (Timestamp, UserID, TargetID, ServerID, Spark, Typ, Anonym, isRevealed))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Insert von Logs: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def getLastStreakPointAdded(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT lastStreakPointAdded
                                FROM User
                                WHERE userID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return None
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen vom lastStreakPointAdded: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def setLastStreakPointAdded(connection, userID, lastStreakPointAdded):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET lastStreakPointAdded = ?
                                WHERE userID = ?''',
                                (lastStreakPointAdded, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen vom lastStreakPointAdded: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def checkUserExists(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT UserID
                                FROM User
                                WHERE userID = ?''',
                                (userID,))
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim Abrufen des Users: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def insertUser(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  INSERT INTO User
                                (UserID, PremiumTimestamp, PremiumTimeInMonths, VotePoints, StreakPoints, Streak, possibleSparks)
                                VALUES(?, 0, 0, 0, 0, 0, 1)''',
                                (userID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Einfügen des Users: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def updateSparkUses(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET SparkUses = SparkUses + 1
                                WHERE UserID = ?''',
                                (userID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Updaten von SparkUses: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def resetSparkUses(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET SparkUses = 0
                                WHERE UserID = ?''',
                                (userID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Updaten von SparkUses: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def getSparkUses(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT SparkUses
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparkUses: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def insertUserSetting(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  INSERT INTO Settings
                                (UserID, SparkTyp, StreakPrivate, SparkDM, Ping, Newsletter)
                                VALUES(?, "Soft", 0, 1, 1, 0)''',
                                (userID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim einfügen des Users in die Settings: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def checkUserSetting(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT UserID
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim überprüfen des Users in die Settings: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def getSparkDM(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT SparkDM
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 1
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparkDM: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def setSparkDM(connection, userID, an): #an = true/false
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Settings
                                SET SparkDM = ?
                                WHERE UserID = ?''',
                                (an, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der SparkDM Setting: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def getHugPatDM(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT HugPatDM
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von HugPatDM: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def setHugPatDM(connection, userID, an): #an = true/false
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Settings
                                SET HugPatDM = ?
                                WHERE UserID = ?''',
                                (an, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der HugPatDM Setting: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def getHugPatPing(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT HugPatPing
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 1
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von HugPatPing: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def setHugPatPing(connection, userID, an): #an = true/false
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Settings
                                SET HugPatPing = ?
                                WHERE UserID = ?''',
                                (an, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der HugPatPing Setting: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def getStatsPrivate(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT StatsPrivate
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von StatsPrivate: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def setStatsPrivate(connection, userID, an): #an = true/false
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Settings
                                SET StatsPrivate = ?
                                WHERE UserID = ?''',
                                (an, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der StatsPrivate Setting: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def getStreakPrivate(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT StreakPrivate
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von StreakPrivate: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setStreakPrivate(connection, userID, an): #an = true/false
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Settings
                                SET StreakPrivate = ?
                                WHERE UserID = ?''',
                                (an, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der StreakPrivate Setting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getTopServerSparks(connection):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT serverID, serverName, COUNT(*) as count 
                                FROM Logs 
                                WHERE Typ = 'Compliment' OR Typ = 'Custom'
                                GROUP BY serverID 
                                ORDER BY count DESC 
                                LIMIT 5''')
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der StatsPrivate Setting: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def getTopServerHugs(connection):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT serverID, serverName, COUNT(*) as count 
                                FROM Logs 
                                WHERE Typ = 'Hug' OR Typ = 'Pat'
                                GROUP BY serverID 
                                ORDER BY count DESC 
                                LIMIT 5''')
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der StatsPrivate Setting: {e}")
    else:
        print("Keine Datenbankverbindung verfügbar")




def getNewsletter(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT Newsletter
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Newsletter: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setNewsletter(connection, userID, an): #an = true/false
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Settings
                                SET Newsletter = ?
                                WHERE UserID = ?''',
                                (an, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der Newsletter Setting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getNewsletterSubs(connection):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT UserID
                                FROM Settings
                                WHERE Newsletter = 1''',
                                )
            result = cursor.fetchall()
            if result is None:
                return 0
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von NewsletterSubscriber: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getNewsletterChannel(connection):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ChannelNewsletterID
                                FROM Server
                                WHERE ChannelNewsletterID IS NOT NULL''',
                                )
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von NewsletterServer: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")





def getCustomSparkSetting(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT CustomSpark
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return True
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von CustomSpark: {e}")

            
            
            
def getStatDisabled(connection, SparkID):
    """
    Gibt den Wert von Disabled für den Spark mit der SparkID zurück.

    Args:
        connection (sqlite3.Connection): Die Verbindung zur Datenbank.
        SparkID (int): Die ID des Sparks.

    Returns:
        int: Der Wert von Disabled (0 = false, 1 = true).
    """
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT Disabled, TargetID
                                FROM Logs
                                WHERE ID = ?''',
                                (SparkID,))
            result = cursor.fetchone() #TODO testen was passiert wenn ungültiger wert eingegeben wird
            print(result)
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von StatDisabled: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")





def setCustomSparkSetting(connection, userID, an): #an = true/false
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Settings
                                SET CustomSpark = ?
                                WHERE UserID = ?''',
                                (an, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der CustomSpark Setting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")

        
        
        
def setStatDisabled(connection, SparkID, an): #an = true/false
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Logs
                                SET Disabled = ?
                                WHERE ID = ?''',
                                (an, SparkID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der StatDisabled Setting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getPingSetting(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT Ping
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return True
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Ping: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setPingSetting(connection, userID, an): #an = true/false
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Settings
                                SET Ping = ?
                                WHERE UserID = ?''',
                                (an, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der Ping Setting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getProfilPrivateSetting(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT StreakPrivate
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Profil: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setProfilPrivateSetting(connection, userID, an): #an = true/false
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Settings
                                SET StreakPrivate = ?
                                WHERE UserID = ?''',
                                (an, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der ProfilPrivate Setting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getBirthday(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT Birthday
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Birthday: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setBirthday(connection, userID, date):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET Birthday = ?
                                WHERE UserID = ?''',
                                (date, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der Birthday Setting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getSparkCount(connection, userID):
    """Gibt zurück wie oft der User gesparkt hat. (UserID)"""
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT COUNT(ID)
                                FROM Logs
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparkCount: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getSparkCountDisabled(connection, userID):
    """Gibt zurück wie viele Sparks jemand Disabled hat (TargetID)"""
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT COUNT(ID)
                                FROM Logs
                                WHERE TargetID = ? AND Disabled = 1''',
                                (userID,))
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparkCountDisabled: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getSparkCountDisabledServer(connection, userID, serverID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT COUNT(ID)
                                FROM Logs
                                WHERE TargetID = ? AND Disabled = 1 AND ServerID = ?''',
                                (userID, serverID))
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparkCountDisabled: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getSparkCountSelf(connection, userID):
    """"Gibt zurück wie oft man selbst gesparkt wurde. (TargetID)"""
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT COUNT(ID)
                                FROM Logs
                                WHERE TargetID = ?''',
                                (userID,))
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparkTargetCount: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getSparkCountSelfServer(connection, userID, serverID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT COUNT(ID)
                                FROM Logs
                                WHERE TargetID = ? AND ServerID = ?''',
                                (userID, serverID))
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparkTargetCount: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getSparkReveal(connection, SparkID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT UserID
                                FROM Logs
                                WHERE ID = ? AND Anonym != 1''',
                                (SparkID,))
            result = cursor.fetchone()
            if result is None:
                return None
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Reveal: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getSparkTargetID(connection, SparkID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT TargetID
                                FROM Logs
                                WHERE ID = ?''',
                                (SparkID,))
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SenderID: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getRevealUses(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT RevealUses
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von RevealUses: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setRevealUses(connection, userID, RevealUses):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET RevealUses = ?
                                WHERE UserID = ?''',
                                (RevealUses, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der RevealUses: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def addRevealUses(connection, userID, RevealUses):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET RevealUses = RevealUses + ?
                                WHERE UserID = ?''',
                                (RevealUses, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim hinzufügen der RevealUses: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setChannelSparkID(connection, serverID, channelID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Server
                                SET ChannelSparkID = ?
                                WHERE ServerID = ?''',
                                (channelID, serverID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der ChannelSparkID: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getChannelSparkID(connection, serverID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ChannelSparkID
                                FROM Server
                                WHERE ServerID = ?''',
                                (serverID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von ChannelSparkID: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setChannelNewsletterID(connection, serverID, channelID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Server
                                SET ChannelNewsletterID = ?
                                WHERE ServerID = ?''',
                                (channelID, serverID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der ChannelNewsletterID Setting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getChannelNewsletterID(connection, serverID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ChannelNewsletterID
                                FROM Server
                                WHERE ServerID = ?''',
                                (serverID,))
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von ChannelNewsletterID: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def insertServer(connection, ServerID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  INSERT INTO Server
                                (ServerID, PremiumTimestamp, PremiumInMonths, ChannelSparkID)
                                VALUES (?, 0, 0, 0)''',
                                (ServerID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim Insert von Server: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def checkServerExists(connection, serverID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ServerID
                                FROM Server
                                WHERE ServerID = ?''',
                                (serverID,))
            result = cursor.fetchone()
            if result is None:
                return False
            return True
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Server: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setVotePoints(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET VotePoints = VotePoints + 1
                                WHERE UserID = ?''',
                                (userID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der VotePoints: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getVotePoints(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT VotePoints
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von VotePoints: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setVoteTimestamp(connection, userID, VoteTimestamp):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET VoteTimestamp = ?
                                WHERE UserID = ?''',
                                (VoteTimestamp, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der VoteTimestamp Setting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getVoteTimestamp(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT VoteTimestamp
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von VoteTimestamp: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")
        



def getReveals(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ID, Timestamp, Spark
                                FROM Logs
                                WHERE TargetID = ? AND Anonym = 2 AND isRevealed = 0''',
                                (userID,))
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Reveals: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getRevealsCustom(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ID, Timestamp, Spark
                                FROM Logs
                                WHERE TargetID = ? AND Reveal = 1 AND isRevealed = 0 AND Typ = 'Custom' ''',
                                (userID,))
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Reveals: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setIsRevealed(connection, SparkID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Logs
                                SET isRevealed = 1
                                WHERE ID = ?''',
                                (SparkID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der Reveal: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getIsRevealed(connection, SparkID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT isRevealed
                                FROM Logs
                                WHERE ID = ?''',
                                (SparkID,))
            result = cursor.fetchone()
            if result is None:
                return False
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Reveal: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getRevealedSparks(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ID, Timestamp, Spark, UserID
                                FROM Logs
                                WHERE TargetID = ? AND isRevealed = 1''',
                                (userID,))
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von RevealedSparks: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getRevealedSparksCustom(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ID, Timestamp, Compliment, UserName
                                FROM Logs
                                WHERE TargetID = ? AND isRevealed = 1 AND Typ = 'Custom' ''',
                                (userID,))
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von RevealedSparks: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def insertItem(connection, Name, Beschreibung, Preis, PreisTyp, ItemURL):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  INSERT INTO Item (Name, Beschreibung, Preis, PreisTyp, ItemURL)
                                VALUES (?, ?, ?, ?, ?)''',
                                (Name, Beschreibung, Preis, PreisTyp, ItemURL))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim inserten von Items: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getItemPrice(connection, Name):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT Preis, PreisTyp
                                FROM Item
                                WHERE Name = ?''',
                                (Name,))
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Items: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getAllShopItems(connection):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT *
                                FROM Item''')
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von Items: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setVotePoints(connection, targetID, Punkte):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET VotePoints = ?
                                WHERE UserID = ?''',
                                (Punkte, targetID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der Punkte: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def updateVotePoints(connection, targetID, Punkte):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET VotePoints = VotePoints + ?
                                WHERE UserID = ?''',
                                (Punkte, targetID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der VotePoints: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def updateStreakPunkte(connection, targetID, Punkte):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET StreakPoints = StreakPoints + ?
                                WHERE UserID = ?''',
                                (Punkte, targetID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der StreakPunkte: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")



def addItemToInventar(connection, userID, itemID, count):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  INSERT INTO Inventar (UserID, ItemID, Anzahl)
                                VALUES (?, ?, ?)''',
                                (userID, itemID, count))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim inserten von UserItems: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def updateUserInventar(connection, userID, itemID, count):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Inventar
                                SET Anzahl = Anzahl + ?
                                WHERE UserID = ?
                                AND ItemID = ?''',
                                (count, userID, itemID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim updaten vom Inventar: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getUserItems(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ItemID, Anzahl
                                FROM Inventar
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von UserItems: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getUserItemCount(connection, userID, itemID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT Anzahl
                                FROM Inventar
                                WHERE UserID = ?
                                AND ItemID = ?''',
                                (userID, itemID))
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von ItemCount: {e}")
    




def getUserItemID(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ItemID
                                FROM Inventar
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchall()
            return [row[0] for row in result]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von ItemID im Inventar: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getItemIDByName(connection, name):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT ItemID
                                FROM Item
                                WHERE Name = ?''',
                                (name,))
            result = cursor.fetchone()
            if result is None:
                return None
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von ItemID: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getSparkIntensity(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT SparkTyp
                                FROM Settings
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            if result is None:
                return "Soft"
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparktypeSetting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setSparkIntensity(connection, userID, typ):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE Settings
                                SET SparkTyp = ?
                                WHERE UserID = ?''',
                                (typ, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der SparktypeSetting: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getServerSettings(connection, serverID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT *
                                FROM ServerSettings
                                WHERE ServerID = ?''',
                                (serverID,))
            result = cursor.fetchone()
            if result == None:
                return False
            return result
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von ServerSettings: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def insertServerSettings(connection, serverID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  INSERT INTO ServerSettings (ServerID)
                                VALUES (?)''',
                                (serverID,))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim inserten von ServerSettings: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getServerAnonymHug(connection, serverID):
    """
    Gibt den Wert von Anonym für den Server mit der ServerID zurück.

    Args:
        connection (sqlite3.Connection): Die Verbindung zur Datenbank.
        serverID (int): Die ID des Servers.

    Returns:
        int: Der Wert von Anonym (0 = Ja/Halb/Nein, 1 = Ja/Halb).
    """
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT AnonymHug
                                FROM ServerSettings
                                WHERE ServerID = ?''',
                                (serverID,))
            result = cursor.fetchone()
            if result is None:
                return 1
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparkPath: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getServerAnonymSpark(connection, serverID):
    """
    Gibt den Wert von Anonym für den Server mit der ServerID zurück.

    Args:
        connection (sqlite3.Connection): Die Verbindung zur Datenbank.
        serverID (int): Die ID des Servers.

    Returns:
        int: Der Wert von Anonym (0 = Ja/Halb/Nein, 1 = Ja/Halb).
    """
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT AnonymSpark
                                FROM ServerSettings
                                WHERE ServerID = ?''',
                                (serverID,))
            result = cursor.fetchone()
            if result is None:
                return 1
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparkPath: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setServerAnonymHug(connection, serverID, value):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE ServerSettings
                                SET AnonymHug = ?
                                WHERE ServerID = ?''',
                                (value, serverID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der AnonymHug: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setServerAnonymSpark(connection, serverID, value):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE ServerSettings
                                SET AnonymSpark = ?
                                WHERE ServerID = ?''',
                                (value, serverID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der AnonymSpark: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getServerPremium(connection, serverID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT PremiumInMonths
                                FROM Server
                                WHERE ServerID = ?''',
                                (serverID,))
            result = cursor.fetchone()
            if result is None:
                return 0
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von SparkPath: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def getPossibleSparks(connection, userID):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  SELECT possibleSparks
                                FROM User
                                WHERE UserID = ?''',
                                (userID,))
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as e:
            print(f"Fehler beim selecten von PossibleSparks: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def setPossibleSparks(connection, userID, possibleSparks):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET possibleSparks = ?
                                WHERE UserID = ?''',
                                (possibleSparks, userID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der PossibleSparks: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")




def addPossibleSparksForAllUsers(connection):
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute('''  UPDATE User
                                SET possibleSparks = MIN(possibleSparks + 1, 10)''',
                                )
            connection.commit()
        except sqlite3.Error as e:
            print(f"Fehler beim setzen der PossibleSparks: {e}")
    else:
        print("Keine Datenbankverbindung verführbar")