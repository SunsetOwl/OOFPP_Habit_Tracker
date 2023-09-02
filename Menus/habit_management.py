import tkinter as tk
from habit import Habit
import habit_analytics as hana
from database_connector import DatabaseConnector
from Menus.settings import Settings
import Menus.standard_menu_elements as elems


class HabitManagement(tk.Frame):

    def __init__(self, window, db_connect):
        self.window = window
        self.db_connect = db_connect
        self.settings = Settings()
        self.colors = self.settings.colors

        tk.Frame.__init__(self, self.window, background=self.colors["background"])

        self.grid(row=0, column=0, sticky="nsew")

        lbl_mm_title = elems.HabitAppTitle(self, "Habit Management")
        lbl_mm_title.grid(row=0, pady=10, padx=15, columnspan=2)

        habit_ids = db_connect.load_all_habit_ids()

        if len(habit_ids) > 0:
            habit_list = hana.list_all_habits(db_connect)

            self.selected_habit = tk.StringVar(self.window)
            self.selected_habit.set("Select a Habit")

            lbl_delete_habit = elems.HabitAppText(self, "To delete a habit,\nchoose it from the dropdown menu:")
            lbl_delete_habit.grid(row=1, pady=10, padx=10, columnspan=2)

            opt_habit_list = elems.HabitAppDropdown(self, self.selected_habit, habit_list)
            opt_habit_list.grid(row=2, column=0, pady=10, padx=10)

            btn_delete_habit = elems.HabitAppButton(self, "Delete Habit",
                                                    lambda: self.delete_habit(self.selected_habit.get()))
            btn_delete_habit.grid(row=2, column=1, pady=10, padx=10)

        btn_reset_database = elems.HabitAppButton(self, "Reset Database", lambda: self.reset_database_button())
        btn_reset_database.grid(row=3, pady=10, padx=15, columnspan=2)

        btn_go_back = elems.HabitAppButton(self, "Back", lambda: self.go_back_button())
        btn_go_back.grid(row=4, pady=10, padx=15, columnspan=2)

        self.window.eval('tk::PlaceWindow . center')
        self.tkraise()

    def reset_database_button(self):

        from Menus.welcome_screen import WelcomeScreen

        self.db_connect.reset_database()

        self.grid_forget()
        self.destroy()

        WelcomeScreen(self.window, self.db_connect)

    def go_back_button(self):

        from Menus.main_menu import MainMenu

        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect)

    def delete_habit(self, habit_name):

        habit_id = self.db_connect.find_habit_id(habit_name)

        if habit_id > 0:
            self.db_connect.delete_habit(habit_id)

        self.grid_forget()
        self.destroy()

        HabitManagement(self.window, self.db_connect)
