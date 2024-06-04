import logging
import socket
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
        
    def receive(self) -> str:
        msg, new_address = self.socket.recvfrom(UDP_BUFFER_SIZE)
        self.address = new_address
        return msg.decode()
    
    def initialize(self) -> None:
        logging.debug(f'{self.address=}')
        self.socket.sendto(MONITOR_INITIAL_MESSAGE.encode(), self.address)