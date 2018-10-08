import json, getpass
from pymongo import MongoClient


client = MongoClient("mongodb+srv://wubrg-db-qpgxr.mongodb.net/test", username=input("Enter MongoDB Username: "), password=getpass.getpass("Enter MongoDB password: "))
db = client['cards']
collection_cards = db['browse_card']

with open('scryfall-all-cards.json', encoding="utf8") as f:
    file_data = json.load(f)

collection_cards.insert(file_data)
client.close()
