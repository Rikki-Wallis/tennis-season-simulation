# Imports
import numpy as np
from set import Set


class Match:
    def __init__(self, player1, player2, setFormat):
        # Match attributes
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.setTarget = 2 if setFormat == 3 else 3
        self.score = (0, 0)

        # Coin toss to see who starting server is
        coinToss = np.random.random_integers(low=1, high=2)
        self.startingServer = player1 if coinToss == 1 else player2
        self.startingReturner = player2 if coinToss == 1 else player1

    def simulate_match(self):
        # Initiating starting server and returner
        playerList = [self.startingServer, self.startingReturner]

        # Play sets until there is a winner of the match
        while self.winner == None:
            # Initiate current set
            currentSet = Set(playerList[0], playerList[1])

            # Simulating the set
            playerList = currentSet.simulate_set()

            # Incrementing score
            self.increment_score(currentSet.winner)

            # Checking if there is a winner
            if self.score[0] == self.setTarget:
                self.winner = self.player1
            elif self.score[1] == self.setTarget:
                self.winner = self.player2

    def increment_score(self, player):
        if player == self.player1:
            self.score[0] += 1
        else:
            self.score[1] += 1
