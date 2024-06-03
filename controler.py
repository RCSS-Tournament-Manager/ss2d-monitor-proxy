from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Manager import Manager

# Abstract class for the controllers
class Controller:
    def __init__(self, manager) -> None:
        self.manager: 'Manager' = manager
        
    def initialize(self):
        pass
    
    def run(self):
        pass
    
    def add_monitor(self):
        pass
    
    def remove_monitor(self):
        pass
    
    def shutdown(self):
        pass