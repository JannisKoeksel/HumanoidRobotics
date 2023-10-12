import serial
import time
import cv2

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

    # ser.write(part.encode())
    position = int(position)
    ser.write((part + f'{ position}').encode())
   
    time.sleep(0.05)

    while ser.in_waiting == 0:
        pass

    akn = ser.readline().decode().strip()

    print(akn)

    if akn == "AKN":
        print("receaved")
    else: 
        print(akn)

    # ser.write((part + f'{ position}\n').encode())

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

def idle_behaviour(position, step_size=50):
    move_servo('i', position) # position here is arbitrary
    time.sleep(2)
    # for position in range(position_init[0], position_max[0] -100, step_size):
    #     move_servo('i', position)
    #     time.sleep(2)
    # for position in range(position_max[0]-100, position_min[0]+100, step_size):
    #     move_servo('i', position)
    #     time.sleep(2)
    
def shoot():
    move_servo('S', 1990.0)
    move_servo('E', 2217.0)
    move_servo('G', 1800.0)  # change depending on laser pointer

while True:

    choice = input("Enter 'B', 'P', 'T', 'S', 'E' or 'G' for part, 'shoot', 'idle' or 'close': ")

    if choice == 'close':
        move_servo('q', position=1500) # position here is arbitrary
        time.sleep(2)
        print('Run is over.')
        break
    elif choice == 'shoot':
        # move_servo('s', position=1500) # position here is arbitrary
        # time.sleep(2)
        shoot()
        print('You are shot!')
        continue
    elif choice == 'test':
        move_servo('E', position=1900) # position here is arbitrary
        move_servo('B', position=1200) # position here is arbitrary
        move_servo('T', position=1000) # position here is arbitrary
        
        # print('You are shot!')
        continue
    elif choice == 'idle':
        for position in range(position_init[0], position_max[0] -100, 50):
            idle_behaviour(position)
            time.sleep(1.5)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                move_servo('s', position=1500) # position here is arbitrary
                time.sleep(2)
                print('You are shot!')
                break
        continue

    elif choice not in body_parts:
        print('Not a valid input. Try again.')
        continue

    position_choice = float(input("Enter rotation from center 0 (-100,100): "))
    new_position = correct_position(choice, position_choice)

    print('Body part chosen: ', choice)
    print('Position value chosen: ', new_position)

    move_servo(choice, new_position)

    
