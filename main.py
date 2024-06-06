from logging_config import logging
from manager.manager import Manager
from manager.proxy_initializer_test import ProxyInitializerTest
from network.simple_queue import SimpleQueue
from network.proxy import Proxy
from network.receiver_udp import ReceiverUDP
from network.sender_udp import SenderUDP
import asyncio


logger = logging.getLogger(__name__)


async def main():
    logger.info('Starting main thread')

    manager = Manager()
    manager.initialize([
        ProxyInitializerTest(),
    ])
    
    manager.run()

    logger.info('Manager started, Waiting in main thread')

    await manager.wait()

    logger.info('Main thread is done, exiting...')
    
    
asyncio.run(main())
asyncio.get_event_loop().run_forever()