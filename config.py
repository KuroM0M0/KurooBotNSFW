import os
from dotenv import load_dotenv
from dataBase import createConnection

connection = createConnection()
load_dotenv()

BotToken = os.getenv("BotToken")
KuroID = os.getenv("KuroID")
Kurocord = os.getenv("Kurocord")
BotID = int(os.getenv("BotID"))