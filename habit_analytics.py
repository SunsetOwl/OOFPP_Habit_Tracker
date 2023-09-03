from datetime import datetime, timedelta
from habit import Habit
from streak import Streak


def list_all_habits(db_connect):
    """
    Creates a list of all the habit names for easy listing in the application.
    :param db_connect: The Database Connector connected to the database.
    :return: A list of all habit names.
    """

    habit_ids = db_connect.load_all_habit_ids()
    habit_names = [habit[1] for habit in db_connect.load_habits_in_list(habit_ids)]

    return habit_names


def list_habits_with_periodicity(db_connect, periodicity):
    """
    Creates a list of all the habit names of habits of a certain periodicity for easy listing in the application.
    :param db_connect: The Database Connector connected to the database.
    :param periodicity: The periodicity to filter by.
    :return: A list of all found habit names.
    """

    habit_ids = db_connect.load_all_habits_of_periodicity(periodicity)
    habit_names = [habit[1] for habit in db_connect.load_habits_in_list(habit_ids)]

    return habit_names


def calculate_streaks(db_connect, habit_id):
    """
    Calculates a list of all the streaks of a given habit by going through checks performed of that particular habit.
    :param db_connect: The Database Connector connected to the database.
    :param habit_id: The id of the habit whose streaks are to be listed.
    :return: A list of all streaks of the habit.
    """

    habit = Habit(db_connect, habit_id)
    all_checks = db_connect.load_all_checks(habit_id)
    streaks = []
    streak_count = 0

    if all_checks == datetime(2000, 1, 1):
        return 0

    for check_time in all_checks:
        if not streaks:
            streaks.append(Streak(habit_id, habit.periodicity, check_time))
        else:
            s = streaks[streak_count]
            ongoing = s.add_check(check_time)
            streaks[streak_count] = s
            if not ongoing:
                streak_count += 1
                streaks.append(Streak(habit_id, habit.periodicity, check_time))

    return streaks


def current_streak_length(db_connect, habit_id):
    """
    Calculates the length of the current streak of a given habit. If the streak is broken, the result is 0.
    :param db_connect: The Database Connector connected to the database.
    :param habit_id: The id of the habit whose streaks are to be listed.
    :return: An integer containing the length of the current streak.
    """

    streaks = calculate_streaks(db_connect, habit_id)

    if streaks == 0:
        return 0

    s = streaks[-1]

    if not s.ongoing or not s.check_continues_streak(datetime.today()):
        return 0

    return s.length()


def current_streak_start(db_connect, habit_id):
    streaks = calculate_streaks(db_connect, habit_id)

    if streaks == 0:
        return "Not performed"

    s = streaks[-1]

    if not s.ongoing or not s.check_continues_streak(datetime.today()):
        return "No ongoing streak"

    return s.started.strftime("%d-%m-%Y")


def longest_streak_dates(db_connect, habit_id):

    streaks = calculate_streaks(db_connect, habit_id)

    if streaks == 0:
        return "Not performed", ""

    streak_lengths = [s.length() for s in streaks]

    i = streak_lengths.index(max(streak_lengths))

    return streaks[i].started.strftime("%d-%m-%Y"), streaks[i].ended.strftime("%d-%m-%Y")


def longest_streak_length(db_connect, habit_id):
    """
    Calculates the length of the longest streak of a given habit.
    :param db_connect: The Database Connector connected to the database.
    :param habit_id: The id of the habit whose streaks are to be listed.
    :return: An integer containing the length of the longest streak.
    """

    streaks = calculate_streaks(db_connect, habit_id)

    if streaks == 0:
        return 0

    streak_lengths = [s.length() for s in streaks]

    return max(streak_lengths)


def longest_streak_length_general(db_connect, current=False):
    """
    Calculates which habit has the longest streak in the database and returns its id and length of the streak.
    In case of a tie multiple habits and their streaks are returned.
    :param db_connect: The Database Connector connected to the database.
    :param current: A boolean that decides whether the streaks to be compared are only the ongoing streaks or not.
    :return: A list containing tuple pairs of habit_ids and streak_lengths.
    """

    habit_ids = db_connect.load_all_habit_ids()
    streak_lengths = []

    for habit_id in habit_ids:
        if current:
            streak_lengths.append(current_streak_length(db_connect, habit_id))
        else:
            streak_lengths.append(longest_streak_length(db_connect, habit_id))
    max_locations = [i for i, length in enumerate(streak_lengths) if length == max(streak_lengths)]

    results = []

    for i in range(len(max_locations)):
        results.append((habit_ids[max_locations[i]], streak_lengths[max_locations[i]]))

    return results


def consistency(db_connect, habit_id, timeframe):
    """
    Calculates how often the given habit has been and should have been performed within a given previous timeframe
    to see how consistent the user has been outside of being able to uphold a streak.
    The calculation of the "should have" does take into account when the habit was created.
    :param db_connect: The Database Connector connected to the database
    :param habit_id: The id of the habit to be analysed
    :param timeframe: The number of days to check. For example: 28 checks the past 4 fours weeks, today included
    :return: A tuple containing the number of times the habit has been performed within that timeframe
             and how often it should have been performed at least (rounded down).
    """

    first_date = datetime.today().date() - timedelta(days=timeframe-1)
    hab = Habit(db_connect, habit_id)

    if hab.created.date() > first_date:
        timeframe = (datetime.today().date() - hab.created.date()).days
        first_date = hab.created.date()
    if hab.created.date() == datetime.today().date():
        timeframe = 1

    all_checks = db_connect.load_all_checks(habit_id)
    valid_checks = []

    if all_checks == datetime(2000, 1, 1):
        return 0, timeframe // hab.periodicity

    for check in all_checks:
        if check.date() >= first_date and check.date() not in valid_checks:
            valid_checks.append(check.date())

    return len(valid_checks), timeframe // hab.periodicity
