import logging
import socket
from network.proxy_queue import IQueue
from network.receiver_udp import MONITOR_INITIAL_MESSAGE, UDP_BUFFER_SIZE
from network.sender import ISender

# TODO MOVE THIS SOMEWHERE ELSE
WAIT_FOR_MONITOR_INTERVAL = 10
NUMBER_OF_TRIES_TO_WAIT_FOR_MONITOR = 3

class SenderUDP(ISender):
    def __init__(self, address: tuple[str, int]) -> None:
        self.address = address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.address)
        self.socket.settimeout(WAIT_FOR_MONITOR_INTERVAL)

    async def send(self) -> None:
        msg = await self.queue.get()
        self.socket.sendto(msg.encode(), self.address)

    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        logging.info("Waiting for monitor to initialize")
        for _ in range(NUMBER_OF_TRIES_TO_WAIT_FOR_MONITOR):
            logging.debug(f"Trying to initialize monitor at {self.address}")
            logging.debug(f"Trying number {_ + 1} out of {NUMBER_OF_TRIES_TO_WAIT_FOR_MONITOR}")
            
            try:
                msg, new_address = self.socket.recvfrom(UDP_BUFFER_SIZE) # TODO IT IS BLOCKING; CHANGE IT WITH ASYNCIO
            except socket.timeout:
                logging.debug("Monitor did not respond")
                continue
            
            self.address = new_address
            
            msg = msg.decode()
            break
            # TODO CHECK THIS ERROR: CRITICAL:root:Expected '(dispinit version 5)', but got '(dispinit version 5)'
            # if msg != MONITOR_INITIAL_MESSAGE:
            #     logging.critical(f"Expected '{MONITOR_INITIAL_MESSAGE}', but got '{msg}'")
            # else:
            #     logging.info("Monitor initialized")
            #     break
        