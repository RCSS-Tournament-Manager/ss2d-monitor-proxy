import logging
from network.communication import ComType
from network.proxy_queue import IQueue
from network.receiver import IReceiver
import aio_pika as pika


class ReceiverRabbitMQ(IReceiver):
    def __init__(self, queue_name="test2") -> None:
        super().__init__()
        self.queue_name = queue_name
        self.logging = logging.getLogger(f"Receiver-{self.get_name()}")

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
        await self.channel.set_qos(prefetch_count=100)
        self.mq_queue = await self.channel.declare_queue(self.queue_name)
        await self.mq_queue.consume(self.receive_callback)
        
    def get_name(self) -> str:
        return f'RMQ-{self.queue_name}'
    
    def get_type(self) -> ComType:
        return ComType.RMQ
        