import json, getpass
from pymongo import MongoClient


client = MongoClient("mongodb+srv://wubrg-db-qpgxr.mongodb.net/test", username=input("Enter Mongo Atlas username: "), password=getpass.getpass("Enter Mongo Atas Password: "))
db = client['cards']
collection_cards = db['card']

with open('scryfall-all-cards.json', encoding="utf8") as f:
    file_data = json.load(f)

collection_cards.insert(file_data)
client.close()
