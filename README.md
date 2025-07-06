# console_fitness_tracker

A simple console-based fitness and diet tracker written in Python. This application allows users to manage their fitness activities and dietary habits efficiently from the command line.

## Features

- **User Management**: Create, select, update, and delete users.
- **Workout Logging**: Record workouts with date, type, and duration.
- **Meal Logging**: Log meals with date, food name, and calories.
- **History Views**: View workout and meal histories.
- **Summary**: Display total workout time and calories consumed for a user.
- **Multiple Users**: Easily switch between different users.

## Getting Started

### Prerequisites

- Python 3.x

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/NISHAKAR06/console_fitness_tracker.git
   cd console_fitness_tracker
   ```

2. **Run the application**

   ```bash
   python main.py
   ```

   The application will automatically create a local SQLite database file (`fitness.db`) in the project directory.

## Usage

When you start the application, you are presented with a user menu:

```
====== User Management ======
1. Create New User
2. Select Existing User
-------------------------------------
```

After creating or selecting a user, you access the main menu:

```
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
```

### Typical Workflow

1. **Create a new user** or select an existing one.
2. **Log workouts** as you exercise.
3. **Log meals** as you eat.
4. **View workout and meal histories**.
5. **Review your summary** to track progress.
6. **Update or delete your user profile** as needed.
7. **Switch users** if multiple people use the tracker.

## Project Structure

- `main.py` - Entry point of the application.
- `fitness_manager.py` - Core logic for managing users, workouts, and meals.
- `db_manager.py` - Handles all SQLite database operations.
- `user.py`, `workout.py`, `meal.py` - Data models for users, workouts, and meals.

## License

This project is open source and currently does not specify a license.

## Author

[NISHAKAR06](https://github.com/NISHAKAR06)
