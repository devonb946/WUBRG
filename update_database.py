import psycopg2 as ps2
import uuid, json, requests
from timeit import default_timer as timer

start = timer()

conn = ps2.connect(dbname="d6tt07mv68p5e3", user="yolvyjabqqcslj", password="f9956ff96e2f12f0c0cda3d0bf9a1e0af88820a88ddda88258310d213ab35634", host="ec2-50-17-225-140.compute-1.amazonaws.com", port=5432)


url = "https://api.scryfall.com/bulk-data"
results = requests.get(url).json()["data"][2]
cards = requests.get(results["permalink_uri"]).json()

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS browse_card_2;")

cur.execute("CREATE TABLE browse_card_2 (data jsonb not null, id uuid PRIMARY KEY);")
conn.commit()

for item in cards:
    cur.execute("INSERT INTO browse_card_2(data, id) VALUES (\'%s\', \'%s\');" % (json.dumps(item).replace("'", "''"), item.get("id")))
conn.commit()

cur.execute("DROP TABLE browse_card;")
cur.execute("ALTER TABLE browse_card_2 RENAME TO browse_card;")
conn.commit()

cur.close()
conn.close()

end = timer()
print(end - start)
