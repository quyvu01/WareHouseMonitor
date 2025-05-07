import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

def detect_anomalies(data, threshold=3.0):
    """
    Detect anomalies in temperature and humidity data.
    
    Args:
        data (pd.DataFrame): DataFrame containing 'timestamp', 'temperature', 'humidity'
        threshold (float): The threshold for anomaly detection (Z-score or contamination)
        
    Returns:
        tuple: (temperature_anomalies, humidity_anomalies) where each is a DataFrame
               containing the anomalous readings
    """
    if data.empty or len(data) < 10:  # Need enough data for meaningful detection
        return pd.DataFrame(), pd.DataFrame()
    
    # Create copies to avoid modifying original data
    temp_data = data.copy()
    humid_data = data.copy()
    
    # Method 1: Z-score detection
    if len(data) < 50:  # For smaller datasets, use Z-score
        # Calculate Z-scores
        temp_data['zscore'] = np.abs(stats.zscore(temp_data['temperature']))
        humid_data['zscore'] = np.abs(stats.zscore(humid_data['humidity']))
        
        # Identify anomalies based on Z-score threshold
        temp_anomalies = temp_data[temp_data['zscore'] > threshold]
        humid_anomalies = humid_data[humid_data['zscore'] > threshold]
    
    # Method 2: Isolation Forest for larger datasets
    else:
        # Prepare data for Isolation Forest
        temp_values = temp_data['temperature'].values.reshape(-1, 1)
        humid_values = humid_data['humidity'].values.reshape(-1, 1)
        
        # Set contamination parameter based on threshold
        # Lower threshold = higher sensitivity = more anomalies
        contamination = max(0.01, min(0.1, 1.0/threshold))
        
        # Initialize and fit the model for temperature
        temp_model = IsolationForest(contamination=contamination, random_state=42)
        temp_model.fit(temp_values)
        temp_data['anomaly'] = temp_model.predict(temp_values)
        
        # Initialize and fit the model for humidity
        humid_model = IsolationForest(contamination=contamination, random_state=42)
        humid_model.fit(humid_values)
        humid_data['anomaly'] = humid_model.predict(humid_values)
        
        # Extract anomalies (-1 indicates an anomaly)
        temp_anomalies = temp_data[temp_data['anomaly'] == -1]
        humid_anomalies = humid_data[humid_data['anomaly'] == -1]
    
    return temp_anomalies, humid_anomalies

def analyze_patterns(data, window_size=24):
    """
    Analyze temperature and humidity patterns over time.
    
    Args:
        data (pd.DataFrame): DataFrame containing 'timestamp', 'temperature', 'humidity'
        window_size (int): Window size for rolling statistics
        
    Returns:
        dict: Dictionary with analysis results
    """
    if data.empty or len(data) < window_size:
        return {
            'temp_trend': 'Insufficient data',
            'humid_trend': 'Insufficient data',
            'temp_stability': 'Insufficient data',
            'humid_stability': 'Insufficient data'
        }
    
    # Calculate rolling mean and standard deviation
    temp_rolling = data['temperature'].rolling(window=window_size)
    humid_rolling = data['humidity'].rolling(window=window_size)
    
    temp_mean = temp_rolling.mean().fillna(data['temperature'].mean())
    humid_mean = humid_rolling.mean().fillna(data['humidity'].mean())
    
    temp_std = temp_rolling.std().fillna(data['temperature'].std())
    humid_std = humid_rolling.std().fillna(data['humidity'].std())
    
    # Calculate trends
    temp_trend = 'Stable'
    humid_trend = 'Stable'
    
    if len(data) > window_size:
        # Linear regression for trend
        x = np.array(range(len(data))).reshape(-1, 1)
        
        # Temperature trend
        temp_slope = np.polyfit(x.flatten(), data['temperature'], 1)[0]
        if temp_slope > 0.05:
            temp_trend = 'Rising'
        elif temp_slope < -0.05:
            temp_trend = 'Falling'
        
        # Humidity trend
        humid_slope = np.polyfit(x.flatten(), data['humidity'], 1)[0]
        if humid_slope > 0.1:
            humid_trend = 'Rising'
        elif humid_slope < -0.1:
            humid_trend = 'Falling'
    
    # Stability assessment
    temp_stability = 'High'
    if data['temperature'].std() > 2.0:
        temp_stability = 'Low'
    elif data['temperature'].std() > 1.0:
        temp_stability = 'Medium'
    
    humid_stability = 'High'
    if data['humidity'].std() > 5.0:
        humid_stability = 'Low'
    elif data['humidity'].std() > 2.5:
        humid_stability = 'Medium'
    
    return {
        'temp_trend': temp_trend,
        'humid_trend': humid_trend,
        'temp_stability': temp_stability,
        'humid_stability': humid_stability,
        'temp_avg': data['temperature'].mean(),
        'humid_avg': data['humidity'].mean(),
        'temp_std': data['temperature'].std(),
        'humid_std': data['humidity'].std()
    }
