import sqlite3

def init_strava_db():
    # This creates the file if it doesn't exist
    conn = sqlite3.connect('strava.db')
    cursor = conn.cursor()

    # Create a table for your activities
    # We use 'strava_id' as a unique key to prevent duplicate runs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            strava_id INTEGER PRIMARY KEY,
            name TEXT,
            distance REAL,
            moving_time INTEGER,
            elapsed_time INTEGER,
            total_elevation_gain REAL,
            type TEXT,
            start_date_local TEXT,
            average_speed REAL,
            max_speed REAL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Strava SQLite database initialized!")

if __name__ == "__main__":
    init_strava_db()