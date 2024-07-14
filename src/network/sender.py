import logging
from src.network.communication import ICom
from src.network.proxy_queue import IQueue

PARAMETERS_INITIAL_MESSAGE = ['(server_param', '(player_param', '(player_type']

class ISender(ICom):
    def __init__(self) -> None:
        super().__init__()
        self.parameters_messages = ''
        self.logging = logging.getLogger(f"ISender")
    
    async def send(self, msg: str) -> None:
        pass
    
    def get_name():
        return "Sender"
    
    def check_parameters(self, msg: str) -> None:
        if msg.startswith('(player_param'):
            self.logging.info(f"Received server parameters message: RESETING")
            self.parameters_messages = ''
        if any(msg.startswith(param) for param in PARAMETERS_INITIAL_MESSAGE):
            self.logging.info(f"Received parameters message: {msg[:10]}")
            if self.parameters_messages != '':
                self.parameters_messages += '\n'
            self.parameters_messages += msg
            