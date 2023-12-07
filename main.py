import tkinter as tk
from database_connector import DatabaseConnector
from Menus.welcome_screen import WelcomeScreen
from Menus.main_menu import MainMenu
from Menus.settings import Settings

# This quick main file sets up the basic tkinter window that will contain all the frames encompassing the tracker

settings = Settings()

window = tk.Tk()
window.title("Grow Your Habits")
window.configure(background=settings.colors["background"])
window.minsize(400, 500)
window.maxsize(400, 700)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

# The database is loaded or the user send to the first time welcome screen, if no database is set up so far

db_connect = DatabaseConnector()

if len(db_connect.load_all_habit_ids()) > 0:
    MainMenu(window, db_connect)
else:
    WelcomeScreen(window, db_connect)

window.mainloop()
