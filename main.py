import tkinter as tk
from datetime import datetime, timedelta
from habit import Habit
from connector import DatabaseConnector

window = tk.Tk()
frame = tk.Frame(master=window, width=500, height=800)
frame.pack()

title = tk.Label(
    text=datetime.today().day,
    background="#F0EAD2",
    master=frame
)
title.place(x=200, y=100)

db = DatabaseConnector()
hab1 = Habit(db_connect=db, name="Tester Habit", periodicity=7)
hab1.new_habit()
hab2 = Habit(db)
hab2.load_data(2)
hab2.print()
hab2.delete()

window.mainloop()
