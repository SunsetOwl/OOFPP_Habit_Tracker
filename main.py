import tkinter as tk
from habit import Habit
from database_connector import DatabaseConnector
import habit_analytics as hana


class MainMenu(tk.Frame):

    def __init__(self, window, db_connect):
        tk.Frame.__init__(self, window, background=colors["background"])

        habit_list = hana.list_all_habits(db_connect)
        list_string = ""
        for habit in habit_list:
            if list_string != "":
                list_string += "\n"
            list_string += habit

        lbl_mm_title = tk.Label(text="~ Your Patch ~",
                                foreground=colors["dark"],
                                background=colors["background"],
                                font=("Courier New", 30, "bold"),
                                master=self
                                )
        lbl_mm_title.grid(row=0, pady=10, padx=15, columnspan=3)

        lbl_mm_habits = tk.Label(text=list_string,
                                 foreground=colors["dark"],
                                 background=colors["background"],
                                 font=("Courier New", 13),
                                 pady=15,
                                 master=self
                                 )
        lbl_mm_habits.grid(row=1, pady=10, padx=15, column=0)


def load_dummy():
    db_connect.load_dummy()
    hab = Habit(db_connect)
    hab.load_data(4)
    hab.print()
    print(hab.latest_check())
    print(hab.perform())
    print(hab.latest_check())
    print(hab.perform())
    print(hab.latest_check())
    hana.list_all_habits(db_connect)
    hana.list_habits_with_periodicity(db_connect, 1)

    frm_main_menu = MainMenu(window, db_connect)

    frm_main_menu.grid(row=0, column=0, sticky="nsew")
    frm_main_menu.tkraise()


colors = {"highlight": "#B6D274",
          "background": "#F2E8CF",
          "light": "#5D8745",
          "dark": "#335C3B",
          "contrast": "#BC4749"}

window = tk.Tk()
window.title("Habit Tracker")
window.configure(background=colors["background"])
window.minsize(400, 500)
window.maxsize(400, 500)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

frm_greeting = tk.Frame(window, background=colors["background"])
frm_greeting.grid(row=0, column=0)

title = tk.Label(
    text="Welcome, User!",
    foreground=colors["dark"],
    background=colors["background"],
    font=("Courier New", 30, "bold"),
    master=frm_greeting
)
title.grid(row=0, pady=10, padx=15, columnspan=2)

lbl_intro = tk.Label(
    text="This is Grow Your Habits\nWhere we nurture our goals\nuntil they grow into healthy\nhabit plants!\n\n"
         "It looks like this is\nyour first time with us.\n\n"
         "Would you like to visit\na pre-grown garden to see\nwhere the journey can go?\n\n"
         "Or do you want to start\nright away and plant\nyour own garden?",
    foreground=colors["dark"],
    background=colors["background"],
    font=("Courier New", 13),
    pady=15,
    master=frm_greeting
)
lbl_intro.grid(row=1, columnspan=2)

btn_load_dummy = tk.Button(master=frm_greeting,
                           text="Dummy",
                           background=colors["highlight"],
                           foreground=colors["light"],
                           activebackground=colors["highlight"],
                           activeforeground=colors["light"],
                           font=("Courier New", 15, "bold"),
                           command=load_dummy)
btn_load_dummy.grid(row=2, column=0, padx=10, pady=15)
btn_start_new = tk.Button(master=frm_greeting,
                          text="New Habit",
                          background=colors["highlight"],
                          foreground=colors["light"],
                          activebackground=colors["highlight"],
                          activeforeground=colors["light"],
                          font=("Courier New", 15, "bold"))
btn_start_new.grid(row=2, column=1, padx=10, pady=15)

db_connect = DatabaseConnector()

window.mainloop()


# TODO Yeet
import os

db_connect.cur.close()
db_connect.db.close()

os.remove("habit-tracker-database.db")
