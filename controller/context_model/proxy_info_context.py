from typing import Union
from pydantic import BaseModel, Field

from controller.context_model.delayed_queue_context import DelayedQueueContext
from controller.context_model.queue_context_interface import IQueueContext
from controller.context_model.rmq_info_context import RMQInfoContext
from controller.context_model.simple_queue_context import SimpleQueueContext
from controller.context_model.stream_context_interface import IStreamContext
from controller.context_model.udp_info_context import UDPInfoContext
from network.communication import ComType
from network.proxy import Proxy
from network.proxy_queue import IQueue, QueueType
from network.receiver import IReceiver
from network.sender import ISender

STREAM_CONTEXTS = Union[RMQInfoContext, UDPInfoContext]
QUEUE_CONTEXTS = Union[DelayedQueueContext, SimpleQueueContext]

class ProxyInfoContext(BaseModel):
    input: STREAM_CONTEXTS = Field(..., description="The input stream context.", discriminator='type') # TODO Example
    output: list[STREAM_CONTEXTS] = Field(..., description="The output stream context.", discriminator='type') # TODO Example
    queue: QUEUE_CONTEXTS = Field(..., description="The queue context.") # TODO Example
    
    @staticmethod
    def convert_to_context(proxy: Proxy = None, proxies: list[Proxy] = None) -> Union['ProxyInfoContext', list['ProxyInfoContext']]:
        if proxy is None and proxies is None:
            raise ValueError("Either proxy or proxies must be provided.")
        if proxy is not None and proxies is not None:
            raise ValueError("Only one of proxy and proxies must be provided.")
        if proxy is not None:
            proxies = [proxy]
        
        infos = []
        for proxy in proxies:
            info = ProxyInfoContext()
            info.input = ProxyInfoContext.convert_input_stream_to_context(proxy.receiver)
            info.queue = ProxyInfoContext.convert_queue_to_context(proxy.queue)
            info.output = ProxyInfoContext.convert_output_stream_to_context(proxy.senders)
            infos.append(info)
        
        return infos if len(infos) > 1 else infos[0]
        
    @staticmethod
    def convert_input_stream_to_context(stream: IReceiver) -> IStreamContext:
        if stream is None:
            return None
        
        info: IStreamContext = None
        if stream.get_type() == ComType.RMQ:
            info = RMQInfoContext()
            info.type = 'RMQ'
            info.queue = stream.queue_name
        elif stream.get_type() == ComType.UDP:
            info = UDPInfoContext()
            info.type = 'UDP'
            info.host = stream.address[0]
            info.port = stream.address[1]
        return info
    
    @staticmethod
    def convert_output_stream_to_context(streams: list[ISender]) -> list[IStreamContext]:
        if streams is None:
            return None
        
        infos: list[IStreamContext] = []
        for stream in streams:
            info: IStreamContext = None
            if stream.get_type() == ComType.RMQ:
                info = RMQInfoContext()
                info.type = 'RMQ'
                info.queue = stream.queue_name
            elif stream.get_type() == ComType.UDP:
                info = UDPInfoContext()
                info.type = 'UDP'
                info.host = stream.address[0]
                info.port = stream.address[1]
            infos.append(info)
        return infos
    
    @staticmethod
    def convert_queue_to_context(queue: IQueue) -> IQueueContext:
        if queue is None:
            return None
        
        info: IQueueContext = None
        if queue.get_type() == QueueType.DELAYED:
            info = DelayedQueueContext()
            info.type = QueueType.DELAYED
            info.delay = queue.buffer_size
        elif queue.get_type() == QueueType.SIMPLE:
            info = SimpleQueueContext()
            info.type = QueueType.SIMPLE
        return info
