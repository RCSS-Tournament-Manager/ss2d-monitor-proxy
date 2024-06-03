from controler import Controller


class ControllerManager:
    def __init__(self):
        self.controllers: list[Controller] = []

    def add_controller(self, controller: Controller):
        self.controllers.append(controller)
