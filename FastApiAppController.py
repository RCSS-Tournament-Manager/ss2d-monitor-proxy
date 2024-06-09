from controler import Controller
from fastapi import FastAPI
import uvicorn

# list of api routes
# /api/addFakeMonitor
# /api/removeFakeMonitor
# /api/startFakeMonitor
# /api/stopFakeMonitor
# /api/addListenerToMonitor
class FastApiApp(Controller):
    def __init__(self):
        self.app = FastAPI()

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
        
    def add_monitor(self):
        return super().add_monitor()