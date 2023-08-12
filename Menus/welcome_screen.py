import tkinter as tk


class WelcomeScreen(tk.Frame):

    def __init__(self, window, db_connect, colors):
        tk.Frame.__init__(self, window, background=colors["background"])
        self.window = window
        self.db_connect = db_connect
        self.colors = colors
        self.grid(row=0, column=0, sticky="nsew")

        title = tk.Label(
            text="Welcome, User!",
            foreground=colors["dark"],
            background=colors["background"],
            font=("Courier New", 30, "bold"),
            master=self
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
            master=self
        )
        lbl_intro.grid(row=1, columnspan=2)

        btn_load_dummy = tk.Button(master=self,
                                   text="Dummy",
                                   background=colors["highlight"],
                                   foreground=colors["light"],
                                   activebackground=colors["highlight"],
                                   activeforeground=colors["light"],
                                   font=("Courier New", 15, "bold"),
                                   command=lambda: self.load_dummy()
                                   )
        btn_load_dummy.grid(row=2, column=0, padx=10, pady=15)
        btn_start_new = tk.Button(master=self,
                                  text="New Habit",
                                  background=colors["highlight"],
                                  foreground=colors["light"],
                                  activebackground=colors["highlight"],
                                  activeforeground=colors["light"],
                                  font=("Courier New", 15, "bold"))
        btn_start_new.grid(row=2, column=1, padx=10, pady=15)

        self.tkraise()

    def load_dummy(self):

        from Menus.main_menu import MainMenu

        self.db_connect.insert_dummy()
        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect, self.colors)
