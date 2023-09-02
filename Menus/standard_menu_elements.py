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
                       font=(settings.font, 13)
                       )


class HabitAppEntry(tk.Entry):

    def __init__(self, master, width, entered):
        tk.Entry.__init__(self,
                          master=master,
                          background=settings.colors["entry"],
                          foreground=settings.colors["light"],
                          font=(settings.font, 13),
                          width=width,
                          textvariable=entered
                          )


class HabitAppRadio(tk.Radiobutton):

    def __init__(self, master, content, chosen):
        tk.Radiobutton.__init__(self,
                                master=master,
                                value=content,
                                variable=chosen,
                                background=settings.colors["background"],
                                activebackground=settings.colors["background"],
                                activeforeground=settings.colors["entry"]
                                )


class HabitAppFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master=master, background=settings.colors["background"])
