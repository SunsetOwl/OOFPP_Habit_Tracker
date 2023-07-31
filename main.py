import tkinter as tk
from datetime import datetime, timedelta
from habit import Habit
from database_connector import DatabaseConnector

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

frmGreeting = tk.Frame(window,
                       background=colors["background"])
frmGreeting.pack()

title = tk.Label(
    text="Welcome, User!",
    foreground=colors["dark"],
    background=colors["background"],
    font=("Courier New", 30, "bold"),
    master=frmGreeting
)
title.grid(row=0, pady=15, padx=15, columnspan=2)

lblIntro = tk.Label(
    text="This is Grow Your Habits\nWhere we nurture our goals\nuntil they grow into healthy\nhabit plants!\n\n"
         "It looks like this is\nyour first time with us.\n\n"
         "Would you like to visit\na pre-grown garden to see\nwhere the journey can go?\n\n"
         "Or do you want to start\nright away and plant\nyour own garden?",
    foreground=colors["dark"],
    background=colors["background"],
    font=("Courier New", 15),
    pady=15,
    master=frmGreeting
)
lblIntro.grid(row=1, pady=5, columnspan=2)

btnDummy = tk.Button(master=frmGreeting,
                     text="Dummy",
                     background=colors["highlight"],
                     foreground=colors["light"],
                     activebackground=colors["highlight"],
                     activeforeground=colors["light"],
                     font=("Courier New", 15, "bold"))
btnDummy.grid(row=2, column=0, padx=10, pady=15)
btnStart = tk.Button(master=frmGreeting,
                     text="New Habit",
                     background=colors["highlight"],
                     foreground=colors["light"],
                     activebackground=colors["highlight"],
                     activeforeground=colors["light"],
                     font=("Courier New", 15, "bold"))
btnStart.grid(row=2, column=1, padx=10, pady=15)

db = DatabaseConnector()
hab1 = Habit(db_connect=db, name="Tester Habit", periodicity=7, todo="Test something or other")
hab1.new_habit()
hab2 = Habit(db)
hab2.load_data(2)
hab2.print()
hab2.delete()

window.mainloop()
