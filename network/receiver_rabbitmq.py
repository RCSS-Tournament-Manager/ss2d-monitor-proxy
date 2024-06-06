import logging
from network.proxy_queue import IQueue
from network.receiver import IReceiver
import aio_pika as pika


class ReceiverRabbitMQ(IReceiver):
    def __init__(self) -> None:
        super().__init__()

    async def receive(self) -> str:
        pass
    
    async def receive_callback(self, message: pika.abc.AbstractIncomingMessage) -> None:
        async with message.process():
            body = message.body.decode()
            await self.queue.put(body)
    
    async def initialize(self, queue: IQueue) -> None:
        await super().initialize(queue)
        self.connection = await pika.connect_robust('amqp://guest:guest@localhost')
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        self.mq_queue = await self.channel.declare_queue('test')
        await self.mq_queue.consume(self.receive_callback)
        