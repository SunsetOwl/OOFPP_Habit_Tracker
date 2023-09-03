class Settings:
    """
    This is a class containing settings for the application, so visual elements like colors or fonts can be changed
    in a central location instead of spread out across the different UI elements.
    """

    def __init__(self):
        """
        Initializes the application's settings
        """

        self.colors = {"highlight": "#B6D274",
                       "background": "#F2E8CF",
                       "entry": "#F5F1E6",
                       "light": "#5D8745",
                       "dark": "#335C3B",
                       "contrast": "#BC4749"
                       }
        self.font = "Courier New"
