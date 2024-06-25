import asyncio
import logging
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
import uvicorn
from starlette.status import HTTP_403_FORBIDDEN
from controller.context_model.proxy_info_context import ProxyInfoContext
from controller.controller_interface import IController
from manager.manager import Manager
from network.delayed_queue_batch import DelayedQueueBatch
from network.proxy import Proxy
from network.proxy_queue import IQueue
from network.receiver import IReceiver
from network.receiver_rabbitmq import ReceiverRabbitMQ
from network.receiver_udp import ReceiverUDP
from network.sender import ISender
from network.sender_rabbitmq import SenderRabbitMQ
from network.sender_udp import SenderUDP
from network.simple_queue_batch import SimpleQueueBatch


class FastAPIController(IController):
    def __init__(self, manager: Manager, api_key: str, api_key_value: str, port: int) -> None:
        super().__init__(manager)
        self.app = FastAPI()
        self.logging = logging.getLogger("FastAPIController")
        self.api_key = api_key
        self.api_key_value = api_key_value
        self.port = port
        self.serve_task = None
        self.setup_routes()
    
    def setup_routes(self):
        api_key_header = APIKeyHeader(name=self.api_key, auto_error=False)

        async def get_api_key(api_key: str = Security(api_key_header)):
            if api_key == self.api_key_value:
                return api_key
            else:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
                )
        
        @self.app.get("/proxies")
        async def api_get_proxies():
            proxies = self.manager.get_proxies()
            context = ProxyInfoContext.convert_to_context(proxies=proxies)
            return context
        
        @self.app.post("/porxy/add")
        async def api_add_proxy(proxy: list[ProxyInfoContext], api_key: str = Depends(get_api_key)):
            await self.add_proxy(ProxyInfoContext.convert_inverse(proxy))
            return {"message": "Proxy added"}
    
    async def run(self):
        config = uvicorn.Config(self.app, host="0.0.0.0", port=self.port)
        server = uvicorn.Server(config)
        self.serve_task = asyncio.create_task(server.serve())
        