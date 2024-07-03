import asyncio
from src.controller.context_model.proxy_info_context import ProxyInfoContext
from src.network.proxy import Proxy
from src.storage.storage_interface import IStorage


class ProxyManager:
    def __init__(self, storage: IStorage) -> None:
        self.proxy: list[Proxy] = []
        self.proxy_tasks: list[asyncio.Task] = []
        self.storage: IStorage = storage
        self.load_proxies()
        
    def add_proxy(self, proxy: Proxy, save=True) -> None:
        self.proxy.append(proxy)
        if save:
            self.storage.add_proxy(ProxyInfoContext.convert_to_context(proxy))
        
    def run(self, index = None) -> None:
        if index is None:
            self.proxy_tasks.extend([asyncio.create_task(proxy.run()) for proxy in self.proxy]) # TODO IT Was proxy.run() before; no task creation; check this for sleep?
        else:
            self.proxy_tasks.append(asyncio.create_task(self.proxy[index].run()))
    
    def stop(self, index = None) -> None:
        if index is None:
            for proxy in self.proxy:
                proxy.stop()
        else:
            self.proxy[index].stop()
            
    def delete(self, index) -> None:
        proxy = self.proxy.pop(index)
        self.storage.remove_proxy(ProxyInfoContext.convert_to_context(proxy))
        
    async def wait_for_proxies(self):
        await asyncio.gather(*self.proxy_tasks)
        
    async def add_and_run_proxy(self, proxy: Proxy):
        self.add_proxy(proxy)
        self.proxy_tasks.append(asyncio.create_task(proxy.run()))
        
    def load_proxies(self):
        for proxy in ProxyInfoContext.convert_inverse(self.storage.get_all_proxies()):
            self.add_proxy(proxy, save=False)