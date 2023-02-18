# Databaslogiken i denna fil
import sqlite3
import os
from typing import Tuple, Dict, List, Any

class DB:
    db_url: str #Det är en url som leder till db

    # Interna metoder som bara används inom DB class (denna fil)
    def __init__(self, db_url: str):
        self.db_url = db_url
        # Om db inte finns, sätt upp db med __set_up_db
        if not os.path.exists(self.db_url):
            self.__set_up_db()
    
    def __set_up_db(self): 
        conn = sqlite3.connect(self.db_url)
        with open("setup.sql", "r") as file: # Öppna sql filen setup.sql
            script = file.read() # Läser sql filen
            conn.executescript(script) # Kör sql filen i sqlite3
            conn.commit()
        conn.close()

    def __call_db(self, query, *args): 
        conn = sqlite3.connect(self.db_url)
        cur = conn.cursor()
        res = cur.execute(query, args)
        data = res.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return data

    def __get_columns(self, table: str) -> List[str]:
        query = f"""
        PRAGMA table_info({table}) 
        """ # PRAGMA används för att hämta info om en table, inklusive namn på kolumen
        data = self.__call_db(query)
        return [row[1] for row in data] # Returnerar en lista med kolumnnamen
    
    # Metoder som kan användas i andra filer (api.py)
    # Hämta data
    def get(self, *, table: str, where: Tuple[str, str] | None = None) -> List[Dict[str, Any]]: # where är optiopnal här
        query = f"""
        SELECT * 
        FROM {table}
        """
        if where: # Om where finns, kör nedan kod för att hämta specifikt efterfrågad data
            key, value = where
            query_with_where = f"""
            WHERE {key} = '{value}'
            """
            query = query + query_with_where
        data = self.__call_db(query)

        # Konverterar tupple list till dict med __get_columns metod
        columns = self.__get_columns(table)
        result = [dict(zip(columns, row)) for row in data] # zip används för att kombinera kolumnnamen med data
        return result
    
    # Skapa data/lägg till ny data
    def insert(self, *, table: str, fields: Dict[str, str]): 
        keys = ",".join(fields.keys())
        values = "','".join(fields.values())
        query = f"""
        INSERT INTO {table} (
            {keys}
        )
        VALUES (
            '{values}'
        )
        """
        data = self.__call_db(query)
        return data

    # Uppdatera data
    def update(self, *, table: str, where: Tuple[str, str], fields: Dict[str, str]):
        where_key, where_value = where
        field_query = ""
        for key, val in fields.items():
            if val == None or val == str(None): # Gör så att när man kommer till None värde i både str och int,
                continue # skippas iterationen och går vidare till nästa iteration = man ändrar alltså inte de värden
            field_query += f"{key} = '{val}',"
        field_query = field_query[:-1]
        update_query = f"""
        UPDATE {table} 
        SET {field_query} 
        WHERE {where_key} = '{where_value}' 
        """
        print(update_query)
        return self.__call_db(update_query)

    # Radera data
    def delete(self, *, table: str, id: int):
        delete_query = f"""
        DELETE FROM {table}
        WHERE id = {id}
        """
        self.__call_db(delete_query)