from manager.proxy_manager import ProxyManager


class IProxyInitializer:
    def __init__(self) -> None:
        pass
    
    def initialize(self, proxy_manager: ProxyManager) -> bool:
        pass
    
    