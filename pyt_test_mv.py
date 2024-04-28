import serial
import keyboard

device = serial.Serial("COM9", 9600 )
cmd = 'Q0,0,0,0e'.encode('utf-8')
try:
    device.open()
except Exception as e:
    pass
while True:
    if keyboard.is_pressed('w'):
        cmd = 'Q1,200,0,0e'.encode('utf-8')
        device.write(cmd)
        print('W')
    #cmd = input('Set please: ')
    elif keyboard.is_pressed('s'):
        cmd = 'Q2,200,0,0e'.encode('utf-8')
        device.write(cmd)
        print('S')
    elif keyboard.is_pressed('a'):
        cmd = 'Q0,000,1,200e'.encode('utf-8')
        device.write(cmd)
    elif keyboard.is_pressed('d'):
        cmd = 'Q0,000,2,200e'.encode('utf-8')
        device.write(cmd)
    elif keyboard.is_pressed('space'):
        cmd = 'Q0,0,0,0e'.encode('utf-8')
        device.write(cmd)
    # else:
    #     cmd = 'Q0,0,0,0e'.encode('utf-8')
    
    #a = device.readline()