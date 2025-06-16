# Imports
import random
from tournament import GrandSlam, Master1000, ATP500, ATP250
import math

class Season:
    def __init__(self, players):
        """
        Method:
            init method for season class
        
        Params:
            players (List(players)) - The players that will be competing in this season
        """
        # Initialise tournament schedule
        self.init_tournaments()
        
        # To properly simulate the skill disparity start all competitors at the same ranking
        self.rankings = players


    def simulate_season(self):
        """
        Method:
            Simulate the season
        """
        # Iterate through each week
        for week in self.tournamentSchedule:
    
            # Update rankings
            self.rankings = sorted(self.rankings, key=lambda player: player.rankingPoints, reverse=True)
            
            # Update ranking for each player
            for idx, player in enumerate(self.rankings):
                player.ranking = idx + 1

            # Players not playing this week
            restingPlayers = []
            
            rankingsIndex = 0
            # Iterate through each tournament in the week
            for tournament in week:
                # Adding set format to tournaments
                if tournament.type == "GrandSlam":
                    tournament.add_set_format(3)
                else:
                    tournament.add_set_format(2)
                
                # Create empty list for tournament registry
                entrants = []
                
                # Iterate through players
                while len(entrants) < tournament.drawSize and rankingsIndex < len(self.rankings):
                    # Grabbing next player to consider for entry
                    player = self.rankings[rankingsIndex]
                    
                    # Game Theory decision of whether this particular player should play the tournament
                    shouldPlay = self.should_play_tournament(player, tournament)
                    
                    # If the player should then register them
                    if shouldPlay:
                        entrants.append(player)
                    # If they shouldn't let them rest for this week
                    else:
                        restingPlayers.append(player)
                    
                    rankingsIndex += 1
                
                # Simulate the tournament
                tournament.generate_draw(entrants)
                tournament.simulate_tournament()
            
            # Handling injuries
            for player in restingPlayers:
                # Randomly treat injury if the player is injured
                if player.isInjured and random.random() <= 0.5:
                    player.isInjured = False
            
                # Increase fitness level
                player.update_fitness(-0.5)
                
            # Update rankings and ranking attribute for player
            self.rankings = sorted(self.rankings, key=lambda player: player.rankingPoints, reverse=True)
            for idx,player in enumerate(self.rankings):
                player.ranking = idx + 1


    def should_play_tournament(self, player, tournament):
        """
        Method:
            Pay off function that decides whether or not a particular player should
            play a tournament given factors such as tournament prestige, injury risk etc.
        
        Params:
            player (Player) - The target player
            tournament (Tournament) - The target tournament
        
        Returns:
            bool - True or False whether the player should play the tournament
        """
        
        # If the player is too unfit to play return False
        if player.fitness < 0.15 or player.isInjured:
            return False

        # Fitness penalty
        fitnessMultiplier = max(0.5, player.fitness)

        # Define the importance and/or prestige of each tournament type
        importance = {
            "GrandSlam" : 10,
            "Master1000" : 7,
            "ATP500" : 4,
            "ATP250" : 2
        }

        # Get expected points for the tournament based on the skill level of the player
        xPoints = self.get_skill_based_expected_points(player, tournament)
        
        # Ranking Pressure
        rankingMultiplier = 1
        if player.ranking > 100:
            rankingMultiplier += 0.3
        elif player.ranking > 50:
            rankingMultiplier += 0.1

        # Injury Risk Consideration
        injuryRisk = self.get_tournament_risk(tournament, player)
        
        # Calculate how close the player is to their injury threshold
        injury_proximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
        
        # Injury risk penalty - higher penalty as we get closer to injury threshold
        injury_risk_multiplier = 1.0
        if injury_proximity > 0.7: 
            injury_risk_multiplier = 0.05
        elif injury_proximity > 0.5:  
            injury_risk_multiplier = 0.1
        elif injury_proximity > 0.3:  
            injury_risk_multiplier = 0.2
        
        # If we expect to get injured, what's the cost of missing future tournaments?
        expected_injury_cost = 0
        if injuryRisk > 0.05:
            future_tournament_value = importance[tournament.type] * 100  
            expected_injury_cost = injuryRisk * future_tournament_value
        
        # Calculate payoff score 
        payoffScore = (xPoints * importance[tournament.type] * rankingMultiplier * fitnessMultiplier * injury_risk_multiplier) - expected_injury_cost

        # Define tournament importance, this will be what the payoff function checks against
        base_threshold = {
            "GrandSlam": 1,  
            "Master1000": 2,
            "ATP500": 3,
            "ATP250": 4
        }
        
        # Increase threshold if injury risk is high
        threshold = base_threshold[tournament.type]
        if injury_proximity > 0.6:
            threshold *= 1.5  
        elif injury_proximity > 0.4:
            threshold *= 1.2  
        
        # Special case: Grand Slams are so important that players might risk injury
        if tournament.type == "GrandSlam" and injury_proximity < 0.8:
            threshold = base_threshold[tournament.type] 
        
        return abs(payoffScore) > threshold
      
    def init_tournaments(self):
        """
        Method:
            Creates the tournament schedule
        """
        # December
        brisbane_international = ATP250("Hard", "Brisbane International")
        hong_kong_open = ATP250("Hard", "Hong Kong Open")

        # January
        adelaide_international = ATP250("Hard", "Adelaide Internationale")
        auckland = ATP250("Hard", "ASB Classic")
        australian_open = GrandSlam("Hard", "AO")
        montpellier = ATP250("Hard", "Open Occitaine")

        # February
        dallas_open = ATP500("Hard", "Dallas Open")
        rotterdam = ATP500("Hard", "ABN AMRO Open")
        marseille = ATP250("Hard", "Open 13 Provence")
        delray_beach = ATP250("Hard", "Delray Beach Open")
        argentina = ATP250("Hard", "IEB+ Argentina Open")
        qatar = ATP500("Hard", "Qatar ExonnMobil Open")
        rio = ATP500("Hard", "Rio Open")
        dubai = ATP500("Hard", "Dubai Duty Free Tennis Chamionships")
        acapulco = ATP500("Hard", "Acapulco")
        santiago = ATP250("Hard", "Movistar Chile Open")

        # March
        indian_wells = Master1000("Hard", "BNP Paribas Open")
        miami = Master1000("Hard", "Miami Open")
        houston = ATP250("Clay", "Houston Open")
        morocco = ATP250("Clay", "Grand Prix Hassan II")
        romania = ATP250("Clay", "Bucharest Open")

        # April
        monte_carlo = Master1000("Clay", "Rolex Monte-Carlo Masters")
        barcelona = ATP500("Clay", "Barcelona Open")
        munich = ATP500("Clay", "BMW Open")
        madrid = Master1000("Clay", "Mutua Madrid Open")

        # May
        rome = Master1000("Clay", "Internazionali BNL d'Italia")
        hamburg = ATP500("Clay", "Hamburg Open")
        geneva = ATP250("Clay", "Gonet Geneva Open")
        roland_garros = GrandSlam("Clay", "Roland Garros")

        # June
        stuttgart = ATP250("Grass", "BOSS Open")
        libema = ATP250("Grass", "Libema Open")
        hsbc_champs = ATP500("Grass", "HSBC Championships")
        halle = ATP500("Grass", "Terra Wortmann Open")
        mallorca = ATP250("Grass", "Mallorca Championships")
        eastbourne = ATP250("Grass", "Lexus Eastbourne Open")
        wimbledon = GrandSlam("Grass", "Wimbledon")

        # July
        los_cabos = ATP250("Hard", "Mifel Tennis Open")
        gstaad = ATP250("Clay", "EFG Swiss Open Gstaad")
        nordea = ATP250("Clay", "Nordea Open")
        generali = ATP250("Clay", "Generali Open")
        umag = ATP250("Clay", "Croatia Open")
        washington = ATP500("Hard", "DC Open")
        toronto = Master1000("Hard", "Toronto Open")

        # August
        cincinatti = Master1000("Hard", "Cincinatti Open")
        winston_salem = ATP250("Hard", "Winston-Salem Open")
        us_open = GrandSlam("Hard", "US Open")

        # September
        chengdu = ATP250("Hard", "Chengdu Open")
        hangzhou = ATP250("Hard", "Hangzhou Open")
        tokyo = ATP500("Hard", "Tokyo Open")
        china = ATP500("Hard", "China Open")

        # October
        shangai = Master1000("Hard", "Shanghai Masters")
        almaty = ATP250("Hard", "Almaty Open")
        stockholm = ATP250("Hard", "BNP Paribas Nordic Open")
        brussels = ATP250("Hard", "European Open")
        vienna = ATP500("Hard", "Erste Bank Open")
        basel = ATP500("Hard", "Swiss Indoors Basel")
        paris_masters = Master1000("Hard", "Rolex Paris Masters")

        # November
        belgrade = ATP250("Hard", "Belgrade Open")
        moselle = ATP250("Hard", "Moselle Open")

        self.tournamentSchedule = [
            [brisbane_international, hong_kong_open],
            [adelaide_international, auckland],
            [australian_open],
            [montpellier],
            [dallas_open, rotterdam],
            [marseille, delray_beach, argentina],
            [qatar, rio],
            [dubai, acapulco, santiago],
            [indian_wells],
            [miami],
            [houston, morocco, romania],
            [monte_carlo],
            [barcelona, munich],
            [madrid],
            [rome],
            [hamburg, geneva],
            [roland_garros],
            [stuttgart, libema],
            [hsbc_champs, halle],
            [mallorca, eastbourne],
            [wimbledon],
            [los_cabos, gstaad, nordea],
            [generali, umag, washington],
            [toronto],
            [cincinatti],
            [winston_salem],
            [us_open],
            [chengdu, hangzhou],
            [tokyo, china],
            [shangai],
            [almaty, stockholm, brussels],
            [vienna, basel],
            [paris_masters],
            [belgrade, moselle]
        ]
    
    """
    ----------------
    HELPER FUNCTIONS
    ----------------
    """
    
    def get_tournament_risk(self, tournament, player):
        """
        Method:
            Calculates the risk of playing in a particular tournament
        
        Params:
            tournament (Tournament) - The target tournament
            player (Player) - The target player
        
        Return:
            adjustedRisk (float) - The risk factor associated with this player playing this tournament
        """
        # Fetch the expected matches that the player is expected to play this tournament
        expectedMatches = self.get_expected_matches(player, tournament)
        
        # Base risk from playing matches
        baseRisk = expectedMatches * tournament.matchRisk
        
        # Factor in current injury proximity
        injuryProximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
        
        # Risk increases exponentially as we approach injury threshold
        proximityMultiplier = 1.0 + (injuryProximity ** 2) * 0.5
        
        # Fitness affects injury risk
        fitnessMultiplier = 2.0 - player.fitness
        
        # Calculate and return the adjusted risk of playing
        adjustedRisk = baseRisk * proximityMultiplier * fitnessMultiplier
        return adjustedRisk


    def get_skill_based_expected_points(self, player, tournament):
        """
        Method:
            Calculate expected points based on player's skill relative to field
        
        Params:
            tournament (Tournament) - The target tournament
            player (Player) - The target player
        
        Return:
            expectedPoints (float) - The number of points the player is expected to recieve
        """
    
        # Get player's total skill
        player_skill = (player.serveStrength + player.returnStrength)*player.form
        
        # Estimate average opponent skill
        if len(self.rankings) >= 128:
            avg_opponent_skill = sum(p.serveStrength + p.returnStrength for p in self.rankings[:128]) / 128
        else:
            avg_opponent_skill = sum(p.serveStrength + p.returnStrength for p in self.rankings) / len(self.rankings)
        
        # Skill difference affects win probability
        skill_diff = player_skill - avg_opponent_skill
        
        # Skill differences of 10-20 points should matter
        base_win_prob = 1 / (1 + math.exp(-skill_diff / 15))
        
        # Adjust for fitness
        win_prob = base_win_prob * max(0.7, player.fitness) 
        
        # Calculate expected performance
        if win_prob < 0.1:
            expected_round_reached = 0.5  
        elif win_prob < 0.3:
            expected_round_reached = 1.0  
        elif win_prob < 0.45:
            expected_round_reached = 1.5  
        elif win_prob < 0.6:
            expected_round_reached = 2.0  
        elif win_prob < 0.75:
            expected_round_reached = 3.0  
        elif win_prob < 0.85:
            expected_round_reached = 4.0  
        elif win_prob < 0.95:
            expected_round_reached = 5.0  
        else:
            expected_round_reached = 6.0  
        
        # Convert to points using ATP point structure
        rounds_to_points = {
            "GrandSlam": [10, 45, 90, 180, 360, 720, 1200, 2000],
            "Master1000": [10, 25, 50, 100, 200, 400, 600, 1000],
            "ATP500": [0, 20, 45, 90, 180, 300, 500, 500],
            "ATP250": [0, 8, 15, 30, 60, 120, 250, 250]
        }
        
        # Interpolate between rounds for more granular expected points
        base_round = int(expected_round_reached)
        fraction = expected_round_reached - base_round
        
        points_array = rounds_to_points[tournament.type]
        base_round = min(base_round, len(points_array) - 1)
        
        if fraction > 0 and base_round < len(points_array) - 1:
            expected_points = points_array[base_round] * (1 - fraction) + points_array[base_round + 1] * fraction
        else:
            expected_points = points_array[base_round]
        
        return expected_points

    
    def get_expected_matches(self, player, tournament, fitnessWeight=0.5, rankingWeight=0.6):
        """
        Method:
            Calculates the expected matches the player should be playing for a tournament
        
        Params:
            player (Player) - Target player
            tournament (Tournament) - Target tournament
            fitnessWeight (float) - The weight that fitness plays in the calculation
            rankingWeight (float) - The weight that ranking plays in the calculation
            
        Return:
            expectedMatches (float) - The number of matches the player is expected to play
        """
        # Max amount of matches for each slam
        maxMatches = {
            "GrandSlam" : 7,
            "Master1000" : 6,
            "ATP500" : 5,
            "ATP250" : 5
        }
        maxMatches = maxMatches[tournament.type]
        
        # Normalize the players ranking
        normalizedRanking = self.normalize_ranking(player, self.rankings)
        
        # Give them a score
        score = (player.fitness * fitnessWeight) + (normalizedRanking * rankingWeight)
        
        # Reduce expected matches if injury risk is high
        injury_proximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
        injury_penalty = max(0.7, 1.0 - injury_proximity * 0.3)  
        
        # Calculate and return the expected matches
        expectedMatches = score * maxMatches * injury_penalty
        return expectedMatches
    
    def normalize_ranking(self, player, rankings):
        """
        Method:
            Normalizes a player's ranking to a value between 0 and 1, where 1 is the best rank
        
        Params:
            player (Player) - The target player
            rankings (List[Player]) - List of all players sorted by ranking
        
        Returns:
            float - Normalized ranking score
        """
        total_players = len(rankings)
        
        # Convert ranking to normalized score
        normalized_score = (total_players - player.ranking + 1) / total_players
        
        return normalized_score
    