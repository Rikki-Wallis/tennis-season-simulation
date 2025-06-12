# Imports
from game import Game
from tiebreak import Tiebreak

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
        self.server = startingServer
        self.returner = startingReturner
        self.score = [0, 0]
        self.winner = None

    def simulate_set(self):
        """
        Method:
            Simulates a set and updates the winner

        Return:
            nextServer (tuple(Player)): the player that serves next idx 0 & returner at idx 1
        """
        # Initiating game list
        self.gameList = []

        # Simulating the set
        while self.winner == None:
            # Creating game object
            game = Game(self.server, self.returner)

            # Simulate the game
            game.simulate_game()

            # Getting winner and updating score
            winner = game.winner
            if winner == self.server:
                self.score[0] += 1
            else:
                self.score[1] += 1

            # If the set has a game score that wins at 6 games
            if max(self.score) == 6 and (self.score != (6, 6) or self.score != (6, 5) or self.score != (5,6)):
                # Updating the set win for the right player
                if self.score[0] == 6:
                    self.winner = self.server
                else:
                    self.winner = self.returner

            # If the game score is 7-5 we should select winner appropriatly
            elif self.score == (7, 5):
                self.winner = self.server
            elif self.score == (5, 7):
                self.winner = self.returner 

            # If it is a tiebreak simulate accordingly
            elif self.score == (6, 6):
                # Simulate tiebreak
                tiebreak = Tiebreak(self.server, self.returner)
                tiebreak.simulate_tiebreak()
                
                # Update winner and score
                if tiebreak.winner == self.server:
                    self.score[0] += 1
                else:
                    self.score[1] += 1
                
                self.winner = tiebreak.winner

            # swap server and return and update score to match
            self.server, self.returner = self.returner, self.server
            
            self.score = [self.score[1], self.score[0]]
                
        return (self.server, self.returner)
