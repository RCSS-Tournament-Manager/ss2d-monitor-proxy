import logging
from queue import Queue


class IQueue:
    def __init__(self) -> None:
        self.queue: list = []
    
    async def put(self, msg: str):
        logging.info("Putting message: IT SHOULD NOT BE PRINTED :X")
        pass
    
    async def get(self, i) -> str:
        pass
    
    def size(self) -> int:
        pass
    
    def get_queue(self, i) -> 'IQueue':
        pass