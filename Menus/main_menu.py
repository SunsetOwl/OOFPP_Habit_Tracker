from habit import Habit
import habit_analytics as hana
import Menus.standard_menu_elements as elems


class MainMenu(elems.HabitAppFrame):
    """
    When a user has set up a previous set of habits either via the dummy database or manually, this is the menu
    they're taken to when booting the software.
    It contains an overview of the current state of their habits and allows them to mark a habit as performed.
    Additionally, it links to the habit management and stats menus.
    """

    def __init__(self, window, db_connect, page=0):
        """
        Initializes the main menu
        :param window: The parent tkinter window
        :param db_connect: The Database Connector connected to the database
        :param page: The current page of habits the user is on (at most 5 habits per page)
        """

        self.window = window
        self.db_connect = db_connect
        self.page = page

        elems.HabitAppFrame.__init__(self, self.window)
        self.pack()
        self.grid_columnconfigure(0, minsize=200)
        self.grid_columnconfigure(1, minsize=40)

        # Title

        lbl_mm_title = elems.HabitAppTitle(self, "~ Your Garden ~")
        lbl_mm_title.grid(row=0, pady=10, padx=15, columnspan=4)

        # Loading the current page of habits into lists

        habit_list = hana.list_all_habits(db_connect)
        habit_ids = db_connect.load_all_habit_ids()

        page_list = []
        for i in [i+self.page*5 for i in range(0, 5)]:
            if i < len(habit_list):
                page_list.append(i)

        list_string = ""
        streaks_string = ""
        for i in page_list:
            if list_string != "":
                list_string += "\n"
                streaks_string += "\n"
            list_string += habit_list[i]
            streaks_string += str(hana.current_streak_length(db_connect, habit_ids[i]))

        # Setting up the labels that will contain and display the list items

        habit_labels = []
        streak_labels = []
        perform_buttons = []
        plant_icons = []

        row = 1

        for i in page_list:

            habit_labels.append(elems.HabitAppText(self, habit_list[i]))
            habit_labels[row-1].grid(row=row, pady=10, padx=10, column=0)

            streak_label = str(hana.current_streak_length(db_connect, habit_ids[i]))
            streak_labels.append(elems.HabitAppText(self, streak_label))
            streak_labels[row-1].grid(row=row, pady=10, padx=10, column=1)

            plant_icons.append(elems.HabitPlant(self, hana.current_streak_length(db_connect, habit_ids[i])))
            plant_icons[row - 1].grid(row=row, pady=10, padx=10, column=2)

            perform_buttons.append(elems.HabitAppButton(self, "Water",
                                                        lambda i=i: self.perform_habit_button(habit_ids[i])))
            perform_buttons[row-1].grid(row=row, pady=5, padx=10, column=3)

            row += 1

        # Set up the Buttons for previous/next page when dealing with more than 5 habits

        frm_back_next = elems.HabitAppFrame(self)

        if page > 0:
            btn_previous = elems.HabitAppButton(frm_back_next, "<", lambda: self.previous_page())
            btn_previous.grid(row=0, padx=15, column=1)
        if len(habit_list) > page_list[-1]+1:
            btn_next = elems.HabitAppButton(frm_back_next, ">", lambda: self.next_page())
            btn_next.grid(row=0, padx=15, column=2)
        frm_back_next.grid(row=6, pady=10, columnspan=4)

        # Set up the Buttons to go to the other menus

        btn_habit_management = elems.HabitAppButton(self, "Habit Management", lambda: self.habit_mgmt_button())
        btn_habit_management.grid(row=7, column=0, pady=20, padx=15, columnspan=3, sticky="w")

        btn_insights = elems.HabitAppButton(self, "Stats", lambda: self.stats_button())
        btn_insights.grid(row=7, column=3, pady=20, padx=15, sticky="e")

        self.window.eval('tk::PlaceWindow . center')
        self.tkraise()

    def perform_habit_button(self, habit_id):
        """
        This buttons adds a check to the chosen habit and reloads the frame.
        """

        hab = Habit(self.db_connect)
        hab.load_data(habit_id)
        hab.perform()

        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect, self.page)

    def next_page(self):
        """
        This buttons reloads the frame on the next page (e.g. from going from habit 1-5 to 6-8)
        """

        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect, self.page+1)

    def previous_page(self):
        """
        This buttons reloads the frame on the previous page (e.g. from going from habit 6-8 to 1-5)
        """

        self.grid_forget()
        self.destroy()

        MainMenu(self.window, self.db_connect, self.page-1)

    def habit_mgmt_button(self):
        """
        This buttons takes the user to the habit management menu.
        """

        from Menus.habit_management import HabitManagement

        self.grid_forget()
        self.destroy()

        HabitManagement(self.window, self.db_connect)

    def stats_button(self):
        """
        This buttons takes the user to the stats menu.
        """

        from Menus.stats_menu import StatsMenu

        self.grid_forget()
        self.destroy()

        StatsMenu(self.window, self.db_connect)
