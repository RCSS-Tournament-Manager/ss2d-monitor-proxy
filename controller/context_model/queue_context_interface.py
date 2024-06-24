from enum import Enum
from pydantic import BaseModel, Field


class IQueueContext(BaseModel):
    type: str