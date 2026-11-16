from datetime import datetime


class Task:
    def __init__(self, id, name, priority, deadline, duration,
                 category, status="pending", created_at=None):
        self.id = id
        self.name = name
        self.priority = priority          # 1 (low) to 5 (high)
        self.deadline = deadline          # datetime
        self.duration = duration          # hours (float)
        self.category = category
        self.status = status              # pending / in_progress / done
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "priority": self.priority,
            "deadline": self.deadline.isoformat(), "duration": self.duration,
            "category": self.category, "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["id"], d["name"], d["priority"],
            datetime.fromisoformat(d["deadline"]), d["duration"],
            d["category"], d.get("status", "pending"),
            datetime.fromisoformat(d["created_at"]) if d.get("created_at") else None,
        )

    def __repr__(self):
        return f"Task({self.id}, {self.name!r}, p={self.priority})"