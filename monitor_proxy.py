from src.controller.fast_api_controller import FastAPIController
from src.logging_config import logging
from src.manager.manager import Manager
from src.manager.proxy_initializer_test import ProxyInitializerTest
from src.network.simple_queue import SimpleQueue
from src.network.proxy import Proxy
from src.network.receiver_udp import ReceiverUDP
from src.network.sender_udp import SenderUDP
import asyncio

from src.storage.json_storage import JSONStorage


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