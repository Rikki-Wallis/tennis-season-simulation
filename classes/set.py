# Imports
from game import Game


class Set:
    def __init__(self, startingServer, startingReturner):
        """
        Method:
            init method for set class, playerList will be used to determine
            who serves first and as such this will be decided in the match
            class.

        Params:
            startingServer (Player): The player that starts serving in the match
            startingReturner (Player): The player that starts returning in the match
        """
        self.player1 = startingServer
        self.player2 = startingReturner
        self.playersList = [self.player1, self.player2]
        self.score = {self.player1: 0, self.player2: 0}
        self.winner = None

    def simulate_set(self):
        """
        Method:
            Simulates a set and updates the winner

        Return:
            nextServer (tuple(Player)): the player that serves next idx 0 & returner at idx 1
        """
        # Setting server and returner index for playersList
        serverIndex = 0
        returnerIndex = 1
        # Initiating game list
        self.gameList = []

        # Simulating the set
        while self.winner == None:
            # Creating game object
            game = Game(self.playersList[serverIndex], self.playersList[returnerIndex])

            # Simulate the game
            game.simulate_game()

            # Tracking games
            self.gameList.append(game)

            # Getting winner and updating score
            gameWinner = game.winner
            self.score[gameWinner] += 1

            # If the set has a game score that wins at 6 games
            if max(self.score) == 6 and (self.score != (6, 6) or self.score != (6, 5)):
                # Updating the set win for the right player
                if self.score(0) == 6:
                    self.winner = self.player1
                else:
                    self.winner = self.player2

            # If the game score is 7-5 we should select winner appropriatly
            elif self.score == (7, 5) or self.score == (5, 7):
                # Updating winner
                if self.score[0] == 7:
                    self.winner = self.player1
                else:
                    self.winner = self.player2

            # If it is a tiebreak simulate accordingly
            elif self.score == (6, 6):
                """
                Figure out tiebreak class
                """

            else:
                pass

            serverIndex = 0 if serverIndex == 1 else 1
            returnerIndex = 0 if returnerIndex == 1 else 1

        return (self.playersList[serverIndex], self.playersList[returnerIndex])
