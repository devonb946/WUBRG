import psycopg2 as ps2
import uuid, json
from timeit import default_timer as timer

start = timer()

conn = ps2.connect(dbname="d6tt07mv68p5e3", user="yolvyjabqqcslj", password="f9956ff96e2f12f0c0cda3d0bf9a1e0af88820a88ddda88258310d213ab35634", host="ec2-50-17-225-140.compute-1.amazonaws.com", port=5432)

with open('scryfall-all-cards.json', encoding="utf8") as f:
    file_data = json.load(f)

cur = conn.cursor()
for item in file_data:
    cur.execute("""INSERT INTO browse_card(id, data) VALUES(%s, %s);""", (item.get("id"), str(json.dumps(item))))
conn.commit()
cur.close()
conn.close()

end = timer()
print(end - start)