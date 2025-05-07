import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

def plot_real_time_temperature(data, min_threshold=15.0, max_threshold=30.0):
    """
    Plot real-time temperature data with threshold lines.
    
    Args:
        data (pd.DataFrame): DataFrame with 'timestamp' and 'temperature' columns
        min_threshold (float): Minimum temperature threshold
        max_threshold (float): Maximum temperature threshold
    """
    if data.empty:
        st.write("No temperature data available.")
        return
    
    # Create figure
    fig = go.Figure()
    
    # Add temperature line
    fig.add_trace(
        go.Scatter(
            x=data['timestamp'], 
            y=data['temperature'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#E74C3C', width=2),
            marker=dict(size=6)
        )
    )
    
    # Add threshold lines
    fig.add_shape(
        type="line",
        x0=data['timestamp'].min(),
        y0=min_threshold,
        x1=data['timestamp'].max(),
        y1=min_threshold,
        line=dict(color="#3498DB", width=2, dash="dash"),
        name="Min Threshold"
    )
    
    fig.add_shape(
        type="line",
        x0=data['timestamp'].min(),
        y0=max_threshold,
        x1=data['timestamp'].max(),
        y1=max_threshold,
        line=dict(color="#E67E22", width=2, dash="dash"),
        name="Max Threshold"
    )
    
    # Add annotations for threshold lines
    fig.add_annotation(
        x=data['timestamp'].max(),
        y=min_threshold,
        text=f"Min: {min_threshold}°C",
        showarrow=False,
        yshift=10,
        font=dict(color="#3498DB")
    )
    
    fig.add_annotation(
        x=data['timestamp'].max(),
        y=max_threshold,
        text=f"Max: {max_threshold}°C",
        showarrow=False,
        yshift=10,
        font=dict(color="#E67E22")
    )
    
    # Update layout
    fig.update_layout(
        title="Real-time Temperature",
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Add a range slider
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_real_time_humidity(data, min_threshold=30.0, max_threshold=70.0):
    """
    Plot real-time humidity data with threshold lines.
    
    Args:
        data (pd.DataFrame): DataFrame with 'timestamp' and 'humidity' columns
        min_threshold (float): Minimum humidity threshold
        max_threshold (float): Maximum humidity threshold
    """
    if data.empty:
        st.write("No humidity data available.")
        return
    
    # Create figure
    fig = go.Figure()
    
    # Add humidity line
    fig.add_trace(
        go.Scatter(
            x=data['timestamp'], 
            y=data['humidity'],
            mode='lines+markers',
            name='Humidity',
            line=dict(color='#3498DB', width=2),
            marker=dict(size=6)
        )
    )
    
    # Add threshold lines
    fig.add_shape(
        type="line",
        x0=data['timestamp'].min(),
        y0=min_threshold,
        x1=data['timestamp'].max(),
        y1=min_threshold,
        line=dict(color="#3498DB", width=2, dash="dash"),
    )
    
    fig.add_shape(
        type="line",
        x0=data['timestamp'].min(),
        y0=max_threshold,
        x1=data['timestamp'].max(),
        y1=max_threshold,
        line=dict(color="#E67E22", width=2, dash="dash"),
    )
    
    # Add annotations for threshold lines
    fig.add_annotation(
        x=data['timestamp'].max(),
        y=min_threshold,
        text=f"Min: {min_threshold}%",
        showarrow=False,
        yshift=10,
        font=dict(color="#3498DB")
    )
    
    fig.add_annotation(
        x=data['timestamp'].max(),
        y=max_threshold,
        text=f"Max: {max_threshold}%",
        showarrow=False,
        yshift=10,
        font=dict(color="#E67E22")
    )
    
    # Update layout
    fig.update_layout(
        title="Real-time Humidity",
        xaxis_title="Time",
        yaxis_title="Humidity (%)",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Add a range slider
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_historical_temperature(data):
    """
    Plot historical temperature data with a trend line.
    
    Args:
        data (pd.DataFrame): DataFrame with 'timestamp' and 'temperature' columns
    """
    if data.empty:
        st.write("No historical temperature data available.")
        return
    
    # Resample data for daily average if the timeframe is large
    if len(data) > 500:
        data_resampled = data.set_index('timestamp').resample('1H').mean().reset_index()
    else:
        data_resampled = data
    
    # Create figure
    fig = go.Figure()
    
    # Add temperature scatter plot
    fig.add_trace(
        go.Scatter(
            x=data_resampled['timestamp'], 
            y=data_resampled['temperature'],
            mode='lines',
            name='Temperature',
            line=dict(color='#E74C3C', width=2),
        )
    )
    
    # Add trend line
    x = np.array(range(len(data_resampled)))
    y = data_resampled['temperature'].values
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    fig.add_trace(
        go.Scatter(
            x=data_resampled['timestamp'],
            y=p(x),
            mode='lines',
            name='Trend',
            line=dict(color='#7F8C8D', width=2, dash='dash')
        )
    )
    
    # Add statistical information
    avg_temp = data['temperature'].mean()
    min_temp = data['temperature'].min()
    max_temp = data['temperature'].max()
    
    fig.add_annotation(
        x=0.02,
        y=0.98,
        xref="paper",
        yref="paper",
        text=f"Avg: {avg_temp:.1f}°C | Min: {min_temp:.1f}°C | Max: {max_temp:.1f}°C",
        showarrow=False,
        font=dict(size=12),
        align="left",
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="gray",
        borderwidth=1,
        borderpad=4
    )
    
    # Update layout
    fig.update_layout(
        title="Historical Temperature Data",
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Add range selector
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_historical_humidity(data):
    """
    Plot historical humidity data with a trend line.
    
    Args:
        data (pd.DataFrame): DataFrame with 'timestamp' and 'humidity' columns
    """
    if data.empty:
        st.write("No historical humidity data available.")
        return
    
    # Resample data for daily average if the timeframe is large
    if len(data) > 500:
        data_resampled = data.set_index('timestamp').resample('1H').mean().reset_index()
    else:
        data_resampled = data
    
    # Create figure
    fig = go.Figure()
    
    # Add humidity scatter plot
    fig.add_trace(
        go.Scatter(
            x=data_resampled['timestamp'], 
            y=data_resampled['humidity'],
            mode='lines',
            name='Humidity',
            line=dict(color='#3498DB', width=2),
        )
    )
    
    # Add trend line
    x = np.array(range(len(data_resampled)))
    y = data_resampled['humidity'].values
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    fig.add_trace(
        go.Scatter(
            x=data_resampled['timestamp'],
            y=p(x),
            mode='lines',
            name='Trend',
            line=dict(color='#7F8C8D', width=2, dash='dash')
        )
    )
    
    # Add statistical information
    avg_humid = data['humidity'].mean()
    min_humid = data['humidity'].min()
    max_humid = data['humidity'].max()
    
    fig.add_annotation(
        x=0.02,
        y=0.98,
        xref="paper",
        yref="paper",
        text=f"Avg: {avg_humid:.1f}% | Min: {min_humid:.1f}% | Max: {max_humid:.1f}%",
        showarrow=False,
        font=dict(size=12),
        align="left",
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="gray",
        borderwidth=1,
        borderpad=4
    )
    
    # Update layout
    fig.update_layout(
        title="Historical Humidity Data",
        xaxis_title="Time",
        yaxis_title="Humidity (%)",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Add range selector
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_temperature_statistics(data, anomalies):
    """
    Plot temperature statistics and highlight anomalies.
    
    Args:
        data (pd.DataFrame): DataFrame with 'timestamp' and 'temperature' columns
        anomalies (pd.DataFrame): DataFrame with anomalous temperature readings
    """
    if data.empty:
        st.write("No temperature statistics available.")
        return
    
    # Create subplots
    fig = make_subplots(
        rows=2, 
        cols=1,
        subplot_titles=("Temperature Distribution", "Temperature Box Plot"),
        vertical_spacing=0.3
    )
    
    # Add histogram to first subplot
    fig.add_trace(
        go.Histogram(
            x=data['temperature'],
            nbinsx=20,
            marker_color='#E74C3C',
            name='Temperature'
        ),
        row=1, col=1
    )
    
    # Add box plot to second subplot
    fig.add_trace(
        go.Box(
            y=data['temperature'],
            name='Temperature',
            marker_color='#E74C3C',
            boxmean=True
        ),
        row=2, col=1
    )
    
    # Highlight anomalies if any
    if not anomalies.empty:
        fig.add_trace(
            go.Scatter(
                x=[anomalies.index] * len(anomalies),
                y=anomalies['temperature'],
                mode='markers',
                name='Anomalies',
                marker=dict(
                    color='red',
                    size=10,
                    symbol='x'
                )
            ),
            row=2, col=1
        )
    
    # Calculate statistics
    avg_temp = data['temperature'].mean()
    median_temp = data['temperature'].median()
    std_temp = data['temperature'].std()
    anomaly_count = len(anomalies)
    
    # Add statistics as annotation
    fig.add_annotation(
        x=0.5,
        y=1.12,
        xref="paper",
        yref="paper",
        text=f"Avg: {avg_temp:.1f}°C | Median: {median_temp:.1f}°C | Std Dev: {std_temp:.2f}°C | Anomalies: {anomaly_count}",
        showarrow=False,
        font=dict(size=12),
        align="center",
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="gray",
        borderwidth=1,
        borderpad=4
    )
    
    # Update layout
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=80, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_humidity_statistics(data, anomalies):
    """
    Plot humidity statistics and highlight anomalies.
    
    Args:
        data (pd.DataFrame): DataFrame with 'timestamp' and 'humidity' columns
        anomalies (pd.DataFrame): DataFrame with anomalous humidity readings
    """
    if data.empty:
        st.write("No humidity statistics available.")
        return
    
    # Create subplots
    fig = make_subplots(
        rows=2, 
        cols=1,
        subplot_titles=("Humidity Distribution", "Humidity Box Plot"),
        vertical_spacing=0.3
    )
    
    # Add histogram to first subplot
    fig.add_trace(
        go.Histogram(
            x=data['humidity'],
            nbinsx=20,
            marker_color='#3498DB',
            name='Humidity'
        ),
        row=1, col=1
    )
    
    # Add box plot to second subplot
    fig.add_trace(
        go.Box(
            y=data['humidity'],
            name='Humidity',
            marker_color='#3498DB',
            boxmean=True
        ),
        row=2, col=1
    )
    
    # Highlight anomalies if any
    if not anomalies.empty:
        fig.add_trace(
            go.Scatter(
                x=[anomalies.index] * len(anomalies),
                y=anomalies['humidity'],
                mode='markers',
                name='Anomalies',
                marker=dict(
                    color='red',
                    size=10,
                    symbol='x'
                )
            ),
            row=2, col=1
        )
    
    # Calculate statistics
    avg_humid = data['humidity'].mean()
    median_humid = data['humidity'].median()
    std_humid = data['humidity'].std()
    anomaly_count = len(anomalies)
    
    # Add statistics as annotation
    fig.add_annotation(
        x=0.5,
        y=1.12,
        xref="paper",
        yref="paper",
        text=f"Avg: {avg_humid:.1f}% | Median: {median_humid:.1f}% | Std Dev: {std_humid:.2f}% | Anomalies: {anomaly_count}",
        showarrow=False,
        font=dict(size=12),
        align="center",
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="gray",
        borderwidth=1,
        borderpad=4
    )
    
    # Update layout
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=80, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
