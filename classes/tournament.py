# Imports
import numpy as np
from match import Match


class Tournament:
    def __init__(self, courtType, name):
        self.courtType = courtType
        self.name = name

    def get_points_for_round(self, round):
        """
        Method:
            Returns the points associated for a given round

        Params:
            round (str): The given round

        Returns:
            roundPoints (int): The points associated with the round
        """
        return self.roundPoints[round]

    def generate_draw(self, players):
        """
        Method:
            Generates the draw for a tournament

        Params:
            players (List(Player)): The list of the players playing the tournament

        Returns:
            draw (List(Match)): A list that contains all the first round matches

        TODO: Create draw so that seeded pairings 1,2,3,4 are all on opposite sides
        """
        # Sort players in terms of rankings
        players = sorted(players, key=lambda player: player.rankingPoints, reverse=True)

        # Seperate seeded players and non seeded players
        seededPlayers = players[: (self.drawsize / 4)]
        nonSeededPlayers = players[(self.drawsize / 4) :]

        # Initial draw variables
        draw = []

        # Getting first matches for round 1 based off of seedings
        for match in range(self.drawsize / 2):
            # getting random players that are seeded and not seeded
            if len(seededPlayers) > 0:
                seededIndex = np.random.random_integers(low=0, high=len(seededPlayers))
                nonSeededIndex = np.random.random_integers(
                    low=0, high=len(nonSeededPlayers)
                )
            # Some matches will have two non seeded players playing eachother
            else:
                seededIndex = np.random.random_integers(
                    low=0, high=len(nonSeededPlayers)
                )
                nonSeededIndex = np.random.random_integers(
                    low=0, high=len(nonSeededPlayers)
                )

            # Appending them to the first round
            draw.append(
                Match(seededPlayers[seededIndex], nonSeededPlayers[nonSeededIndex])
            )

            # Deleting random players from their respective lists
            del seededPlayers[seededIndex]
            del nonSeededPlayers[nonSeededIndex]

        return draw


class GrandSlam(Tournament):
    def __init__(self, courtType):
        super.__init__(self, courtType)
        self.roundPoints = {
            "R1": 10,
            "R2": 50,
            "R3": 100,
            "R4": 200,
            "quarter final": 400,
            "semi final": 800,
            "finalist": 1300,
            "winner": 2000,
        }
        self.drawSize = 128


class Master1000(Tournament):
    def __init__(self, courtType):
        super.__init__(self, courtType)
        self.roundPoints = {
            "R1": 30,
            "R2": 50,
            "R3": 100,
            "quarter final": 200,
            "semi final": 400,
            "finalist": 650,
            "winner": 1000,
        }
        self.drawSize = 128


class ATP500(Tournament):
    def __init__(self, courtType):
        super.__init__(self, courtType)
        self.roundPoints = {
            "R1": 25,
            "R2": 50,
            "quarter final": 100,
            "semi final": 200,
            "finalist": 330,
            "winner": 500,
        }
        self.drawSize = 64


class ATP250(Tournament):
    def __init__(self, courtType):
        super.__init__(self, courtType)
        self.roundPoints = {
            "R1": 13,
            "R2": 25,
            "quarter final": 50,
            "semi final": 100,
            "finalist": 165,
            "winner": 250,
        }
        self.drawSize = 64
