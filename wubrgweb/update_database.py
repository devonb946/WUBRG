import requests, json, sqlite3, uuid
"""This script is designed to bulk download data from Scryfall and update the database accordingly"""

url = "https://api.scryfall.com/bulk-data"
database = "db.sqlite3"
sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)

def convert_border(crd_brdr):
    """quick little one-liner to convert json representation of border to database representation"""
    return {"black":"B", "white":"W", "silver":"S", "borderless":"N", "gold":"G"}[crd_brdr]

def convert_rarity(crd_rar):
    """quick little one-liner to convert json representation of rarity to database representation"""
    return {"common": 1, "uncommon": 2, "rare": 3, "mythic": 4}[crd_rar]

def convert_frame(crd_frame):
    """quick little one-liner to convert json representation of frame to database representation"""
    return {"1993": 1, "1997": 2, "2003": 3, "2015": 4, "future": "F"}[crd_frame]

def convert_layout(crd_lyot):
    """quick little 1.75-liner to convert json representation of layout to database representation"""
    return {"normal": "NRML", "split": "SPLT", "flip": "FLIP", "transform": "TRFM", "meld": "MELD", "leveler": "LVLR",\
            "saga": "SAGA", "planar": "PLNR", "scheme": "SCHM", "vanguard": "VGRD", "token": "TOKN", "double-faced token": "DFTK",\
            "emblem": "EMBL", "augment": "AGMT", "host": "HOST"}[crd_lyot]


def rip_card(card):
    print(card.get("name"))
    """extracts all of the relevant fields from a card in JSON format"""
    data = [uuid.uuid4(), card.get("cmc"), card.get("loyalty"), card.get("mana_cost"), card.get("name"), card.get("oracle_text"), card.get("power"),\
                          card["reserved"], card.get("toughness"), card.get("type_line"), card.get("artist"), card.get("collector_number"),\
                          card.get("flavor_text"), card.get("image_uris").get("png"), card.get("set"), card.get("set_name"), convert_rarity(card["rarity"]), convert_frame(card["frame"]), convert_border(card["border_color"]), convert_layout(card["layout"])]
    print("\n",data, len(data),"\n")
    return data

#get requests as json
results = requests.get(url).json()["data"][1]

with open("database_status.json") as cur:
    current = json.load(cur)

#compare to existing
#if we need to update
if (current["updated_at"] != results["updated_at"]):
    #update our records
    print("Data outdated, replaceing...")
    print("Updating local records...")
    with open("database_status.json", "w") as file:
        json.dump(results, file, indent=4, sort_keys=True)

    #update the database remotely
    print("Connecting to Scryfall...")
    local = requests.get(results["permalink_uri"]).json()
    db = sqlite3.connect(database)
    c = db.cursor()
    print("Updating cards...")
    #iteratively add all to the database
    skipped = []
    for i in local:
        try:
            print(i.get("card_faces"))
            if(i.get("card_faces") is None):
                c.execute("""INSERT INTO browse_card(id, cmc, loyalty, mana_cost, name, oracle_text, power, reserved, toughness, type_line, artist, collector_number, flavor_text, image, set_abbr, set_name, rarity, frame, border_color, layout)
                                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", rip_card(i))
            else:
                skipped.append(i.get("name"))
        except sqlite3.IntegrityError:
            print('ERROR with card {}'.format(i["name"]))

    #verify for dev enviornmnet
    #TODO: Remove
    if "y" == input("Would you like to commit these changes to the database? (y)"):
        db.commit()
    db.close()

    for i in set(skipped):
        print(i)

else:
    print("Database is up to date.")
