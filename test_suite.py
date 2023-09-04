from habit import Habit
from streak import Streak
from database_connector import DatabaseConnector
from datetime import datetime, timedelta
from freezegun import freeze_time
import habit_analytics as hana
import pytest


class TestHabit:

    def setup_method(self):
        self.empty_db = DatabaseConnector("test_empty_database.db")
        self.test_db = DatabaseConnector("test_database.db")

        self.test_db.insert_dummy()

    @pytest.fixture
    def loaded_habit(self):
        return Habit(self.test_db, 1)

    @pytest.fixture
    def newly_added_habit(self):
        hab = Habit(self.test_db)
        hab.new_habit()
        return hab

    @pytest.fixture
    def weekly_streak(self):
        return Streak(1, 7, datetime(2023, 1, 1))

    def test_dummy_habit_data_loaded_correctly_in_setup(self, loaded_habit):
        assert loaded_habit.created.day == (datetime.today()-timedelta(days=63)).day

    def test_dummy_checks_data_loaded_correctly_in_setup(self, loaded_habit):
        assert loaded_habit.latest_check().hour == 21

    def test_deleting_the_database_and_reloading_a_dummy_dataset_in_then_reset_database_works(self):
        self.test_db.reset_database()
        self.test_db.insert_dummy()

        habit_a = Habit(self.test_db, 1)

        assert habit_a.latest_check().hour == 21

    def test_when_habit_added_then_habit_loadable_from_database(self, newly_added_habit):
        habit_b = Habit(self.test_db, newly_added_habit.habit_id)

        assert (newly_added_habit.name, newly_added_habit.created, newly_added_habit.description) == \
               (habit_b.name, habit_b.created, habit_b.description)

    def test_when_habit_added_then_one_more_entry_in_database(self):
        entries_before = len(self.test_db.load_all_habit_ids())
        habit_a = Habit(self.test_db)
        habit_a.new_habit()
        entries_after = len(self.test_db.load_all_habit_ids())

        assert entries_before + 1 == entries_after

    def test_when_loading_nonexistent_habit_from_database_then_no_change_to_base_habit(self):
        habit_new = Habit(self.empty_db)
        habit_load = Habit(self.empty_db, created=habit_new.created)
        habit_load.load_data(0)

        assert (habit_new.habit_id, habit_new.name, habit_new.periodicity, habit_new.created) == \
               (habit_load.habit_id, habit_load.name, habit_load.periodicity, habit_load.created)

    def test_fetch_check_of_habit_that_hasnt_been_performed_then_return_year_2000_and_0_checks(self, newly_added_habit):
        assert self.test_db.load_latest_check(newly_added_habit.habit_id) == datetime(2000, 1, 1)
        assert newly_added_habit.check_count() == 0

    def test_perform_a_habit_then_return_saved_and_latest_check_is_in_database(self, loaded_habit):
        result = loaded_habit.perform()

        assert result == "Saved"
        assert self.test_db.load_latest_check(loaded_habit.habit_id).day == (datetime.today() - timedelta(hours=2)).day

    def test_perform_a_habit_at_that_has_been_performed_before_today_then_return_too_early(self, loaded_habit):
        result_one = loaded_habit.perform()
        result_two = loaded_habit.perform()

        assert result_one == "Saved"
        assert result_two == "Too Early"

    @freeze_time('01:12:13.000001', tick=True)
    def test_perform_a_habit_at_1_am_that_has_been_performed_before_today_then_return_too_early(self, loaded_habit):
        result_one = loaded_habit.perform()
        result_two = loaded_habit.perform()

        assert result_one == "Saved"
        assert result_two == "Too Early"

    def test_check_that_will_or_will_not_break_the_streak_then_streak_check_returns_true_or_false(self, weekly_streak):

        assert weekly_streak.check_continues_streak(datetime(2023, 1, 8))
        assert not weekly_streak.check_continues_streak(datetime(2023, 1, 10))

    def test_add_a_check_that_will_continue_the_streak_then_streak_is_ongoing(self, weekly_streak):
        weekly_streak.add_check(datetime(2023, 1, 5))

        assert weekly_streak.ongoing
        assert weekly_streak.length() == 5

    def test_add_a_check_that_will_not_continue_the_streak_then_streak_is_not_ongoing(self, weekly_streak):
        weekly_streak.add_check(datetime(2023, 1, 10))

        assert not weekly_streak.ongoing

    def test_the_consistency_of_a_habit(self):
        assert hana.consistency(self.test_db, 2, 28) == (27, 28)

    def test_the_consistency_calculation_of_a_habit_that_has_been_performed_more_than_necessary(self):
        assert hana.consistency(self.test_db, 1, 28) == (5, 4)

    def test_create_a_habit_then_its_consistency_will_be_0_out_of_1(self, newly_added_habit):
        assert hana.consistency(self.test_db, newly_added_habit.habit_id, 28) == (0, 1)

    def test_consistency_of_1_day_tests_if_habit_was_performed_today(self, loaded_habit, newly_added_habit):
        loaded_habit.perform()

        assert hana.consistency(self.test_db, loaded_habit.habit_id, 1)[0] == 1
        assert hana.consistency(self.test_db, newly_added_habit.habit_id, 1)[0] == 0

    def test_delete_a_habit_then_checks_are_deleted_as_well(self, loaded_habit):
        loaded_habit.perform()
        loaded_habit.delete()

        assert not self.test_db._check_if_in_table("habits", 1)

    def teardown_method(self):
        self.test_db.delete_database()
        self.empty_db.delete_database()
