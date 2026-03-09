import sqlite3
import pandas as pd
import json
import os

DB_PATH = os.path.join('data', 'strava.db')
METRICS_PATH = os.path.join('data', 'metrics.json')

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM raw_activities", conn)
    conn.close()
    return df

def perform_transformations(df):
    print("Running transformations...")
    # Force UTC to avoid the comparison error
    df['start_date_local'] = pd.to_datetime(df['start_date_local'], utc=True)
    
    # Meters to Miles
    df['distance_miles'] = df['distance'] * 0.000621371
    
    # Validation
    df = df[df['distance_miles'] > 0.1].copy()
    
    # Pace calculation (Seconds per mile)
    df['pace_raw'] = df['moving_time'] / df['distance_miles']
    
    return df

def calculate_weekly_metrics(df):
    print("Calculating weekly analytics...")
    
    # Use UTC-aware "Now" to match the DataFrame
    now_utc = pd.Timestamp.now(tz='UTC')
    last_7_days = df[df['start_date_local'] > (now_utc - pd.Timedelta(days=7))]
    
    # Calculate Weekly Totals safely
    weekly_dist = last_7_days['distance_miles'].sum() if not last_7_days.empty else 0
    weekly_elev = (last_7_days['total_elevation_gain'].sum() * 3.28084) if not last_7_days.empty else 0
    avg_pace_raw = last_7_days['pace_raw'].mean() if not last_7_days.empty else 0

    # Helper to format seconds into MM:SS
    def format_seconds(s):
        if pd.isna(s) or s == 0: return "0:00"
        return f"{int(s//60)}:{int(s%60):02d}"

    # Prepare recent activities list safely
    recent = df.sort_values('start_date_local', ascending=False).head(5).copy()
    recent['date_display'] = recent['start_date_local'].dt.strftime("%b %d, %Y")
    recent['dist_display'] = recent['distance_miles'].round(2)
    
    metrics = {
        "last_updated": now_utc.strftime("%Y-%m-%d %H:%M UTC"),
        "weekly_stats": {
            "total_distance": round(weekly_dist, 2),
            "total_elevation_feet": int(weekly_elev),
            "activity_count": int(len(last_7_days)),
            "avg_pace": format_seconds(avg_pace_raw)
        },
        "recent_activities": recent[['name', 'dist_display', 'type', 'date_display']].to_dict(orient='records')
    }
    
    return metrics

if __name__ == "__main__":
    try:
        raw_df = load_data()
        if raw_df.empty:
            print("Database is empty. Run extract.py first.")
        else:
            clean_df = perform_transformations(raw_df)
            final_metrics = calculate_weekly_metrics(clean_df)
            
            os.makedirs('data', exist_ok=True)
            with open(METRICS_PATH, 'w') as f:
                json.dump(final_metrics, f, indent=4)
            
            print(f"Metrics exported to {METRICS_PATH}")
            
    except Exception as e:
        print(f"Transformation failed: {e}")
        import traceback
        traceback.print_exc() # This will tell us exactly which line failed