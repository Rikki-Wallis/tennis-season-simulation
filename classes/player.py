# Imports
import numpy as np
import random

class Player:

    def __init__(self, name):
        """
        Method:
            init method where serve, return and form multipliers are assigned random values

        Params:
            name (str): The name of the player
        """
        # Player Identity
        self.name = name

        # Player attributes
        self.serveStrength = 58 * np.random.normal( loc=1.0, scale=0.2 )  # Tour average of service points won is 58%
        self.returnStrength = 42 * np.random.normal( loc=1.0, scale=0.2 )  # Tour average of return points won is 42%
        self.form = np.random.normal(loc=1.0, scale=0.2)
        
        # Manage injuries
        self.fitness = 1.0
        self.injuryRisk = 0.0
        self.injuryThreshold = np.random.normal(loc=0.6, scale=0.1)
        self.injuryProbability = np.random.normal(loc=0.2, scale=0.1)
        self.isInjured = False
        self.noInjured = 0

        # Player stats
        self.ranking = 0
        self.rankingPoints = 0

    def increment_points(self, points):
        """
        Method:
            Increments the players ranking points by given points

        Params:
            points (int): The amount of points to increment by
        """
        self.rankingPoints += points
    
    def update_fitness(self, matchRisk):
        """
        Method:
            Updates the fitness and injury attributes of the player
        
        Params:
            matchRisk (float): The risk associated with playing a match
        """
        # If match risk is negative we should reduce injury risk instead of increase
        if matchRisk < 0:
            self.injuryRisk += matchRisk
            self.fitness -= 1+matchRisk
        # Otherwise increase injury risk and update fitness
        else:
            self.injuryRisk += matchRisk
            self.fitness = max(0, 1-self.injuryRisk)
    
    def check_injury(self):
        """
        Method:
            Checks if the player has passed their injury threshold and draw a random value
            to assign if they are injured.
        """
        if self.injuryRisk >= self.injuryThreshold and random.random() < self.injuryProbability:
            self.isInjured = True
