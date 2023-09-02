import tkinter as tk
from database_connector import DatabaseConnector
from Menus.welcome_screen import WelcomeScreen
from Menus.main_menu import MainMenu
from Menus.settings import Settings

settings = Settings()

window = tk.Tk()
window.title("Habit Tracker")
window.configure(background=settings.colors["background"])
window.minsize(400, 500)
window.maxsize(400, 700)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

db_connect = DatabaseConnector()

if len(db_connect.load_all_habit_ids()) > 0:
    MainMenu(window, db_connect)
else:
    WelcomeScreen(window, db_connect)

window.mainloop()
