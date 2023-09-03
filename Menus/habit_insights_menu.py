from habit import Habit
import habit_analytics as hana
import Menus.standard_menu_elements as elems
import tkinter as tk


class HabitInsightsMenu(elems.HabitAppFrame):

    def __init__(self, window, db_connect, habit_id):
        self.window = window
        self.db_connect = db_connect
        self.hab = Habit(db_connect, habit_id)

        elems.HabitAppFrame.__init__(self, self.window)
        self.pack()

        lbl_mm_title = elems.HabitAppTitle(self, "~ Your Stats ~")
        lbl_mm_title.grid(row=0, pady=10, padx=15)

        insights_text = "Habit: " + self.hab.name + "\n"

        match self.hab.periodicity:
            case 1:
                insights_text = insights_text + "Periodicity: Daily\n"
            case 7:
                insights_text = insights_text + "Periodicity: Weekly\n"
            case _:
                insights_text = insights_text + "Periodicity: Every " + str(self.hab.periodicity) + " Days\n"

        insights_text = insights_text + "Description:\n" + self.hab.description_with_line_breaks() + "\n"
        insights_text = insights_text + "Created on: " + self.hab.created.strftime("%d-%m-%Y") + "\n\n"

        insights_text = insights_text + "Current Streak: "
        insights_text = insights_text + str(hana.current_streak_length(self.db_connect, self.hab.habit_id)) + "\n"
        if hana.current_streak_length(self.db_connect, self.hab.habit_id) > 0:
            insights_text = insights_text + "First Day: "
            insights_text = insights_text + hana.current_streak_start(self.db_connect, self.hab.habit_id) + "\n"

        insights_text = insights_text + "\nLongest Streak: "
        insights_text = insights_text + str(hana.longest_streak_length(self.db_connect, self.hab.habit_id)) + "\n"
        if hana.longest_streak_length(self.db_connect, self.hab.habit_id) > 0:
            insights_text = insights_text + "First Day: "
            insights_text = insights_text + hana.longest_streak_dates(self.db_connect, self.hab.habit_id)[0] + "\n"
            insights_text = insights_text + "Last Day: "
            insights_text = insights_text + hana.longest_streak_dates(self.db_connect, self.hab.habit_id)[1] + "\n"

        lbl_stats = elems.HabitAppText(self, insights_text)
        lbl_stats.grid(row=1, pady=10, padx=15)

        btn_go_back = elems.HabitAppButton(self, "Back", lambda: self.go_back_button())
        btn_go_back.grid(row=4, pady=(10, 20), padx=20, sticky="w")

        self.window.eval('tk::PlaceWindow . center')
        self.tkraise()

    def go_back_button(self):

        from Menus.stats_menu import StatsMenu

        self.grid_forget()
        self.destroy()

        StatsMenu(self.window, self.db_connect)
