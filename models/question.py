class Question:
    def __init__(self, q_no, difficulty, start_date, schedule, patterns=None):
        self.q_no = q_no
        self.difficulty = difficulty
        self.start_date = start_date
        self.schedule = schedule

        self.completed_dates = []
        self.missed_dates = []
        self.total_solves = 0

        # NEW: DSA pattern tags
        self.patterns = patterns or []

    def to_dict(self):
        return {
            "difficulty": self.difficulty,
            "start_date": str(self.start_date),
            "schedule": self.schedule,
            "completed_dates": self.completed_dates,
            "missed_dates": self.missed_dates,
            "total_solves": self.total_solves,
            "patterns": self.patterns
        }
