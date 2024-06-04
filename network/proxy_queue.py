from queue import Queue


class IQueue:
    def __init__(self) -> None:
        self.queue = Queue()
    
    def put(self, msg: str) -> None:
        pass
    
    def get(self) -> str:
        pass