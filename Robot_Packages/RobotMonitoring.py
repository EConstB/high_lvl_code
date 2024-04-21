from Robot_Packages.BatterySolver import BatteryUnit
from Robot_Packages.DistanceSensor import DistanceSensorUnit
from Robot_Packages.Robot_state_parameters import RobotParameters as rb
import asyncio
import random

class MonitoringSystem:
    def __init__(self) -> None:
        self.bat = BatteryUnit(rb.Battery.bat_max_volt, rb.Battery.bat_min_volt)
        self.distance_sensors = self.init_ds(4)
        self.stop_event = asyncio.Event()
        self.resume_event = asyncio.Event()
        self.running_tasks = True

    def init_ds(self, qnt):
        return [DistanceSensorUnit(ds_unit) for ds_unit in range(qnt)]

    async def shutdown(self):
        print("Shutting down sensors and other components, robot is going to sleep")
        for task in self.tasks:
            task.cancel()
        # Here you could reset the events if you plan to restart tasks in future
        self.stop_event.clear()
        self.resume_event.set()

    async def bat_monitoring(self):
        while True:
            self.bat.bat_percent_value = self.bat.get_percent_val()
            print('bat_monitoring in progress', f'{self.bat.bat_percent_value:.2f}')
            
            if self.bat.bat_percent_value < 2 and self.running_tasks:
                print("Battery critically low. We die, capitan.")
                self.stop_event.set()
                self.resume_event.clear()
                self.running_tasks = False
            
            elif self.bat.bat_percent_value >= 2 and not self.running_tasks:
                print("Battery level recovered. Resuming operations.")
                self.resume_event.set()
                self.stop_event.clear()
                self.running_tasks = True

            await asyncio.sleep(1)

    async def ds_monitoring(self):
        while True:
            while not self.stop_event.is_set():
                print('TOF sensors monitoring in progress', random.randint(20, 200))
                await asyncio.sleep(0.2)
                
                await self.stop_event.wait()
                print("Monitoring paused due to low battery.")
                
                await self.resume_event.wait()
                print("Resuming TOF sensors monitoring.")
            
    async def task_launch(self):
        self.tasks = [
            asyncio.create_task(self.bat_monitoring()),
            asyncio.create_task(self.ds_monitoring())
        ]
        
        # Wait for the tasks to finish, which in this setup, they should only do so upon cancellation
        await asyncio.gather(*self.tasks, return_exceptions=True)

    def running(self):
        asyncio.run(self.task_launch())

