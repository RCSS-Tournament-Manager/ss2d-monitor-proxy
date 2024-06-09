from network.communication import ICom
from network.proxy_queue import IQueue


class ISender(ICom):
    def __init__(self) -> None:
        super().__init__()
    
    async def send(self, msg: str) -> None:
        pass
    
    def get_name():
        return "Sender"