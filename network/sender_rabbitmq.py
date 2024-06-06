import logging

import aio_pika as pika
from network.proxy_queue import IQueue
from network.sender import ISender


class SenderRabbitMQ(ISender):
    def __init__(self) -> None:
        super().__init__()
    
    async def send(self):
        msg = await self.queue.get()
        await self.channel.default_exchange.publish(
            pika.Message(body=msg.encode()),
            routing_key='test'
        )
    
    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        self.connection = await pika.connect_robust('amqp://guest:guest@localhost')
        self.channel = await self.connection.channel()