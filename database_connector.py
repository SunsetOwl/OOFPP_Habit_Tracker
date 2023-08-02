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
                             name CHAR(30),
                             periodicity INTEGER,
                             creation_date TIMESTAMP,
                             todo TEXT
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

    def new_habit(self, name, periodicity, created, todo):
        """
        Adds a new habit to the habits table by entering all the provided data, then returns the newly assigned id.
        :param name: name of the habit to be set up
        :param periodicity: how many days there are to be in between habit checks
        :param created: timestamp of creation of the habit
        :return: The assigned id of the habit
        """

        if self._check_if_empty("habits"):
            habit_id = 0
        else:
            max_habit_query = "SELECT MAX(habit_id) FROM habits"
            habit_id = self.cur.execute(max_habit_query).fetchone()[0] + 1

        habit_data = (habit_id, name, periodicity, created, todo)
        insert_habit_query = "INSERT INTO habits VALUES (?, ?, ?, ?, ?)"
        self.cur.execute(insert_habit_query, habit_data)
        self.db.commit()

        return habit_id

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
            self.cur.execute(query, (habit_id,))
            self.db.commit()

    def get_all_habit_ids(self):
        """
        Loads all habitsIDs from the database and returns them for, for example, easy counting.
        :return: A tuple containing the ids of all habits in the database.
        """

        query = "SELECT habit_id FROM habits"
        all_habit_ids = self.cur.execute(query).fetchall()
        return [habit[0] for habit in all_habit_ids]

    def get_all_habits_of_periodicity(self, periodicity):
        """
        Loads all habitsIDs of matching periodicity from the database and returns them.
        :return: A tuple containing the ids of all selected habits.
        """

        query = "SELECT habit_id FROM habits WHERE periodicity == ?"
        habit_ids = self.cur.execute(query, (periodicity,)).fetchall()
        return [habit[0] for habit in habit_ids]

    def get_habits_in_list(self, habit_ids):
        """
        Loads all habitsIDs of matching periodicity from the database and returns them.
        :return: A tuple containing the ids of all selected habits.
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

    def latest_check(self, habit_id):
        """
        Loads the latest check stored in the database for a certain habit.
        :param habit_id: ID of the habit to be searched for
        :return: A datetime containing the stored datetime from the database or a dummy value, if the habit isn't found.
        """

        if self._check_if_in_table("checks", habit_id):
            query = "SELECT MAX(check_time) FROM checks WHERE habit_id=?"
            check_data = self.cur.execute(query, (habit_id,)).fetchall()[0]
            check_date = check_data[0]
            return datetime.strptime(check_date, '%Y-%m-%d %H:%M:%S.%f')
        else:
            return datetime(2000, 1, 1)

    def save_check(self, habit_id, check_time):
        """
        Saves a check of a habit to the database, meaning the habit has been performed at this time.
        :param habit_id: ID of the habit performed
        :param check_time: datetime of when the habit was performed
        """

        query = "INSERT INTO checks VALUES (?, ?)"
        self.cur.execute(query, (habit_id, check_time))
        self.db.commit()

    def load_dummy(self):
        """

        :return:
        """

        habits_data = pd.read_csv('testdata_habits.csv', sep=';')

        # Technically .to_sql would be better here, but because the habit tracker is better tested with running streaks,
        # some calculations need to be made on the data saved in the .csv files before importing into the database.

        for index, row in habits_data.iterrows():
            date_to_save = datetime.today() - timedelta(days=row["days_ago"])
            time_to_save = datetime.strptime(row["time"], "%H:%M:%S")
            date_to_save = date_to_save.replace(hour=time_to_save.hour,
                                                minute=time_to_save.minute,
                                                second=time_to_save.second)
            query = "INSERT INTO habits VALUES (?, ?, ?, ?, ?)"
            self.cur.execute(query, (row["habit_id"], row["name"], row["periodicity"], date_to_save, row["todo"]))

        self.db.commit()

        checks_data = pd.read_csv('testdata_checks.csv', sep=';')

        for index, row in checks_data.iterrows():
            date_to_save = datetime.today() - timedelta(days=row["days_ago"])
            time_to_save = datetime.strptime(row["time"], "%H:%M:%S")
            date_to_save = date_to_save.replace(hour=time_to_save.hour,
                                                minute=time_to_save.minute,
                                                second=time_to_save.second)
            query = "INSERT INTO checks VALUES (?, ?)"
            self.cur.execute(query, (row["habit_id"], date_to_save))

        self.db.commit()

    def delete_database(self):
        self.cur.close()
        self.db.close()

        os.remove(self.name)
