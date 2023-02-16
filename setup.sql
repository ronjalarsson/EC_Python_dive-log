CREATE TABLE freedivers (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER NOT NULL
    );

CREATE TABLE freedives (
        id INTEGER PRIMARY KEY,
        depth_m REAL NOT NULL,
        discipline TEXT NOT NULL,
        dive_time_sec INTEGER NOT NULL,
        down_speed_m_per_sec REAL,
        up_speed_m_per_sec REAL,
        dive_site TEXT, 
        date TEXT NOT NULL,
        diver_id INTEGER,
        FOREIGN KEY (diver_id) REFERENCES freedivers(id)
    );

