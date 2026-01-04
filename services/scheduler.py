from datetime import timedelta

def generate_schedule(start_date, difficulty):
    if difficulty in ["easy", "medium"]:
        offsets = [0, 1, 3, 5]      # Day 1,2,4,6
    else:
        offsets = list(range(7))   # Hard → Day 1 to 7

    return [str(start_date + timedelta(days=o)) for o in offsets]
