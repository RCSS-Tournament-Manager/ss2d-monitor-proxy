import logging
from queue import Queue


class IQueue:
    def __init__(self) -> None:
        self.queue = Queue()
    
    async def put(self, msg: str):
        logging.info("Putting message: IT SHOULD NOT BE PRINTED :X")
        pass
    
    async def get(self) -> str:
        pass