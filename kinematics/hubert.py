import serial
import time
import cv2
import numpy as np
# import keyboard

import os
os.system("cls")


# last_command = np.datetime64(0,"ms")


#               body    headPan  headTilt  shoulder  elbow  gripper
body_parts    = ['B',   'P',    'T',     'S',      'E',   'G']
position_init = [1700,  1500,    2000,   2130,   1485,  1390] # E: 1650, S: 2200, G: 1600
position_min  = [560,   550,     950,    750,      550,   550]
position_max  = [2330,  2340,    2400,   2200,     2400,  2150]

def move(part, pos, ser):
    """
    Moves a specified body part of the robot to a given percentage position.

    Parameters:
    - part (str): The identifier of the body part to move, e.g., 'B', 'P', 'T', etc.
    - pos (float): The desired position in percentage (-100 to 100).
    - ser (serial.Serial): The serial object for communication with the robot.

    Returns:
    - tuple: A tuple containing the body part and its absolute position value.
    """
    print("moving", part, pos)
    pos_abs_val = correct_position(part,pos)
    move_servo(part, pos_abs_val, ser)
    return (part, pos_abs_val)





def move_servo(part, pos, ser):
    """
    Sends a command to move a specified servo to an absolute position.

    Parameters:
    - part (str): The identifier of the servo to move.
    - pos (float): The desired absolute position.
    - ser (serial.Serial): The serial object for communication.

    Returns:
    - tuple: A tuple containing the body part and its absolute position value.
    """
    # print("SER start")
    if(ser.out_waiting > 50):
        ser.reset_output_buffer()
    if(ser.in_waiting > 50):
        ser.reset_input_buffer()
    ser.write(part.encode())
    ser.write(f'{pos:.2f}\n'.encode())  # Send the position as a float with two decimal places
    # print("SER done")
    return (part,pos)

def correct_position(part, perc_position):
    """
    Converts a percentage position into an absolute value for a given body part.

    Parameters:
    - part (str): The identifier of the body part.
    - perc_position (float): The desired position in percentage (-100 to 100).

    Returns:
    - float: The absolute position value.
    """
    index = body_parts.index(part)

    if abs(perc_position) >= 100:
        perc_position = min(abs(perc_position), 100) * (1 if perc_position >= 0 else -1)

    if perc_position < 0:
        new_pos = (position_init[index] - position_min[index])*((100+perc_position)/100) + position_min[index]
    elif perc_position > 0:
        new_pos = (position_max[index] - position_init[index])*(perc_position/100) + position_init[index]
    else:
        new_pos = position_init[index]

    return new_pos
    

def move_to_init():
    """
    Moves all servos to their initial positions.
    """
    for j, servo in enumerate(body_parts):
        move_servo(servo, position_init[j])
