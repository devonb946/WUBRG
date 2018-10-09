import json, getpass
from pymongo import MongoClient


client = MongoClient("mongodb://wubrgadmin:hunter2@ds227053-a0.mlab.com:27053,ds227053-a1.mlab.com:27053/heroku_v5994ldl?replicaSet=rs-ds227053", username="wubrgadmin", password="hunter2")
db = client['heroku_v5994ldl']
collection_cards = db['browse_card']

with open('scryfall-all-cards.json', encoding="utf8") as f:
    file_data = json.load(f)

collection_cards.insert(file_data)
client.close()
