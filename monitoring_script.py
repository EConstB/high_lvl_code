from Robot_Packages.RobotMonitoring import MonitoringSystem
import asyncio
from multiprocessing import Process, Queue

class RobotController:
    def __init__(self, queue) -> None:
        self.msys = MonitoringSystem()
        self.bat = self.msys.bat
        self.queue = queue
        self.bat.bat_curr_volt = 36

    async def bat_testing(self):
        while True:
            self.bat.bat_curr_volt -= 0.8
            await asyncio.sleep(2)

    async def monsys_solver(self):
        async for msg in self.msys.monsys():
            self.queue.put(msg)
        self.queue.put(None)  # Сигнал о завершении

async def main_async(queue):
    robot = RobotController(queue)
    tasks = [
        robot.bat_testing(),
        robot.msys.task_run(),
        robot.monsys_solver()
    ]
    await asyncio.gather(*tasks)

def process_main(queue):
    asyncio.run(main_async(queue))

def main():
    queue = Queue()
    p = Process(target=process_main, args=(queue,))
    p.start()
    p.join()

if __name__ == "__main__":
    main()
