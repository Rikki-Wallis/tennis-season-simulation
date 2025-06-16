# Imports
import numpy as np
from set import Set


class Match:
    def __init__(self, player1, player2, setFormat):
        """
        Method:
            init method for match class
        
        Params:
            player1 (Player) - One of the players participating in the match
            player2 (Player) - One of the players participating in the match
            setFormat (int) - The format of the set e.g. grand slams are 5 sets and other events are 3
        """
        # Match attributes
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.loser = None
        self.setTarget = 2 if setFormat == 3 else 3
        self.score = [0, 0]

        # Coin toss to see who starting server is
        coinToss = np.random.random_integers(low=1, high=2)
        self.startingServer = player1 if coinToss == 1 else player2
        self.startingReturner = player2 if coinToss == 1 else player1

    def simulate_match(self):
        """
        Method:
            Simulates the match using Monte Carlo
        """
        # Checking if any of the players is none and handle withdrawal
        if self.player1 is None:
            self.winner = self.player2
            self.loser = self.player1
            return None
        elif self.player2 is None:
            self.winner = self.player1
            self.loser = self.player2
            return None
        
        # If one of the players is injured, handle withdrawal
        if self.startingServer.isInjured:
            self.winner = self.startingReturner
            self.loser = self.startingServer
            return None
        elif self.startingReturner.isInjured:
            self.winner = self.startingReturner
            self.loser = self.startingServer
            return None
        
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
                self.loser = self.player2
                self.player1.form += 0.1
                self.player2.form -= 0.1

            elif self.score[1] == self.setTarget:
                self.winner = self.player2
                self.loser = self.player1
                self.player1.form -= 0.1
                self.player2.form += 0.1

    def increment_score(self, player):
        """
        Method:
            Increments the match score
        
        Params:
            player (Player) - The player whos score is being incremented
        """
        if player == self.player1:
            self.score[0] += 1
        else:
            self.score[1] += 1
