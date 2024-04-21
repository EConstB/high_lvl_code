from Robot_Packages.BatterySolver import BatteryUnit
from Robot_Packages.DistanceSensor import DistanceSensorUnit
import asyncio

class MonitoringSystem:
    def __init__(self) -> None:

        self.bat = BatteryUnit()

        self.dist_sensors = []
        self.ds_quantity = 0

        self.ita = 0
        self.ita1 = 0

        for ds_unit in range(self.ds_quantity):
            self.dist_sensors.append(DistanceSensorUnit(ds_unit))
        
    async def bat_monitoring(self):
        while True:
            self.bat.bat_percent_value = self.bat.get_percent_val()
            print('bat_monitoring in progress', f'{self.bat.bat_percent_value:.2f}' )
            if self.bat.bat_percent_value < 2:
                print(" We are dead, capitan")
                break

            await asyncio.sleep(1)

            
    async def ds_monitoring(self):
        while True:
            self.ita1 += 1
            print('tof_sensors monitoring in progress', self.ita1)
            await asyncio.sleep(0.2)


    async def task_launch(self):
        tasks = [
            self.bat_monitoring(),
            self.ds_monitoring()
        ]
        await asyncio.gather(*tasks)

    def running(self):
        asyncio.run(self.task_launch())
