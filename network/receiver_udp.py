import asyncio
import logging
import socket
from network.proxy_queue import IQueue
from network.receiver import IReceiver

# TODO MOVE THIS SOMEWHERE ELSE
SOCKET_INTERVAL = 1 
UDP_BUFFER_SIZE = 10000
MONITOR_INITIAL_MESSAGE = '(dispinit version 5)'

class ReceiverUDP(IReceiver):
    def __init__(self, address: tuple[str, int]) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(SOCKET_INTERVAL)
        self.address = address
        
    async def receive(self) -> str:
        msg = await asyncio.get_event_loop().sock_recv(self.socket, UDP_BUFFER_SIZE)
        await self.queue.put(msg.decode())
    
    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        logging.debug(f'{self.address=}')
        self.socket.sendto(MONITOR_INITIAL_MESSAGE.encode(), self.address)