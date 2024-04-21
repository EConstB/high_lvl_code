from Robot_Packages.RobotMonitoring import MonitoringSystem
import asyncio

class RobotController:
    def __init__(self) -> None:
        self.msys = MonitoringSystem()
        self.bat = self.msys.bat
        self.bat.bat_max_volt = 36.00
        self.bat.bat_min_volt = 28.00
        self.bat.bat_curr_volt = None
        self.ds_sens = self.msys.dist_sensors


robot = RobotController()
battery = robot.bat
battery.bat_curr_volt = battery.bat_max_volt

async def bat_testing():
    while True:
        battery.bat_curr_volt -= 0.8
        await asyncio.sleep(1)

async def main():
    tasks = [ bat_testing(),
              robot.msys.task_launch() ]

    await asyncio.gather(*tasks)

asyncio.run(main())
#robot.msys.running()