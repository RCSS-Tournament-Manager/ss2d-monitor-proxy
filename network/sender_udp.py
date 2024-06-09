import asyncio
import logging
import socket
from network.proxy_queue import IQueue
from network.receiver_udp import MONITOR_INITIAL_MESSAGE, UDP_BUFFER_SIZE
from network.sender import ISender

# TODO MOVE THIS SOMEWHERE ELSE
WAIT_FOR_MONITOR_INTERVAL = 10

class SenderUDP(ISender):
    def __init__(self, address: tuple[str, int]) -> None:
        self.address = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.address)
        self.socket.settimeout(WAIT_FOR_MONITOR_INTERVAL)
        self.logging = logging.getLogger(f"Sender-{self.get_name()}")

    async def send(self) -> None:
        dummy_sender_task = asyncio.create_task(self.send_dummy())
        msg = await self.queue.get()
        dummy_sender_task.cancel()
        self.socket.sendto(msg.encode(), self.address)
        
    async def send_dummy(self) -> None:
        while True:
            await asyncio.sleep(0.5)
            self.socket.sendto("()".encode(), self.address)

    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        self.logging.info("Waiting for monitor to initialize")
        while True:
            await asyncio.sleep(0.1)
            self.logging.info(f"Trying to initialize monitor at {self.address}")
            
            try:
                msg, new_address = await asyncio.get_event_loop().run_in_executor(None, self.socket.recvfrom, UDP_BUFFER_SIZE)
                self.logging.debug(f"Received {msg}")
            except socket.timeout:
                self.logging.debug("Monitor did not respond")
                continue
            
            self.address = new_address
            msg = msg.decode()
            break
            # TODO CHECK THIS ERROR: CRITICAL:root:Expected '(dispinit version 5)', but got '(dispinit version 5)'
            # if msg != MONITOR_INITIAL_MESSAGE:
            #     self.logging.critical(f"Expected '{MONITOR_INITIAL_MESSAGE}', but got '{msg}'")
            # else:
            #     self.logging.info("Monitor initialized")
            #     break
    
    def get_name(self) -> str:
        return f"UDP-{self.address[0]}-{self.address[1]}"