from fastapi import FastAPI
from typing import List, Optional

from core.tracker_service import (
    add_question,
    get_today_tasks,
    mark_done,
    get_consistency,
    get_missed_days,
    get_weak_questions,
    get_daily_activity,
    get_pattern_stats
)

app = FastAPI(title="DSA Tracker API")


# ------------------ BASIC ROUTE (OPTIONAL) ------------------

@app.get("/")
def root():
    return {"message": "DSA Tracker API is running"}


# ------------------ CORE ROUTES ------------------

@app.post("/add-question")
def add(
    q_no: str,
    difficulty: str,
    patterns: Optional[List[str]] = None
):
    """
    Add a new question with difficulty and optional DSA patterns
    """
    return {"message": add_question(q_no, difficulty, patterns)}


@app.get("/today")
def today():
    """
    Get today's pending tasks
    """
    return {"tasks": get_today_tasks()}


@app.post("/done")
def done(q_no: str):
    """
    Mark a question as done for today
    """
    return {"message": mark_done(q_no)}


# ------------------ REPORTS ------------------

@app.get("/consistency")
def consistency():
    """
    Get consistency score and streaks
    """
    return get_consistency()


@app.get("/missed")
def missed():
    """
    Get missed days per question
    """
    return get_missed_days()


@app.get("/weak")
def weak():
    """
    Get weak questions (missed >= 2)
    """
    return get_weak_questions()


@app.get("/daily-activity")
def daily_activity():
    """
    Get daily solve counts (for trends)
    """
    return get_daily_activity()


@app.get("/patterns")
def patterns():
    """
    Get weak pattern statistics
    """
    return get_pattern_stats()
