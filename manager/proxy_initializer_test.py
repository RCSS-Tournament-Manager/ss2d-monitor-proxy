from manager.proxy_initializer import IProxyInitializer
from manager.proxy_manager import ProxyManager
from network.delayed_queue_batch import DelayedQueueBatch
from network.proxy import Proxy
from network.receiver_rabbitmq import ReceiverRabbitMQ
from network.receiver_udp import ReceiverUDP
from network.receiver_web_socket import ReceiverWebSocket
from network.sender_rabbitmq import SenderRabbitMQ
from network.sender_udp import SenderUDP
from network.sender_web_socket import SenderWebSocket
from network.simple_queue import SimpleQueue
from network.simple_queue_batch import SimpleQueueBatch


class ProxyInitializerTest(IProxyInitializer):
    def __init__(self) -> None:
        super().__init__()
        
    def init_1(self, proxy_manager: ProxyManager) -> bool:
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverUDP(('localhost', 6000)), # RCSSServer
            senders=[SenderUDP(('localhost', 6500))],
            queue=SimpleQueue()
        ))
        
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverUDP(('localhost', 6000)),
            senders=[SenderRabbitMQ()],
            queue=SimpleQueue()
        ))
        
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverRabbitMQ(),
            senders=[SenderUDP(('localhost', 6600))],
            queue=SimpleQueue()
        ))
        
    def init_2(self, proxy_manager: ProxyManager) -> bool:
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverUDP(('localhost', 6000)), # RCSSServer
            senders=[
                SenderUDP(('localhost', 6500)),
                SenderRabbitMQ()
            ],
            queue=SimpleQueueBatch(2)
        ))
        
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverRabbitMQ(),
            senders=[SenderUDP(('localhost', 6600))],
            queue=SimpleQueueBatch(1)
        ))
        
    def init_3(self, proxy_manager: ProxyManager) -> bool:
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverUDP(('localhost', 6000)), # RCSSServer
            senders=[
                SenderUDP(('localhost', 6500)),
                SenderRabbitMQ()
            ],
            queue=DelayedQueueBatch(2, 50)
        ))
        
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverRabbitMQ(),
            senders=[SenderUDP(('localhost', 6600))],
            queue=SimpleQueueBatch(1)
        ))
    
    def init_4(self, proxy_manager: ProxyManager) -> bool:
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverUDP(('localhost', 6000)), # RCSSServer
            senders=[
                SenderWebSocket(('localhost', 7000)),
            ],
            queue=SimpleQueueBatch(1)
        ))
        
        proxy_manager.add_proxy(Proxy(
            receiver=ReceiverWebSocket(('localhost', 7000)),
            senders=[
                SenderUDP(('localhost', 6800)),
            ],
            queue=SimpleQueueBatch(1)
        ))
        
    def init_5(self, proxy_manager: ProxyManager) -> bool:
        self.init_3(proxy_manager)
        self.init_4(proxy_manager)
        
    def initialize(self, proxy_manager: ProxyManager) -> bool:
        # self.init_3(proxy_manager)
        self.init_5(proxy_manager)