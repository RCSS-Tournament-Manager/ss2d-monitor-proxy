from manager.proxy_initializer import IProxyInitializer
from manager.proxy_manager import ProxyManager

class Manager:
    def __init__(self) -> None:
        self.proxy_manager = ProxyManager()
    
    def initialize(self, proxy_initializers: list[IProxyInitializer]):
        for initializer in proxy_initializers:
            initializer.initialize(self.proxy_manager)
            