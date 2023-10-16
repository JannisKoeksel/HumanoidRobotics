import serial
import time
import cv2

# import keyboard

import os
os.system("cls")

# OBS!! must close monitor before running
# if a position is given while the robot is still moving it wont recognize that command

ser = serial.Serial('COM3', 57600)

#               body    headPan  headTilt  shoulder  elbow  gripper
body_parts    = ['B',   'P',    'T',     'S',      'E',   'G']
position_init = [1700,  1500,    2000,   2127.5,   1485,  1390] # E: 1650, S: 2200, G: 1600
position_min  = [560,   550,     950,    750,      550,   550]
position_max  = [2330,  2340,    2400,   2200,     2400,  2150]

def move_servo(part, position):
    ser.write(part.encode())
    ser.write(f'{position:.2f}\n'.encode())  # Send the position as a float with two decimal places

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
    
def shoot():
    # move_servo('S', 1990)
    # move_servo('E', 2217) # bra med S1852 och E2125
    # time.sleep(2)
    # move_servo('G', 1694)  # change depending on laser pointer
    move_servo('E', 2050)
    time.sleep(1.2)
    move_servo('S', 1750)
    time.sleep(1.5)
    move_servo('G', 1700)  # 1694


def move_to_init():
    for j, servo in enumerate(body_parts):
        move_servo(servo, position_init[j])

while True:

    choice = input("Enter 'B', 'P', 'T', 'S', 'E' or 'G' for part, 'shoot', 'scan', 'init' or 'close': ")

    if choice == 'close':
        move_to_init()
        print('Run is over.')
        break
    elif choice == 'shoot':
        shoot()
        print('You are shot!')
        continue
    elif choice == 'scan':  # this is just to build on for when we can integrate the movement detection
        for i in range(0,10):  # change this to a while and add a break in each position if movement is detected
            print(i)
            if i%4 == 0:
                move_servo('B', position_max[0]-200)
                time.sleep(3)
            elif i%2 == 0:
                move_servo('B', position_min[0]+200)
                time.sleep(3)
            else:
                move_servo('B', position_init[0])
                time.sleep(3)
        continue
    elif choice == 'init':
        move_to_init()
        continue
    elif choice not in body_parts:
        print('Not a valid input. Try again.')
        continue

    position_choice = int(input("Enter rotation from center 0 (-100,100): "))
    new_position = correct_position(choice, position_choice)

    print('Body part chosen: ', choice)
    print('Position value chosen: ', new_position)

    move_servo(choice, new_position)

    
