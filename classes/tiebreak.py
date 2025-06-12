"""
Imports
"""

import numpy as np


class Tiebreak:
    def __init__(self, server, returner):
        """
        Method:
            init method for Game class

        Params:
            server (Player):   The player that is serving in the game
            returner (Player): The player that is returning in the game
        """
        # Players
        self.server = server
        self.returner = returner

        # Points
        self.score = (0, 0)
        self.pointProgression = [0, 15, 30, 40, ("Hold", "Break")]
        self.winner = None

    def simulate_tiebreak(self):
        """
        Method:
            simulates the tiebreak using monte carlo technique
        """
        # Initialising variables
        pointNumber = 0
        server = self.server
        returner = self.returner

        # Simulate game
        while True:

            # Swapping server and returner
            if pointNumber % 2 == 1:
                returnerTemp = returner
                serverTemp = server
                server = returnerTemp
                returner = serverTemp

                # Swap score to display server first
                self.score = (self.score[1], self.score[0])

            # Simulate point
            sWin = (server.serveStrength * server.form) / (
                server.serveStrength * server.form
                + returner.returnStrength * returner.form
            )

            if np.random.uniform(0, 1) <= sWin:
                self.score[0] += 1
            else:
                self.score[1] += 1

            # Check if win is present (Assumes the first score is that of the current server)
            if (self.score[0] >= 7 or self.score[1] >= 7) and abs(
                self.score[0] - self.score[1]
            ) >= 2:
                # Update correct player
                if self.score[0] > self.score[1]:
                    self.winner = server
                else:
                    self.winner = returner

                # Break out of while loop
                break

            # increment point number
            pointNumber += 1
