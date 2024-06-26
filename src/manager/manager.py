import asyncio
from src.manager.proxy_initializer import IProxyInitializer
from src.manager.proxy_manager import ProxyManager
from src.storage.storage_interface import IStorage

class Manager:
    def __init__(self, storage: IStorage) -> None:
        self.proxy_manager = ProxyManager(storage)
    
    def initialize(self, proxy_initializers: list[IProxyInitializer]):
        for initializer in proxy_initializers:
            initializer.initialize(self.proxy_manager)
            
    def run(self, index=None) -> None:
        self.proxy_manager.run(index)
        
    async def wait(self):
        while len(self.proxy_manager.proxy) == 0:
            await asyncio.sleep(0.5)
        await self.proxy_manager.wait_for_proxies()
        
    def get_proxies(self):
        return self.proxy_manager.proxy
    
    async def add_proxies(self, proxies):
        for proxy in proxies:
            await self.proxy_manager.add_and_run_proxy(proxy)