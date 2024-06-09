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
        self.logging = logging.getLogger(f"Receiver-{self.get_name()}")
        
    async def receive(self) -> str:
        try:
            msg, new_address = await asyncio.get_event_loop().run_in_executor(None, self.socket.recvfrom, UDP_BUFFER_SIZE)
            await self.queue.put(msg.decode())
        except socket.timeout:
            self.logging.info(f"Timeout at {self.address}, retrying...")
            dummy_sender_task = asyncio.create_task(self.send_dummy())
            await self.initialize(self.queue)
            dummy_sender_task.cancel()
            
    
    async def send_dummy(self) -> None:
        while True:
            self.logging.info("Sending dummy message, to keep the connection alive")
            self.logging.info("#"*30)
            await self.queue.put('()')
            await asyncio.sleep(0.5)
    
    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        while True:
            await asyncio.sleep(0.5)
            self.logging.info('Initializing receiver connection')
            self.socket.sendto(MONITOR_INITIAL_MESSAGE.encode(), self.address)
            try:
                msg, new_address = await asyncio.get_event_loop().run_in_executor(None, self.socket.recvfrom, UDP_BUFFER_SIZE)
                break
            except socket.timeout:
                self.logging.debug(f"Receiver did not get any response {self.address}")
                continue
    
    def get_name(self) -> str:
        return f"UDP-{self.address[0]}-{self.address[1]}"
            