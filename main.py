import logging
from network.proxy import Proxy
from network.receiver_udp import ReceiverUDP
from network.sender_udp import SenderUDP

logging.basicConfig(level=logging.DEBUG)


proxy = Proxy(
    receiver=ReceiverUDP(("localhost", 6000)),
    sender=SenderUDP(("localhost", 6500))
)

proxy.run()