import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import os


class DatabaseConnector:

    def __init__(self, name="habit-tracker-database.db"):
        """
        A DatabaseConnector handles all communication with a sqlite3 based database.
        The initialization establishes a connection with the database and creates the cursor object,
        after which it initializes all required tables, if they haven't been previously set up.
        :param name: name of the database file, default: "habit-tracker-database.db", testing default: "test.db"
        """

        self.name = name
        self.db = sqlite3.connect(name)
        self.cur = self.db.cursor()

        habits_query = """CREATE TABLE IF NOT EXISTS habits (
                             habit_id INTEGER PRIMARY KEY,
                             name CHAR(30) UNIQUE,
                             periodicity INTEGER,
                             creation_date TIMESTAMP,
                             description TEXT
                             )"""
        checks_query = """CREATE TABLE IF NOT EXISTS checks (
                             habit_id INTEGER,
                             check_time TIMESTAMP,
                             PRIMARY KEY (habit_id, check_time),
                             FOREIGN KEY (habit_id)
                                 REFERENCES habits (habit_id)
                                     ON DELETE CASCADE
                                     ON UPDATE NO ACTION 
                             )"""
        self.cur.execute(habits_query)
        self.cur.execute(checks_query)
        self.db.commit()

    def delete_database(self):
        """
        Fully deletes the database, including its .db file.
        """

        self.cur.close()
        self.db.close()

        os.remove(self.name)

    def reset_database(self):
        """
        Fully deletes the database, including its .db file.
        """

        self.cur.close()
        self.db.close()

        os.remove(self.name)

        self.__init__(self.name)

    def insert_dummy(self):
        """
        Loads the dummy dataset provided in the two .csv files into the database.
        Note: Instead of importing the data simply via the to_sql function included in pandas,
        some calculations are performed on the dates to make the dataset current.
        """

        habits_data = pd.read_csv('testdata_habits.csv', sep=';')

        for index, row in habits_data.iterrows():
            date_to_save = datetime.today() - timedelta(days=row["days_ago"])
            time_to_save = datetime.strptime(row["time"], "%H:%M:%S")
            date_to_save = date_to_save.replace(hour=time_to_save.hour,
                                                minute=time_to_save.minute,
                                                second=time_to_save.second)
            query = "INSERT INTO habits VALUES (?, ?, ?, ?, ?)"
            self.cur.execute(query, (row["habit_id"], row["name"],
                                     row["periodicity"], date_to_save, row["description"]))

        checks_data = pd.read_csv('testdata_checks.csv', sep=';')
        self.cur.execute("PRAGMA foreign_keys = on")

        for index, row in checks_data.iterrows():
            date_to_save = datetime.today() - timedelta(days=row["days_ago"])
            time_to_save = datetime.strptime(row["time"], "%H:%M:%S")
            date_to_save = date_to_save.replace(hour=time_to_save.hour,
                                                minute=time_to_save.minute,
                                                second=time_to_save.second)
            query = "INSERT INTO checks VALUES (?, ?)"
            self.cur.execute(query, (row["habit_id"], date_to_save))

        self.db.commit()

    def _check_if_empty(self, table_name):
        """
        A quick check to see if the table is empty to avoid errors when fetching data.
        :param table_name: Name of the table to be checked
        :return: A Boolean answering if the table is empty
        """

        query = "SELECT COUNT(*) FROM {table}".format(table=table_name)
        count = self.cur.execute(query).fetchone()[0]
        return count == 0

    def _check_if_in_table(self, table_name, habit_id):
        """
        A quick check to see if a specific habit_id is listed in a table to avoid errors when fetching data.
        :param table_name: Name of the table to be checked
        :param habit_id: ID of the habit to be checked
        :return: A Boolean answering if the habit is in the table
        """

        query = "SELECT COUNT(*) FROM {table} WHERE habit_id={id}".format(table=table_name, id=habit_id)
        count = self.cur.execute(query).fetchone()[0]
        return count != 0

    def new_habit(self, name, periodicity, created, description):
        """
        Adds a new habit to the habits table by entering all the provided data, then returns the newly assigned id.
        :param name: The name of the habit.
        :param periodicity: Integer indicating after how many days a habit needs to be re-performed to retain a streak.
        :param created: Saves the exact time and date of when the habit was set up.
        :param description: Contains a more detailed description of the habit.
        :return: The assigned id of the habit
        """

        if self._check_if_empty("habits"):
            habit_id = 0
        else:
            max_habit_query = "SELECT MAX(habit_id) FROM habits"
            habit_id = self.cur.execute(max_habit_query).fetchone()[0] + 1

        habit_data = (habit_id, name, periodicity, created, description)
        insert_habit_query = "INSERT INTO habits VALUES (?, ?, ?, ?, ?)"
        self.cur.execute(insert_habit_query, habit_data)
        self.db.commit()

        return habit_id

    def find_habit_id(self, habit_name):
        """
        Finds the id of the given habit, as names are unique.
        If the habit_name is not in the database, it returns 0 instead.
        :param habit_name: Name of the habit to be loaded
        :return: An integer containing the habit's id or 0, if habit isn't in database.
        """

        query = "SELECT COUNT(*) FROM habits WHERE name=?"
        count = self.cur.execute(query, (habit_name,)).fetchone()[0]

        if count != 0:
            query = "SELECT habit_id FROM habits WHERE name=?"
            habit_id = self.cur.execute(query, (habit_name,)).fetchone()[0]
        else:
            habit_id = 0
        return habit_id

    def load_habit(self, habit_id):
        """
        Loads the data of the habit object found under the habit_id key in the habits table of the database.
        If the habit_id is not in the database, it returns "Empty" instead.
        :param habit_id: ID of the habit to be loaded
        :return: A tuple containing the data of the habit's row in the table or "Empty", if habit isn't in database.
        """

        if self._check_if_in_table("habits", habit_id):
            query = "SELECT * FROM habits WHERE habit_id=?"
            habit_data = self.cur.execute(query, (habit_id,)).fetchone()
        else:
            habit_data = ("Empty", 0, 0, 0, 0)
        return habit_data

    def delete_habit(self, habit_id):
        """
        Deletes the habit found under the habit_id key in the habits table of the database, if it exists.
        :param habit_id: ID of the habit to be deleted
        """

        if self._check_if_in_table("habits", habit_id):
            query = "DELETE FROM habits WHERE habit_id=?"
            self.cur.execute("PRAGMA foreign_keys = on")
            self.cur.execute(query, (habit_id,))
            self.db.commit()

    def load_all_habit_ids(self):
        """
        Loads all habitsIDs from the database and returns them for, for example, easy counting.
        :return: A tuple containing the ids of all habits in the database.
        """

        query = "SELECT habit_id FROM habits ORDER BY habit_id ASC"
        all_habit_ids = self.cur.execute(query).fetchall()
        return [habit[0] for habit in all_habit_ids]

    def load_all_habits_of_periodicity(self, periodicity):
        """
        Loads all habitsIDs of matching periodicity from the database and returns them.
        :param periodicity: The periodicity to be checked for.
        :return: A tuple containing the ids of all selected habits.
        """

        query = "SELECT habit_id FROM habits WHERE periodicity == ? ORDER BY habit_id ASC"
        habit_ids = self.cur.execute(query, (periodicity,)).fetchall()
        return [habit[0] for habit in habit_ids]

    def load_habits_in_list(self, habit_ids):
        """
        Loads the habit data of a set list of ids.
        :param habit_ids: List containing all requested habit ids.
        :return: A nested tuple containing the habit data.
        """

        id_list = "("
        for habit_id in habit_ids:
            if id_list != "(":
                id_list += ", "
            id_list += str(habit_id)
        id_list += ")"
        query = "SELECT * FROM habits WHERE habit_id IN " + id_list
        habits = self.cur.execute(query).fetchall()
        return habits

    def save_check(self, habit_id, check_time):
        """
        Saves a check of a habit to the database, meaning the habit has been performed at this time.
        :param habit_id: ID of the habit performed
        :param check_time: datetime of when the habit was performed
        """

        query = "INSERT INTO checks VALUES (?, ?)"
        self.cur.execute("PRAGMA foreign_keys = on")
        self.cur.execute(query, (habit_id, check_time))
        self.db.commit()

    def load_latest_check(self, habit_id):
        """
        Loads the latest check stored in the database for a certain habit.
        :param habit_id: ID of the habit to be searched for
        :return: A datetime containing the last time the habit has been performed (01.01.2000 if it hasn't yet)
        """

        if self._check_if_in_table("checks", habit_id):
            query = "SELECT MAX(check_time) FROM checks WHERE habit_id=?"
            check_data = self.cur.execute(query, (habit_id,)).fetchall()[0]
            check_date = check_data[0]
            return datetime.strptime(check_date, '%Y-%m-%d %H:%M:%S.%f')
        else:
            return datetime(2000, 1, 1)

    def load_all_checks(self, habit_id):
        """
        Checks the database for all times a habit has been performed.
        :param habit_id: The habit whose checks have been requested.
        :return: A tuple containing all datetimes of when the habit has been performed (01.01.2000 if it hasn't yet)
        """

        if self._check_if_in_table("checks", habit_id):
            query = "SELECT check_time FROM checks WHERE habit_id=?"
            check_data = self.cur.execute(query, (habit_id,)).fetchall()
            return [datetime.strptime(str(check[0]), '%Y-%m-%d %H:%M:%S.%f') for check in check_data]
        else:
            return datetime(2000, 1, 1)

    def load_number_of_checks(self, habit_id):
        """
        Checks the database for the number of times a habit has been performed.
        :param habit_id: The habit whose checks have been requested.
        :return: The number of times the habit has been performed.
        """

        query = "SELECT COUNT(*) FROM checks WHERE habit_id=?"
        check_count = self.cur.execute(query, (habit_id,)).fetchall()[0][0]
        return check_count

    def print_habits(self):

        query = "SELECT * FROM habits"
        all_habit_data = self.cur.execute(query).fetchall()
        for data in all_habit_data:
            print(data)

    def print_checks(self):

        query = "SELECT * FROM checks"
        all_check_data = self.cur.execute(query).fetchall()
        for data in all_check_data:
            print(data)

