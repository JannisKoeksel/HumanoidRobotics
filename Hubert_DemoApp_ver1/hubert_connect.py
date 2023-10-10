import serial
import time

import os
os.system("cls")

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

while True:

    part_choice = input("Enter 'B', 'P', 'T', 'S', 'E' or 'G' for part, 'shoot' or 'close': ")

    if part_choice == 'close':
        move_servo('q', position=1500) # position here is arbitrary
        time.sleep(2)
        print('Run is over.')
        break
    elif part_choice == 'shoot':
        move_servo('s', position=1500) # position here is arbitrary
        time.sleep(2)
        print('You are shot!')
        continue
    elif part_choice not in body_parts:
        print('Not a valid input. Try again.')
        continue

    position_choice = float(input("Enter rotation from center 0 (-100,100): "))
    new_position = correct_position(part_choice, position_choice)

    print('Body part chosen: ', part_choice)
    print('Position value chosen: ', new_position)

    move_servo(part_choice, new_position)

    
