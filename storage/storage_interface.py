from controller.context_model.proxy_info_context import ProxyInfoContext


class IStorage:
    def __init__(self) -> None:
        pass
    
    def add_proxy(self, proxy: ProxyInfoContext) -> None:
        pass
    
    def remove_proxy(self, proxy: ProxyInfoContext) -> None:
        pass
    
    def get_all_proxies(self) -> list[ProxyInfoContext]:
        pass
    
    def remove_all_proxies(self) -> None:
        pass