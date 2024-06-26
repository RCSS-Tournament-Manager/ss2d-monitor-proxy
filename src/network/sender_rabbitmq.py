import logging

import aio_pika as pika
from src.network.communication import ComType
from src.network.proxy_queue import IQueue
from src.network.sender import ISender


class SenderRabbitMQ(ISender):
    def __init__(self, queue_name="test2") -> None:
        super().__init__()
        self.queue_name = queue_name
        self.logging = logging.getLogger(f"Sender-{self.get_name()}")
    
    async def send(self):
        msg = await self.queue.get()
        await self.channel.default_exchange.publish(
            pika.Message(body=msg.encode()),
            routing_key=self.queue_name
        )
    
    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        self.connection = await pika.connect_robust('amqp://guest:guest@localhost')
        self.channel = await self.connection.channel()
        
    def get_name(self) -> str:
        return f"RMQ-{self.queue_name}"        
    
    def get_type(self) -> ComType:
        return ComType.RMQ