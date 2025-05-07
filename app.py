import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import sqlite3
import os

from database import init_db, store_readings, get_readings_by_timeframe, get_latest_readings
from mock_data import generate_mock_data
from sensor import read_serial_data
from anomaly_detection import detect_anomalies
from visualization import (
    plot_real_time_temperature, 
    plot_real_time_humidity, 
    plot_historical_temperature,
    plot_historical_humidity,
    plot_temperature_statistics,
    plot_humidity_statistics
)
from utils import export_to_csv

# App configuration
st.set_page_config(
    page_title="Warehouse Temperature Monitoring",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Session state initialization
if 'use_real_sensors' not in st.session_state:
    st.session_state.use_real_sensors = False

if 'monitoring_active' not in st.session_state:
    st.session_state.monitoring_active = False

if 'anomaly_threshold' not in st.session_state:
    st.session_state.anomaly_threshold = 3.0  # Default value

if 'alert_threshold_temp_min' not in st.session_state:
    st.session_state.alert_threshold_temp_min = 15.0  # Default minimum temperature

if 'alert_threshold_temp_max' not in st.session_state:
    st.session_state.alert_threshold_temp_max = 30.0  # Default maximum temperature

if 'alert_threshold_humid_min' not in st.session_state:
    st.session_state.alert_threshold_humid_min = 30.0  # Default minimum humidity

if 'alert_threshold_humid_max' not in st.session_state:
    st.session_state.alert_threshold_humid_max = 70.0  # Default maximum humidity

# Sidebar
st.sidebar.title("Settings")

# Data source selection
data_source = st.sidebar.radio(
    "Data Source",
    ["Mock Data", "Serial Port"],
    index=0 if not st.session_state.use_real_sensors else 1
)
st.session_state.use_real_sensors = (data_source == "Serial Port")

# Serial port configuration (if real sensors selected)
if st.session_state.use_real_sensors:
    serial_port = st.sidebar.text_input("Serial Port", "/dev/ttyUSB0")
    baud_rate = st.sidebar.selectbox("Baud Rate", [9600, 19200, 38400, 57600, 115200], index=0)
else:
    st.sidebar.info("Using mock data for demonstration")

# Alert thresholds
st.sidebar.subheader("Alert Thresholds")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.session_state.alert_threshold_temp_min = st.number_input(
        "Min Temp (°C)", 
        value=st.session_state.alert_threshold_temp_min,
        step=0.5
    )
    st.session_state.alert_threshold_humid_min = st.number_input(
        "Min Humidity (%)", 
        value=st.session_state.alert_threshold_humid_min,
        step=1.0
    )
with col2:
    st.session_state.alert_threshold_temp_max = st.number_input(
        "Max Temp (°C)", 
        value=st.session_state.alert_threshold_temp_max,
        step=0.5
    )
    st.session_state.alert_threshold_humid_max = st.number_input(
        "Max Humidity (%)", 
        value=st.session_state.alert_threshold_humid_max,
        step=1.0
    )

# Anomaly detection settings
st.sidebar.subheader("Anomaly Detection")
st.session_state.anomaly_threshold = st.sidebar.slider(
    "Anomaly Sensitivity", 
    min_value=1.0, 
    max_value=5.0, 
    value=st.session_state.anomaly_threshold,
    step=0.1,
    help="Lower values detect more anomalies (more sensitive)"
)

# Historical data timeframe
st.sidebar.subheader("Historical Data")
timeframe = st.sidebar.selectbox(
    "Timeframe",
    ["Last Hour", "Last 6 Hours", "Last 12 Hours", "Last Day", "Last Week", "Last Month", "All Data"],
    index=3
)

# Start/Stop monitoring
monitoring_button = st.sidebar.button(
    "Stop Monitoring" if st.session_state.monitoring_active else "Start Monitoring"
)
if monitoring_button:
    st.session_state.monitoring_active = not st.session_state.monitoring_active

# Export data
if st.sidebar.button("Export Data"):
    timeframe_dict = {
        "Last Hour": 1,
        "Last 6 Hours": 6,
        "Last 12 Hours": 12,
        "Last Day": 24,
        "Last Week": 24*7,
        "Last Month": 24*30,
        "All Data": 0
    }
    hours = timeframe_dict[timeframe]
    data = get_readings_by_timeframe(hours)
    if not data.empty:
        csv = export_to_csv(data)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"temperature_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.warning("No data available to export")

# Main content
st.title("Warehouse Temperature Monitoring System")

# Real-time monitoring section
st.header("Real-time Monitoring")

# Display the current status
status_container = st.container()

# Create placeholders for real-time charts
col1, col2 = st.columns(2)
with col1:
    temp_chart_placeholder = st.empty()
with col2:
    humidity_chart_placeholder = st.empty()

# Historical data section
st.header("Historical Data Analysis")

# Create placeholders for historical charts
col1, col2 = st.columns(2)
with col1:
    hist_temp_chart_placeholder = st.empty()
with col2:
    hist_humidity_chart_placeholder = st.empty()

# Statistics section
st.header("Statistics & Anomaly Detection")
col1, col2 = st.columns(2)
with col1:
    temp_stats_placeholder = st.empty()
with col2:
    humidity_stats_placeholder = st.empty()

# Get timeframe in hours
def get_hours_from_timeframe(timeframe):
    if timeframe == "Last Hour":
        return 1
    elif timeframe == "Last 6 Hours":
        return 6
    elif timeframe == "Last 12 Hours":
        return 12
    elif timeframe == "Last Day":
        return 24
    elif timeframe == "Last Week":
        return 24*7
    elif timeframe == "Last Month":
        return 24*30
    else:  # All Data
        return 0

# Main app loop
while st.session_state.monitoring_active:
    try:
        # Get current time
        current_time = datetime.now()
        
        # Read data from source
        if st.session_state.use_real_sensors:
            try:
                temperature, humidity = read_serial_data(serial_port, baud_rate)
            except Exception as e:
                status_container.error(f"Error reading from serial port: {e}")
                temperature, humidity = None, None
        else:
            temperature, humidity = generate_mock_data()
        
        # Store data if valid
        if temperature is not None and humidity is not None:
            store_readings(current_time, temperature, humidity)
            
            # Get latest readings for real-time display
            latest_data = get_latest_readings(30)  # Last 30 readings
            
            # Get historical data based on selected timeframe
            hours = get_hours_from_timeframe(timeframe)
            historical_data = get_readings_by_timeframe(hours)
            
            # Check for anomalies
            temp_anomalies, humid_anomalies = detect_anomalies(historical_data, st.session_state.anomaly_threshold)
            
            # Update status
            with status_container:
                status_cols = st.columns(4)
                
                # Current temperature
                with status_cols[0]:
                    st.metric(
                        "Current Temperature", 
                        f"{temperature:.1f} °C",
                        delta=f"{temperature - latest_data['temperature'].iloc[-2] if len(latest_data) > 1 else 0:.1f} °C"
                    )
                    
                # Current humidity
                with status_cols[1]:
                    st.metric(
                        "Current Humidity", 
                        f"{humidity:.1f} %",
                        delta=f"{humidity - latest_data['humidity'].iloc[-2] if len(latest_data) > 1 else 0:.1f} %"
                    )
                
                # Anomaly status
                with status_cols[2]:
                    if not temp_anomalies.empty:
                        st.error("⚠️ Temperature anomaly detected!")
                    else:
                        st.success("✅ Temperature normal")
                
                with status_cols[3]:
                    if not humid_anomalies.empty:
                        st.error("⚠️ Humidity anomaly detected!")
                    else:
                        st.success("✅ Humidity normal")
                
                # Alert based on thresholds
                if (temperature < st.session_state.alert_threshold_temp_min or 
                    temperature > st.session_state.alert_threshold_temp_max):
                    st.warning(f"⚠️ Temperature outside acceptable range: {st.session_state.alert_threshold_temp_min} - {st.session_state.alert_threshold_temp_max} °C")
                
                if (humidity < st.session_state.alert_threshold_humid_min or 
                    humidity > st.session_state.alert_threshold_humid_max):
                    st.warning(f"⚠️ Humidity outside acceptable range: {st.session_state.alert_threshold_humid_min} - {st.session_state.alert_threshold_humid_max} %")
            
            # Update real-time charts
            with temp_chart_placeholder:
                plot_real_time_temperature(latest_data, 
                                         st.session_state.alert_threshold_temp_min,
                                         st.session_state.alert_threshold_temp_max)
                
            with humidity_chart_placeholder:
                plot_real_time_humidity(latest_data,
                                      st.session_state.alert_threshold_humid_min,
                                      st.session_state.alert_threshold_humid_max)
                
            # Update historical charts
            with hist_temp_chart_placeholder:
                plot_historical_temperature(historical_data)
                
            with hist_humidity_chart_placeholder:
                plot_historical_humidity(historical_data)
                
            # Update statistics
            with temp_stats_placeholder:
                plot_temperature_statistics(historical_data, temp_anomalies)
                
            with humidity_stats_placeholder:
                plot_humidity_statistics(historical_data, humid_anomalies)
                
        else:
            status_container.warning("No valid data received")
            
        # Wait before next update
        time.sleep(3)
        
        # Refresh the app
        st.rerun()
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
        time.sleep(5)
        st.session_state.monitoring_active = False
        st.rerun()

if not st.session_state.monitoring_active:
    status_container.info("Monitoring is currently inactive. Press 'Start Monitoring' to begin.")
