import tkinter as tk
from habit import Habit
import habit_analytics as hana
from database_connector import DatabaseConnector


class HabitManagement(tk.Frame):

    def __init__(self, window, db_connect, colors):
        self.window = window
        self.db_connect = db_connect
        self.colors = colors

        tk.Frame.__init__(self, self.window, background=colors["background"])

        self.grid(row=0, column=0, sticky="nsew")

        lbl_mm_title = tk.Label(text="Habit Management",
                                foreground=colors["dark"],
                                background=colors["background"],
                                font=("Courier New", 30, "bold"),
                                master=self
                                )
        lbl_mm_title.grid(row=0, pady=10, padx=15, columnspan=2)

        habit_ids = db_connect.load_all_habit_ids()

        if len(habit_ids) > 0:
            habit_list = hana.list_all_habits(db_connect)

            self.selected_habit = tk.StringVar(self.window)
            self.selected_habit.set("Select a Habit")

            lbl_delete_habit = tk.Label(text="To delete a habit,\nchoose it from the dropdown menu:",
                                        foreground=colors["dark"],
                                        background=colors["background"],
                                        font=("Courier New", 15, "bold"),
                                        master=self
                                        )
            lbl_delete_habit.grid(row=0, pady=10, padx=10, columnspan=2)

            opt_habit_list = tk.OptionMenu(self,
                                           self.selected_habit,
                                           *habit_list)
            opt_habit_list.configure(background=colors["entry"],
                                     foreground=colors["light"],
                                     activebackground=colors["entry"],
                                     activeforeground=colors["light"],
                                     font=("Courier New", 15)
                                     )
            opt_habit_list.grid(row=1, column=0, pady=10, padx=10)

            btn_delete_habit = tk.Button(master=self,
                                         text="Delete Habit",
                                         background=colors["highlight"],
                                         foreground=colors["light"],
                                         activebackground=colors["highlight"],
                                         activeforeground=colors["light"],
                                         font=("Courier New", 15, "bold"),
                                         command=lambda: self.delete_habit(self.selected_habit.get())
                                         )
            btn_delete_habit.grid(row=1, column=1, pady=10, padx=10)

        btn_reset_database = tk.Button(master=self,
                                       text="Reset Database",
                                       background=colors["highlight"],
                                       foreground=colors["light"],
                                       activebackground=colors["highlight"],
                                       activeforeground=colors["light"],
                                       font=("Courier New", 15, "bold"),
                                       command=lambda: self.reset_database_button()
                                       )
        btn_reset_database.grid(row=2, pady=10, padx=15, columnspan=2)

        btn_go_back = tk.Button(master=self,
                                text="Back",
                                background=colors["highlight"],
                                foreground=colors["light"],
                                activebackground=colors["highlight"],
                                activeforeground=colors["light"],
                                font=("Courier New", 15, "bold"),
                                command=lambda: self.go_back_button()
                                )
        btn_go_back.grid(row=3, pady=10, padx=15, columnspan=2)

        self.window.eval('tk::PlaceWindow . center')
        self.tkraise()

    def reset_database_button(self):

        from Menus.welcome_screen import WelcomeScreen

        self.db_connect.reset_database()

        self.grid_forget()
        self.destroy()

        WelcomeScreen(self.window, self.db_connect, self.colors)

    def go_back_button(self):

        from Menus.main_menu import MainMenu

        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect, self.colors)

    def delete_habit(self, habit_name):

        print(habit_name)

        habit_id = self.db_connect.find_habit_id(habit_name)

        print(habit_id)

        if habit_id > 0:
            self.db_connect.delete_habit(habit_id)

        self.grid_forget()
        self.destroy()

        HabitManagement(self.window, self.db_connect, self.colors)
