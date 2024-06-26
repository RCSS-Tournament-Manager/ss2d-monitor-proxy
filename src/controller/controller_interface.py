import logging
from src.manager.manager import Manager
from src.network.proxy import Proxy


class IController:
    def __init__(self, manager: Manager) -> None:
        self.manager: Manager = manager
        self.logging = logging.getLogger("IController")
        
    async def add_proxy(self, proxies: list[Proxy]):
        self.logging.info("add_proxy")
        await self.manager.add_proxies(proxies)
        
    async def remove_proxy(self):
        self.logging.info("remove_proxy")
        
    async def restart_proxy(self):
        self.logging.info("restart_proxy")
    
    async def run(self):
        pass