from datetime import datetime, timedelta


class Habit:

    def __init__(self, db_connect, habit_id=0, name="New", periodicity=1,
                 created=datetime.today(), description="Do the Task"):
        """
        The Habit class is used to contain all relevant information about a habit.
        It has functions for loading, saving and deleting a habit.
        :param db_connect: The DatabaseConnector object that interacts with the database this Habit belongs to.
        :param habit_id: The unique id of the habit, which at 0 indicated an empty, unsaved habit.
        :param name: The name of the habit.
        :param periodicity: Integer indicating after how many days a habit needs to be re-performed to retain a streak.
        :param created: Saves the exact time and date of when the habit was set up.
        :param description: Contains a more detailed description of the habit.
        """
        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.created = created
        self.db_connect = db_connect
        self.description = description

        if self.habit_id > 0:
            self.load_data(self.habit_id)

    def new_habit(self):
        """
        Saves the habit to the database with all current parameters,
        then assigns it the automatically generated habit_id.
        """

        self.habit_id = self.db_connect.new_habit(self.name, self.periodicity, self.created, self.description)

    def load_data(self, habit_id):
        """
        Loads all data of the referenced habit from the database into this habit object,
        unless the habit_id can't be found.
        :param habit_id: The ID of the habit to be loaded into this habit object
        """

        habit_data = self.db_connect.load_habit(habit_id)
        if habit_data[0] != "Empty":
            self.habit_id = habit_data[0]
            self.name = habit_data[1]
            self.periodicity = habit_data[2]
            self.created = datetime.strptime(habit_data[3], '%Y-%m-%d %H:%M:%S.%f')
            self.description = habit_data[4]

    def delete(self):
        """
        Deletes the habit from the database.
        """

        if self.habit_id != 0:
            self.db_connect.delete_habit(self.habit_id)

    def perform(self):
        """
        Adjusts the current datetime to two hours ago to account for nightowls that finish their list at 1:30 AM,
        which means that technically all timestamps for completions are "mistimed" by two hours in the database.
        Fetches the last check date and compares it to the date for this check. If it's the same day, nothing is added.
        If it's at least one day (date, not 24 hours) later, the check is added to the database.
        :return: Final state of the function as a string (Too Early, Saved)
        """

        if (datetime.today() - self.created).seconds < 2*60*60:  # Ensure no check is saved before the creation time
            check_data = datetime.today()
        else:
            check_data = datetime.today() - timedelta(hours=2)
        latest_check = self.latest_check() + timedelta(hours=2)

        self.db_connect.save_check(self.habit_id, check_data)
        state = "Saved"

        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        latest_day = latest_check.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if (today - latest_day).days == 0:
            state = "Too Early"

        return state

    def latest_check(self):
        """
        Fetches when this habit has last been performed from the database.
        :return: Datetime containing when it was last performed
        """

        return self.db_connect.load_latest_check(self.habit_id)

    def check_count(self):
        """
        Fetches the amount of times the habit has been performed.
        :return: An integer of all times the habit has been performed.
        """

        return self.db_connect.load_number_of_checks(self.habit_id)

    def description_with_line_breaks(self):
        """
        Fetches the description of the habit with more easily displayable line breaks.
        :return: The broken up description string.
        """

        output = ""
        description_cut = self.description.split()

        for word in description_cut:
            if output == "":
                output = word
            elif len(output.splitlines()[-1]) + 1 + len(word) < 35:
                output = output + " " + word
            else:
                output = output + "\n" + word

        return output

