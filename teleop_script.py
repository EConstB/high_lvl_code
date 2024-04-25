import socket
import asyncio
from Robot_Packages.RobotMovement import RobotMovement

rm = RobotMovement()

async def teleOp_solver(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("TeleOp script is connected")

    # Отправляем идентификатор клиента
    client_socket.send("1_TO".encode())
    for msg in rm.teleOp():
        client_socket.send(str(msg).encode())
    client_socket.send("END".encode())
    client_socket.close()
    print("Messages sent and connection closed.")

async def main_async(host, port):
    asyncio.gather(teleOp_solver(host, port))

def main(host, port):
    asyncio.run(main_async(host, port))

if __name__ == "__main__":
    host = "localhost"
    port = 8888
    main(host, port)
