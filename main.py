import logging
from manager.manager import Manager
from manager.proxy_initializer_test import ProxyInitializerTest
from network.simple_queue import SimpleQueue
from network.proxy import Proxy
from network.receiver_udp import ReceiverUDP
from network.sender_udp import SenderUDP
import asyncio

logging.basicConfig(level=logging.DEBUG)

async def main():
    manager = Manager()
    manager.initialize([
        ProxyInitializerTest(),
    ])
    
    manager.run()
    logging.info('Manager started, Waiting in main thread')
    await manager.wait()
    logging.info('Main thread is done, exiting...')
    
    

asyncio.run(main())
asyncio.get_event_loop().run_forever()