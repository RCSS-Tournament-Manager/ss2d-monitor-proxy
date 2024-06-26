from typing import Literal
from pydantic import Field
from src.controller.context_model.stream_context_interface import IStreamContext


class UDPInfoContext(IStreamContext):
    type: Literal['UDP']
    host: str = Field(..., description="The host of the UDP stream.", example="localhost")
    port: int = Field(..., description="The port of the UDP stream.", example=1234)