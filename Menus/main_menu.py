import tkinter as tk
from habit import Habit
import habit_analytics as hana
from datetime import datetime
from Menus.settings import Settings
import Menus.standard_menu_elements as elems


class MainMenu(tk.Frame):

    def __init__(self, window, db_connect):
        self.window = window
        self.db_connect = db_connect
        self.settings = Settings()
        self.colors = self.settings.colors

        tk.Frame.__init__(self, self.window, background=self.colors["background"])

        self.grid(row=0, column=0, sticky="nsew")

        lbl_mm_title = elems.HabitAppTitle(self, "~ Your Patch ~")
        lbl_mm_title.grid(row=0, pady=10, padx=15, columnspan=3)

        habit_list = hana.list_all_habits(db_connect)
        habit_ids = db_connect.load_all_habit_ids()
        list_string = ""
        streaks_string = ""
        for i in range(len(habit_list)):
            if list_string != "":
                list_string += "\n"
                streaks_string += "\n"
            list_string += habit_list[i]
            streaks_string += str(hana.current_streak_length(db_connect, habit_ids[i]))

        habit_labels = []
        streak_labels = []
        perform_buttons = []

        for i in range(len(habit_list)):
            habit_labels.append(elems.HabitAppText(self, habit_list[i]))
            habit_labels[i].grid(row=i + 1, pady=0, padx=15, column=0)

            streak_labels.append(elems.HabitAppText(self, str(hana.current_streak_length(db_connect, habit_ids[i]))))
            streak_labels[i].grid(row=i + 1, pady=15, padx=15, column=1)

            perform_buttons.append(elems.HabitAppButton(self, "Water",
                                                        lambda i=i: self.perform_habit_button(habit_ids[i])))
            perform_buttons[i].grid(row=i + 1, pady=0, padx=15, column=2)

        stats_text = "Longest streak(s) ever:"
        for (habit_id, length) in hana.longest_streak_length_general(db_connect):
            hab = Habit(db_connect)
            hab.load_data(habit_id)
            stats_text += "\n" + str(hab.name) + ": " + str(length)
        stats_text += "\n\n Currently longest streak(s):"
        for (habit_id, length) in hana.longest_streak_length_general(db_connect, True):
            hab = Habit(db_connect)
            hab.load_data(habit_id)
            stats_text += "\n" + str(hab.name) + ": " + str(length)

        lbl_stats = elems.HabitAppText(self, stats_text)
        lbl_stats.grid(row=1 + len(habit_list), pady=10, padx=15, columnspan=3)

        if datetime.today().microsecond % 2 == 0:
            grow_button = elems.HabitAppButton(self, "Add habit", lambda: self.add_dummy())
            grow_button.grid(row=2 + len(habit_list), pady=10, padx=15, columnspan=3)
        else:
            btn_habit_management = elems.HabitAppButton(self, "Habit Management", lambda: self.habit_mgmt_button())
            btn_habit_management.grid(row=2 + len(habit_list), pady=10, padx=15, columnspan=3)

        self.window.eval('tk::PlaceWindow . center')
        self.tkraise()

    def perform_habit_button(self, habit_id):
        hab = Habit(self.db_connect)
        hab.load_data(habit_id)
        hab.perform()

        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect)

    def add_dummy(self):

        hab = Habit(self.db_connect, name="Water the Garden", periodicity=7,
                    description="Water all plants in the garden")

        if hab.name not in hana.list_all_habits(self.db_connect):
            hab.new_habit()

        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect)

    def habit_mgmt_button(self):
        from Menus.habit_management import HabitManagement

        self.grid_forget()
        self.destroy()

        HabitManagement(self.window, self.db_connect)
