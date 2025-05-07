import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# Database file name
DB_FILE = "warehouse_temperature.db"

def init_db():
    """Initialize the database with required tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create table for temperature and humidity readings
    c.execute('''
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def store_readings(timestamp, temperature, humidity):
    """Store temperature and humidity readings in the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute(
        "INSERT INTO sensor_readings (timestamp, temperature, humidity) VALUES (?, ?, ?)",
        (timestamp, temperature, humidity)
    )
    
    conn.commit()
    conn.close()

def get_readings_by_timeframe(hours=24):
    """
    Retrieve readings from a specific timeframe.
    
    Args:
        hours (int): Number of hours to look back. If 0, returns all data.
        
    Returns:
        pandas.DataFrame: DataFrame containing the readings
    """
    conn = sqlite3.connect(DB_FILE)
    
    if hours > 0:
        # Calculate the start time
        start_time = datetime.now() - timedelta(hours=hours)
        query = "SELECT * FROM sensor_readings WHERE timestamp >= ? ORDER BY timestamp"
        df = pd.read_sql_query(query, conn, params=(start_time,))
    else:
        # Get all data
        query = "SELECT * FROM sensor_readings ORDER BY timestamp"
        df = pd.read_sql_query(query, conn)
    
    conn.close()
    
    # Convert timestamp to datetime
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

def get_latest_readings(count=1):
    """
    Retrieve the latest readings from the database.
    
    Args:
        count (int): Number of latest readings to retrieve
        
    Returns:
        pandas.DataFrame: DataFrame containing the latest readings
    """
    conn = sqlite3.connect(DB_FILE)
    
    query = f"SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT {count}"
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    
    # Convert timestamp to datetime and sort by timestamp
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
    
    return df

def clear_old_data(days=30):
    """Delete data older than specified days to manage database size."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Calculate cutoff date
    cutoff_date = datetime.now() - timedelta(days=days)
    
    c.execute("DELETE FROM sensor_readings WHERE timestamp < ?", (cutoff_date,))
    
    conn.commit()
    conn.close()
    
    return c.rowcount  # Return number of deleted rows
