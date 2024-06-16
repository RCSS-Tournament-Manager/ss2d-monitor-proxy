from enum import Enum
from pydantic import BaseModel, Field

class QueueTypeContext(Enum):
    DELAYED = "DELAYED"
    SIMPLE = "SIMPLE"

class IQueueContext(BaseModel):
    type: QueueTypeContext = Field(None, description="The type of the queue.")