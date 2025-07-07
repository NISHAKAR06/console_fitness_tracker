from db_manager import DBManager
from user import User
from datetime import datetime

class FitnessManager:
    def __init__(self):
        self.db = DBManager()
        self.user = None

    def create_user(self):
        name = input("Name: ")
        age = int(input("Age: "))
        weight = float(input("Weight (kg): "))
        self.db.execute(
            "INSERT INTO users (name, age, weight) VALUES (?, ?, ?)",
            (name, age, weight)
        )
        self.user = self.get_last_user()
        print(f"User {self.user.name} created!")

    def get_last_user(self):
        user = self.db.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1", fetchone=True)
        if user:
            return User(user[1], user[2], user[3], user[0])
        return None

    def get_all_users(self):
        return self.db.execute("SELECT * FROM users", fetch=True)

    def set_user(self, user_id):
        user = self.db.execute("SELECT * FROM users WHERE id=?", (user_id,), fetchone=True)
        if user:
            self.user = User(user[1], user[2], user[3], user[0])
            print(f"User switched to {self.user.name}")
        else:
            print("⚠ User not found.")

    def update_user(self):
        if not self.user:
            print("⚠ No user to update.")
            return
        print(f"Current name: {self.user.name}, age: {self.user.age}, weight: {self.user.weight}")
        name = input("New name (press Enter to keep current): ") or self.user.name
        age_input = input("New age (press Enter to keep current): ")
        weight_input = input("New weight (press Enter to keep current): ")

        age = int(age_input) if age_input else self.user.age
        weight = float(weight_input) if weight_input else self.user.weight

        self.db.execute(
            "UPDATE users SET name=?, age=?, weight=? WHERE id=?",
            (name, age, weight, self.user.id)
        )
        self.set_user(self.user.id)
        print("User updated!")

    def delete_user(self):
        confirm = input(f"⚠ Are you sure you want to delete user '{self.user.name}' and all their data? (yes/no): ")
        if confirm.lower() == 'yes':
            self.db.execute("DELETE FROM workouts WHERE user_id=?", (self.user.id,))
            self.db.execute("DELETE FROM meals WHERE user_id=?", (self.user.id,))
            self.db.execute("DELETE FROM users WHERE id=?", (self.user.id,))
            self.user = None
            print("User and all associated data deleted.")
        else:
            print("Delete cancelled.")

    def log_workout(self):
        now = datetime.now()
        date = input("Date (YYYY-MM-DD) [today]: ") or now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")  # Automatically get current time
        wtype = input("Workout Type: ")
        duration = float(input("Duration (minutes): "))
        self.db.execute(
            "INSERT INTO workouts (user_id, date, time, type, duration) VALUES (?, ?, ?, ?, ?)",
            (self.user.id, date, time_str, wtype, duration)
        )
        print("Workout logged!")

    def log_meal(self):
        food_calories = {
            "apple": 95,
            "banana": 105,
            "rice": 206,
            "chicken breast": 165,
            "egg": 78,
            "bread": 80,
            "milk": 122,
            "orange": 62,
            "potato": 163,
            "salad": 33,
            "cheese": 113,
            "beef steak": 271,
            "pasta": 221,
            "pizza": 285,
            "burger": 354,
            "fish": 206,
            "yogurt": 59,
            "oatmeal": 158,
            "peanut butter": 188,
            "almonds": 164,
            "carrot": 25,
            "broccoli": 55,
            "cucumber": 16,
            "grapes": 62,
            "mango": 99,
            "pineapple": 82,
            "watermelon": 85,
            "chocolate": 208,
            "ice cream": 137,
            "fries": 312,
            "soda": 150,
            "coffee": 2,
            "tea": 2,
            "butter": 102,
            "honey": 64,
            "lentils": 230,
            "beans": 127,
            "corn": 96,
            "spinach": 23,
            "tofu": 76,
            "chicken curry": 293,
            "dal": 198,
            "roti": 85,
            "paratha": 210,
            "idli": 39,
            "dosa": 133,
            "sambar": 130,
            "upma": 192,
            "poha": 206,
            "biryani": 290,
            "paneer": 265
        }
        print("Available foods in store:")
        for food in food_calories:
            print(f"- {food.title()} ")    #({food_calories[food]} cal)
        now = datetime.now()
        date = input("Date (YYYY-MM-DD) [today]: ") or now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S") 
        food = input("Food: ").strip().lower()
        calories = food_calories.get(food)
        if calories is None:
            calories = float(input("Calories not found. Please enter calories: "))
        print(f"Calories for {food}: {calories}")
        self.db.execute(
            "INSERT INTO meals (user_id, date, time, food, calories) VALUES (?, ?, ?, ?, ?)",
            (self.user.id, date, time_str, food, calories)
        )
        print("Meal logged!")

    def view_workouts(self):
        rows = self.db.execute(
            "SELECT date, time, type, duration FROM workouts WHERE user_id=? ORDER BY date, time",
            (self.user.id,), fetch=True
        )
        print("\n--- Workout History ---")
        for r in rows:
            print(f"{r[0]} {r[1]}: {r[2].title()} for {r[3]} min")

    def view_meals(self):
        rows = self.db.execute(
            "SELECT date, time, food, calories FROM meals WHERE user_id=? ORDER BY date, time",
            (self.user.id,), fetch=True
        )
        print("\n--- Meal History ---")
        for r in rows:
            print(f"{r[0]} {r[1]}: {r[2].title()} ({r[3]} cal)")

    def summary(self):
        rows = self.db.execute(
            "SELECT SUM(duration) FROM workouts WHERE user_id=?",
            (self.user.id,), fetchone=True
        )
        total_workout = rows[0] if rows[0] else 0

        rows = self.db.execute(
            "SELECT SUM(calories) FROM meals WHERE user_id=?",
            (self.user.id,), fetchone=True
        )
        total_calories = rows[0] if rows[0] else 0

        print("\n--- Summary ---")
        print(f"Total workout time: {total_workout} min")
        print(f"Total calories consumed: {total_calories} cal")

    # Run this once to add the time column if not present
    def add_time_column(self):
        try:
            self.db.execute("ALTER TABLE meals ADD COLUMN time TEXT")
            print("Time column added to meals table.")
        except Exception as e:
            print(f"Error adding time column: {e}")
