import logging
from manager.manager import Manager


class IController:
    def __init__(self, manager: Manager) -> None:
        self.manager: Manager = manager
        self.logging = logging.getLogger("IController")
        
    async def add_proxy(self):
        self.logging.info("add_proxy")
        
    async def remove_proxy(self):
        self.logging.info("remove_proxy")
        
    async def restart_proxy(self):
        self.logging.info("restart_proxy")
    
    async def run(self):
        pass