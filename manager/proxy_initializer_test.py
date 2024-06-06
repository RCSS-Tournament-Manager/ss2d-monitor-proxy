from manager.proxy_initializer import IProxyInitializer
from manager.proxy_manager import ProxyManager
from network.proxy import Proxy
from network.receiver_rabbitmq import ReceiverRabbitMQ
from network.receiver_udp import ReceiverUDP
from network.sender_rabbitmq import SenderRabbitMQ
from network.sender_udp import SenderUDP
from network.simple_queue import SimpleQueue


class ProxyInitializerTest(IProxyInitializer):
    def __init__(self) -> None:
        super().__init__()
    
    def initialize(self, proxy_manager: ProxyManager) -> bool:
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverUDP(('localhost', 6000)),
            sender=SenderUDP(('localhost', 6500)),
            queue=SimpleQueue()
        ))
        
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverUDP(('localhost', 6000)),
            sender=SenderRabbitMQ(),
            queue=SimpleQueue()
        ))
        
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverRabbitMQ(),
            sender=SenderUDP(('localhost', 6600)),
            queue=SimpleQueue()
        ))