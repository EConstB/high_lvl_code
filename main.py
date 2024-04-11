from Robot_Packages.BatterySolver import BatteryUnit
from Robot_Packages.DistanceSensor import DistanceSensorUnit
import asyncio
import random


class Robot:
    def __init__(self) -> None:
        self.battery = BatteryUnit(36.00, 28.00)

        self.distance_sensors = [DistanceSensorUnit(1),
                                 DistanceSensorUnit(2),
                                 DistanceSensorUnit(3),
                                 DistanceSensorUnit(4)]


robot = Robot()
battery = robot.battery
ds = robot.distance_sensors
curr_val = battery.bat_max_volt


async def get_battery_data(curr_val=None):
    ita = 0
    while True:
        ita += 1
        curr_val -= 0.01
        battery.get_bat_data(curr_value=curr_val)
        battery.battery_monitoring()
        if 48 <= battery.bat_percent_value <= 50:
            pass
        if battery.bat_percent_value <= 0.5:
            break
        await asyncio.sleep(0.2)


async def get_ds_data():
    while True:
        for ds_units in ds:
            ds_units.cur_value_ds = random.randint(0, 100, ) / 100
        await asyncio.sleep(0.4)


async def monitoring_ds_and_bat():
    while True:
        print(f'bat:{battery.bat_percent_value:.2f}%,'
              f' ds0={ds[0].cur_value_ds}, ds1={ds[1].cur_value_ds},'
              f' ds2={ds[2].cur_value_ds}, ds3={ds[3].cur_value_ds}', end='')
        await asyncio.sleep(1)
        print(end='\r')


async def main():
    tasks = [
        get_battery_data(curr_val),
        get_ds_data(),
        monitoring_ds_and_bat()
    ]
    await asyncio.gather(*tasks)


asyncio.run(main())
