from typing import Union
from pydantic import BaseModel, Field

from src.controller.context_model.delayed_queue_context import DelayedQueueContext
from src.controller.context_model.queue_context_interface import IQueueContext
from src.controller.context_model.rmq_info_context import RMQInfoContext
from src.controller.context_model.simple_queue_context import SimpleQueueContext
from src.controller.context_model.stream_context_interface import IStreamContext
from src.controller.context_model.udp_info_context import UDPInfoContext
from src.controller.context_model.ws_info_context import WebSocketInfoContext
from src.network.communication import ComType
from src.network.delayed_queue_batch import DelayedQueueBatch
from src.network.proxy import Proxy
from src.network.proxy_queue import IQueue, QueueType
from src.network.receiver import IReceiver
from src.network.receiver_rabbitmq import ReceiverRabbitMQ
from src.network.receiver_udp import ReceiverUDP
from src.network.receiver_web_socket import ReceiverWebSocket
from src.network.sender import ISender
from src.network.sender_rabbitmq import SenderRabbitMQ
from src.network.sender_udp import SenderUDP
from src.network.sender_web_socket import SenderWebSocket
from src.network.simple_queue_batch import SimpleQueueBatch

STREAM_CONTEXTS = Union[RMQInfoContext, UDPInfoContext, WebSocketInfoContext]
QUEUE_CONTEXTS = Union[DelayedQueueContext, SimpleQueueContext]

class ProxyInfoContext(BaseModel):
    input: STREAM_CONTEXTS = Field(..., description="The input stream context.", discriminator='type') # TODO Example
    output: list[STREAM_CONTEXTS] = Field(..., description="The output stream context.", discriminator='type') # TODO Example
    queue: QUEUE_CONTEXTS = Field(..., description="The queue context.") # TODO Example
    
    @staticmethod
    def convert_to_context(proxy: Proxy = None, proxies: list[Proxy] = None) -> Union['ProxyInfoContext', list['ProxyInfoContext']]:
        if proxy is None and proxies is None:
            raise ValueError("Either proxy or proxies must be provided.")
        # if proxy is not None and proxies is not None:
            raise ValueError("Only one of proxy and proxies must be provided.")
        if proxy is not None:
            proxies = [proxy]
        
        infos = []
        for proxy in proxies:
            input = ProxyInfoContext.convert_input_stream_to_context(proxy.receiver)
            queue = ProxyInfoContext.convert_queue_to_context(proxy.queue)
            output = ProxyInfoContext.convert_output_stream_to_context(proxy.senders)
            info = ProxyInfoContext(
                input=input,
                output=output,
                queue=queue
            )
            infos.append(info)
        
        return infos if len(infos) > 1 else infos[0] if len(infos) == 1 else []
        
    @staticmethod
    def convert_input_stream_to_context(stream: IReceiver) -> IStreamContext:
        if stream is None:
            return None
        
        info: IStreamContext = None
        if stream.get_type() == ComType.RMQ:
            info = RMQInfoContext(type='RMQ', queue=stream.queue_name)
        elif stream.get_type() == ComType.UDP:
            info = UDPInfoContext(type='UDP', host=stream.address[0], port=stream.address[1])
        elif stream.get_type() == ComType.WS:
            info = WebSocketInfoContext(type='WS', host=stream.address[0], port=stream.address[1], file_stream=stream.file_stream)
        return info
    
    @staticmethod
    def convert_output_stream_to_context(streams: list[ISender]) -> list[IStreamContext]:
        if streams is None:
            return None
        
        infos: list[IStreamContext] = []
        for stream in streams:
            info: IStreamContext = None
            if stream.get_type() == ComType.RMQ:
                info = RMQInfoContext(type='RMQ', queue=stream.queue_name)
            elif stream.get_type() == ComType.UDP:
                info = UDPInfoContext(type='UDP', host=stream.address[0], port=stream.address[1])
            elif stream.get_type() == ComType.WS:
                info = WebSocketInfoContext(type='WS', host=stream.address[0], port=stream.address[1])
            infos.append(info)
        return infos
    
    @staticmethod
    def convert_queue_to_context(queue: IQueue) -> IQueueContext:
        if queue is None:
            return None
        
        info: IQueueContext = None
        if queue.get_type() == QueueType.DELAYED:
            info = DelayedQueueContext(type='DELAYED' ,delay=queue.buffer_size)
        elif queue.get_type() == QueueType.SIMPLE:
            info = SimpleQueueContext(type='SIMPLE')
        return info

    @staticmethod
    def convert_inverse(proxy_info: list['ProxyInfoContext']) -> list[Proxy]:
        proxies: Proxy = []
        for info in proxy_info:
            try:
                info = ProxyInfoContext.model_validate(info.model_dump())
            except Exception as e:
                return None
            
            receiver: IReceiver = None
            if info.input.type == 'UDP':
                receiver = ReceiverUDP((info.input.host, info.input.port))
            elif info.input.type == 'RMQ':
                receiver = ReceiverRabbitMQ(info.input.queue)
            elif info.input.type == 'WS':
                receiver = ReceiverWebSocket((info.input.host, info.input.port), info.input.file_stream)
            else:
                raise ValueError(f"Unknown stream type: {info.input.type}")
            
            senders: ISender = []
            for sender_info in info.output:
                if sender_info.type == 'UDP':
                    sender = SenderUDP((sender_info.host, sender_info.port))
                elif sender_info.type == 'RMQ':
                    sender = SenderRabbitMQ(sender_info.queue)
                elif sender_info.type == 'WS':
                    sender = SenderWebSocket((sender_info.host, sender_info.port))
                else:
                    raise ValueError(f"Unknown stream type: {sender_info.type}")
                senders.append(sender)

            queue: IQueue = None
            if info.queue.type == "SIMPLE":
                queue = SimpleQueueBatch(len(senders))
            elif info.queue.type == "DELAYED":
                queue = DelayedQueueBatch(len(senders), info.queue.delay)
            else:
                raise ValueError(f"Unknown queue type: {info.queue.type}")
            
            proxy = Proxy(receiver, senders, queue)
            proxies.append(proxy)
        return proxies