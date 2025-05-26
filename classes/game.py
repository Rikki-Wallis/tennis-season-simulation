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

    def simulate_point(self):
        """
        Method:
            Simulates a point between the two players based off of
            probabilities obtained from the Markov Chain, While the we
            find the probabilities of transition to each absorption state,
            this function will be used along with monte-carlo to verify
            the probabilities of both stochastic methods.

        Return:
            updatedScore (tuple(int|str,int|str)): The updated score after point simulation
        """
        # Fetching each players points
        serverPoints = self.score[0]
        returnerPoints = self.score[1]

        # Fetching target scores for both players
        serverTargetIndex = self.pointProgression.index(serverPoints) + 1
        returnerTargetIndex = self.pointProgression.index(returnerPoints) + 1
        serverTargetScore = self.pointProgression[serverTargetIndex]
        returnerTargetScore = self.pointProgression[returnerTargetIndex]

        # Checking whether the target score results in a hold or a break
        if serverTargetIndex == len(self.pointProgression) - 1:
            serverTargetScore = "Hold"
        elif returnerTargetIndex == len(self.pointProgression) - 1:
            returnerTargetScore = "Break"

        # Fetching probability that server wins the point
        currentMarkovIndex = self.markovChainIndex[
            self.format_score(serverPoints, returnerPoints)
        ]
        targetMarkovIndex = self.markovChainIndex[
            self.format_score(serverTargetScore, returnerPoints)
        ]
        serverProb = self.markovChainIndex[currentMarkovIndex, targetMarkovIndex]

        # Randomly sampling to see if server wins the point
        sample = np.random.uniform(low=0, high=1)

        # Updating score based on random sample
        if sample <= serverProb:
            updatedScore = (serverTargetScore, returnerPoints)
        else:
            updatedScore = (serverPoints, returnerTargetScore)

        # If the updated score results in deuce we need to set it to 30-30 so markov indexing works
        if updatedScore == (40, 40):
            updatedScore = (30, 30)

        return updatedScore

    def simulate_game(self):
        """
        Method:
            Simulates the game
        """
        while self.winner == None:
            # Simulate the point
            updatedScore = self.simulate_point()

            # If the game has a winner update to exit loop
            if "Hold" in updatedScore:
                self.winner = self.server
            elif "Break" in updatedScore:
                self.winner = self.returner

            # Update score
            self.score = updatedScore

    def generate_markov_chain(self):
        """
        Method:
            Generates a markov chain of the point transitions of the game.
            Calculates probability of server winning the point based off of both
            the server and returners personal attributes. For simplicity deuce is
            simplified to 30-30 as they are essentially the same thing.

        Return:
            markovChain (List(List(float))): The generated markov chain
        """
        # Obtaining probability that server will win each point based on player attributes
        sWin = (self.server.serveStrength * self.server.form) / (
            self.server.serveStrength * self.server.form
            + self.returner.returnStrength * self.returner.form
        )

        # The probability that the returner will win the point is just the compliment of the server's probability
        rWin = 1 - sWin

        # Creating Markov chain
        markovChain = np.array(
            [  # 0-0   15-0    30-0    40-0    0-15    0-30    0-40    15-15   30-15   40-15   15-30   15-40   30-30   40-30   30-40   Hold    Break
                [0, sWin, 0, 0, rWin, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0-0
                [0, 0, sWin, 0, 0, 0, 0, rWin, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 15-0
                [0, 0, 0, sWin, 0, 0, 0, 0, rWin, 0, 0, 0, 0, 0, 0, 0, 0],  # 30-0
                [0, 0, 0, 0, 0, 0, 0, 0, 0, rWin, 0, 0, 0, 0, 0, sWin, 0],  # 40-0
                [0, 0, 0, 0, 0, rWin, 0, sWin, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0-15
                [0, 0, 0, 0, 0, 0, rWin, 0, 0, 0, sWin, 0, 0, 0, 0, 0, 0],  # 0-30
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sWin, 0, 0, 0, 0, rWin],  # 0-40
                [0, 0, 0, 0, 0, 0, 0, 0, sWin, 0, rWin, 0, 0, 0, 0, 0, 0],  # 15-15
                [0, 0, 0, 0, 0, 0, 0, 0, 0, sWin, 0, 0, rWin, 0, 0, 0, 0],  # 30-15
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, rWin, 0, sWin, 0],  # 40-15
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, rWin, sWin, 0, 0, 0, 0],  # 15-30
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sWin, 0, rWin],  # 15-40
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sWin, rWin, 0, 0],  # 30-30
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    rWin,
                    0,
                    0,
                    sWin,
                    0,
                ],  # 40-30 (A-40)
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    sWin,
                    0,
                    0,
                    0,
                    rWin,
                ],  # 30-40 (40-A)
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # Hold
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # Break
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

    def format_score(self, score=None):
        """
        Method:
            Formats a score to a string

        Params:
            score (None|tuple(int|str, int|str)): The score that will be formatted. If none,
                                                  formats the game classes own score.

        Return:
            formattedScore (str): The formatted score
        """
        if score != None:
            return f"{score[0]}-{score[1]}"
        else:
            return f"{self.score[0]}-{self.score[1]}"
