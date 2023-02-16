import json
import sqlite3

# Kopplar till freedive.db
conn = sqlite3.connect("freedive.db")
cursor = conn.cursor()

# Öppnar JSON fil och hämtar data
with open("seed.json") as f:
    data = json.load(f)

# Lägger in data till tables
# Seedar data för table freedivers
for record in data["freedivers"]:
    query = """INSERT INTO  freedivers (
                    first_name, last_name, age
                )
                VALUES (
                    ?, ?, ?
                    )"""
    values = (record["first_name"], record["last_name"], record["age"])
    cursor.execute(query, values)

# Seedar data för table freedives
for record in data["freedives"]:
    query = """INSERT INTO  freedives (
                    depth_m,
                    discipline,
                    dive_time_sec,
                    down_speed_m_per_sec,
                    up_speed_m_per_sec,
                    dive_site,
                    date,
                    diver_id
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?
                )"""

    values = (record["depth_m"], record["discipline"], record["dive_time_sec"], record["down_speed_m_per_sec"], record["up_speed_m_per_sec"], record["dive_site"], record["date"], record["diver_id"])
    cursor.execute(query, values)

# Commitar uppdateringen och stänger ner
conn.commit()
conn.close()