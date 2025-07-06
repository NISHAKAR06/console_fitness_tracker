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
        date = input("Date (YYYY-MM-DD) [today]: ") or datetime.today().strftime("%Y-%m-%d")
        wtype = input("Workout Type: ")
        duration = float(input("Duration (minutes): "))
        self.db.execute(
            "INSERT INTO workouts (user_id, date, type, duration) VALUES (?, ?, ?, ?)",
            (self.user.id, date, wtype, duration)
        )
        print("Workout logged!")

    def log_meal(self):
        date = input("Date (YYYY-MM-DD) [today]: ") or datetime.today().strftime("%Y-%m-%d")
        food = input("Food: ")
        calories = float(input("Calories: "))
        self.db.execute(
            "INSERT INTO meals (user_id, date, food, calories) VALUES (?, ?, ?, ?)",
            (self.user.id, date, food, calories)
        )
        print("Meal logged!")

    def view_workouts(self):
        rows = self.db.execute(
            "SELECT date, type, duration FROM workouts WHERE user_id=? ORDER BY date",
            (self.user.id,), fetch=True
        )
        print("\n--- Workout History ---")
        for r in rows:
            print(f"{r[0]}: {r[1]} for {r[2]} min")

    def view_meals(self):
        rows = self.db.execute(
            "SELECT date, food, calories FROM meals WHERE user_id=? ORDER BY date",
            (self.user.id,), fetch=True
        )
        print("\n--- Meal History ---")
        for r in rows:
            print(f"{r[0]}: {r[1]} ({r[2]} cal)")

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
