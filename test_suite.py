from habit import Habit
from database_connector import DatabaseConnector
from datetime import datetime


class TestHabit:

    def setup_method(self):
        self.empty_db = DatabaseConnector("test_empty_database.db")
        self.test_db = DatabaseConnector("test_database.db")

        habit_a = Habit(self.test_db)
        habit_a.new_habit()

    def test_when_habit_added_then_habit_loadable_from_database(self):
        habit_a = Habit(self.test_db)
        habit_a.new_habit()
        habit_b = Habit(self.test_db)
        habit_b.load_data(habit_a.habit_id)

        assert (habit_a.habit_id, habit_a.name, habit_a.periodicity, habit_a.created) == \
               (habit_b.habit_id, habit_b.name, habit_b.periodicity, habit_b.created)

    def test_when_habit_added_then_one_more_entry_in_database(self):
        entries_before = len(self.test_db.get_all_habits())
        habit_a = Habit(self.test_db)
        habit_a.new_habit()
        entries_after = len(self.test_db.get_all_habits())

        assert entries_before + 1 == entries_after

    def test_when_loading_nonexistent_habit_from_database_then_no_change_to_base_habit(self):
        habit_new = Habit(self.empty_db)
        habit_load = Habit(self.empty_db, created=habit_new.created)
        habit_load.load_data(0)
        assert (habit_new.habit_id, habit_new.name, habit_new.periodicity, habit_new.created) == \
               (habit_load.habit_id, habit_load.name, habit_load.periodicity, habit_load.created)

    def teardown_method(self):
        import os

        self.test_db.cur.close()
        self.test_db.db.close()
        self.empty_db.cur.close()
        self.empty_db.db.close()

        os.remove("test_database.db")
        os.remove("test_empty_database.db")
