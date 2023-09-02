import tkinter as tk
from Menus.settings import Settings
import Menus.standard_menu_elements as elems


class WelcomeScreen(tk.Frame):

    def __init__(self, window, db_connect):
        self.window = window
        self.db_connect = db_connect
        self.settings = Settings()
        self.colors = self.settings.colors

        tk.Frame.__init__(self, window, background=self.colors["background"])

        self.grid(row=0, column=0, sticky="nsew")

        title = elems.HabitAppTitle(master=self, text="Welcome, User!")
        title.grid(row=0, pady=10, padx=15, columnspan=2)

        lbl_intro = elems.HabitAppText(
            master=self,
            text="This is Grow Your Habits\nWhere we nurture our goals\nuntil they grow into healthy\nhabit plants!\n\n"
                 "It looks like this is\nyour first time with us.\n\n"
                 "Would you like to visit\na pre-grown garden to see\nwhere the journey can go?\n\n"
                 "Or do you want to start\nright away and plant\nyour own garden?"
        )
        lbl_intro.grid(row=1, pady=15, columnspan=2)

        btn_load_dummy = elems.HabitAppButton(self, "Dummy", lambda: self.load_dummy())
        btn_load_dummy.grid(row=2, column=0, padx=10, pady=15)

        btn_start_new = elems.HabitAppButton(self, "New Habit", lambda: self.load_dummy_management())
        btn_start_new.grid(row=2, column=1, padx=10, pady=15)

        self.window.eval('tk::PlaceWindow . center')
        self.tkraise()

    def load_dummy(self):

        from Menus.main_menu import MainMenu

        self.db_connect.insert_dummy()
        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect)

    def load_dummy_management(self):

        from Menus.habit_management import HabitManagement

        self.db_connect.insert_dummy()
        self.grid_forget()
        self.destroy()

        HabitManagement(self.window, self.db_connect)
