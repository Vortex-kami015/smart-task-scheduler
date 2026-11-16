import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import json

from scheduler.task import Task
from scheduler.scheduler import generate_schedule
from scheduler.heap import MaxHeap

BASE_DIR = Path(__file__).resolve().parent

TASKS = [
    Task(1, "Submit Assignment", 5, __import__("datetime").datetime.now() + __import__("datetime").timedelta(hours=8), 2, "College"),
    Task(2, "Complete Project", 4, __import__("datetime").datetime.now() + __import__("datetime").timedelta(days=3), 4, "College"),
    Task(3, "Study DSA", 3, __import__("datetime").datetime.now() + __import__("datetime").timedelta(days=5), 1, "Study"),
    Task(4, "Watch Lecture", 2, __import__("datetime").datetime.now() + __import__("datetime").timedelta(days=10), 1, "Study"),
]


def build_dashboard_data():
    schedule = generate_schedule(TASKS)
    heap = MaxHeap()
    heap.push(75, 1, "Study DSA")
    heap.push(95, 2, "Submit Assignment")
    heap.push(40, 3, "Watch Lecture")

    ordered_heap = []
    while not heap.is_empty():
        ordered_heap.append(heap.pop())

    return {
        "tasks": [task.to_dict() for task in TASKS],
        "schedule": [
            {
                "task": item["task"].name,
                "priority": item["task"].priority,
                "category": item["task"].category,
                "score": item["score"],
                "start": item["start"].isoformat(),
                "end": item["end"].isoformat(),
                "misses_deadline": item["misses_deadline"],
            }
            for item in schedule
        ],
        "heap": ordered_heap,
        "top_heap_item": ordered_heap[0] if ordered_heap else None,
    }


class SchedulerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/tasks":
            self.send_json(build_dashboard_data())
            return

        if parsed.path in ("/", ""):
            target = BASE_DIR / "index.html"
        else:
            target = (BASE_DIR / parsed.path.lstrip("/")).resolve()
            if BASE_DIR not in target.parents and target != BASE_DIR:
                self.send_error(403)
                return

        if target.is_dir():
            target = target / "index.html"

        if target.exists() and target.is_file():
            self.send_file(target)
            return

        self.send_error(404)

    def send_json(self, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path):
        content = path.read_bytes()
        mime = "text/html; charset=utf-8"
        if path.suffix.lower() == ".css":
            mime = "text/css; charset=utf-8"
        elif path.suffix.lower() == ".js":
            mime = "application/javascript; charset=utf-8"

        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        return


def main():
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), SchedulerHandler)
    print(f"Smart Task Scheduler frontend running at http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
