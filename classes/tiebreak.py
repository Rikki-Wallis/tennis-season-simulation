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

    def generate_markov_chain():
        pass
