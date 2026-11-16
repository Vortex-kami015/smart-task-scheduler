from datetime import datetime, timedelta
from .priority_queue import PriorityQueue
from .priority import calculate_score


def _place(cursor, duration, day_start, day_end):
    """Return the earliest valid start time for a task of `duration` hours."""
    if cursor.hour < day_start:
        cursor = cursor.replace(hour=day_start, minute=0, second=0, microsecond=0)
    day_end_dt = cursor.replace(hour=day_end, minute=0, second=0, microsecond=0)
    fits_in_a_day = duration <= (day_end - day_start)
    if fits_in_a_day and cursor + timedelta(hours=duration) > day_end_dt:
        cursor = (cursor + timedelta(days=1)).replace(
            hour=day_start, minute=0, second=0, microsecond=0)
    return cursor


def generate_schedule(tasks, start=None, day_start=9, day_end=17):
    start = start or datetime.now()

    # 1. keep only pending tasks, build the heap
    pq = PriorityQueue(now=start)
    for t in tasks:
        if t.status == "pending":
            pq.add_task(t)

    # 2. repeatedly extract the highest-priority task
    schedule, cursor = [], start
    while not pq.is_empty():
        task = pq.pop_task()
        slot_start = _place(cursor, task.duration, day_start, day_end)
        slot_end = slot_start + timedelta(hours=task.duration)
        schedule.append({
            "task": task,
            "score": calculate_score(task, start),
            "start": slot_start,
            "end": slot_end,
            "misses_deadline": slot_end > task.deadline,
        })
        cursor = slot_end
    return schedule