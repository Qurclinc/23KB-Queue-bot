from typing import List
from core.models import Queue

class QueueManager:
    def __init__(self, queue: List[Queue]):
        self.queue = queue
        
    def get_