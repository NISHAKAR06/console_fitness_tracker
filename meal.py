class Meal:
    def __init__(self, date, food, calories, meal_id=None):
        self.id = meal_id
        self.date = date
        self.food = food
        self.calories = calories
