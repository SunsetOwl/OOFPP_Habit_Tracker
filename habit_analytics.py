"""
- return a list of all currently tracked habits,
- return a list of all habits with the same periodicity,
- return the longest run streak of all defined habits,
- and return the longest run streak for a given habit.
"""

from datetime import datetime, timedelta
from habit import Habit
from database_connector import DatabaseConnector
from streak import Streak

def list_all_habits(db_connect):

    habit_ids = db_connect.get_all_habit_ids()
    habit_names = [habit[1] for habit in db_connect.get_habits_in_list(habit_ids)]

    print(habit_names)

    return habit_names

def list_habits_with_periodicity(db_connect, periodicity):

    habit_ids = db_connect.get_all_habits_of_periodicity(periodicity)
    habit_names = [habit[1] for habit in db_connect.get_habits_in_list(habit_ids)]

    print(habit_names)

    return habit_names