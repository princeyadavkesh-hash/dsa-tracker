def update_consistency(consistency, solved_today):
    consistency["total_days"] += 1

    if solved_today:
        consistency["active_days"] += 1
        consistency["current_streak"] += 1
        consistency["max_streak"] = max(
            consistency["max_streak"],
            consistency["current_streak"]
        )
    else:
        consistency["current_streak"] = 0
