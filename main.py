import logging
from network.simple_queue import SimpleQueue
from network.proxy import Proxy
from network.receiver_udp import ReceiverUDP
from network.sender_udp import SenderUDP
import asyncio

logging.basicConfig(level=logging.DEBUG)



async def main():
    proxy = Proxy(
        receiver=ReceiverUDP(("localhost", 6000)),
        sender=SenderUDP(("localhost", 6500)),
        queue=SimpleQueue()
    )
    await proxy.run()

asyncio.run(main())
asyncio.get_event_loop().run_forever()