import asyncio
from network.proxy import Proxy


class ProxyManager:
    def __init__(self) -> None:
        self.proxy: list[Proxy] = []
        self.proxy_tasks: list[asyncio.Task] = []
    
    def add_proxy(self, proxy: Proxy) -> None:
        self.proxy.append(proxy)
        
    def run(self, index = None) -> None:
        if index is None:
            self.proxy_tasks.extend([proxy.run() for proxy in self.proxy])
        else:
            self.proxy_tasks.append(self.proxy[index].run())
    
    def stop(self, index = None) -> None:
        if index is None:
            for proxy in self.proxy:
                proxy.stop()
        else:
            self.proxy[index].stop()
            
    def delete(self, index) -> None:
        self.proxy.pop(index)
        
    async def wait_for_proxies(self):
        await asyncio.gather(*self.proxy_tasks)