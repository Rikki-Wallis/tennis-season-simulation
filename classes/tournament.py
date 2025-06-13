# Imports
import numpy as np
from match import Match

class Tournament:
    def __init__(self, courtType, name):
        self.courtType = courtType
        self.name = name
        # Default match risk for 3 set tournaments
        self.matchRisk = 0.03

    def add_set_format(self, setFormat):
        self.setFormat = setFormat

    def generate_draw(self, players):
        """
        Method:
            Generates the draw for a tournament

        Params:
            players (List(Player)): The list of the players playing the tournament

        Returns:
            draw (List(Match)): A list that contains all the first round matches

        TODO: Create draw so that seeded pairings 1,2,3,4 are all on opposite sides
        """
        # Sort players in terms of rankings
        players = sorted(players, key=lambda player: player.rankingPoints, reverse=True)

        # Seperate seeded players and non seeded players
        seededPlayers = players[: (self.drawSize // 4)]
        nonSeededPlayers = players[(self.drawSize // 4) :]

        # Initial draw variables
        self.draw = []
        round1 = []
        seedExist = True

        # Getting first matches for round 1 based off of seedings
        for match in range(self.drawSize // 2):
            # getting random players that are seeded and not seeded
            if len(seededPlayers) > 0:
                seededIndex = np.random.randint(low=0, high=len(seededPlayers))
                nonSeededIndex = np.random.randint(low=0, high=len(nonSeededPlayers))
            # Some matches will have two non seeded players playing eachother
            else:
                seedExist = False
                while True:
                    seededIndex = np.random.randint(low=0, high=len(nonSeededPlayers))
                    nonSeededIndex = np.random.randint(low=0, high=len(nonSeededPlayers))

                    # Make sure indexes are different
                    if seededIndex != nonSeededIndex:
                        break
            
            # Appending to first roudn and deleting random players from their respective lists
            if seedExist:
                round1.append( Match(seededPlayers[seededIndex], nonSeededPlayers[nonSeededIndex], self.setFormat) )
                
                del seededPlayers[seededIndex]
                del nonSeededPlayers[nonSeededIndex]
            else:
                round1.append( Match(nonSeededPlayers[seededIndex], nonSeededPlayers[nonSeededIndex], self.setFormat) )
                
                # Always delete the higher index first to avoid shifting
                for i in sorted([seededIndex, nonSeededIndex], reverse=True):
                    del nonSeededPlayers[i]

        # Creating the rest of the rounds
        self.draw.append(round1)
        drawSize = self.drawSize // 2
        while drawSize != 1:
            # Get next draw size (round 1 has already been added)
            drawSize = drawSize / 2

            # Inserting empty list to draw as the current round
            self.draw.append([])

    def simulate_tournament(self):
        # Initialising variables
        roundIndex = 0
        completed = False

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
            
                # Update both players injuries
                match.winner.update_fitness(self.matchRisk)
                match.loser.update_fitness(self.matchRisk)

                if currentRound == "final":
                    match.winner.increment_points(self.roundPoints["winner"])
                    match.loser.increment_points(self.roundPoints["finalist"])
                    completed = True
                else:
                    # Add winner to nextRoundPlayers
                    nextRoundPlayers.append(match.winner)

                    # Add points to loser
                    match.loser.increment_points(self.roundPoints[currentRound])

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
                player1.check_injury()
                if not player1.isInjured:
                    player2.check_injury()
                    
                # Appending match to next round draw
                drawForNextRound.append(Match(player1, player2, self.setFormat))

                player1Index += 2
                player2Index += 2


class GrandSlam(Tournament):
    def __init__(self, courtType, name):
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
        super().__init__(courtType, name)
        self.roundPoints = {
            "R1": 25,
            "R2": 50,
            "quarter final": 100,
            "semi final": 200,
            "finalist": 330,
            "winner": 500,
        }
        self.rounds = ["R1", "R2", "quarter final", "semi final", "final"]
        self.drawSize = 32
        self.type = "ATP500"


class ATP250(Tournament):
    def __init__(self, courtType, name):
        super().__init__(courtType, name)
        self.roundPoints = {
            "R1": 13,
            "R2": 25,
            "quarter final": 50,
            "semi final": 100,
            "finalist": 165,
            "winner": 250,
        }
        self.rounds = ["R1", "R2", "quarter final", "semi final", "final"]
        self.drawSize = 32
        self.type = "ATP250"
