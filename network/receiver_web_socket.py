import asyncio
import logging

import websockets
from network.communication import ComType
from network.proxy_queue import IQueue
from network.receiver import IReceiver
from network.receiver_udp import MONITOR_INITIAL_MESSAGE


class ReceiverWebSocket(IReceiver):
    def __init__(self, address: tuple[str, int]) -> None:
        self.address = address
        self.logging = logging.getLogger(f"Receiver-{self.get_name()}")
        self.web_socket = None
        self.receiver_task = None

    async def receive(self) -> str:
        msg = await self.web_socket.recv()
        self.logging.info(f"<--- Receiving message: {msg}")
        await self.queue.put(msg)
    
    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        while True:
            await asyncio.sleep(0.5)
            self.logging.info('Initializing receiver connection')
            try:
                self.web_socket = await websockets.connect(f'ws://{self.address[0]}:{self.address[1]}')
                await self.web_socket.send(f'{MONITOR_INITIAL_MESSAGE}|123.rcg')
                break
            except Exception as e:
                self.logging.debug(f"Receiver did not get any response {self.address}")
                self.logging.error(e)
        

    def get_name(self) -> str:
        return f"WS-{self.address}"

    def get_type(self) -> ComType:
        return ComType.WS