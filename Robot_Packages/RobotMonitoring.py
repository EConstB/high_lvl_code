from Robot_Packages.BatterySolver import BatteryUnit
from Robot_Packages.DistanceSensor import DistanceSensorUnit
from Robot_Packages.Robot_state_parameters import RobotParameters as rb
import colorama
from colorama import Fore
import asyncio
import random

class MonitoringSystem:
    

    def __init__(self) -> None:
        colorama.init(autoreset=True)
        # Initialize the battery unit with max and min voltage from the robot parameters
        self.bat = BatteryUnit(rb.Battery.bat_max_volt, rb.Battery.bat_min_volt)
        # Initialize the distance sensors array with the specified number
        self.distance_sensors = self.init_ds(4)
        # Create an asyncio Event to manage the stopping of sensors based on battery level
        self.stop_event = asyncio.Event()
        # Flag to keep track of whether tasks should be running
        self.running_tasks = True


    def init_ds(self, quantity):
        # Create a list of distance sensor units
        return [DistanceSensorUnit(i) for i in range(quantity)]


    async def bat_monitoring(self):
        # Continuously monitor the battery percentage
        while True:
            
            self.bat.bat_percent_value = self.bat.get_percent_val()

            # Check if battery level is critically low and if tasks are currently running
            if self.bat.bat_percent_value < 2 and self.running_tasks:
                print(f"{Fore.RED}Battery critically low. System shutdown initiated.")
                self.running_tasks = False
                self.stop_event.set()

            # Check if battery level has recovered and if tasks are not running
            elif self.bat.bat_percent_value >= 5 and not self.running_tasks:
                print(f"{Fore.GREEN}Battery level recovered. Restarting system.")
                self.running_tasks = True
                self.stop_event.clear()
                await self.restart_tasks()

            await asyncio.sleep(1)


    async def ds_monitoring(self):
        # Monitor distance sensors unless the stop event is set
        try:
            while not self.stop_event.is_set():

                # it's emulated of getting data from ds with random values
                for dsunit in self.distance_sensors:
                    dsunit.cur_value_ds = random.randint(2, 100)

                await asyncio.sleep(0.2)

        except asyncio.CancelledError:
            print(f"{Fore.MAGENTA}TOF sensors monitoring task was cancelled.")


    async def monsys(self):

        while True:
            print(f'Bat:{self.bat.bat_percent_value:.2f}%', end=' ')

            for dsunit in self.distance_sensors:
                print(f'DS{dsunit.name}:{dsunit.cur_value_ds}', end=' ')

            print(end='\r')

            await asyncio.sleep(0.5)


    async def restart_tasks(self):
        # Restart distance sensor monitoring task if it has completed (either normally or due to cancellation)
        if self.ds_task.done():
            self.ds_task = asyncio.create_task(self.ds_monitoring())


    async def task_run(self, print_values:int=0):
        # Launch battery and distance sensor monitoring tasks
        self.bat_task = asyncio.create_task(self.bat_monitoring())
        self.ds_task = asyncio.create_task(self.ds_monitoring())

        if print_values == 1:
            self.monsys_task = asyncio.create_task(self.monsys())

        # Await the battery monitoring task to complete
        await self.bat_task 
        # If the distance sensor task is not yet done, cancel it
        if not self.ds_task.done():
            self.ds_task.cancel()
        # Await the distance sensor task to handle cancellation properly
        await self.ds_task


    def running(self):
        # Run the main task launching function within an asyncio event loop
        asyncio.run(self.task_run())

