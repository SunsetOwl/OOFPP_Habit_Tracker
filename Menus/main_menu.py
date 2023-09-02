import tkinter as tk
from habit import Habit
import habit_analytics as hana
from datetime import datetime
from Menus.settings import Settings
import Menus.standard_menu_elements as elems


class MainMenu(tk.Frame):

    def __init__(self, window, db_connect, page=0):
        self.window = window
        self.db_connect = db_connect
        self.settings = Settings()
        self.colors = self.settings.colors
        self.page = page

        tk.Frame.__init__(self, self.window, background=self.colors["background"])
        self.pack()
        self.grid_columnconfigure(0, minsize=200)
        self.grid_columnconfigure(1, minsize=40)

        lbl_mm_title = elems.HabitAppTitle(self, "~ Your Patch ~")
        lbl_mm_title.grid(row=0, pady=10, padx=15, columnspan=3)

        habit_list = hana.list_all_habits(db_connect)
        habit_ids = db_connect.load_all_habit_ids()

        page_list = []
        for i in [i+self.page*5 for i in range(0, 5)]:
            if i < len(habit_list):
                page_list.append(i)

        list_string = ""
        streaks_string = ""
        for i in page_list:
            if list_string != "":
                list_string += "\n"
                streaks_string += "\n"
            list_string += habit_list[i]
            streaks_string += str(hana.current_streak_length(db_connect, habit_ids[i]))

        habit_labels = []
        streak_labels = []
        perform_buttons = []

        row = 1

        for i in page_list:
            habit_labels.append(elems.HabitAppText(self, habit_list[i]))
            habit_labels[row-1].grid(row=row, pady=15, padx=10, column=0)

            streak_label = str(hana.current_streak_length(db_connect, habit_ids[i]))
            streak_labels.append(elems.HabitAppText(self, streak_label))
            streak_labels[row-1].grid(row=row, pady=15, padx=10, column=1)

            perform_buttons.append(elems.HabitAppButton(self, "Water",
                                                        lambda i=i: self.perform_habit_button(habit_ids[i])))
            perform_buttons[row-1].grid(row=row, pady=10, padx=10, column=2)

            row += 1

        # Set up the Buttons for previous/next page when dealing with more than 5 habits
        frm_back_next = tk.Frame(master=self, background=self.colors["background"])

        if page > 0:
            btn_previous = elems.HabitAppButton(frm_back_next, "<", lambda: self.previous_page())
            btn_previous.grid(row=0, padx=15, column=0)
        if len(habit_list) > page_list[-1]+1:
            btn_next = elems.HabitAppButton(frm_back_next, ">", lambda: self.next_page())
            btn_next.grid(row=0, padx=15, column=1)
        frm_back_next.grid(row=6, pady=10, columnspan=3)

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
        lbl_stats.grid(row=7, pady=10, padx=15, columnspan=3)

        if datetime.today().microsecond % 2 == 0:
            btn_grow = elems.HabitAppButton(self, "Add habit", lambda: self.add_dummy())
            btn_grow.grid(row=8, pady=10, padx=15, columnspan=3)
        else:
            btn_habit_management = elems.HabitAppButton(self, "Habit Management", lambda: self.habit_mgmt_button())
            btn_habit_management.grid(row=8, pady=10, padx=15, columnspan=3)

        self.window.eval('tk::PlaceWindow . center')
        self.tkraise()

    def perform_habit_button(self, habit_id):
        hab = Habit(self.db_connect)
        hab.load_data(habit_id)
        hab.perform()

        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect, self.page)

    def next_page(self):
        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect, self.page+1)

    def previous_page(self):
        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect, self.page-1)

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
