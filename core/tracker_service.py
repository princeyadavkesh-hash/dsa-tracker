import json
from services.time_service import today_ist, today_str
from services.scheduler import generate_schedule
from services.consistency import update_consistency
from services.reports import update_missed_days
from models.question import Question

FILE = "storage/data.json"


# ------------------ DATA ------------------

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "questions": {},
            "consistency": {
                "total_days": 0,
                "active_days": 0,
                "current_streak": 0,
                "max_streak": 0,
                "last_updated": None,
                "daily_activity": {}
            }
        }


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ------------------ CORE ACTIONS ------------------

def add_question(q_no, difficulty, patterns=None):
    data = load_data()
    today = today_ist()

    if q_no in data["questions"]:
        return "⚠️ Question already exists"

    schedule = generate_schedule(today, difficulty)
    q = Question(q_no, difficulty, today, schedule, patterns)

    data["questions"][q_no] = q.to_dict()
    save_data(data)

    return f"✅ Added {q_no} ({difficulty.upper()})"


def get_today_tasks():
    data = load_data()
    update_missed_days(data["questions"])
    today = today_str()

    tasks = []
    for q_no, q in data["questions"].items():
        if today in q["schedule"] and today not in q["completed_dates"]:
            tasks.append((q_no, q["difficulty"], q["patterns"]))

    save_data(data)
    return tasks


def mark_done(q_no):
    data = load_data()
    today = today_str()

    if q_no not in data["questions"]:
        return "❌ Question not found"

    q = data["questions"][q_no]

    if today not in q["completed_dates"]:
        q["completed_dates"].append(today)
        q["total_solves"] += 1

        daily = data["consistency"].setdefault("daily_activity", {})
        daily[today] = daily.get(today, 0) + 1

    if data["consistency"]["last_updated"] != today:
        update_consistency(data["consistency"], solved_today=True)
        data["consistency"]["last_updated"] = today

    save_data(data)
    return f"✅ Done: {q_no}"


# ------------------ ANALYTICS ------------------

def get_consistency():
    c = load_data()["consistency"]
    score = 0 if c["total_days"] == 0 else (c["active_days"] / c["total_days"]) * 100
    return {
        "score": round(score, 2),
        "current_streak": c["current_streak"],
        "max_streak": c["max_streak"]
    }


def get_daily_activity():
    data = load_data()
    return data["consistency"].get("daily_activity", {})


def get_missed_days():
    data = load_data()
    update_missed_days(data["questions"])
    save_data(data)
    return {
        q_no: q["missed_dates"]
        for q_no, q in data["questions"].items()
        if q["missed_dates"]
    }


def get_weak_questions():
    data = load_data()
    return {
        q_no: len(q["missed_dates"])
        for q_no, q in data["questions"].items()
        if len(q["missed_dates"]) >= 2
    }


def get_pattern_stats():
    data = load_data()
    stats = {}

    for q in data["questions"].values():
        for p in q.get("patterns", []):
            stats[p] = stats.get(p, 0) + len(q["missed_dates"])

    return stats
