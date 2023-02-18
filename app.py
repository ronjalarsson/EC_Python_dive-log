# Allt funkar per idag 20230218
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
        6: Add a new freediver
        7: Log a new dive
        8: Update a diver info
        9: Update a logged dive
        10: Delete a freediver by ID
        11: Delete a logged dive by ID
        12: Exit dive log
        """
    )

def get_all_freedivers():
    #freedivers = []
    print("Getting a list of all divers...")
    res = requests.get(url("/freedivers"))
    if not res.status_code == 200:
        return

    data = res.json()
    for freediver in data:
        freediver = Freediver(id=freediver["id"], first_name=freediver["first_name"], last_name=freediver["last_name"], age=freediver["age"])
        print("__________")
        print(f"Diver ID: {freediver.id}")
        print(f"Name: {freediver.first_name} {freediver.last_name}")
        print(f"Age: {freediver.age}")
        freedivers.append(freediver)
    return freedivers

def get_diver_by_id():
    diver_to_get = input("Please enter diver ID: ")
    print("Getting your data ready...")
    res = requests.get(url(f"/freediver_by_id/{diver_to_get}"))
    if res.status_code == 404:
        print("Freediver not found.")
        return
    if not str.isdigit(diver_to_get):
        print("You did not enter a valid diver ID.")
        return

    data = res.json()
    if not data:
        print("Freediver with this ID not found.")
        return

    for info in data:
        freediver = Freediver(id=info["id"], first_name=info["first_name"], last_name=info["last_name"], age=info["age"])    
        print("__________")
        print(f"Diver ID: {freediver.id}")
        print(f"Name: {freediver.first_name} {freediver.last_name}")
        print(f"Age: {freediver.age}")
        

def get_diver_by_name():
    diver_to_get = input("Please enter the first name of the freediver: ")
    diver_to_get = diver_to_get.strip().capitalize()
    print("Getting your data ready...")
    res = requests.get(url(f"/freediver_by_name/{diver_to_get}"))
    if res.status_code == 404:
        print("Freediver not found.")
        return

    data = res.json()
    if not data:
        print("Freediver with this name not found.")
        return

    for info in data:
        freediver = Freediver(id=info["id"], first_name=info["first_name"], last_name=info["last_name"], age=info["age"])    
        print("__________")
        print(f"Diver ID: {freediver.id}")
        print(f"Name: {freediver.first_name} {freediver.last_name}")
        print(f"Age: {freediver.age}")

def get_all_dives():
    #freedives = []
    print("Getting a list of all logged dives...")
    res = requests.get(url("/dive_logs")) 
    if not res.status_code == 200:
        return
        
    data = res.json()
    for dive in data:
        dive = FreediveLog(id=dive["id"], depth_m=dive["depth_m"], discipline=dive["discipline"], dive_time_sec=dive["dive_time_sec"], down_speed_m_per_sec=dive["down_speed_m_per_sec"], up_speed_m_per_sec=dive["up_speed_m_per_sec"], dive_site=dive["dive_site"], date=dive["date"], diver_id=dive["diver_id"])
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
        freedives.append(dive)
    return freedives

def get_dive_by_id():
    dive_to_get = input("Please enter dive ID: ")
    print("Getting your data ready...")
    res = requests.get(url(f"/dive_logs/{dive_to_get}"))
    if res.status_code == 404:
        print("This logged dive not found.")
        return
    if not str.isdigit(dive_to_get):
        print("You did not enter a valid dive ID.")
        return
   
    data = res.json()
    if not data:
        print("There is not a log with this dive ID.")
        return

    for info in data:
        dive = FreediveLog(id=info["id"], depth_m=info["depth_m"], discipline=info["discipline"], dive_time_sec=info["dive_time_sec"], down_speed_m_per_sec=info["down_speed_m_per_sec"], up_speed_m_per_sec=info["up_speed_m_per_sec"], dive_site=info["dive_site"], date=info["date"], diver_id=info["diver_id"])
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

def add_new_freediver():
    print("Please enter below information for the new diver.")
    print("__________")
    first_name = input("First Name: ")
    last_name = input("Last name: ")
    age = input("Age: ")
    new_freediver = Freediver(first_name=first_name, last_name=last_name, age=age) # id skapas automatiskt
    requests.post(url("/add_freediver"), json=new_freediver.dict())
    print("__________")
    print(f"{first_name} {last_name} has been added into the register.")
    
def log_new_dive():
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
    new_dive_log = FreediveLog(depth_m=depth_m, discipline=discipline, dive_time_sec=dive_time_sec, down_speed_m_per_sec=down_speed_m_per_sec, up_speed_m_per_sec=up_speed_m_per_sec, dive_site=dive_site, date=date, diver_id=diver_id) # id skapas automatiskt
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
    
    index = None
    for i, freediver in enumerate(freedivers):
        #print(str(freediver.id) + ": " + freediver.first_name + " " + freediver.last_name)
        if freediver.id == int(diver_to_update):
            index = i
            break

    if index is None:
        print("There is not a diver with this ID.")
        return
    
    # Ändra freediver format till dictionary
    freediver = freedivers[i].dict()
    #print(freediver)

    # Hämta ny info från användaren
    print("__________")
    f_name = input("First name (leave blank if no change): ")
    l_name = input("Last name (leave blank if no change): ")
    age = input("Age (leave blank if no change): ")

    # Uppdatera ny info
    if f_name != "":
        freediver["first_name"] = f_name
    if l_name != "":
        freediver["last_name"] = l_name
    if age != "":
        freediver["age"] = age
    #print(freediver)

    res = requests.put(url(f"/update_freediver/{diver_to_update}"), json=freediver)
    if res.status_code == 200:
        print("Freediver info updated successfully.")
    else:
        print("Failed to update freediver info.")

def update_dive(freedives: List[UpdateFreediveLog]):
    print("__________")
    print("You are requesting to update info about a logged dive...")
    dive_to_update = input("Enter the dive ID of the log you want to update: ")
    if not str.isdigit(dive_to_update):
        print("You did not enter a valid dive ID.")
        return

    index = None
    for i, dive in enumerate(freedives):
        #print(str(dive.id))
        if dive.id == int(dive_to_update):
            index = i
            break

    if index is None:
        print("There is not a dive with this ID.")
        return
    
    # Ändra dive format till dictionary
    dive = freedives[i].dict()
    #print(dive)

    # Hämta ny info från användaren
    print("__________")
    diver_id = input(f"Diver ID (leave blank if no change): ")
    depth_m = input(f"Depth in meter (leave blank if no change): ")
    discipline = input(f"Discipline (leave blank if no change): ")
    dive_time_sec = input(f"Dive time in seconds (leave blank if no change): ")
    down_speed_m_per_sec = input(f"Down speed m/s (leave blank if no change): ")
    up_speed_m_per_sec = input(f"Up speed m/s (leave blank if no change): ")
    dive_site = input(f"Dive site (leave blank if no change): ")
    date = input(f"Date (leave blank if no change): ")

    # Uppdatera ny info
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
    #print(dive)

    res = requests.put(url(f"/update_dive_log/{dive_to_update}"), json=dive)
    if res.status_code == 200:
        print("Dive log updated successfully.")
    else:
        print("Failed to update dive log.")

def delete_freediver():
    print("You are about to delete a freediver in the register...")
    diver_to_delete = input("Please enter the diver ID of the freediver you want to delete: ")
    if not str.isdigit(diver_to_delete):
        print("You did not enter a valid diver ID.")
        return
    requests.delete(url(f"/delete_freediver/{diver_to_delete}"))
    print(f"You have sucessefully deleted freediver with ID {diver_to_delete}.")

def delete_dive():
    print("You are about to delete a logged dive in the register...")
    log_to_delete = input("Please enter the dive ID of the logged dive you want to delete: ")
    if not str.isdigit(log_to_delete):
        print("You did not enter a valid dive ID.")
        return
    requests.delete(url(f"/delete_dive_log/{log_to_delete}"))
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
            add_new_freediver()

        case 7:
            log_new_dive()

        case 8:
            freediver = get_all_freedivers()
            update_freediver(freediver)
    
        case 9:
            dive = get_all_dives()
            update_dive(dive)

        case 10:
            delete_freediver()

        case 11:
            delete_dive()

        case 12:
            exit() # Lämna programmet, inbyggt funktion

        case __:
            # Be användaren att ange korrekt värde om hen angett nån annan siffra eller sträng
            print("Please enter a valid option.")

while __name__ == "__main__":
    main()