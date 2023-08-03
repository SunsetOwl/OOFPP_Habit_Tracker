class Streak:

    ongoing = True  # Boolean that describes whether a streak is ongoing or not. All streaks start out as ongoing.

    def __init__(self, habit_id, periodicity, started):
        """
        Creates a Streak object used for easier calculation of habit statistics.
        :param habit_id: The Habit this streak belongs to.
        :param periodicity: How often the habit is to be performed.
        :param started: First day of the streak
        """

        self.habit_id = habit_id
        self.periodicity = periodicity
        self.started = started
        self.ended = started

    def length(self):
        """
        Returns the length of the streak in days including the first day as a single day.
        :return: integer of the streak length
        """

        return (self.ended - self.started).days + 1

    def check_continues_streak(self, check_time):
        """
        Checks whether adding the check in check_time will prolong the streak or not.
        :param check_time: Datetime containing the check to be tested
        :return: Boolean of whether the check will continue or break the streak
        """

        check_day = check_time.replace(hour=0, minute=0, second=0)
        ended_day = self.ended.replace(hour=0, minute=0, second=0)

        if (check_day - ended_day).days <= self.periodicity:
            return True
        else:
            return False

    def add_check(self, check_time):
        """
        Prolongs the streak by the given date, if the streak can be prolonged with it, otherwise ends it.
        :param check_time: The check to be added to the streak
        :return: Boolean of whether the check continued (True) or broke the streak (False)
        """

        if not self.ongoing:
            return

        if self.check_continues_streak(check_time):
            self.ended = check_time
            return True
        else:
            self.ongoing = False
            return False
