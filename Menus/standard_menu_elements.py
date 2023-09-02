import tkinter as tk
from Menus.settings import Settings

settings = Settings()


class HabitAppButton(tk.Button):

    def __init__(self, master, text, command):

        tk.Button.__init__(self,
                           master=master,
                           text=text,
                           background=settings.colors["highlight"],
                           foreground=settings.colors["light"],
                           activebackground=settings.colors["highlight"],
                           activeforeground=settings.colors["light"],
                           font=(settings.font, 15, "bold"),
                           command=command
                           )


class HabitAppText(tk.Label):

    def __init__(self, master, text):

        tk.Label.__init__(self,
                          master=master,
                          text=text,
                          foreground=settings.colors["dark"],
                          background=settings.colors["background"],
                          font=(settings.font, 13),
                          )


class HabitAppTitle(tk.Label):

    def __init__(self, master, text):

        tk.Label.__init__(self,
                          master=master,
                          text=text,
                          foreground=settings.colors["dark"],
                          background=settings.colors["background"],
                          font=(settings.font, 30, "bold"),
                          )


class HabitAppDropdown(tk.OptionMenu):

    def __init__(self, master, choice, choices):
        tk.OptionMenu.__init__(self, master, choice, *choices)
        self.configure(background=settings.colors["entry"],
                       foreground=settings.colors["light"],
                       activebackground=settings.colors["entry"],
                       activeforeground=settings.colors["light"],
                       font=(settings.font, 15)
                       )