from datetime import datetime, timedelta
from scheduler.task import Task
from scheduler.scheduler import generate_schedule
from scheduler.heap import MaxHeap

now = datetime.now()
tasks = [
    Task(1, "Submit Assignment", 5, now + timedelta(hours=8),  2, "College"),
    Task(2, "Complete Project",  4, now + timedelta(days=3),   4, "College"),
    Task(3, "Study DSA",         3, now + timedelta(days=5),   1, "Study"),
    Task(4, "Watch Lecture",     2, now + timedelta(days=10),  1, "Study"),
]

for item in generate_schedule(tasks):
    t = item["task"]
    flag = "  LATE!" if item["misses_deadline"] else ""
    print(f'{item["score"]:6.2f}  {t.name:<20} '
          f'{item["start"]:%a %H:%M} -> {item["end"]:%H:%M}{flag}')

h = MaxHeap()
h.push(75, 1, "Study DSA")
h.push(95, 2, "Submit Assignment")
h.push(40, 3, "Watch Lecture")

print(h.pop())