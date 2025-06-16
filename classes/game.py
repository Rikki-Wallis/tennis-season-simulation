# Imports
import numpy as np


class Game:
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

        # Markov Chain
        self.markovChainIndex = self.generate_markov_chain_index()
        self.markovChain = self.generate_markov_chain()

        # Points
        self.score = (0, 0)
        self.pointProgression = [0, 15, 30, 40, ("Hold", "Break")]
        self.winner = None

    def simulate_game(self):
        """
        Method:
            Simulates the game
        """
        # Get index of initial transition value of markov chain to the absorption value
        startIndex = self.markovChainIndex["0-0"]
        holdIndex = self.markovChainIndex["Hold"]
        
        # Find the fundemental matrix of the Markov Chain
        B, transient_indices, absorbing_indices = self.compute_absorption_probabilities(self.markovChain)

        # Fetch the win percentage of server holding their game from the fundemental matrix
        start_i = np.where(transient_indices == startIndex)[0][0]
        hold_j = np.where(absorbing_indices == holdIndex)[0][0]
        sWin = B[start_i, hold_j]

        # Monte Carlo to draw the winner of the game
        if np.random.uniform(0,1) <= sWin:
            self.winner = self.server
        else:
            self.winner = self.returner


    def compute_absorption_probabilities(self, P):
        """
        Compute the absorption probabilities for a Markov chain with absorbing states.
        
        Args:
            P (np.ndarray): Transition matrix with absorbing states at the end.

        Returns:
            B (np.ndarray): Matrix of absorption probabilities where B[i, j] is the probability
                            of ending in absorbing state j from transient state i.
        """
        n = P.shape[0]

        # Identify absorbing states
        absorbing = np.isclose(P, np.eye(n)).all(axis=1)

        # Partition the matrix into Q and R
        transient_indices = np.where(~absorbing)[0]
        absorbing_indices = np.where(absorbing)[0]

        Q = P[np.ix_(transient_indices, transient_indices)]
        R = P[np.ix_(transient_indices, absorbing_indices)]

        # Fundamental matrix
        I = np.eye(Q.shape[0])
        N = np.linalg.inv(I - Q)

        # Absorption probabilities
        B = N @ R

        return B, transient_indices, absorbing_indices

    def generate_markov_chain(self):
        """
        Method:
            Generates a markov chain of the point transitions of the game.
            Calculates probability of server winning the point based off of both
            the server and returners personal attributes. For simplicity deuce is
            simplified to 30-30 as they are essentially the same thing.

        Return:
            markovChain (np.ndarray): The generated markov chain
        """
        # Obtaining probability that server will win each point based on player attributes
        sWin = (self.server.serveStrength * self.server.form) / (self.server.serveStrength * self.server.form + self.returner.returnStrength * self.returner.form )

        # The probability that the returner will win the point is just the compliment of the server's probability
        rWin = 1 - sWin

        # Creating Markov chain
        markovChain = np.array(
            [  # 0-0   15-0    30-0    40-0    0-15    0-30    0-40    15-15   30-15   40-15   15-30   15-40   30-30   40-30   30-40   Hold    Break
                [0,     sWin,    0,      0,    rWin,     0,     0,       0,      0,      0,      0,      0,      0,      0,      0,      0,      0],  # 0-0
                [0,     0,     sWin,     0,      0,      0,     0,       rWin,   0,      0,      0,      0,      0,      0,      0,      0,      0],  # 15-0
                [0,     0,       0,    sWin,     0,      0,     0,       0,      rWin,   0,      0,      0,      0,      0,      0,      0,      0],  # 30-0
                [0,     0,       0,      0,      0,      0,     0,       0,      0,    rWin,     0,      0,      0,      0,      0,    sWin,     0],  # 40-0
                [0,     0,       0,      0,      0,    rWin,    0,      sWin,    0,      0,      0,      0,      0,      0,      0,      0,      0],  # 0-15
                [0,     0,       0,      0,      0,      0,    rWin,     0,      0,      0,    sWin,     0,      0,      0,      0,      0,      0],  # 0-30
                [0,     0,       0,      0,      0,      0,     0,       0,      0,      0,      0,    sWin,     0,      0,      0,      0,   rWin],  # 0-40
                [0,     0,       0,      0,      0,      0,     0,       0,     sWin,    0,    rWin,     0,      0,      0,      0,      0,      0],  # 15-15
                [0,     0,       0,      0,      0,      0,     0,       0,      0,     sWin,    0,      0,     rWin,    0,      0,      0,      0],  # 30-15
                [0,     0,       0,      0,      0,      0,     0,       0,      0,      0,      0,      0,      0,     rWin,    0,     sWin,    0],  # 40-15
                [0,     0,       0,      0,      0,      0,     0,       0,      0,      0,      0,     rWin,   sWin,    0,      0,      0,      0],  # 15-30
                [0,     0,       0,      0,      0,      0,     0,       0,      0,      0,      0,      0,      0,      0,     sWin,    0,   rWin],  # 15-40
                [0,     0,       0,      0,      0,      0,     0,       0,      0,      0,      0,      0,      0,     sWin,   rWin,    0,      0],  # 30-30
                [0,     0,       0,      0,      0,      0,     0,       0,      0,      0,      0,      0,     rWin,    0,      0,     sWin,    0],  # 40-30 (A-40)
                [0,     0,       0,      0,      0,      0,     0,       0,      0,      0,      0,      0,     sWin,    0,      0,      0,   rWin],  # 30-40 (40-A)
                [0,     0,       0,      0,      0,      0,     0,       0,      0,      0,      0,      0,      0,      0,      0,      1,     0 ],  # Hold
                [0,     0,       0,      0,      0,      0,     0,       0,      0,      0,      0,      0,      0,      0,      0,      0,     1 ],  # Break
            ]
        )

        return markovChain
    
    def generate_markov_chain_index(self):
            """
            Method:
                Returns a dictionary of the indexes for the markov
                chain given a score

            Return:
                markovIndexes (dict)
            """
            return {
                "0-0": 0,
                "15-0": 1,
                "30-0": 2,
                "40-0": 3,
                "0-15": 4,
                "0-30": 5,
                "0-40": 6,
                "15-15": 7,
                "30-15": 8,
                "40-15": 9,
                "15-30": 10,
                "15-40": 11,
                "30-30": 12,
                "40-30": 13,
                "30-40": 14,
                "Hold": 15,
                "Break": 16,
            }