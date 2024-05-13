import serial
import keyboard
from Robot_Packages.Robot_state_parameters import RobotParameters as robpar

class teleOp:
    def __init__(self) -> None:
        self.device = serial.Serial("COM4", 9600 )
        self.cmd = 'Q0,0,0,0e'.encode('utf-8')
        self.forward_speed = robpar.MotorWheels.teleop_forward_speed
        self.backward_speed = robpar.MotorWheels.teleop_backward_speed
        self.steer = robpar.MotorWheels.teleop_steer_speed


    def connect(self):
        try:
            self.device.open()
            return self.device.is_open
        except Exception as e:
            return False
            

    def drive(self):
        while True:
            if keyboard.is_pressed('w'):
                cmd = f'Q1,{self.forward_speed},0,0e'.encode('utf-8')
                self.device.write(cmd)
                print('W')
            elif keyboard.is_pressed('s'):
                cmd = f'Q2,{self.backward_speed},0,0e'.encode('utf-8')
                self.device.write(cmd)
                print('S')
            elif keyboard.is_pressed('d'):
                cmd = f'Q0,000,1,{self.steer}e'.encode('utf-8')
                self.device.write(cmd)
            elif keyboard.is_pressed('a'):
                cmd = f'Q0,000,2,{self.steer}e'.encode('utf-8')
                self.device.write(cmd)
            elif keyboard.is_pressed('space'):  
                cmd = 'Q0,0,0,0e'.encode('utf-8')
                self.device.write(cmd)

# tp = teleOp()
# tp.connect()
# tp.drive()