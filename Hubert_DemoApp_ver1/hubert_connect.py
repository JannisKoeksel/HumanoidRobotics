import serial
import time

# obs!! must close monitor before running

# const int pos_min[]  = {560,   550,     950,      750,      550,   550};
# const int pos_max[]  = {2330,  2340,    2400,     2200,     2400,  2150};

# const int pos_init[] = {1700,  1500,    2000,     2200,     1650,  1600};
#                        body    headPan  headTilt  shoulder  elbow  gripper

# Define the serial port and baud rate
ser = serial.Serial('COM3', 57600)

# def move_body(position):
#     ser.write(b'B')
#     ser.write(f'{position}\n'.encode())
# def move_head_pan(position):
#     ser.write(b'Hp')
#     ser.write(f'{position}\n'.encode())
# def move_head_tilt(position):
#     ser.write(b'Ht')
#     ser.write(f'{position}\n'.encode())
# def move_shoulder(position):
#     ser.write(b'S')
#     ser.write(f'{position}\n'.encode())
# def move_elbow(position):
#     ser.write(b'E')
#     ser.write(f'{position}\n'.encode())
# def move_gripper(position):
#     ser.write(b'G')
#     ser.write(f'{position}\n'.encode())
# def move_head(pan_pos, tilt_pos):
#     # Send head movement command to Arduino
#     ser.write(b'H')
#     ser.write(f'{pan_pos} {tilt_pos}\n'.encode())

def move_servo(part, position):
    # Send servo movement command to Arduino
    ser.write(part.encode())
    ser.write(f'{position}\n'.encode())


#istället för for i in range så kan vi ha while true, och om ett input är "klar" så sätt False

for i in range(2):
    choice = input("Enter 'B', 'Hp', 'Ht', 'S', 'E' or 'G' for part: ")

    # if choice == 'B':
    #     body = int(input("Enter body position (560-2330): "))
    #     move_body(body)
    # elif choice == 'Hp':
    #     pan = int(input("Enter pan position (1500-2400): "))
    # elif choice == 'Ht':
    #     tilt = int(input("Enter tilt position (950-2400): "))
    #     move_head(pan, tilt)
    # elif choice == 'S':
    #     shoulder = int(input("Enter shoulder position (750-2200): "))
    #     move_elbow(elbow)
    # elif choice == 'E':
    #     elbow = int(input("Enter elbow position (550-2200): "))
    #     move_elbow(elbow)
    # elif choice == 'G':
    #     gripper = int(input("Enter elbow position (550-2200): "))
    #     move_elbow(elbow)
    # else:
    #     print("Invalid choice. Try again.")

    # if choice == 'H':
    #     pan = int(input("Enter pan position (1500-2400): "))
    #     tilt = int(input("Enter tilt position (950-2400): "))
    #     move_head(pan, tilt)
    # elif choice == 'E':
    #     elbow = int(input("Enter elbow position (550-2200): "))
    #     move_elbow(elbow)
    # elif choice == 'B':
    #     body = int(input("Enter body position (560-2330): "))
    #     move_body(body)
    # else:
    #     print("Invalid choice. Try again.")
