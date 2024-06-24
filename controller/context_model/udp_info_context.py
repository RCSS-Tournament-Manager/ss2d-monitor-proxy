from typing import Literal
from pydantic import Field
from controller.context_model.stream_context_interface import IStreamContext


class UDPInfoContext(IStreamContext):
    type: Literal['UDP'] = Field('RMQ', description="The type of the stream.", example="RMQ")
    host: str = Field(None, description="The host of the UDP stream.", example="localhost")
    port: int = Field(None, description="The port of the UDP stream.", example=1234)