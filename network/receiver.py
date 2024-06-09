from network.proxy_queue import IQueue


class IReceiver:
    def __init__(self) -> None:
        self.queue = None
    
    async def receive(self) -> str:
        pass
    
    async def initialize(self, queue: IQueue) -> None:
        self.queue = queue
        
    def get_name(self) -> str:
        return "Receiver"
    
    