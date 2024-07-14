
import asyncio
import websockets

from src.network.receiver_udp import MONITOR_INITIAL_MESSAGE


async def main():
    web_socket = await websockets.connect(f'ws://localhost:{4000}')
    await web_socket.send(MONITOR_INITIAL_MESSAGE)
    while True:
        msg = await web_socket.recv()
        print(msg)
        
# run main
asyncio.run(main())
