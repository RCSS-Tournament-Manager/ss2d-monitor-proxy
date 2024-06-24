from typing import Literal
from controller.context_model.queue_context_interface import IQueueContext


class SimpleQueueContext(IQueueContext):
    type: Literal["SIMPLE"]