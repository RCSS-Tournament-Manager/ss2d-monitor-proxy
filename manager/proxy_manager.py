from network.proxy import Proxy


class ProxyManager:
    def __init__(self) -> None:
        self.proxy: list[Proxy] = []
    
    def add_proxy(self, proxy: Proxy) -> None:
        self.proxy.append(proxy)
        
    def run(self, index = None) -> None:
        if index is None:
            for proxy in self.proxy:
                proxy.run()
        else:
            self.proxy[index].run()
    
    def stop(self, index = None) -> None:
        if index is None:
            for proxy in self.proxy:
                proxy.stop()
        else:
            self.proxy[index].stop()
            
    def delete(self, index) -> None:
        self.proxy.pop(index)
    