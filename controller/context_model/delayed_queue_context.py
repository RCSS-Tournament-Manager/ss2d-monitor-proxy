from pydantic import Field
from controller.context_model.queue_context_interface import IQueueContext


class DelayedQueueContext(IQueueContext):
    delay: int = Field(None, description="The delay of the delayed queue.", example=1000)