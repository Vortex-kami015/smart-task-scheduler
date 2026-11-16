from datetime import datetime
from .heap import MaxHeap
from .priority import calculate_score


class PriorityQueue:
    def __init__(self, now=None):
        self._heap = MaxHeap()
        self._now = now                   # lets tests fix the "current time"

    def _key(self, task):
        now = self._now or datetime.now()
        # tuple compare: higher score first, then earlier deadline, then lower id
        return (calculate_score(task, now), -task.deadline.timestamp(), -task.id)

    def add_task(self, task):             # O(log n)
        self._heap.push(self._key(task), task.id, task)

    def pop_task(self):                   # O(log n)
        return self._heap.pop()

    def peek(self):                       # O(1)
        return self._heap.peek()

    def remove_task(self, task_id):       # O(log n)
        return self._heap.remove(task_id)

    def update_task(self, task):          # remove + re-insert
        self._heap.remove(task.id)
        self.add_task(task)

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        return self._heap.is_empty()