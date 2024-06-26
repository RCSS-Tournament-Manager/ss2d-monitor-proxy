from typing import Literal
from pydantic import Field
from src.controller.context_model.stream_context_interface import IStreamContext


class RMQInfoContext(IStreamContext):
    type: Literal['RMQ']
    queue: str = Field(..., description="The name of the queue.", example="queue_name")