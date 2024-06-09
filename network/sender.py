from network.proxy_queue import IQueue


class ISender:
    def __init__(self) -> None:
        self.queue = None
    
    async def send(self, msg: str) -> None:
        pass
    
    async def initialize(self, queue: IQueue) -> None:
        self.queue = queue
        
    def get_name():
        return "Sender"