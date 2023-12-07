import Menus.standard_menu_elements as elems


class WelcomeScreen(elems.HabitAppFrame):
    """
    To allow for a user to get a good overview of the software before committing to it, this menu offers them the
    choice of entering a preset garden or continuing to set up of their own.
    """

    def __init__(self, window, db_connect):
        """
        Initializes the welcome screen
        :param window: The parent tkinter window
        :param db_connect: The Database Connector connected to the database
        """

        self.window = window
        self.db_connect = db_connect

        elems.HabitAppFrame.__init__(self, window)

        self.pack()

        # Title

        title = elems.HabitAppTitle(master=self, text="Welcome, User!")
        title.grid(row=0, pady=10, padx=15, columnspan=2)

        # Greeting and Explanation

        lbl_intro = elems.HabitAppText(
            master=self,
            text="This is Grow Your Habits\nwhere we nurture our goals\nuntil they grow into healthy\nhabit plants!\n\n"
                 "It looks like this is\nyour first time with us.\n\n"
                 "Would you like to visit\na pre-grown garden to see\nwhere the journey can go?\n\n"
                 "Or do you want to start\nright away and plant\nyour own garden?"
        )
        lbl_intro.grid(row=1, pady=15, columnspan=2)

        # Buttons for choosing preset or own start

        btn_load_dummy = elems.HabitAppButton(self, "Pre-Grown", lambda: self.load_dummy())
        btn_load_dummy.grid(row=2, column=0, padx=10, pady=15)

        btn_start_new = elems.HabitAppButton(self, "My Own Garden", lambda: self.load_new_management())
        btn_start_new.grid(row=2, column=1, padx=10, pady=15)

        self.window.eval('tk::PlaceWindow . center')
        self.tkraise()

    def load_dummy(self):
        """
        This button loads the dummy data provided by the attached .csv files into the database and then
        takes the user to the main menu, which should now display a number of preset habits.
        """

        from Menus.main_menu import MainMenu

        self.db_connect.insert_dummy()
        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect)

    def load_new_management(self):
        """
        This button initializes an empty habit database and takes the user to the habit management menu
        where they can set up their first habit.
        """

        from Menus.habit_management import HabitManagement

        self.grid_forget()
        self.destroy()

        HabitManagement(self.window, self.db_connect)
