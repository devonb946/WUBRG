import psycopg2 as ps2
import uuid, json, requests
from timeit import default_timer as timer

start = timer()

conn = ps2.connect(dbname="d6tt07mv68p5e3", user="yolvyjabqqcslj", password="f9956ff96e2f12f0c0cda3d0bf9a1e0af88820a88ddda88258310d213ab35634", host="ec2-50-17-225-140.compute-1.amazonaws.com", port=5432)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS browse_card_2;")

cur.execute("CREATE TABLE browse_card_2 (data jsonb not null, id uuid PRIMARY KEY);")
conn.commit()

url = "https://api.scryfall.com/cards"
has_more = True
count = 0

while (has_more):
    result = requests.get(url).json()

    cards = result["data"]
    has_more = result["has_more"]
    url = result["next_page"]

    total_cards = result["total_cards"]

    query_string = "INSERT INTO browse_card_2(data, id) VALUES "
    for item in cards:
        count += 1
        print(count, "/", total_cards, " cards inserted")

        values_to_add = "(\'%s\', \'%s\'), " % (json.dumps(item).replace("'", "''"), item.get("id"))
        query_string += values_to_add

        # cur.execute("INSERT INTO browse_card_2(data, id) VALUES (\'%s\', \'%s\');" % (json.dumps(item).replace("'", "''"), item.get("id")))
    query_string = query_string[:-2] + ';'
    cur.execute(query_string)

conn.commit()

cur.execute("DROP TABLE browse_card;")
cur.execute("ALTER TABLE browse_card_2 RENAME TO browse_card;")
conn.commit()

cur.close()
conn.close()

end = timer()
print(end - start)
