# Imports
import numpy as np
from match import Match

class Tournament:
    def __init__(self, courtType, name):
        """
        Method:
            init method for the Tournament class
        
        Params:
            courtType (str)
            name (str)
        """
        self.courtType = courtType
        self.name = name
        
        # Default match risk for 3 set tournaments
        self.matchRisk = 0.03


    def add_set_format(self, setFormat):
        """
        Method:
            setter method for setFormat attribute
        
        Params:
            setFormat (int)
        """
        self.setFormat = setFormat
        
        
    def generate_draw(self, players):
        """
        Method:
            Generates the draw for a tournament

        Params:
            players (List(Player)): The list of the players playing the tournament

        Returns:
            draw (List(List(Match))): A list that contains all rounds of the tournament
        """
        # Sort players in terms of rankings
        players = sorted(players, key=lambda player: player.rankingPoints, reverse=True)

        # Seperate seeded players and non seeded players
        seededPlayers = players[: (self.drawSize // 4)]
        nonSeededPlayers = players[(self.drawSize // 4) :]

        # Initial draw variables
        self.draw = []
        round1 = []

        # Getting first matches for round 1 based off of seedings
        for match in range(self.drawSize // 2):
            
            # Check if we have enough players to add to round 1
            if len(seededPlayers) == 0 and len(nonSeededPlayers) < 2:
                # Not enough players left for a match
                round1.append(Match(None, None, self.setFormat))
            
            # Otherwise check if there are still seeded players to be given a match
            elif len(seededPlayers) > 0 and len(nonSeededPlayers) > 0:
                # Get random index of a seeded player and a non seeded one
                seededIndex = np.random.randint(low=0, high=len(seededPlayers))
                nonSeededIndex = np.random.randint(low=0, high=len(nonSeededPlayers))
                
                # Add them to round 1 matches
                round1.append(Match(seededPlayers[seededIndex], nonSeededPlayers[nonSeededIndex], self.setFormat))
                
                # Delete both players from list to avoid duplicate matches
                del seededPlayers[seededIndex]
                del nonSeededPlayers[nonSeededIndex]
        
            # If there are no seeded players left make sure we have enough non seeded players to create a match
            elif len(nonSeededPlayers) >= 2:
                # Only non-seeded players left, need at least 2 for a match
                seededIndex = np.random.randint(low=0, high=len(nonSeededPlayers))
                
                # Make sure we don't pick the same player twice
                remaining_indices = [i for i in range(len(nonSeededPlayers)) if i != seededIndex]
                nonSeededIndex = np.random.choice(remaining_indices)
                
                # Append match to round 1
                round1.append(Match(nonSeededPlayers[seededIndex], nonSeededPlayers[nonSeededIndex], self.setFormat))
                
                # Always delete the higher index first to avoid shifting
                for i in sorted([seededIndex, nonSeededIndex], reverse=True):
                    del nonSeededPlayers[i]
            
            # Otherwise we do not have enough players and the bracket should be empty
            else:
                round1.append(Match(None, None, self.setFormat))

        self.draw.append(round1)
        
        # Round 1 has been created, create empty lists for the rest of the rounds
        drawSize = self.drawSize // 2
        while drawSize != 1:
            # Get next draw size (round 1 has already been added)
            drawSize = drawSize / 2

            # Inserting empty list to draw as the current round
            self.draw.append([])
    
    
    def simulate_tournament(self):
        """
        Method:
            Simulates the tournament using Monte Carlo techniques    
        """
        # Initialising variables
        roundIndex = 0
        completed = False
        injureCount = 0

        # Simulate all matches in the tournament
        while completed == False:
            # Initialising variables
            nextRoundPlayers = []
            drawForCurrentRound = self.draw[roundIndex]
            currentRound = self.rounds[roundIndex]

            # Simulate each match for this round
            for match in drawForCurrentRound:
                
                # Simulate match
                match.simulate_match()

                # Logic is different if the match is the final round
                if currentRound == "final":
                    
                    # If there was a no show for both players do nothing
                    if match.winner is None:
                        pass
                    
                    # Otherwise if the winner won by default handle only winner
                    elif match.loser is None:
                        match.winner.increment_points(self.roundPoints["winner"])
                        self.winner = match.winner
                        self.winner.form += 0.5
                    
                    # If both players played update accordingly
                    else:
                        match.winner.increment_points(self.roundPoints["winner"])
                        self.winner = match.winner
                        match.loser.increment_points(self.roundPoints["finalist"])
                        self.winner.form += 0.5
                    
                    completed = True
                
                # If the round isn't the final progress the tournament
                else:
                    # Add winner to nextRoundPlayers
                    nextRoundPlayers.append(match.winner)
                    
                    # If there was no winner do nothing
                    if match.winner == None:
                        pass
                    
                    # If the match was won by default handle only the winner
                    elif match.loser == None:
                        match.winner.update_fitness(self.matchRisk)
                    
                    # Otherwise handle normally
                    else:
                        # Add points to loser
                        match.loser.increment_points(self.roundPoints[currentRound])
                        # Update both players injuries
                        match.winner.update_fitness(self.matchRisk)
                        match.loser.update_fitness(self.matchRisk)

            # Safety check to make sure the loop breaks correctly
            if completed == True:
                break
            
            # Setting up next round
            roundIndex += 1
            drawForNextRound = self.draw[roundIndex]

            # Creating new matches
            player1Index = 0
            player2Index = 1
            while player1Index < len(nextRoundPlayers):
                # Fetching players
                player1 = nextRoundPlayers[player1Index]
                player2 = nextRoundPlayers[player2Index]

                # Checking for injuries (only one player per match gets injured for simplicity)
                player1Injured = False if player1 is None else player1.check_injury()
                if not player1Injured:
                    player2Injured = False if player2 is None else player2.check_injury()
    
                # Appending match to next round draw
                drawForNextRound.append(Match(player1, player2, self.setFormat))

                player1Index += 2
                player2Index += 2


class GrandSlam(Tournament):
    def __init__(self, courtType, name):
        """
        Method:
            init method for a grand slam tournament
        
        Params:
            courtType (str)
            name (str)
        """
        super().__init__(courtType, name)
        self.roundPoints = {
            "R1": 10,
            "R2": 50,
            "R3": 100,
            "R4": 200,
            "quarter final": 400,
            "semi final": 800,
            "finalist": 1300,
            "winner": 2000,
        }
        self.rounds = ["R1", "R2", "R3", "R4", "quarter final", "semi final", "final"]
        self.drawSize = 128
        # 5 set tournament so higher match risk
        self.matchRisk = 0.045
        self.type = "GrandSlam"


class Master1000(Tournament):
    def __init__(self, courtType, name):
        """
        Method:
            init method for a Master's 1000 tournament
        
        Params:
            courtType (str)
            name (str)
        """
        super().__init__(courtType, name)
        self.roundPoints = {
            "R1": 30,
            "R2": 50,
            "R3": 100,
            "quarter final": 200,
            "semi final": 400,
            "finalist": 650,
            "winner": 1000,
        }
        self.rounds = ["R1", "R2", "R3", "quarter final", "semi final", "final"]
        self.drawSize = 64
        self.type = "Master1000"


class ATP500(Tournament):
    def __init__(self, courtType, name):
        """
        Method:
            init method for an ATP 500 tournament
        
        Params:
            courtType (str)
            name (str)
        """
        super().__init__(courtType, name)
        self.roundPoints = {
            "R1": 25,
            "R2": 50,
            "R3": 75,
            "quarter final": 100,
            "semi final": 200,
            "finalist": 330,
            "winner": 500,
        }
        self.rounds = ["R1", "R2", "quarter final", "semi final", "final"]
        self.drawSize = 64
        self.type = "ATP500"


class ATP250(Tournament):
    def __init__(self, courtType, name):
        """
        Method:
            init method for an ATP 250 tournament
        
        Params:
            courtType (str)
            name (str)
        """
        super().__init__(courtType, name)
        self.roundPoints = {
            "R1": 13,
            "R2": 25,
            "R3" : 35,
            "quarter final": 50,
            "semi final": 100,
            "finalist": 165,
            "winner": 250,
        }
        self.rounds = ["R1", "R2", "quarter final", "semi final", "final"]
        self.drawSize = 64
        self.type = "ATP250"
