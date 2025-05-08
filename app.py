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
    page_title="Hệ Thống Giám Sát Nhiệt Độ Kho Hàng",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Define global variables for serial connection
serial_port = "/dev/ttyUSB0"
baud_rate = 9600

# Session state initialization
if 'use_real_sensors' not in st.session_state:
    st.session_state.use_real_sensors = False

if 'monitoring_active' not in st.session_state:
    st.session_state.monitoring_active = False

# Store the serial configuration in session state
if 'serial_port' not in st.session_state:
    st.session_state.serial_port = serial_port
if 'baud_rate' not in st.session_state:
    st.session_state.baud_rate = baud_rate

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
st.sidebar.title("Cài Đặt")

# Data source selection
data_source = st.sidebar.radio(
    "Nguồn Dữ Liệu",
    ["Dữ Liệu Mẫu", "Cổng Serial"],
    index=0 if not st.session_state.use_real_sensors else 1
)
st.session_state.use_real_sensors = (data_source == "Cổng Serial")

# Serial port configuration (if real sensors selected)
if st.session_state.use_real_sensors:
    st.session_state.serial_port = st.sidebar.text_input("Cổng Serial", st.session_state.serial_port)
    st.session_state.baud_rate = st.sidebar.selectbox("Tốc Độ Baud", [9600, 19200, 38400, 57600, 115200], index=0)
else:
    st.sidebar.info("Đang sử dụng dữ liệu mẫu để demo")

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
st.sidebar.subheader("Phát Hiện Bất Thường")
st.session_state.anomaly_threshold = st.sidebar.slider(
    "Độ Nhạy Phát Hiện", 
    min_value=1.0, 
    max_value=5.0, 
    value=st.session_state.anomaly_threshold,
    step=0.1,
    help="Giá trị thấp hơn phát hiện nhiều bất thường hơn (độ nhạy cao hơn)"
)

# Historical data timeframe
st.sidebar.subheader("Dữ Liệu Lịch Sử")
timeframe = st.sidebar.selectbox(
    "Khoảng Thời Gian",
    ["1 Giờ Qua", "6 Giờ Qua", "12 Giờ Qua", "1 Ngày Qua", "1 Tuần Qua", "1 Tháng Qua", "Tất Cả Dữ Liệu"],
    index=3
)



# Start/Stop monitoring
monitoring_button = st.sidebar.button(
    "Dừng Giám Sát" if st.session_state.monitoring_active else "Bắt Đầu Giám Sát"
)
if monitoring_button:
    st.session_state.monitoring_active = not st.session_state.monitoring_active

# Export data
if st.sidebar.button("Xuất Dữ Liệu"):
    timeframe_dict = {
        "1 Giờ Qua": 1,
        "6 Giờ Qua": 6,
        "12 Giờ Qua": 12,
        "1 Ngày Qua": 24,
        "1 Tuần Qua": 24*7,
        "1 Tháng Qua": 24*30,
        "Tất Cả Dữ Liệu": 0
    }
    hours = timeframe_dict[timeframe]
    data = get_readings_by_timeframe(hours)
    if not data.empty:
        csv = export_to_csv(data)
        st.sidebar.download_button(
            label="Tải File CSV",
            data=csv,
            file_name=f"du_lieu_nhiet_do_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.warning("Không có dữ liệu để xuất")

# Main content
st.title("Hệ Thống Giám Sát Nhiệt Độ Kho Hàng")

# Real-time monitoring section
st.header("Giám Sát Thời Gian Thực")

# Display the current status
status_container = st.container()

# Create placeholders for real-time charts
col1, col2 = st.columns(2)
with col1:
    temp_chart_placeholder = st.empty()
with col2:
    humidity_chart_placeholder = st.empty()

# Historical data section
st.header("Phân Tích Dữ Liệu Lịch Sử")

# Create placeholders for historical charts
col1, col2 = st.columns(2)
with col1:
    hist_temp_chart_placeholder = st.empty()
with col2:
    hist_humidity_chart_placeholder = st.empty()

# Statistics section
st.header("Thống Kê & Phát Hiện Bất Thường")
col1, col2 = st.columns(2)
with col1:
    temp_stats_placeholder = st.empty()
with col2:
    humidity_stats_placeholder = st.empty()

# Get timeframe in hours
def get_hours_from_timeframe(timeframe):
    if timeframe == "1 Giờ Qua":
        return 1
    elif timeframe == "6 Giờ Qua":
        return 6
    elif timeframe == "12 Giờ Qua":
        return 12
    elif timeframe == "1 Ngày Qua":
        return 24
    elif timeframe == "1 Tuần Qua":
        return 24*7
    elif timeframe == "1 Tháng Qua":
        return 24*30
    else:  # Tất Cả Dữ Liệu
        return 0

# Function to update data - separated this to avoid full page refreshes
def update_monitoring_data():
    if not st.session_state.monitoring_active:
        return
    
    try:
        # Get current time
        current_time = datetime.now()
        
        # Read data from source
        if st.session_state.use_real_sensors:
            try:
                temperature, humidity = read_serial_data(st.session_state.serial_port, st.session_state.baud_rate)
            except Exception as e:
                st.session_state.error_message = f"Lỗi đọc từ cổng serial: {e}"
                return
        else:
            temperature, humidity = generate_mock_data()
        
        # Store data if valid
        if temperature is not None and humidity is not None:
            store_readings(current_time, temperature, humidity)
            
            # Store current values in session state
            st.session_state.current_temperature = temperature
            st.session_state.current_humidity = humidity
            
            # Get latest readings for real-time display
            st.session_state.latest_data = get_latest_readings(30)  # Last 30 readings
            
            # Get historical data based on selected timeframe
            hours = get_hours_from_timeframe(timeframe)
            st.session_state.historical_data = get_readings_by_timeframe(hours)
            
            # Check for anomalies
            st.session_state.temp_anomalies, st.session_state.humid_anomalies = detect_anomalies(
                st.session_state.historical_data, 
                st.session_state.anomaly_threshold
            )
            
            # Clear any previous error
            if 'error_message' in st.session_state:
                del st.session_state.error_message
        else:
            st.session_state.error_message = "Không nhận được dữ liệu hợp lệ"
            
    except Exception as e:
        st.session_state.error_message = f"Đã xảy ra lỗi: {e}"
        st.session_state.monitoring_active = False

# Initialize session state variables for monitoring
if 'current_temperature' not in st.session_state:
    st.session_state.current_temperature = None
if 'current_humidity' not in st.session_state:
    st.session_state.current_humidity = None
if 'latest_data' not in st.session_state:
    st.session_state.latest_data = pd.DataFrame()
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = pd.DataFrame()
if 'temp_anomalies' not in st.session_state:
    st.session_state.temp_anomalies = pd.DataFrame()
if 'humid_anomalies' not in st.session_state:
    st.session_state.humid_anomalies = pd.DataFrame()
if 'error_message' not in st.session_state:
    st.session_state.error_message = None

# Update data if monitoring is active
if st.session_state.monitoring_active:
    update_monitoring_data()
    
    # Rerun the script after 3 seconds - this is the standard Streamlit way to get real-time updates
    time.sleep(3)  # Wait for 3 seconds to avoid UI flickering
    st.rerun()

# Main display logic - separated from data collection
# Display placeholders with real-time data
if st.session_state.monitoring_active:
    # Now display the data if we have it
    if 'current_temperature' in st.session_state and st.session_state.current_temperature is not None and 'current_humidity' in st.session_state and st.session_state.current_humidity is not None:
        # Update status
        with status_container:
            status_cols = st.columns(4)
            
            # Current temperature
            with status_cols[0]:
                st.metric(
                    "Nhiệt Độ Hiện Tại", 
                    f"{st.session_state.current_temperature:.1f} °C",
                    delta=f"{st.session_state.current_temperature - st.session_state.latest_data['temperature'].iloc[-2] if len(st.session_state.latest_data) > 1 else 0:.1f} °C"
                )
                
            # Current humidity
            with status_cols[1]:
                st.metric(
                    "Độ Ẩm Hiện Tại", 
                    f"{st.session_state.current_humidity:.1f} %",
                    delta=f"{st.session_state.current_humidity - st.session_state.latest_data['humidity'].iloc[-2] if len(st.session_state.latest_data) > 1 else 0:.1f} %"
                )
            
            # Anomaly status
            with status_cols[2]:
                if 'temp_anomalies' in st.session_state and not st.session_state.temp_anomalies.empty:
                    st.error("⚠️ Phát hiện nhiệt độ bất thường!")
                else:
                    st.success("✅ Nhiệt độ bình thường")
            
            with status_cols[3]:
                if 'humid_anomalies' in st.session_state and not st.session_state.humid_anomalies.empty:
                    st.error("⚠️ Phát hiện độ ẩm bất thường!")
                else:
                    st.success("✅ Độ ẩm bình thường")
            
            # Alert based on thresholds
            if (st.session_state.current_temperature < st.session_state.alert_threshold_temp_min or 
                st.session_state.current_temperature > st.session_state.alert_threshold_temp_max):
                st.warning(f"⚠️ Nhiệt độ ngoài phạm vi cho phép: {st.session_state.alert_threshold_temp_min} - {st.session_state.alert_threshold_temp_max} °C")
            
            if (st.session_state.current_humidity < st.session_state.alert_threshold_humid_min or 
                st.session_state.current_humidity > st.session_state.alert_threshold_humid_max):
                st.warning(f"⚠️ Độ ẩm ngoài phạm vi cho phép: {st.session_state.alert_threshold_humid_min} - {st.session_state.alert_threshold_humid_max} %")
        
        # Update real-time charts
        with temp_chart_placeholder:
            if 'latest_data' in st.session_state and not st.session_state.latest_data.empty:
                plot_real_time_temperature(st.session_state.latest_data, 
                                         st.session_state.alert_threshold_temp_min,
                                         st.session_state.alert_threshold_temp_max)
            
        with humidity_chart_placeholder:
            if 'latest_data' in st.session_state and not st.session_state.latest_data.empty:
                plot_real_time_humidity(st.session_state.latest_data,
                                      st.session_state.alert_threshold_humid_min,
                                      st.session_state.alert_threshold_humid_max)
            
        # Update historical charts
        with hist_temp_chart_placeholder:
            if 'historical_data' in st.session_state and not st.session_state.historical_data.empty:
                plot_historical_temperature(st.session_state.historical_data)
            
        with hist_humidity_chart_placeholder:
            if 'historical_data' in st.session_state and not st.session_state.historical_data.empty:
                plot_historical_humidity(st.session_state.historical_data)
            
        # Update statistics
        with temp_stats_placeholder:
            if ('historical_data' in st.session_state and 'temp_anomalies' in st.session_state and 
                not st.session_state.historical_data.empty):
                plot_temperature_statistics(st.session_state.historical_data, st.session_state.temp_anomalies)
            
        with humidity_stats_placeholder:
            if ('historical_data' in st.session_state and 'humid_anomalies' in st.session_state and 
                not st.session_state.historical_data.empty):
                plot_humidity_statistics(st.session_state.historical_data, st.session_state.humid_anomalies)
    
    # Show any errors
    if 'error_message' in st.session_state and st.session_state.error_message:
        status_container.error(st.session_state.error_message)
        
    # We already have auto-refresh at the top level, so no need for another one here

if not st.session_state.monitoring_active:
    status_container.info("Hệ thống giám sát hiện đang không hoạt động. Nhấn 'Bắt Đầu Giám Sát' để bắt đầu.")
