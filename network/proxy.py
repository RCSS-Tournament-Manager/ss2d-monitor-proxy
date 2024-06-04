from network.receiver import IReceiver
from network.sender import ISender


class Proxy:
    def __init__(self, receiver: IReceiver, sender: ISender) -> None:
        self.receiver = receiver
        self.sender = sender
    
    def run(self) -> None:
        # TODO INITIALIZE HERE?
        self.sender.initialize()
        self.receiver.initialize()
        
        while True:
            msg = self.receiver.receive()
            self.sender.send(msg)