from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

class MongoService:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client["etablissement"]
        self.etudiants = self.db["etudiants"]
        self.utilisateurs = self.db["utilisateurs"]

    def close(self):
        self.client.close()
