from Robot_Packages.RobotMonitoring import MonitoringSystem
from Robot_Packages.RobotMovement import RobotMovement
import asyncio
import time
from multiprocessing import Process

class RobotController:
    def __init__(self) -> None:
        self.msys = MonitoringSystem()
        self.bat = self.msys.bat
        self.ds_sens = self.msys.distance_sensors

robot = RobotController()
battery = robot.bat
battery.bat_curr_volt = battery.bat_max_volt

async def bat_testing():
    while True:
        battery.bat_curr_volt -=0.12
        await asyncio.sleep(0.6)

async def main_async():
    tasks = [bat_testing(), robot.msys.task_launch()]
    await asyncio.gather(*tasks)

def main():
    asyncio.run(main_async())
       

if __name__ == '__main__':
    # Creating separate processes
    p1 = Process(target=main)
    # Starting the processes
    p1.start()
    # Joining the processes to ensure they complete execution
    p1.join()
