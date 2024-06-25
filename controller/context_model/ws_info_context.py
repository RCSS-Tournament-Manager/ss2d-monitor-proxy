from typing import Literal

from pydantic import Field
from controller.context_model.stream_context_interface import IStreamContext


class WebSocketInfoContext(IStreamContext):
    type: Literal['WS']
    host: str = Field(..., description="The host of the UDP stream.", example="localhost")
    port: int = Field(..., description="The port of the UDP stream.", example=1234)
    file_stream: str = Field(None, description="The file stream.", example="file.rcg")