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

        # Markov Chain
        self.markovChainIndex = self.generate_markov_chain_index()
        self.markovChain = self.generate_markov_chain()

        # Points
        self.score = (0, 0)
        self.pointProgression = [0, 15, 30, 40, ("Hold", "Break")]
        self.winner = None

    def simulate_tiebreak(self):
        """
        Method:
            simulates the tiebreak using monte carlo
        """
        # Initialising variables
        pointNumber = 0
        server = self.server
        returner = self.returner
        servingPlayer = self.server
        returningPlayer = self.returner

        # Simulate game
        while True:

            # Swapping server and returner
            if pointNumber % 2 == 1:
                returnerTemp = returner
                serverTemp = server
                server = returnerTemp
                returner = serverTemp
                
                servingPlayerTemp = servingPlayer
                returningPlayerTemp = returningPlayer
                servingPlayer = returningPlayerTemp
                returningPlayer = servingPlayerTemp

            # Simulate point
            sWin = (server.serveStrength * server.form) / (server.serveStrength * server.form
                    + returner.returnStrength * returner.form)
            
            randFloat = np.random.uniform(0,1)
            
            if randFloat <= sWin:
                
            
            
            # increment point number
            pointNumber += 1
