import tkinter as tk
from database_connector import DatabaseConnector
from Menus.welcome_screen import WelcomeScreen

colors = {"highlight": "#B6D274",
          "background": "#F2E8CF",
          "entry": "#F5F1E6",
          "light": "#5D8745",
          "dark": "#335C3B",
          "contrast": "#BC4749"}

window = tk.Tk()
window.title("Habit Tracker")
window.configure(background=colors["background"])
window.minsize(400, 500)
window.maxsize(400, 700)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

db_connect = DatabaseConnector()

WelcomeScreen(window, db_connect, colors)

window.mainloop()

# TODO Yeet

db_connect.delete_database()
