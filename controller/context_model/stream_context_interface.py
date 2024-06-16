from enum import Enum
from pydantic import BaseModel, Field

class StreamType(Enum):
    RMQ = "RMQ"
    UDP = "UDP"

class IStreamContext(BaseModel):
    type: StreamType = Field(None, description="The type of the stream.")