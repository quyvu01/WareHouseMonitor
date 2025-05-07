import pandas as pd
import io
import datetime
import sqlite3
import os

def export_to_csv(data):
    """
    Export data to CSV format.
    
    Args:
        data (pd.DataFrame): DataFrame to export
        
    Returns:
        str: CSV data as string
    """
    if data.empty:
        return ""
    
    # Create a copy of the data to avoid modifying the original
    export_data = data.copy()
    
    # Format timestamp for better readability
    if 'timestamp' in export_data.columns:
        export_data['timestamp'] = export_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Convert to CSV
    csv_buffer = io.StringIO()
    export_data.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def backup_database(db_file="warehouse_temperature.db", backup_dir="backups"):
    """
    Create a backup of the database.
    
    Args:
        db_file (str): Path to the database file
        backup_dir (str): Directory to store backups
        
    Returns:
        str: Path to backup file or None if backup failed
    """
    try:
        # Ensure backup directory exists
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Generate backup filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.db")
        
        # Connect to source database
        conn = sqlite3.connect(db_file)
        
        # Backup database to the new file
        with sqlite3.connect(backup_file) as backup_conn:
            conn.backup(backup_conn)
        
        # Close connections
        conn.close()
        
        return backup_file
    
    except Exception as e:
        print(f"Backup failed: {e}")
        return None

def calculate_statistics(data):
    """
    Calculate basic statistics from the data.
    
    Args:
        data (pd.DataFrame): DataFrame with 'temperature' and 'humidity' columns
        
    Returns:
        dict: Dictionary with calculated statistics
    """
    if data.empty:
        return {
            'temp_min': None,
            'temp_max': None,
            'temp_avg': None,
            'temp_median': None,
            'temp_std': None,
            'humid_min': None,
            'humid_max': None,
            'humid_avg': None,
            'humid_median': None,
            'humid_std': None
        }
    
    # Calculate statistics
    stats = {
        'temp_min': data['temperature'].min(),
        'temp_max': data['temperature'].max(),
        'temp_avg': data['temperature'].mean(),
        'temp_median': data['temperature'].median(),
        'temp_std': data['temperature'].std(),
        'humid_min': data['humidity'].min(),
        'humid_max': data['humidity'].max(),
        'humid_avg': data['humidity'].mean(),
        'humid_median': data['humidity'].median(),
        'humid_std': data['humidity'].std()
    }
    
    return stats

def format_datetime(dt):
    """
    Format datetime object to string.
    
    Args:
        dt (datetime): Datetime object to format
        
    Returns:
        str: Formatted datetime string
    """
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def parse_datetime(dt_str):
    """
    Parse datetime string to datetime object.
    
    Args:
        dt_str (str): Datetime string to parse
        
    Returns:
        datetime: Parsed datetime object
    """
    try:
        return datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            return datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return None
