import keyboard
import time
import colorama
from colorama import Fore


class RobotMovement:
    def __init__(self):
        colorama.init(autoreset=True)
        self.straight_speed = 0  # Speed range: -4000 to 4000
        self.straight_dir = 0 # Straight dir: 0 , 1 , 2
        self.rot_dir = 0  # "None", "Right", or "Left"
        self.rot_angle = 0  # Angle range: 0 to 360 degrees
        self.last_update_time = time.time()
        self.acceleration_rate = 400  # Speed change per update
        self.rotation_rate = 200  # Rotation change per update


    def create_cmd(self):
        # Command format showing speed and rotation direction with angle
        cmd_str = f'Sd{self.straight_dir}s{abs(self.straight_speed)}Rr{self.rot_dir}a{abs(self.rot_angle)}'
        return cmd_str


    def teleOp(self):
        print(f"{Fore.GREEN}Control the robot with keyboard.")
        print(f"{Fore.CYAN}Use W/S to increase/decrease speed.")
        print(f"{Fore.CYAN}Use A/D to rotate left/right.")
        print(f"{Fore.CYAN}Press Space to reset rotation and speed.")
        print(f"{Fore.CYAN}Press ESC to exit.")

        last_rotation = "None"

        try:
            while True:
                current_time = time.time()
                delta_time = current_time - self.last_update_time

                # Calculate speed and rotation updates based on time
                speed_change = int(self.acceleration_rate * delta_time)
                rotation_change = int(self.rotation_rate * delta_time)

                if keyboard.is_pressed('w'):
                    self.straight_speed = min(4000, self.straight_speed + speed_change)
                    
                elif keyboard.is_pressed('s'):
                    self.straight_speed = max(-4000, self.straight_speed - speed_change)

                # Manage rotation direction and angle
                if keyboard.is_pressed('a'):
                    if last_rotation != "Left":
                        last_rotation = "Left"
                        self.rot_angle = self.rot_angle

                    if  self.rot_angle > -360:
                        self.rot_angle = (self.rot_angle - rotation_change)
                    else: self.rot_angle = -360

                elif keyboard.is_pressed('d'):
                    if last_rotation != "Right":
                        last_rotation = "Right"
                        self.rot_angle = self.rot_angle

                    if self.rot_angle < 360:
                        self.rot_angle = (self.rot_angle + rotation_change)
                    else: self.rot_angle = 360

                elif not keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
                    last_rotation = "None"


                if keyboard.is_pressed('space'):
                    # Reset rotation and speed
                    self.rot_dir = 0
                    self.rot_angle = 0
                    self.straight_speed = 0
                    self.straight_dir = 0


                if self.straight_speed > 0:
                    self.straight_dir = 1
                elif self.straight_speed < 0:
                    self.straight_dir = 2
                else:
                    self.straight_dir = 0
                

                if self.rot_angle > 0:
                    self.rot_dir = 1
                elif self.rot_angle < 0:
                    self.rot_dir = 2
                else:
                    self.rot_dir = 0
                

                # Update the last time
                self.last_update_time = current_time
                time.sleep(0.05)
                # Display command string
                print(f"{Fore.YELLOW}DIR {self.straight_dir} SPEED {self.straight_speed:5d}{Fore.GREEN} ROTDIR {self.rot_dir} ANGLE {self.rot_angle:4d}", end='\r')
                if keyboard.is_pressed('esc'):
                    print(f"{Fore.RED}\nExiting...")
                    break
                time.sleep(0.05)  # Short delay to prevent excessive CPU usage
                
        except KeyboardInterrupt:
            print("\nProgram exited by user.")


