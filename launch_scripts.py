import asyncio

# Использование словаря для организации данных по категориям
data_store = {
    "0_MS": [],
    "1_TO": []
}

async def handle_client(reader, writer):
    try: 
        addr = writer.get_extra_info('peername')
        client_id = await reader.read(100)
        client_id = client_id.decode().strip()
        print(f"New connection from {addr}, identified as {client_id}")
    except E:
        print("Error with connection")
    try:
        while True:
            data = await reader.read(4096)
            if not data:
                print(f"Client {client_id} disconnected.")
                break
            message = data.decode().strip()
            
            if client_id in data_store:
                data_store[client_id].append(message)
                print(f"Data updated for {client_id}: {data_store[client_id][-1]}")
            else:
                print(f"Unknown client ID {client_id}. Ignoring data.")

            writer.write(f"Received your message: {message}".encode())
            await writer.drain()
    except Exception as e:
        print(f"Error with {client_id}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Connection with {client_id} closed")

async def main_server():
    server = await asyncio.start_server(handle_client, 'localhost', 8888)
    async with server:
        print("Server started at localhost:8888")
        await server.serve_forever()

asyncio.run(main_server())
