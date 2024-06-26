import asyncio
import logging

import websockets
from src.network.communication import ComType
from src.network.proxy_queue import IQueue
from src.network.receiver import IReceiver
from src.network.receiver_udp import MONITOR_INITIAL_MESSAGE


class ReceiverWebSocket(IReceiver):
    def __init__(self, address: tuple[str, int], file_stream: str = None) -> None:
        self.address = address
        self.logging = logging.getLogger(f"Receiver-{self.get_name()}")
        self.web_socket = None
        self.receiver_task = None
        self.file_stream = file_stream
        self.inital_message = f'{MONITOR_INITIAL_MESSAGE}'
        if self.file_stream is not None:
            self.inital_message += f'|{self.file_stream}'

    async def receive(self) -> str:
        msg = await self.web_socket.recv()
        await self.queue.put(msg)
    
    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        while True:
            await asyncio.sleep(0.5)
            self.logging.info('Initializing receiver connection')
            try:
                self.web_socket = await websockets.connect(f'ws://{self.address[0]}:{self.address[1]}')
                await self.web_socket.send(self.inital_message)
                break
            except Exception as e:
                self.logging.debug(f"Receiver did not get any response {self.address}")
                self.logging.error(e)
        

    def get_name(self) -> str:
        return f"WS-{self.address}"

    def get_type(self) -> ComType:
        return ComType.WS