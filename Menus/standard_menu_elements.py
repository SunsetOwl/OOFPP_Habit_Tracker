import tkinter as tk
from Menus.settings import Settings
from PIL import ImageTk, Image

settings = Settings()

"""
In order to avoid having to redefine all elements making up the UI in regards to color, font or similar,
as well as to ensure consistency across the application, all common elements are set up as subclasses 
of their regular tkinter counterparts here instead.
"""


class HabitAppButton(tk.Button):

    def __init__(self, master, text, command):
        """
        Sets up the Button as an extension of the tkinter Button
        :param master: The Frame the element will be added to.
        :param text: The text to be displayed on the button.
        :param command: The command to be executed when the button is pressed.
        """

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
        """
        Sets up a general text Label as an extension of the tkinter Label
        :param master: The Frame the element will be added to.
        :param text: The text to be displayed by the label.
        """

        tk.Label.__init__(self,
                          master=master,
                          text=text,
                          foreground=settings.colors["dark"],
                          background=settings.colors["background"],
                          font=(settings.font, 14),
                          )


class HabitAppTitle(tk.Label):

    def __init__(self, master, text):
        """
        Sets up the Label for titles as an extension of the tkinter Label
        :param master: The Frame the element will be added to.
        :param text: The text to be displayed by the label.
        """

        tk.Label.__init__(self,
                          master=master,
                          text=text,
                          foreground=settings.colors["dark"],
                          background=settings.colors["background"],
                          font=(settings.font, 30, "bold"),
                          )


class HabitAppDropdown(tk.OptionMenu):

    def __init__(self, master, choice, choices):
        """
        Sets up a dropdown list as an extension of the tkinter OptionMenu
        :param master: The Frame the element will be added to.
        :param choice: The String variable that will store the chosen value.
        :param choices: The list of options.
        """

        tk.OptionMenu.__init__(self, master, choice, *choices)
        self.configure(background=settings.colors["entry"],
                       foreground=settings.colors["light"],
                       activebackground=settings.colors["entry"],
                       activeforeground=settings.colors["light"],
                       font=(settings.font, 13)
                       )


class HabitAppEntry(tk.Entry):

    def __init__(self, master, width, entered):
        """
        Sets up a textbox for entry by the user as an extension of the tkinter Entry box
        :param master: The Frame the element will be added to.
        :param width: The width of the textbox.
        :param entered: The String variable that will store the chosen value.
        """

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
        """
        Sets up a radiobutton as an extension of the tkinter Radiobutton
        :param master: The Frame the element will be added to.
        :param content: The String value that represents this box.
        :param chosen: The String variable that will store the chosen value.
        """

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
        """
        Sets up a general tkinter Frame in the right background color.
        :param master: The Frame the element will be added to.
        """
        tk.Frame.__init__(self, master=master, background=settings.colors["background"])


class HabitPlant(tk.Label):

    def __init__(self, master, days):
        """
        Sets up a tkinter Label containing the plant icon matching the user's current streak level.
        :param master: The Frame the element will be added to.
        :param days: The length of the user's current habit streak in days.
        """

        if days == 0:
            self.img_link = "Icons/0.png"
        elif days < 7:
            self.img_link = "Icons/1.png"
        elif days < 14:
            self.img_link = "Icons/7.png"
        elif days < 21:
            self.img_link = "Icons/14.png"
        elif days < 28:
            self.img_link = "Icons/21.png"
        else:
            self.img_link = "Icons/28.png"

        self.img = ImageTk.PhotoImage(Image.open(self.img_link))
        tk.Label.__init__(self, master=master, image=self.img, background=settings.colors["background"])
