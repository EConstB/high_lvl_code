import Robot_Packages.keyboard_teleop as ktp
import Robot_Packages as rp
from threading import Thread
import threading
import asyncio
import time
import sys

class Robot():
    def __init__(self) -> None:
        self.Battery = rp.BatteryUnit()
        self.bat_state = rp.RobotParameters.Battery.state.normal

        self.ds_sens = self.init_ds(4)


    def init_ds(self, quantity):
    # Create a list of distance sensor units
        return [rp.DistanceSensorUnit(i) for i in range(quantity)]



class mainMenu():
    def __init__(self, robot: Robot) -> None:
        self.mode = "None" # tp_key, tp_joystick, autonomy
        self.input_ready = threading.Event()
        self.robot = robot

   
    def launch(self):
        self.input_ready.clear()
        self.main_menu()

    def input_thread(self):
        while not self.input_ready.is_set():
            self.cmd = input('>')
            self.input_ready.set()

    def main_menu(self):
        input_thread = threading.Thread(target=self.input_thread)
        input_thread.start()
        try:
            while not self.input_ready.is_set():
                # Clear screen and print the menu
                print("\033[H\033[J", end="")
                print("\nIt's Econstb Robot interface V1.0")
                print(f"System Parameters:\tCur_V: {self.robot.Battery.bat_curr_volt:.2f}\tMax_V: {self.robot.Battery.bat_max_volt}\tMode:{self.mode}")
                print("Setting\n1) Change Mode\n2) Monitoring System\n3) Launch Teleop\n4) Reload")
                time.sleep(0.5)  # Refresh rate of the display

            # When input is ready, process it
            try:
                if self.cmd == '1':
                    self.mode_menu()
                elif self.cmd == '2':
                    self.input_ready.clear()
                    self.monitoring_menu()
                elif self.cmd == '3':
                    self.run_teleop()
                elif self.cmd == '4':
                    sys.exit(0)
            except Exception as err:
                print('Incorrect cmd')

        finally:
            input_thread.join()
            self.input_ready.clear()
            self.main_menu()


    def mode_menu(self):
        print("\033[H\033[J", end="")
        print('Choose Movement Mode\n1)Teleop Keyboard Mode\n2)Teleop Joystick Mode\n3)Back')
        cmd = input(">")
        try:
            if int(cmd) == 1:
                self.mode = 'Keyb'
                self.input_ready.clear()
                self.main_menu()

            elif int(cmd) == 2:
                self.mode = "Joys"
                self.input_ready.clear()
                self.main_menu()
            elif int(cmd) == 3:
                self.input_ready.clear()
                self.main_menu()
            else:
                print("Incorrect")
                time.sleep(0.2)
                self.input_ready.clear()
                self.main_menu()

        except Exception as Err:
            print("Incorrect")
            time.sleep(0.2)
            self.main_menu()
            self.input_ready.clear()


    def monitoring_menu(self):
        input_thread = threading.Thread(target=self.input_thread)
        input_thread.start()
        while not self.input_ready.is_set():
            print("\033[H\033[J", end="")
            print(f"1)Back \nDistance Sensor Data:", end='')
            for ds in self.robot.ds_sens:
                print(f'\tDS{ds.name} {ds.cur_value_ds:2}', end='')
            print(f"\nBat state({self.robot.Battery.bat_state}): {self.robot.Battery.bat_curr_volt:.2f}V  {self.robot.Battery.bat_percent_value:.2f}%")
            time.sleep(0.5)
            
            try:
                if self.cmd == '1':
                    self.cmd = '0'
                    self.main_menu()
            finally:
                pass


    def run_teleop(self):
        print("\033[H\033[J", end="")
        print("Are you sure to launch script?(y/n)")
        cmd = input('>')
        if cmd == 'y':
            if self.mode == "Keyb":
                print('Keyb')
                keyop = ktp.teleOp()
                res = keyop.connect()
                print(f"Device connection is {res}")
                time.sleep(2)
                if res:
                    keyop.drive()

            elif self.mode == 'Joys':
                print('Joystick  development in progress')
                time.sleep(1)
                self.input_ready.clear()
                #self.main_menu()

            else:
                print('Choose some mode, please')
                time.sleep(1)
                self.input_ready.clear()
                # self.main_menu()
        elif cmd == 'n':
            print('Choose some mode, please')
            time.sleep(1)
            self.input_ready.clear()
            self.main_menu()

class MonitoringHandler(rp.MonitoringSystem):
    def __init__(self, robot):
        super().__init__(robot=robot)

    async def testing(self):
        self.tasks = [self.task_run(), self.bat_testing()]
        return await asyncio.gather(*self.tasks)

    def testing_run(self):
        asyncio.run(self.testing())

def main():
    robot = Robot()
    monsys = MonitoringHandler(robot=robot)
    monsys.bat = robot.Battery

    main_menu = mainMenu(robot=robot)
    monsys_thread = Thread(target=monsys.testing_run, daemon=True)
    menu_thread = Thread(target=main_menu.launch)

    monsys_thread.start()
    menu_thread.start()

    try:
        while menu_thread.is_alive():
            menu_thread.join(timeout=0.5)
    except KeyboardInterrupt:
        print("Program has been terminated by user.")
        menu_thread.join()

    print("\033[H\033[J", end="")
    sys.exit(0)

if __name__ == "__main__":
    main()


