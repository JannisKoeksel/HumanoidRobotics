import serial
import time

# import os
# os.system("cls")

# OBS!! must close monitor before running
# if a position is given while the robot is still moving it wont recognize that command

ser = serial.Serial('COM3', 57600)

#               body    headPan  headTilt  shoulder  elbow  gripper
body_parts    = ['B',   'P',    'T',     'S',      'E',   'G']
position_init = [1700,  1500,    2000,   2127.5,   1485,  1600] # E: 1650, S: 2200
position_min  = [560,   550,     950,    750,      550,   550]
position_max  = [2330,  2340,    2400,   2200,     2400,  2150]

def move_servo(part, position):
    ser.write(part.encode())
    ser.write(f'{position}\n'.encode())

def correct_position(part, perc_position):
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

def front_and_back(body_part, sleep_time=0.5, repeats=1, high = 71, low=-71, step_size=10):  # not used
    for _ in range(repeats):
        for angle in range(0, high, step_size):
            time.sleep(sleep_time)
            position = correct_position(body_part, angle)
            move_servo(body_part, position)
        for angle in range(high-step_size, low, -step_size):
            time.sleep(sleep_time)
            position = correct_position(body_part, angle)
            move_servo(body_part, position)
        for angle in range(low, 0, step_size):
            time.sleep(sleep_time)
            position = correct_position(body_part, angle)
            move_servo(body_part, position)
