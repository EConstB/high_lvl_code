import asyncio
from Robot_Packages.RobotMonitoring import MonitoringSystem
import os
import sys
class RobotController:
    def __init__(self, host, port) -> None:
        self.msys = MonitoringSystem()
        self.bat = self.msys.bat
        self.bat.bat_curr_volt = 36
        self.host = host
        self.port = port

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.writer.write("0_MS".encode())

    async def bat_testing(self):
        while True:
            self.bat.bat_curr_volt -= 0.8
            await asyncio.sleep(2)

    async def monsys_solver(self):
        try:
            async for msg in self.msys.monsys():
                self.writer.write(str(msg).encode())
                await self.writer.drain()
                print(f"Process with pid", os.getpid(), f"Send pckg {sys.getsizeof(msg)} bytes")
        finally:
            self.writer.write("END".encode())
            await self.writer.drain()
            self.writer.close()
            await self.writer.wait_closed()

async def main_async(host, port):
    robot = RobotController(host, port)
    await robot.connect()
    tasks = [
        robot.bat_testing(),
        robot.msys.task_run(),
        robot.monsys_solver()
    ]
    await asyncio.gather(*tasks)

def main():
    host = 'localhost'
    port = 8888
    asyncio.run(main_async(host, port))

if __name__ == "__main__":
    main()
