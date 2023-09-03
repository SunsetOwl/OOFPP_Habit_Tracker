from habit import Habit
import habit_analytics as hana
import Menus.standard_menu_elements as elems
import tkinter as tk


class StatsMenu(elems.HabitAppFrame):
    """
    This menu displays information about the user's habit statistics in general like longest current and overall streak
    and allows for the user to select a habit to analyze further.
    """

    def __init__(self, window, db_connect):
        """
        Initializes the general habit statistics menu
        :param window: The parent tkinter window
        :param db_connect: The Database Connector connected to the database
        """

        self.window = window
        self.db_connect = db_connect

        elems.HabitAppFrame.__init__(self, self.window)
        self.pack()

        # Title

        lbl_mm_title = elems.HabitAppTitle(self, "~ Your Stats ~")
        lbl_mm_title.grid(row=0, pady=10, padx=15)

        # Streaks

        stats_text = "Longest streak(s) ever:"
        for (habit_id, length) in hana.longest_streak_length_general(db_connect):
            hab = Habit(db_connect, habit_id)
            stats_text += "\n" + str(hab.name) + ": " + str(length)
        stats_text += "\n\n Currently longest streak(s):"
        for (habit_id, length) in hana.longest_streak_length_general(db_connect, True):
            hab = Habit(db_connect, habit_id)
            stats_text += "\n" + str(hab.name) + ": " + str(length)

        lbl_stats = elems.HabitAppText(self, stats_text)
        lbl_stats.grid(row=1, pady=10, padx=15)

        # Habit selection for further analysis

        habit_list = hana.list_all_habits(db_connect)

        self.selected_habit = tk.StringVar(self.window)
        self.selected_habit.set("Select a Habit")

        lbl_insights_habit = elems.HabitAppText(self, "To gain further insights\ninto one particular habit,\n" +
                                                "choose it from the dropdown menu:")
        lbl_insights_habit.grid(row=2, padx=10)

        frm_habit_insights = elems.HabitAppFrame(self)

        opt_habit_list = elems.HabitAppDropdown(frm_habit_insights, self.selected_habit, habit_list)
        opt_habit_list.grid(row=0, column=0, pady=10, padx=10)

        btn_delete_habit = elems.HabitAppButton(frm_habit_insights, "Insights", lambda: self.habit_insights_button())
        btn_delete_habit.grid(row=0, column=1, pady=10, padx=15)

        frm_habit_insights.grid(row=3, pady=10)

        # Return Button

        btn_go_back = elems.HabitAppButton(self, "Back", lambda: self.go_back_button())
        btn_go_back.grid(row=4, pady=(10, 20), padx=20, sticky="w")

        self.window.eval('tk::PlaceWindow . center')
        self.tkraise()

    def go_back_button(self):
        """
        This button returns the user to the previous menu: the main menu.
        """

        from Menus.main_menu import MainMenu

        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect)

    def habit_insights_button(self):
        """
        This button takes the user to a menu containing more information about the habit chosen in the dropdown menu.
        """

        habit_id = self.db_connect.find_habit_id(self.selected_habit.get())

        if habit_id > 0:

            from Menus.habit_insights_menu import HabitInsightsMenu

            self.grid_forget()
            self.destroy()

            HabitInsightsMenu(self.window, self.db_connect, habit_id)
