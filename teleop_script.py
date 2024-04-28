import socket
import asyncio
from Robot_Packages.RobotMovement import RobotMovement
import serial
rm = RobotMovement()

async def teleOp_solver(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("TeleOp script is connected")
    device = serial.Serial("COM9", 9600 )
    #device.timeout = 0.05
    try:
        device.open()
    except Exception as e:
        pass
    # Отправляем идентификатор клиента
    client_socket.send("1_TO".encode())
    for msg in rm.teleOp():
        #cmd = f'Q{msg[0]},{msg[1]},{msg[2]},{msg[3]}e'.encode('utf-8')
        cmd = 'Q1,100,0,0e'.encode('utf-8')
        print(cmd)
        device.write(cmd)
    #     client_socket.send(str(msg).encode())
    # client_socket.send("END".encode())
    # client_socket.close()
    # print("Messages sent and connection closed.")

async def main_async(host, port):
    asyncio.gather(teleOp_solver(host, port))

def main(host, port):
    asyncio.run(main_async(host, port))

if __name__ == "__main__":
    host = "localhost"
    port = 8888
    main(host, port)
