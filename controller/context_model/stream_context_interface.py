from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field

class IStreamContext(BaseModel):
    type: str