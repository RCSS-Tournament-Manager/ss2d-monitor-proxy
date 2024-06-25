import asyncio
import logging

import websockets
from network.communication import ComType
from network.proxy_queue import IQueue
from network.receiver_udp import MONITOR_INITIAL_MESSAGE
from network.sender import ISender


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
        if message.startswith(MONITOR_INITIAL_MESSAGE):
            self.connected = True
        while True:
            self.logging.info("Waiting for message")
            msg = await self.queue.get()
            self.logging.info(f"---> Sending message: {msg}")
            await websocket.send(msg)

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