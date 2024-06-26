import asyncio
import logging

import websockets
from src.network.communication import ComType
from src.network.proxy_queue import IQueue
from src.network.receiver_udp import MONITOR_INITIAL_MESSAGE
from src.network.sender import ISender


class SenderWebSocket(ISender):
    def __init__(self, address: tuple[str, int]) -> None:
        self.address = address
        self.logging = logging.getLogger(f"Sender-{self.get_name()}")
        self.server_task = None
        self.connected = False

    async def send(self) -> None:
        pass
    
    async def sender(self, websocket) -> None:
        if self.connected:
            self.logging.warning("Already connected")
            return
        
        message = await websocket.recv()
        self.logging.info(f"Received initial message: {message}")
        file = None
        if message.startswith(MONITOR_INITIAL_MESSAGE):
            self.connected = True
            
            data = message.split('|')
            if len(data) > 1:
                self.logging.info(f"File Streaming: {data[1]}")
                file = open(data[1], 'r')
        sleep = False
        while True:
            if file is None:
                msg = await self.queue.get()
                await websocket.send(msg)
            else:
                if sleep:
                    await asyncio.sleep(0.1)
                    sleep = False
                line = file.readline()
                if line.startswith('(show'):
                    sleep = True
                if not line:
                    break
                await websocket.send(line)

    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        await websockets.serve(self.sender, self.address[0], self.address[1])
        self.logging.info("Server started")
            
    def get_name(self) -> str:
        return f"WS-{self.address}"
    
    def get_type(self) -> ComType:
        return ComType.WS

# json
# app folder
# websocket
# file reader