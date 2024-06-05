from queue import SimpleQueue
from manager.proxy_initializer import IProxyInitializer
from network.proxy import Proxy
from network.receiver_udp import ReceiverUDP
from network.sender_udp import SenderUDP


class ProxyInitializerTest(IProxyInitializer):
    def __init__(self) -> None:
        super().__init__()
    
    def initialize(self, proxy_manager) -> bool:
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverUDP(('localhost', 6000)),
            sender=SenderUDP(('localhost', 6500)),
            queue=SimpleQueue()
        ))