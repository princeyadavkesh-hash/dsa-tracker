from services.time_service import today_str

def update_missed_days(questions):
    today = today_str()

    for q in questions.values():
        for d in q["schedule"]:
            if d < today and d not in q["completed_dates"]:
                if d not in q["missed_dates"]:
                    q["missed_dates"].append(d)

def weak_questions(questions):
    return {
        q_no: q for q_no, q in questions.items()
        if len(q["missed_dates"]) >= 2
    }
