from datetime import datetime, timedelta


class Habit:

    def __init__(self, db_connect, habit_id=0, name="New Habit", periodicity=1, created=datetime.today(), todo="Fulfill a Task"):
        """

        :param db_connect: The DatabaseConnector object that interacts with the database this Habit belongs to.

        """
        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.created = created
        self.db_connect = db_connect
        self.todo = todo

    def new_habit(self):
        """"""
        self.habit_id = self.db_connect.new_habit(self.name, self.periodicity, self.created, self.todo)

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
            self.todo = habit_data[4]

    def delete(self):

        self.db_connect.delete_habit(self.habit_id)

    def print(self):
        print("ID: ", self.habit_id)
        print("Name: ", self.name)
        print("Periodicity: ", self.periodicity)
        print("Created: ", self.created)
        print("ToDo: ", self.todo)

    def perform(self):
        """
        Adjusts the current datetime to two hours ago to account for nightowls that finish their list at 1:30 AM,
        which means that technically all timestamps for completions are "mistimed" by two hours in the database.
        Fetches the last check date and compares it to the date for this check. If it's the same day, nothing is added.
        If it's at least one day later, the check is added to the database.
        :return: final state of the function as a string (Too Early, Saved)
        """

        state = "Saving"
        if (datetime.today() - self.created).seconds < 2*60*60:  # Ensure no check is saved before the creation time
            check_data = datetime.today()
        else:
            check_data = datetime.today() - timedelta(hours=2)
        latest_check = self.latest_check()

        self.db_connect.save_check(self.habit_id, check_data)
        state = "Saved"
        
        if (datetime.today().day - latest_check.day) == 0:
            state = "Too Early"

        return state

    def latest_check(self):
        """
        Fetches when this habit has last been performed from the database.
        :return: datetime containing when it was last performed
        """

        return self.db_connect.latest_check(self.habit_id)

