import psycopg2 as ps2
import os, uuid, json, requests
from timeit import default_timer as timer

start = timer()

conn = ps2.connect(
    dbname = os.environ.get('WUBRG_NAME'),
    user = os.environ.get('WUBRG_USER'),
    password = os.environ.get('WUBRG_PASSWORD'),
    host = os.environ.get('WUBRG_HOST'),
    port = os.environ.get('WUBRG_PORT'),
)


url = "https://archive.scryfall.com/json/scryfall-default-cards.json"
cards = requests.get(url).json()

cur = conn.cursor()

total_cards = len(cards)
count = 0

query_string = ""
for item in cards:

    query_string += "INSERT INTO browse_card(data, id) VALUES\n"
    values_to_add = "(\'%s\', \'%s\'), " % (json.dumps(item).replace("'", "''"), item.get("id"))
    query_string += values_to_add + "\n\n"

    # implementing UPSERT functionality (insert if new id, update if existing)
    query_string = query_string[:-4] + "\n"
    query_string = query_string + "ON CONFLICT (id) DO UPDATE\n  SET " + "data = \'" + json.dumps(item).replace("'", "''") + "\';"

    if (count != 0) and (count % 20 == 0 or count == total_cards-1):
        cur.execute(query_string)
        query_string = ""

    count += 1
    print(count, "/", total_cards, " cards inserted")

conn.commit()

cur.close()
conn.close()

end = timer()
print(end - start)
