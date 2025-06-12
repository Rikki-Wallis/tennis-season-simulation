# Imports
import numpy as np


class Player:
    # Ensure each new player has a unique ID
    idCounter = 0

    def __init__(
        self,
        name,
        serveStrength,
        returnStrength,
        form,
        hardStrength,
        clayStrength,
        grassStrength,
    ):
        """
        Method:
            init method with adjustable parameters for serve, return strength and form.

        Params:
            name (str):               The name of the player
            serveStrength (float):    A multiplier for the players serve effectiveness
            returnStrength (float):   A multiplier for the players return effectiveness
            form (float):             A multiplier for the players current form
            hardStrength (float):     A multiplier for the players strength on hard courts
            clayStrength (float):     A multiplier for the players strength on clay courts
            grassStrength (float):    A multiplier for the players strength on grass courts
        """
        # Player identity
        self.name = name
        self.playerID = Player.idCounter

        # Player attributes
        self.serveStrength = (
            58 * serveStrength
        )  # Tour average of service points won is 58%
        self.returnStrength = (
            42 * returnStrength
        )  # Tour average of return points won is 42%
        self.form = form
        self.hardStrength = hardStrength
        self.clayStrength = clayStrength
        self.grassStrength = grassStrength

        # Player Stats
        self.gamesPlayer = 0
        self.tournamentsWon = {
            "Grand Slam": 0,
            "ATP Final": 0,
            "Master 1000": 0,
            "ATP 500": 0,
            "ATP 250": 0,
        }

        # Increment ID counter to ensure every player has a unique ID
        Player.idCounter += 1

    def __init__(self, name):
        """
        Method:
            init method where serve, return and form multipliers are assigned random values

        Params:
            name (str): The name of the player
        """
        # Player Identity
        self.name = name
        self.playerID = Player.idCounter

        # Player attributes
        self.serveStrength = 58 * np.random.normal(
            loc=1.0, scale=0.2
        )  # Tour average of service points won is 58%
        self.returnStrength = 42 * np.random.normal(
            loc=1.0, scale=0.2
        )  # Tour average of return points won is 42%
        self.form = np.random.normal(loc=1.0, scale=1)
        self.hardStrength = np.random.normal(loc=1.0, scale=1)
        self.clayStrength = np.random.normal(loc=1.0, scale=1)
        self.grassStrength = np.random.normal(loc=1.0, scale=1)

        # Player stats
        self.gamesPlayed = 0
        self.tournamentsWon = {
            "Grand Slam": 0,
            "ATP Final": 0,
            "Master 1000": 0,
            "ATP 500": 0,
            "ATP 250": 0,
        }
        self.rankingPoints = 0

        # Increment ID counter to ensure every player has a unique ID
        Player.idCounter += 1

    def increment_tournament_win(self, tournamentType):
        """
        Method:
            Increments the type of tournament the player won

        Params:
            tournamentType (str): The type of tournament won e.g. ATP 500
        """
        self.tournamentsWon[tournamentType] += 1

    def increment_points(self, points):
        """
        Method:
            Increments the players ranking points by given points

        Params:
            points (int): The amount of points to increment by
        """
        self.rankingPoints += points

    def increment_games_played(self):
        """
        Method:
            Increments the gamesPlayed attribute
        """
        self.gamesPlayed += 1
