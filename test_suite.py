from habit import Habit
from streak import Streak
from database_connector import DatabaseConnector
from datetime import datetime, timedelta
from freezegun import freeze_time
import pytest


class TestHabit:

    def setup_method(self):
        self.empty_db = DatabaseConnector("test_empty_database.db")
        self.test_db = DatabaseConnector("test_database.db")

        self.test_db.load_dummy()

    def test_dummy_habit_data_loaded_correctly_in_setup(self):
        habit_a = Habit(self.test_db)
        habit_a.load_data(1)

        assert habit_a.created.day == (datetime.today()-timedelta(days=63)).day

    def test_dummy_checks_data_loaded_correctly_in_setup(self):
        habit_a = Habit(self.test_db)
        habit_a.load_data(1)

        assert habit_a.latest_check().hour == 21

    def test_deleting_the_database_and_reloading_a_dummy_dataset_in_the_reset_database_works(self):
        self.test_db.delete_database()
        self.test_db = DatabaseConnector("test_database.db")

        self.test_db.load_dummy()

        habit_a = Habit(self.test_db)
        habit_a.load_data(1)

        assert habit_a.latest_check().hour == 21

    def test_when_habit_added_then_habit_loadable_from_database(self):
        habit_a = Habit(self.test_db)
        habit_a.new_habit()
        habit_b = Habit(self.test_db)
        habit_b.load_data(habit_a.habit_id)

        assert (habit_a.habit_id, habit_a.name, habit_a.periodicity, habit_a.created, habit_a.todo) == \
               (habit_b.habit_id, habit_b.name, habit_b.periodicity, habit_b.created, habit_b.todo)

    def test_when_habit_added_then_one_more_entry_in_database(self):
        entries_before = len(self.test_db.get_all_habit_ids())
        habit_a = Habit(self.test_db)
        habit_a.new_habit()
        entries_after = len(self.test_db.get_all_habit_ids())

        assert entries_before + 1 == entries_after

    def test_when_loading_nonexistent_habit_from_database_then_no_change_to_base_habit(self):
        habit_new = Habit(self.empty_db)
        habit_load = Habit(self.empty_db, created=habit_new.created)
        habit_load.load_data(0)

        assert (habit_new.habit_id, habit_new.name, habit_new.periodicity, habit_new.created) == \
               (habit_load.habit_id, habit_load.name, habit_load.periodicity, habit_load.created)

    def test_fetch_check_of_habit_that_has_not_been_performed_then_returned_2000(self):
        habit_a = Habit(self.test_db)
        habit_a.new_habit()

        assert self.test_db.latest_check(habit_a.habit_id) == datetime(2000, 1, 1)

    def test_perform_a_habit_then_return_saved_and_latest_check_is_in_database(self):
        habit_a = Habit(self.test_db)
        habit_a.load_data(1)
        result = habit_a.perform()

        assert result == "Saved"
        assert self.test_db.latest_check(habit_a.habit_id).day == (datetime.today() - timedelta(hours=2)).day

    def test_perform_a_habit_at_that_has_been_performed_before_today_then_return_too_early(self):
        habit_a = Habit(self.test_db)
        habit_a.load_data(1)
        result_one = habit_a.perform()
        result_two = habit_a.perform()

        assert result_one == "Saved"
        assert result_two == "Too Early"

    @freeze_time('2023-08-03 01:12:13.000001', tick=True)
    def test_edgecase_perform_a_habit_at_1_am_that_has_been_performed_before_today_then_return_too_early(self):
        habit_a = Habit(self.test_db)
        habit_a.load_data(1)
        result_one = habit_a.perform()
        result_two = habit_a.perform()

        assert result_one == "Saved"
        assert result_two == "Too Early"

    def test_a_check_that_will_or_will_not_break_the_streak_then_streak_check_returns_true_or_false(self):
        streak = Streak(1, 7, datetime(2023, 1, 1))

        assert streak.check_continues_streak(datetime(2023, 1, 8))
        assert not streak.check_continues_streak(datetime(2023, 1, 10))

    def test_add_a_check_that_will_continue_the_streak_then_streak_is_ongoing(self):
        streak = Streak(1, 7, datetime(2023, 1, 1))
        streak.add_check(datetime(2023, 1, 5))

        assert streak.ongoing
        assert streak.length() == 5

    def test_add_a_check_that_will_not_continue_the_streak_then_streak_is_not_ongoing(self):
        streak = Streak(1, 7, datetime(2023, 1, 1))
        streak.add_check(datetime(2023, 1, 10))

        assert not streak.ongoing

    def teardown_method(self):
        self.test_db.delete_database()
        self.empty_db.delete_database()
