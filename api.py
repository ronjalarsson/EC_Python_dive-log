# Allt funkar per idag 20230216
from fastapi import FastAPI
from typing import List
from fastapi.responses import HTMLResponse

from models import FreediveLog, Freediver, UpdateFreediver, UpdateFreediveLog
from db import DB

app = FastAPI()
db = DB("freedive.db")

app.freedivers: List[Freediver] = []
app.curr_diver_id = 1 # Fungerar detta?

app.freedives: List[FreediveLog] = []
app.curr_dive_id = 1 # Fungerar detta?

# Minst 2 "routes/endpoints" för att hämta olika typer av data (GET)
@app.get("/", response_class=HTMLResponse) # Kan koppla root page till en HTML, jag behöver ej ha detta i slutinlämningen
def root():
    with open("index.html") as html_file:
        return html_file.read()

@app.get("/freedivers") # Returnera en lista med alla dykare
def get_freedivers():
    data = db.get(table="freedivers")
    return data

@app.get("/freediver_by_id/{id}") # Returnera en dykare baserat på diver id
def get_freediver_by_id(id: int):
    data = db.get(table="freedivers", where=("id", str(id)))
    return data
  
@app.get("/freediver_by_name/{name}") # Returnera en dykare baserat på dykarens namn
def get_freediver_by_name(name: str):
    data = db.get(table="freedivers", where=("first_name", name))
    return data

@app.get("/dive_logs") # Returnera en lista med alla loggade dyk
def get_freedives():
    data = db.get(table="freedives")
    return data

@app.get("/dive_logs/{id}") # Returnera ett specifik dyk med tillhörande dyk id
def get_freedive_by_id(id:int):
    data = db.get(table="freedives", where=("id", str(id)))
    return data

# Minst 2 "routes/endpoints" för att skapa data (POST)
@app.post("/add_freediver") # Lägga till en ny dykare
def add_freediver(freediver: Freediver):
    freediver.id = app.curr_diver_id
    app.freedivers.append(freediver)
    app.curr_diver_id += 1
    db.insert(
        table="freedivers", 
        fields={
            "first_name": freediver.first_name, 
            "last_name": freediver.last_name, 
            "age": str(freediver.age)
        })

@app.post("/add_dive_log") # Logga ett nytt dyk
def log_freedive(freedive: FreediveLog):
    freedive.id = app.curr_dive_id
    app.freedives.append(freedive)
    app.curr_dive_id += 1
    db.insert(
        table="freedives",
        fields={
            "depth_m": str(freedive.depth_m),
            "discipline": freedive.discipline,
            "dive_time_sec": str(freedive.dive_time_sec),
            "down_speed_m_per_sec": str(freedive.down_speed_m_per_sec),
            "up_speed_m_per_sec": str(freedive.up_speed_m_per_sec),
            "dive_site": freedive.dive_site,
            "date": freedive.date,
            "diver_id":str(freedive.diver_id)
        })


# Minst 1 "route/endpoints" för att uppdatera data (PUT)  
@app.put("/update_freediver/{id}") # Uppdatera en dykares info
def update_freediver(freediver: UpdateFreediver):
    data = db.update(
        table="freedivers",
        fields={
            "first_name": freediver.first_name, 
            "last_name": freediver.last_name, 
            "age": str(freediver.age)},
        where=("id", str(freediver.id))
    )
    return data
 
@app.put("/update_dive_log/{id}") # Uppdatera ett redan loggat dyk
def update_freedive(freedive: UpdateFreediveLog):
    data = db.update(
        table="freedives",
        fields={
            "depth_m": str(freedive.depth_m),
            "discipline": freedive.discipline,
            "dive_time_sec": str(freedive.dive_time_sec),
            "down_speed_m_per_sec": str(freedive.down_speed_m_per_sec),
            "up_speed_m_per_sec": str(freedive.up_speed_m_per_sec),
            "dive_site": freedive.dive_site,
            "date": freedive.date,
            "diver_id":str(freedive.diver_id)},
        where=("id", str(freedive.id))
    )
    return data

# Minst 1 "route/endpoints" för att ta bort data (DELETE)
@app.delete("/delete_freediver/{id}") # Radera en dykare baserat på id
def delete_freediver(id):
    db.delete(table="freedivers", id=id)

@app.delete("/delete_dive_log/{id}") # Radera en dyk baserat på dive_id
def delete_freedive(id):
    db.delete(table="freedives", id=id)