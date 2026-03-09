import os
import sqlite3
from api_client import StravaClient

DB_PATH = os.path.join('data', 'strava.db')

def init_db():
    """Ensures the data directory exists and the SQLite table is ready."""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created 'data' directory.")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS raw_activities (
                id INTEGER PRIMARY KEY,
                name TEXT,
                distance REAL,
                moving_time INTEGER,
                elapsed_time INTEGER,
                total_elevation_gain REAL,
                type TEXT,
                sport_type TEXT,
                start_date_local TEXT,
                average_speed REAL,
                max_speed REAL
            )
        ''')
        conn.commit()
    print(f"Database initialized at {DB_PATH}")

def upsert_to_db(activities):
    """Inserts activities into SQLite. Updates existing ones if the ID matches."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        data_to_save = [
            (
                a['id'], a['name'], a['distance'], a['moving_time'],
                a['elapsed_time'], a['total_elevation_gain'], a['type'],
                a.get('sport_type', ''), a['start_date_local'],
                a['average_speed'], a['max_speed']
            ) for a in activities
        ]

        cursor.executemany('''
            INSERT OR REPLACE INTO raw_activities 
            (id, name, distance, moving_time, elapsed_time, total_elevation_gain, type, sport_type, start_date_local, average_speed, max_speed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data_to_save)
        
        conn.commit()
        print(f"Successfully synced {len(data_to_save)} activities.")

if __name__ == "__main__":
    try:
        init_db()
        
        # Look how clean this is now!
        client = StravaClient()
        raw_data = client.get_activities()
        
        upsert_to_db(raw_data)
        print("ETL Extraction Phase Complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)