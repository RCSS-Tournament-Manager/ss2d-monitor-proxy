from pydantic import Field
from controller.context_model.stream_context_interface import IStreamContext


class RMQInfoContext(IStreamContext):
    queue: str = Field(None, description="The name of the queue.", example="queue_name")