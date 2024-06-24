from typing import Literal
from pydantic import Field
from controller.context_model.queue_context_interface import IQueueContext


class DelayedQueueContext(IQueueContext):
    type: Literal["DELAYED"]
    delay: int = Field(..., description="The delay of the delayed queue.", example=1000)