# import serial 
# import time 

# arduino = serial.Serial(port='COM3', baudrate=57600, timeout=.1) 
# def write_read(x): 
#     arduino.write(bytes(x, 'utf-8')) 
#     time.sleep(0.05) 
#     data = arduino.readline() 
#     return data

# while True: 
#     num = input("Enter a number: ") # Taking input from user 
#     value = write_read(num) 
#     print(value) # printing the value 

import serial
import time

# Define the serial port and baud rate
serial_port = '/dev/ttyACM0'  # Replace with your Arduino's serial port
baud_rate = 57600  # Match the baud rate in your Arduino sketch

# Create a serial connection to the Arduino
arduino = serial.Serial(serial_port, baud_rate, timeout=1)

# Function to send servo commands to the Arduino
def send_servo_command(servo_number, angle):
    command = f"{servo_number} {angle}\n"
    arduino.write(command.encode())
    arduino.flush()  # Ensure the data is sent immediately

# Example usage: Move servo 0 to 90 degrees, servo 3 to 1100, and servo 2 to 1200
send_servo_command(0, 90)
send_servo_command(3, 1100)
send_servo_command(2, 1200)

# Close the serial connection
arduino.close()
