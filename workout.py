class Workout:
    def __init__(self, date, wtype, duration, workout_id=None):
        self.id = workout_id
        self.date = date
        self.type = wtype
        self.duration = duration
