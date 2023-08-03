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


def calculate_streaks(db_connect, habit_id):

    habit = Habit(db_connect)
    habit.load_data(habit_id)
    all_checks = db_connect.load_all_checks(habit_id)
    streaks = []
    streak_count = 0

    if all_checks == datetime(2000, 1, 1):
        return 0

    for check_time in all_checks:
        if streaks == []:
            streaks.append(Streak(habit_id, habit.periodicity, check_time))
        else:
            s = streaks[streak_count]
            ongoing = s.add_check(check_time)
            streaks[streak_count] = s
            if not ongoing:
                streak_count += 1
                streaks.append(Streak(habit_id, habit.periodicity, check_time))

    for s in streaks:
        print(habit_id, s.started, s.ended, s.length())

    return streaks


def current_streak_length(db_connect, habit_id):

    streaks = calculate_streaks(db_connect, habit_id)

    if streaks == 0:
        return 0

    s = streaks[-1]

    if not s.ongoing or not s.check_continues_streak(datetime.today()):
        return 0
    else:
        return s.length()

