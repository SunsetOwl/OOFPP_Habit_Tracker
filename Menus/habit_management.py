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

        self.period_chosen = tk.StringVar()
        self.period_chosen.set("D")

        lbl_add_habit = elems.HabitAppText(self, "To add a habit, \nfill in the following information:")
        lbl_add_habit.grid(row=1, pady=10, columnspan=2)

        frm_name = tk.Frame(master=self, background=self.colors["background"])
        lbl_name = elems.HabitAppText(frm_name, "Name:")
        txt_name = elems.HabitAppEntry(frm_name, 20)
        lbl_name.grid(row=2, padx=20, column=0)
        txt_name.grid(row=2, padx=20, column=1)
        frm_name.grid(row=2, pady=(20, 0), columnspan=2)

        frm_period_choice = tk.Frame(master=self, background=self.colors["background"])

        lbl_periodicity = elems.HabitAppText(frm_period_choice, "How often do\nyou want to\nperform\nthis habit?")
        lbl_periodicity.grid(row=0, column=0, padx=(10, 30))

        frm_period_options = tk.Frame(master=frm_period_choice, background=self.colors["background"])

        rb_daily = elems.HabitAppRadio(frm_period_options, "D", self.period_chosen)
        rb_daily.grid(row=0, column=0)
        rb_daily.select()
        rb_weekly = elems.HabitAppRadio(frm_period_options, "W", self.period_chosen)
        rb_weekly.grid(row=1, column=0)
        rb_custom = elems.HabitAppRadio(frm_period_options, "C", self.period_chosen)
        rb_custom.grid(row=2, column=0)
        lbl_daily = elems.HabitAppText(frm_period_options, "Daily")
        lbl_daily.grid(row=0, padx=(5, 20), column=1, sticky="w")
        lbl_weekly = elems.HabitAppText(frm_period_options, "Weekly")
        lbl_weekly.grid(row=1, padx=(5, 20), column=1, sticky="w")

        frm_custom_entry = tk.Frame(master=frm_period_options, background=self.colors["background"])
        lbl_custom_front = elems.HabitAppText(frm_custom_entry, "Every")
        lbl_custom_front.grid(row=0, column=0)
        txt_custom = elems.HabitAppEntry(frm_custom_entry, 5)
        txt_custom.grid(row=0, padx=5, column=1)
        lbl_custom_back = elems.HabitAppText(frm_custom_entry, "Days")
        lbl_custom_back.grid(row=0, column=2)

        frm_custom_entry.grid(row=2, padx=(5, 20), column=1, sticky="w")

        frm_period_options.grid(row=0, column=1)

        frm_period_choice.grid(row=3, pady=(20, 0), rowspan=2, columnspan=2)

        lbl_description = elems.HabitAppText(self, "What does this habit entail?")
        lbl_description.grid(row=5, pady=(20, 0), columnspan=2)
        txt_description = elems.HabitAppEntry(self, 30)
        txt_description.grid(row=6, columnspan=2)

        btn_add_habit = elems.HabitAppButton(self, "Add Habit",
                                                lambda: print("hello"))
        btn_add_habit.grid(row=7, columnspan=2, pady=(20, 0), padx=10)

        if len(habit_ids) > 0:
            habit_list = hana.list_all_habits(db_connect)

            self.selected_habit = tk.StringVar(self.window)
            self.selected_habit.set("Select a Habit")

            lbl_delete_habit = elems.HabitAppText(self, "To delete a habit,\nchoose it from the dropdown menu:")
            lbl_delete_habit.grid(row=8, pady=10, padx=10, columnspan=2)

            opt_habit_list = elems.HabitAppDropdown(self, self.selected_habit, habit_list)
            opt_habit_list.grid(row=9, column=0, pady=10, padx=10)

            btn_delete_habit = elems.HabitAppButton(self, "Delete Habit",
                                                    lambda: self.delete_habit(self.selected_habit.get()))
            btn_delete_habit.grid(row=9, column=1, pady=10, padx=10)

        btn_reset_database = elems.HabitAppButton(self, "Reset Database", lambda: self.reset_database_button())
        btn_reset_database.grid(row=10, pady=10, padx=15, columnspan=2)

        btn_go_back = elems.HabitAppButton(self, "Back", lambda: self.go_back_button())
        btn_go_back.grid(row=11, pady=10, padx=15, columnspan=2)

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
