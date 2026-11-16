from datetime import datetime

PRIORITY_WEIGHT = 10      # priority 1-5  -> 10-50
MAX_URGENCY = 40
WAIT_PER_DAY = 2
MAX_WAIT = 10


def calculate_score(task, now=None):
    now = now or datetime.now()

    priority_score = task.priority * PRIORITY_WEIGHT

    days_left = (task.deadline - now).total_seconds() / 86400
    urgency = MAX_URGENCY if days_left <= 0 else MAX_URGENCY / (1 + days_left)

    waited_days = max((now - task.created_at).total_seconds() / 86400, 0)
    waiting = min(waited_days * WAIT_PER_DAY, MAX_WAIT)

    return round(priority_score + urgency + waiting, 2)