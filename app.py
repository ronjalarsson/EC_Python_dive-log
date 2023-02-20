# Allt funkar när man kör programmet i terminalen per idag 20230220
from typing import List 
# requests gör att vi kan koppla på API med funktionerna i denna fil
import requests
from models import Freediver, FreediveLog, UpdateFreediver, UpdateFreediveLog

freedivers: List[Freediver] = []
curr_diver_id = 1

freedives: List[FreediveLog] = []
curr_dive_id = 1

# Denna funktion gör att vi kan skicka url med korrekt route till requests funtionernan nedan
def url(route:str):
    return f"http://127.0.0.1:8000{route}"

def print_menu():
    print(
        """
        1: Get all freedivers
        2: Get a freediver by ID
        3: Get a freediver by name
        4: Get all logged dives
        5: Get a dive by ID
        6: Get all logged dives from a selected freediver by ID
        7: Add a new freediver
        8: Log a new dive
        9: Update a freediver info
        10: Update a logged dive
        11: Delete a freediver by ID
        12: Delete a logged dive by ID
        13: Exit dive log
        """
    )

def get_all_freedivers():
    # Skickar GET request till /freedivers endpoint
    print("Getting a list of all divers...")
    res = requests.get(url("/freedivers"))

    # Om request inte returnerar statuskoden 200, returnera None
    if not res.status_code == 200:
        return None

    # Konverterar res till json och sparar i variablen data
    data = res.json()

    # För varje freediver i variablen data, skapar en Freediver objekt och printar ut deras info
    for freediver in data:
        freediver = Freediver(id=freediver["id"], first_name=freediver["first_name"], last_name=freediver["last_name"], age=freediver["age"])
        print("__________")
        print(f"Diver ID: {freediver.id}")
        print(f"Name: {freediver.first_name} {freediver.last_name}")
        print(f"Age: {freediver.age}")
        # Nedan kod behövs för att funktionen update_freediver ska fungera
        freedivers.append(freediver)
    return freedivers

def get_diver_by_id():
    # Ber användaren om input diver ID
    diver_to_get = input("Please enter diver ID: ")

    # Kollar om dykare finns i db
    print("Getting your data ready...")
    res = requests.get(url(f"/freediver_by_id/{diver_to_get}"))
    if res.status_code == 404:
        print("__________")
        print("Freediver not found.")
        return
    if not str.isdigit(diver_to_get):
        print("__________")
        print("You did not enter a valid diver ID.")
        return

    # Konverterar res till json och sparar i variablen data
    data = res.json()
    # Om input värde inte finns
    if not data:
        print("__________")
        print("Freediver with this ID not found.")
        return

    for info in data:
        # Skapar en en Freediver objekt för efterfrågad dykare
        freediver = Freediver(id=info["id"], first_name=info["first_name"], last_name=info["last_name"], age=info["age"])    
        # Printar ut info om efterfrågad dykare
        print("__________")
        print(f"Diver ID: {freediver.id}")
        print(f"Name: {freediver.first_name} {freediver.last_name}")
        print(f"Age: {freediver.age}")
        
def get_diver_by_name():
    # Ber användaren om input första namnet för dykaren
    diver_to_get = input("Please enter the first name of the freediver: ")
    # Tar bort whitespaces om det finns och gör inputen till en capitalized sträng t.ex: ronja till Ronja
    diver_to_get = diver_to_get.strip().capitalize()

    # Kollar om dykare finns i db
    print("Getting your data ready...")
    res = requests.get(url(f"/freediver_by_name/{diver_to_get}"))
    if res.status_code == 404:
        print("__________")
        print("Freediver not found.")
        return

    # Konverterar res till json och sparar i variablen data
    data = res.json()
    # Om input värde inte finns
    if not data:
        print("__________")
        print("Freediver with this name not found.")
        return

    for info in data:
        # Skapar en en Freediver objekt för efterfrågad dykare
        freediver = Freediver(id=info["id"], first_name=info["first_name"], last_name=info["last_name"], age=info["age"]) 
        # Printar ut info om efterfrågad dykare   
        print("__________")
        print(f"Diver ID: {freediver.id}")
        print(f"Name: {freediver.first_name} {freediver.last_name}")
        print(f"Age: {freediver.age}")

def get_all_dives():
    # Skickar GET request till /dive_logs endpoint
    print("Getting a list of all logged dives...")
    res = requests.get(url("/dive_logs")) 

    # Om request inte returnerar statuskoden 200, returnera None
    if not res.status_code == 200:
        return None
    
    # Konverterar res till json och sparar i variablen data
    data = res.json()

    # För varje dyk i variablen data
    for dive in data:
        # Konverterar "None" sträng till None datatyp för down_speed_m_per_sec och up_speed_m_per_sec om "None" sräng finns
        if dive["down_speed_m_per_sec"] == "None":
            dive["down_speed_m_per_sec"] = None
        if dive["up_speed_m_per_sec"] == "None":
            dive["up_speed_m_per_sec"] = None

        # Skapar FreedivLog objekt
        dive = FreediveLog(id=dive["id"], depth_m=dive["depth_m"], discipline=dive["discipline"], dive_time_sec=dive["dive_time_sec"], down_speed_m_per_sec=dive["down_speed_m_per_sec"], up_speed_m_per_sec=dive["up_speed_m_per_sec"], dive_site=dive["dive_site"], date=dive["date"], diver_id=dive["diver_id"])
        # Printar ut info om dyk
        print("__________")
        print(f"Dive ID: {dive.id}")
        print(f"Diver ID: {dive.diver_id}")
        print(f"Depth in meter: {dive.depth_m}")
        print(f"Discipline: {dive.discipline}")
        print(f"Dive time in seconds: {dive.dive_time_sec}")
        print(f"Down speed m/s: {dive.down_speed_m_per_sec}")
        print(f"Up speed m/s: {dive.up_speed_m_per_sec}")
        print(f"Dive site: {dive.dive_site}")
        print(f"Date: {dive.date}")
        # Nedan kod behövs för att funktionen update_freedive ska fungera
        freedives.append(dive)
    return freedives

def get_dive_by_id():
    # Ber användarens input om dive ID
    dive_to_get = input("Please enter dive ID: ")

    # Kollar om det finns ett dyk med inputen dive ID
    print("Getting your data ready...")
    res = requests.get(url(f"/dive_logs/{dive_to_get}"))
    if res.status_code == 404:
        print("__________")
        print("This logged dive not found.")
        return
    if not str.isdigit(dive_to_get):
        print("__________")
        print("You did not enter a valid dive ID.")
        return
    
    # Konverterar res till json och sparar i data
    data = res.json()
    # Om input värde inte finns
    if not data:
        print("__________")
        print("There is not a log with this dive ID.")
        return

    # För varje info sparad i data av vald dive ID
    for info in data:
    # Konverterar "None" sträng till None datatyp för down_speed_m_per_sec och up_speed_m_per_sec om "None" sräng finns
        if info["down_speed_m_per_sec"] == "None":
            info["down_speed_m_per_sec"] = None
        if info["up_speed_m_per_sec"] == "None":
            info["up_speed_m_per_sec"] = None

        # Skapar FreedivLog objekt
        dive = FreediveLog(id=info["id"], depth_m=info["depth_m"], discipline=info["discipline"], dive_time_sec=info["dive_time_sec"], down_speed_m_per_sec=info["down_speed_m_per_sec"], up_speed_m_per_sec=info["up_speed_m_per_sec"], dive_site=info["dive_site"], date=info["date"], diver_id=info["diver_id"])
        # Printar ut info om dyk
        print("__________")
        print(f"Diver ID: {dive.diver_id}")
        print(f"Dive ID: {dive.id}")
        print(f"Depth in meter: {dive.depth_m}")
        print(f"Discipline: {dive.discipline}")
        print(f"Dive time in seconds: {dive.dive_time_sec}")
        print(f"Down speed m/s: {dive.down_speed_m_per_sec}")
        print(f"Up speed m/s: {dive.up_speed_m_per_sec}")
        print(f"Dive site: {dive.dive_site}")
        print(f"Date: {dive.date}")

def get_freedives_by_freediver():
    # Ber om anväändarens input diver ID
    dives_to_get = input("Please enter diver ID: ")

    # Kollar om data finns i db
    print("Getting your data ready...")
    res = requests.get(url(f"/dive_logs_by_freediver/{dives_to_get}"))
    if res.status_code == 404:
        print("__________")
        print("Dives not found.")
        return
    if not str.isdigit(dives_to_get):
        print("__________")
        print("You did not enter a valid diver ID.")
        return

    # Konverterar res till json och sparar i data
    data = res.json()
    # Om input värde inte finns
    if not data:
        print("__________")
        print("There is no dive registered with this diver ID.")
        return

    # För varje dyk sparad i data variablen
    for dive in data:
        # Konverterar "None" sträng till None datatyp för down_speed_m_per_sec och up_speed_m_per_sec
        if dive["down_speed_m_per_sec"] == "None":
            dive["down_speed_m_per_sec"] = None
        if dive["up_speed_m_per_sec"] == "None":
            dive["up_speed_m_per_sec"] = None

        # Skapar FreedivLog objekt
        dive = FreediveLog(id=dive["id"], depth_m=dive["depth_m"], discipline=dive["discipline"], dive_time_sec=dive["dive_time_sec"], down_speed_m_per_sec=dive["down_speed_m_per_sec"], up_speed_m_per_sec=dive["up_speed_m_per_sec"], dive_site=dive["dive_site"], date=dive["date"], diver_id=dive["diver_id"])
        # Printar ut alla dyk för efterfrügad dykare
        print("__________")
        print(f"Dive ID: {dive.id}")
        print(f"Diver ID: {dive.diver_id}")
        print(f"Depth in meter: {dive.depth_m}")
        print(f"Discipline: {dive.discipline}")
        print(f"Dive time in seconds: {dive.dive_time_sec}")
        print(f"Down speed m/s: {dive.down_speed_m_per_sec}")
        print(f"Up speed m/s: {dive.up_speed_m_per_sec}")
        print(f"Dive site: {dive.dive_site}")
        print(f"Date: {dive.date}")

def add_new_freediver():
    # Ber användare input för dykarens info
    print("Please enter below information for the new diver.")
    print("__________")
    first_name = input("First Name: ")
    last_name = input("Last name: ")
    age = input("Age: ")

    # Skapar en ny dykare objekt med vad användaren skriver in
    new_freediver = Freediver(first_name=first_name, last_name=last_name, age=age) # id skapas automatiskt

    # Skickar post request till /add_freediver endpoint
    requests.post(url("/add_freediver"), json=new_freediver.dict())
    print("__________")
    print(f"{first_name} {last_name} has been added into the register.")
    
def log_new_dive():
    # Ber användare input för info om det nya dykloggen
    print("Please enter your dive data...")
    print("__________")
    diver_id = input("Diver ID: ")
    depth_m = input("Depth in meter: ")
    discipline = input("Discipline: ")
    dive_time_sec = input("Dive time in seconds: ")
    down_speed_m_per_sec = input("Down speed m/s: ")
    up_speed_m_per_sec = input("Up speed m/s: ")
    dive_site = input("Dive site: ")
    date = input("Date: ")
    
    # Skapar en ny dyklog objekt med vad användaren skriver in
    new_dive_log = FreediveLog(depth_m=depth_m, discipline=discipline, dive_time_sec=dive_time_sec, down_speed_m_per_sec=down_speed_m_per_sec, up_speed_m_per_sec=up_speed_m_per_sec, dive_site=dive_site, date=date, diver_id=diver_id) # id skapas automatiskt
    
    # Skickar post request till /add_dive_log endpoint
    requests.post(url("/add_dive_log"), json=new_dive_log.dict())
    print("__________")
    print("The new dive has been logged into the register.")
  
def update_freediver(freedivers: List[UpdateFreediver]):
    print("__________")
    print("You are requesting to update info about a freediver...")
    diver_to_update = input("Enter the ID of the freediver you want to update: ")
    if not str.isdigit(diver_to_update):
        print("You did not enter a valid diver ID.")
        return
    
    # Kollar om användaren input finns i db
    index = None
    for i, freediver in enumerate(freedivers):
        if freediver.id == int(diver_to_update):
            index = i
            break

    if index is None:
        print("__________")
        print("There is not a diver with this ID.")
        return
    
    # Ändrar freediver format till dictionary
    freediver = freedivers[i].dict()

    # Hämtar ny info från användaren
    print("__________")
    f_name = input("First name (leave blank if no change): ")
    l_name = input("Last name (leave blank if no change): ")
    age = input("Age (leave blank if no change): ")

    # Uppdaterar ny info
    if f_name != "":
        freediver["first_name"] = f_name
    if l_name != "":
        freediver["last_name"] = l_name
    if age != "":
        freediver["age"] = age

    res = requests.put(url(f"/update_freediver/{diver_to_update}"), json=freediver)
    if res.status_code == 200:
        print("__________")
        print("Freediver info updated successfully.")
    else:
        print("__________")
        print("Failed to update freediver info.")

def update_dive(freedives: List[UpdateFreediveLog]):
    print("__________")
    print("You are requesting to update info about a logged dive...")
    dive_to_update = input("Enter the dive ID of the log you want to update: ")
    if not str.isdigit(dive_to_update):
        print("You did not enter a valid dive ID.")
        return

    # Kollar om användaren input finns i db
    index = None
    for i, dive in enumerate(freedives):
        if dive.id == int(dive_to_update):
            index = i
            break

    if index is None:
        print("__________")
        print("There is not a dive with this ID.")
        return
    
    # Ändrar dive format till dictionary
    dive = freedives[i].dict()

    # Hämtar ny info från användaren
    print("__________")
    diver_id = input(f"Diver ID (leave blank if no change): ")
    depth_m = input(f"Depth in meter (leave blank if no change): ")
    discipline = input(f"Discipline (leave blank if no change): ")
    dive_time_sec = input(f"Dive time in seconds (leave blank if no change): ")
    down_speed_m_per_sec = input(f"Down speed m/s (leave blank if no change): ")
    up_speed_m_per_sec = input(f"Up speed m/s (leave blank if no change): ")
    dive_site = input(f"Dive site (leave blank if no change): ")
    date = input(f"Date (leave blank if no change): ")

    # Uppdaterar ny info
    if diver_id != "":
        dive["diver_id"] = diver_id
    if depth_m != "":
        dive["depth_m"] = depth_m
    if discipline != "":
        dive["discipline"] = discipline
    if dive_time_sec != "":
        dive["dive_time_sec"] = dive_time_sec
    if down_speed_m_per_sec != "":
        dive["down_speed_m_per_sec"] = down_speed_m_per_sec
    if up_speed_m_per_sec != "":
        dive["up_speed_m_per_sec"] = up_speed_m_per_sec
    if dive_site != "":
        dive["dive_site"] = dive_site
    if date != "":
        dive["date"] = date

    res = requests.put(url(f"/update_dive_log/{dive_to_update}"), json=dive)
    if res.status_code == 200:
        print("__________")
        print("Dive log updated successfully.")
    else:
        print("__________")
        print("Failed to update dive log.")

def delete_freediver():
    print("You are about to delete a freediver in the register...")
    diver_to_delete = input("Please enter the diver ID of the freediver you want to delete: ")
    if not str.isdigit(diver_to_delete):
        print("__________")
        print("You did not enter a valid diver ID.")
        return

    # Kollar om användaren input finns i db
    index = None
    for i, freediver in enumerate(freedivers):
        if freediver.id == int(diver_to_delete):
            index = i
            break

    if index is None:
        print("__________")
        print("There is not a diver with this ID.")
        return

    # Skickar delete request till /delete_freediver/input från användaren    
    requests.delete(url(f"/delete_freediver/{diver_to_delete}"))
    print("__________")
    print(f"You have sucessefully deleted freediver with ID {diver_to_delete}.")

def delete_dive():
    print("You are about to delete a logged dive in the register...")
    log_to_delete = input("Please enter the dive ID of the logged dive you want to delete: ")
    if not str.isdigit(log_to_delete):
        print("__________")
        print("You did not enter a valid dive ID.")
        return

    # Kollar om användaren input finns i db
    index = None
    for i, dive in enumerate(freedives):
        if dive.id == int(log_to_delete):
            index = i
            break

    if index is None:
        print("__________")
        print("There is not a dive with this ID.")
        return

    # Skickar delete request till /delete_dive_log/input från användaren  
    requests.delete(url(f"/delete_dive_log/{log_to_delete}"))
    print("__________")
    print(f"You have sucessefully deleted dive log with ID {log_to_delete}.")

def main():
    print("  ")
    print("Welcome to Ronja's dive log!") 
    print_menu()
    choice = input("Please choose your action: ")
    choice = choice.strip() # Tar bort whitespaces
    if not str.isdigit(choice): # Kollar om valet är en siffra, om inte kör nedan kod
        print("Please enter a valid option.")
        return
    
    match int(choice):
        case 1:
            freediver = get_all_freedivers()

        case 2:
            get_diver_by_id()

        case 3:
            get_diver_by_name()

        case 4:
            get_all_dives()

        case 5:
            get_dive_by_id()
        
        case 6:
            get_freedives_by_freediver()

        case 7:
            add_new_freediver()

        case 8:
            log_new_dive()

        case 9:
            freediver = get_all_freedivers()
            update_freediver(freediver)
    
        case 10:
            dive = get_all_dives()
            update_dive(dive)

        case 11:
            delete_freediver()

        case 12:
            delete_dive()

        case 13:
            exit() # Lämnar programmet, inbyggt funktion

        case __:
            # Ber användaren att ange korrekt värde om hen angett nån annan siffra eller sträng
            print("__________")
            print("Please enter a valid option.")

while __name__ == "__main__":
    main()