from .tournament_strategy import TournamentStrategy


class Original(TournamentStrategy):
    """The original sophisticated strategy from the Season class"""
    def __init__(self):
        super().__init__("Original Strategy")

    def should_play_tournament(self, player, tournament, season):
        # If the player is too unfit to play return False
        if player.fitness < 0.15 or player.isInjured:
            return False

        # Fitness penalty
        fitnessMultiplier = max(0.5, player.fitness)

        # Define the importance and/or prestige of each tournament type
        importance = {
            "GrandSlam": 10,
            "Master1000": 7,
            "ATP500": 4,
            "ATP250": 2
        }

        # Get expected points for the tournament based on the skill level of the player
        xPoints = season.get_skill_based_expected_points(player, tournament)
        
        # Ranking Pressure
        rankingMultiplier = 1
        if player.ranking > 100:
            rankingMultiplier += 0.3
        elif player.ranking > 50:
            rankingMultiplier += 0.1

        # Injury Risk Consideration
        injuryRisk = season.get_tournament_risk(tournament, player)
        
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