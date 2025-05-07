import serial
import time
import random  # For fallback when actual serial fails

def read_serial_data(port, baud_rate=9600, timeout=2.0):
    """
    Read temperature and humidity data from a serial port.
    
    Args:
        port (str): Serial port to connect to (e.g., '/dev/ttyUSB0')
        baud_rate (int): Baud rate for the serial connection
        timeout (float): Timeout for the serial connection in seconds
        
    Returns:
        tuple: (temperature, humidity) or (None, None) if reading fails
        
    Expects serial data in format: "Temperature: XX.X, Humidity: YY.Y"
    """
    try:
        # Connect to the serial port
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        
        # Allow time for connection to establish
        time.sleep(0.5)
        
        # Read data from serial port
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            
            # Parse the line for temperature and humidity
            # Expected format: "Temperature: XX.X, Humidity: YY.Y"
            try:
                if "Temperature" in line and "Humidity" in line:
                    # Split by comma and extract values
                    parts = line.split(',')
                    temperature = float(parts[0].split(':')[1].strip())
                    humidity = float(parts[1].split(':')[1].strip())
                    
                    # Close the serial connection
                    ser.close()
                    
                    return temperature, humidity
            except (ValueError, IndexError) as e:
                # Handle parsing errors
                print(f"Error parsing serial data: {e}")
                print(f"Raw data: {line}")
        
        # Close the serial connection
        ser.close()
        
        # If we got here, we couldn't get valid data
        return None, None
        
    except serial.SerialException as e:
        # Handle serial connection errors
        print(f"Serial connection error: {e}")
        return None, None

def format_command(command):
    """
    Format command for sending to the sensor controller.
    This is a placeholder for when you need to send commands to the sensor.
    
    Args:
        command (str): Command to send
        
    Returns:
        bytes: Formatted command as bytes
    """
    # This is a simple example - adjust based on your sensor's protocol
    return f"{command}\n".encode('utf-8')

def send_command(port, baud_rate, command, timeout=2.0):
    """
    Send a command to the sensor controller.
    
    Args:
        port (str): Serial port to connect to
        baud_rate (int): Baud rate for the serial connection
        command (str): Command to send
        timeout (float): Timeout for the serial connection in seconds
        
    Returns:
        str: Response from the sensor or None if failed
    """
    try:
        # Connect to the serial port
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        
        # Allow time for connection to establish
        time.sleep(0.5)
        
        # Send the command
        ser.write(format_command(command))
        
        # Wait for response
        time.sleep(0.5)
        
        # Read response
        response = ""
        while ser.in_waiting > 0:
            response += ser.readline().decode('utf-8').strip()
        
        # Close the serial connection
        ser.close()
        
        return response
        
    except serial.SerialException as e:
        # Handle serial connection errors
        print(f"Serial command error: {e}")
        return None
