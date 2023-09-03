import tkinter as tk
import tkinter.messagebox
from habit import Habit
import habit_analytics as hana
import Menus.standard_menu_elements as elems


class HabitManagement(elems.HabitAppFrame):
    """
    This menu provides the user with functionalities to create and delete habits
    as well as clearing the entire database, should they wish to return to a clean slate.
    """

    def __init__(self, window, db_connect):
        """
        Initializes the habit management menu
        :param window: The parent tkinter window
        :param db_connect: The Database Connector connected to the database
        """

        self.window = window
        self.db_connect = db_connect

        elems.HabitAppFrame.__init__(self, self.window)

        self.pack()

        # Title

        lbl_mm_title = elems.HabitAppTitle(self, "Habit Management")
        lbl_mm_title.grid(row=0, pady=10, padx=15, columnspan=2)

        habit_ids = db_connect.load_all_habit_ids()

        # Preparation of the necessary variables for selection and input

        self.period_chosen = tk.StringVar()
        self.period_chosen.set("D")
        self.period_custom = tk.StringVar()
        self.period_custom.set("0")
        self.new_name = tk.StringVar()
        self.new_name.set("")
        self.new_description = tk.StringVar()
        self.new_description.set("")

        # Habit Creation

        lbl_add_habit = elems.HabitAppText(self, "To add a habit, \nfill in the following information:")
        lbl_add_habit.grid(row=1, pady=(10, 0), columnspan=2)

        frm_name = elems.HabitAppFrame(self)
        lbl_name = elems.HabitAppText(frm_name, "Name:")
        txt_name = elems.HabitAppEntry(frm_name, 20, self.new_name)
        lbl_name.grid(row=2, padx=20, column=0)
        txt_name.grid(row=2, padx=20, column=1)
        frm_name.grid(row=2, pady=(15, 0), columnspan=2)

        frm_period_choice = elems.HabitAppFrame(self)

        # Habit Periodicity

        lbl_periodicity = elems.HabitAppText(frm_period_choice, "How often do\nyou want to\nperform\nthis habit?")
        lbl_periodicity.grid(row=0, column=0, padx=(10, 30))

        frm_period_options = elems.HabitAppFrame(frm_period_choice)

        rb_daily = elems.HabitAppRadio(frm_period_options, "D", self.period_chosen)
        rb_daily.grid(row=0, column=0)
        rb_daily.select()
        rb_weekly = elems.HabitAppRadio(frm_period_options, "W", self.period_chosen)
        rb_weekly.grid(row=1, column=0)
        rb_custom = elems.HabitAppRadio(frm_period_options, "C", self.period_chosen)
        rb_custom.grid(row=2, column=0)
        lbl_daily = elems.HabitAppText(frm_period_options, "Daily")
        lbl_daily.grid(row=0, padx=(5, 20), column=1, sticky="w")
        lbl_weekly = elems.HabitAppText(frm_period_options, "Weekly")
        lbl_weekly.grid(row=1, padx=(5, 20), column=1, sticky="w")

        frm_custom_entry = elems.HabitAppFrame(frm_period_options)
        lbl_custom_front = elems.HabitAppText(frm_custom_entry, "Every")
        lbl_custom_front.grid(row=0, column=0)
        txt_custom = elems.HabitAppEntry(frm_custom_entry, 4, self.period_custom)
        txt_custom.grid(row=0, padx=5, column=1)
        lbl_custom_back = elems.HabitAppText(frm_custom_entry, "Days")
        lbl_custom_back.grid(row=0, column=2)

        frm_custom_entry.grid(row=2, padx=(5, 20), column=1, sticky="w")

        frm_period_options.grid(row=0, column=1)

        frm_period_choice.grid(row=3, pady=(15, 0), columnspan=2)

        # Habit Description

        lbl_description = elems.HabitAppText(self, "What does this habit entail?")
        lbl_description.grid(row=4, pady=(15, 0), columnspan=2)
        txt_description = elems.HabitAppEntry(self, 34, self.new_description)
        txt_description.grid(row=5, columnspan=2)

        btn_add_habit = elems.HabitAppButton(self, "Add Habit", lambda: self.add_habit_button())
        btn_add_habit.grid(row=6, columnspan=2, pady=(15, 0), padx=10)

        # Habit Deletion, if at least one habit is in the database

        if len(habit_ids) > 0:

            lbl_line = elems.HabitAppText(self, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            lbl_line.grid(row=7, columnspan=2, pady=(10, 0))

            habit_list = hana.list_all_habits(db_connect)

            self.selected_habit = tk.StringVar(self.window)
            self.selected_habit.set("Select a Habit")

            lbl_delete_habit = elems.HabitAppText(self, "To delete a habit,\nchoose it from the dropdown menu:")
            lbl_delete_habit.grid(row=8, padx=10, columnspan=2)

            frm_delete = elems.HabitAppFrame(self)

            opt_habit_list = elems.HabitAppDropdown(frm_delete, self.selected_habit, habit_list)
            opt_habit_list.grid(row=0, column=0, pady=10, padx=10)

            btn_delete_habit = elems.HabitAppButton(frm_delete, "Delete", lambda: self.delete_habit())
            btn_delete_habit.grid(row=0, column=1, pady=10, padx=15)

            frm_delete.grid(row=9, columnspan=2, pady=10)

        # Database reset and return buttons

        lbl_line2 = elems.HabitAppText(self, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        lbl_line2.grid(row=10, columnspan=2)

        btn_reset_database = elems.HabitAppButton(self, "Reset Database", lambda: self.reset_database_button())
        btn_reset_database.grid(row=11, pady=(10, 20), padx=20, column=1, sticky="e")

        btn_go_back = elems.HabitAppButton(self, "Back", lambda: self.go_back_button())
        btn_go_back.grid(row=11, pady=(10, 20), padx=20, column=0, sticky="w")

        self.window.eval('tk::PlaceWindow . center')
        self.tkraise()

    def add_habit_button(self):
        """
        This buttons checks whether the user has provided all data needed to set up a habit in the database.
        If all information is provided, the habit is added and the frame cleared.
        """

        # Checking input for obvious errors

        if self.new_name.get() == "":
            tk.messagebox.showerror("No Name", "You have not provided a name for your new habit.\n" +
                                    "Please enter one in the provided field.")
            return
        elif len(self.new_name.get()) > 20:
            tk.messagebox.showerror("Name too long", "The name you've chosen for your habit is a bit too long.\n" +
                                    "Try to be more precise and keep it within 20 characters.\n" +
                                    "Habits work best when they're clear and not too convoluted. " +
                                    "Maybe you can break it down into smaller steps? :)")
            return
        if self.new_description.get() == "":
            tk.messagebox.showerror("No Description", "You have not described your new habit.\n" +
                                    "Please add a description in the provided field.")
            return
        if self.period_chosen.get() == "C":
            if self.period_custom.get() == "0":
                tk.messagebox.showerror("No Periodicity", "You have chosen a custom periodicity for your new habit, " +
                                        "but haven't provided a day count.\n" +
                                        "Please enter one in the provided field or choose 'Daily' or 'Weekly'.")
                return
            elif not str.isnumeric(self.period_custom.get()):
                tk.messagebox.showerror("No Number", "You have chosen a custom periodicity for your new habit, " +
                                        "but haven't entered a valid number for your day count." +
                                        "This is most likely due to you entering letters, or special characters." +
                                        "Non-natural numbers like 4.5, pi or -4 are also not good numbers " +
                                        "to set for watering your habit plants.\n" +
                                        "Please check your entry for any rogue characters.")
                return

        # Translate the chosen periodicity

        periodicity = 0

        match self.period_chosen.get():
            case "D":
                periodicity = 1
            case "W":
                periodicity = 7
            case "C":
                periodicity = int(self.period_custom.get())

        hab = Habit(self.db_connect,
                    name=self.new_name.get(),
                    periodicity=periodicity,
                    description=self.new_description.get()
                    )

        # To avoid habit confusion the user can't add two of the same name to the database.

        if hab.name in hana.list_all_habits(self.db_connect):
            tk.messagebox.showerror("Duplicate Habit", "You already planted a habit of this name, " +
                                    "please choose a different name for your new habit.\n")
            return

        # If everything has worked as intended, the habit is added to the database and the frame cleared.

        hab.new_habit()

        self.grid_forget()
        self.destroy()

        HabitManagement(self.window, self.db_connect)

    def reset_database_button(self):
        """
        This buttons resets the entire database and sends the user back to the welcome screen.
        """

        from Menus.welcome_screen import WelcomeScreen

        self.db_connect.reset_database()

        self.grid_forget()
        self.destroy()

        WelcomeScreen(self.window, self.db_connect)

    def go_back_button(self):
        """
        If there is at least one habit set up, this button takes the user to the main menu from which all other
        functions of the application can be accessed.
        """

        if len(self.db_connect.load_all_habit_ids()) == 0:
            tk.messagebox.showerror("No Habits", "You haven't set up a habit yet,\n" +
                                    "so there is no habit patch for you to get back to.\n" +
                                    "Plant a habit first, then you can go explore!")
            return

        from Menus.main_menu import MainMenu

        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect)

    def delete_habit(self):
        """
        If the user has selected a habit in the dropdown menu, the habit is removed from the database
        and the frame reloaded to now no longer include the habit.
        """

        habit_id = self.db_connect.find_habit_id(self.selected_habit.get())

        if habit_id > 0:
            self.db_connect.delete_habit(habit_id)

        self.grid_forget()
        self.destroy()

        HabitManagement(self.window, self.db_connect)
