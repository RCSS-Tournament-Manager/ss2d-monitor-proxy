from typing import Literal
from pydantic import Field
from controller.context_model.stream_context_interface import IStreamContext


class RMQInfoContext(IStreamContext):
    type: Literal['RMQ'] = Field('RMQ', description="The type of the stream.", example="RMQ")
    queue: str = Field(None, description="The name of the queue.", example="queue_name")