import random
import math
from datetime import datetime, timedelta
import numpy as np

# Global variables to maintain state between calls
last_temp = 23.0
last_humid = 50.0
time_offset = 0
trend_temp = 0
trend_humid = 0
seasonal_offset = 0

def generate_mock_data():
    """
    Generate realistic mock temperature and humidity data.
    
    Returns:
        tuple: (temperature, humidity) with realistic variations
    """
    global last_temp, last_humid, time_offset, trend_temp, trend_humid, seasonal_offset
    
    # Time progression
    time_offset += 1
    
    # Adjust seasonal factors (simulate day/night cycle)
    seasonal_offset = math.sin(time_offset / 100) * 3
    
    # Gradual trends (simulate slow weather changes)
    if random.random() < 0.02:  # 2% chance of changing trend
        trend_temp = random.uniform(-0.1, 0.1)
    if random.random() < 0.02:  # 2% chance of changing humidity trend
        trend_humid = random.uniform(-0.2, 0.2)
    
    # Apply trends
    last_temp += trend_temp
    last_humid += trend_humid
    
    # Apply seasonal factors
    last_temp += seasonal_offset * 0.1
    last_humid -= seasonal_offset * 0.2
    
    # Random fluctuation
    temp_fluctuation = random.uniform(-0.3, 0.3)
    humid_fluctuation = random.uniform(-0.5, 0.5)
    
    # Calculate final values with constraints
    temperature = max(min(last_temp + temp_fluctuation, 35.0), 15.0)  # Constrain between 15-35°C
    humidity = max(min(last_humid + humid_fluctuation, 90.0), 30.0)   # Constrain between 30-90%
    
    # Occasionally simulate anomalies (1% chance)
    if random.random() < 0.01:
        # Sudden temperature spike or drop
        temperature += random.choice([-5, -4, -3, 3, 4, 5])
    
    if random.random() < 0.01:
        # Sudden humidity spike or drop
        humidity += random.choice([-10, -8, -6, 6, 8, 10])
    
    # Update the last values for next iteration
    last_temp = temperature
    last_humid = humidity
    
    return round(temperature, 1), round(humidity, 1)

def generate_historical_mock_data(hours=24, interval_minutes=5):
    """
    Generate a set of historical mock data points.
    
    Args:
        hours (int): Number of hours to generate data for
        interval_minutes (int): Interval between data points in minutes
        
    Returns:
        tuple: (timestamps, temperatures, humidities)
    """
    global last_temp, last_humid, time_offset, trend_temp, trend_humid, seasonal_offset
    
    # Reset global variables to ensure consistent start
    last_temp = 23.0
    last_humid = 50.0
    time_offset = 0
    trend_temp = 0
    trend_humid = 0
    seasonal_offset = 0
    
    # Calculate how many data points to generate
    data_points = int((hours * 60) / interval_minutes)
    
    timestamps = []
    temperatures = []
    humidities = []
    
    current_time = datetime.now() - timedelta(hours=hours)
    
    for _ in range(data_points):
        temp, humid = generate_mock_data()
        
        timestamps.append(current_time)
        temperatures.append(temp)
        humidities.append(humid)
        
        current_time += timedelta(minutes=interval_minutes)
    
    return timestamps, temperatures, humidities
