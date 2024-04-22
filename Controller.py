from Robot_Packages.RobotMonitoring import MonitoringSystem
import asyncio

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
        battery.bat_curr_volt += float(input('Enter your info: '))
        #battery.bat_curr_volt -= 0.12
        await asyncio.sleep(0.6)

async def main():
    tasks = [ bat_testing(),
              robot.msys.task_launch() ]

    await asyncio.gather(*tasks)

asyncio.run(main())
#robot.msys.running()