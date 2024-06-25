from controller.fast_api_controller import FastAPIController
from logging_config import logging
from manager.manager import Manager
from manager.proxy_initializer_test import ProxyInitializerTest
from network.simple_queue import SimpleQueue
from network.proxy import Proxy
from network.receiver_udp import ReceiverUDP
from network.sender_udp import SenderUDP
import asyncio

from storage.json_storage import JSONStorage


logger = logging.getLogger(__name__)


async def main():
    logger.info('Starting main thread')
    
    storage = JSONStorage()
    
    manager = Manager(storage)
    manager.initialize([])
    manager.run()
    controller = FastAPIController(manager, 'token', 'safe', 8500)

    logger.info('Main thread Waiting for manager and controller to finish')
    manager_task = asyncio.create_task(manager.wait())
    controller_task = asyncio.create_task(controller.run())
    await asyncio.gather(manager_task, controller_task)

    
    
asyncio.run(main())
asyncio.get_event_loop().run_forever()