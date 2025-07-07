from fitness_manager import FitnessManager

def main_menu():
    print("""
====== Fitness & Diet Tracker ======
1. Log Workout
2. Log Meal
3. View Workouts
4. View Meals
5. Show Summary
6. Update User
7. Delete User
8. Switch User
9. Exit
!-----------------------------------!
""")

def user_menu():
    print("""
====== User Management ======
1. Create New User
2. Select Existing User
-----------------------------
""")

def main():
    app = FitnessManager()
    while True:
        if not app.user:
            user_menu()
            choice = input("Enter choice: ")
            if choice == '1':
                app.create_user()
            elif choice == '2':
                users = app.get_all_users()
                if not users:
                    print("⚠ No users found. Please create a user.")
                else:
                    for u in users:
                        print(f"{u[0]}. {u[1]} (Age: {u[2]}, Weight: {u[3]})")
                    uid = input("Enter user ID to select: ")
                    app.set_user(int(uid))
            else:
                print("Invalid choice.")
        else:
            print(f"\nLogged in as: {app.user.name}")
            main_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                app.log_workout()
            elif choice == '2':
                app.log_meal()
            elif choice == '3':
                app.view_workouts()
            elif choice == '4':
                app.view_meals()
            elif choice == '5':
                app.summary()
            elif choice == '6':
                app.update_user()
            elif choice == '7':
                app.delete_user()
                app.user = None
            elif choice == '8':
                app.user = None
            elif choice == '9':
                print("👋 Goodbye!")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()
