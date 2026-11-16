import unittest
from datetime import datetime, timedelta
from scheduler.heap import MaxHeap
from scheduler.task import Task
from scheduler.priority import calculate_score
from scheduler.priority_queue import PriorityQueue
from scheduler.scheduler import generate_schedule

NOW = datetime(2026, 10, 5, 9, 0)


def make(id, p, days, dur=1):
    return Task(id, f"T{id}", p, NOW + timedelta(days=days), dur, "x", created_at=NOW)


class TestHeap(unittest.TestCase):
    def test_pop_order(self):
        h = MaxHeap()
        for k in [5, 1, 9, 3, 7]:
            h.push(k, k, f"item{k}")
        self.assertEqual([h.pop() for _ in range(5)],
                         ["item9", "item7", "item5", "item3", "item1"])

    def test_remove_middle(self):
        h = MaxHeap()
        for k in [5, 1, 9, 3, 7]:
            h.push(k, k, k)
        h.remove(5)
        self.assertEqual([h.pop() for _ in range(4)], [9, 7, 3, 1])

    def test_empty_pop_raises(self):
        with self.assertRaises(IndexError):
            MaxHeap().pop()


class TestScore(unittest.TestCase):
    def test_urgent_beats_relaxed(self):
        a = make(1, 5, 0.01)
        b = make(2, 3, 5)
        self.assertGreater(calculate_score(a, NOW), calculate_score(b, NOW))


class TestScheduler(unittest.TestCase):
    def test_highest_score_first(self):
        pq = PriorityQueue(now=NOW)
        for t in [make(1, 2, 9), make(2, 5, 0.5), make(3, 3, 4)]:
            pq.add_task(t)
        self.assertEqual(pq.pop_task().id, 2)

    def test_done_tasks_skipped(self):
        t = make(1, 5, 1)
        t.status = "done"
        self.assertEqual(generate_schedule([t], start=NOW), [])

    def test_tasks_do_not_overlap(self):
        s = generate_schedule([make(i, 3, 5, 3) for i in range(1, 5)], start=NOW)
        for a, b in zip(s, s[1:]):
            self.assertLessEqual(a["end"], b["start"])


if __name__ == "__main__":
    unittest.main()