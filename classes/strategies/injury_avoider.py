from .tournament_strategy import TournamentStrategy


class InjuryAvoider(TournamentStrategy):
    """Strategy: Heavy focus on avoiding injury, very conservative"""
    def __init__(self, injury_threshold=0.2, fitness_threshold=0.6):
        super().__init__("Injury Avoider")
        self.injury_threshold = injury_threshold
        self.fitness_threshold = fitness_threshold

    def should_play_tournament(self, player, tournament, season):
        # Skip if injured or low fitness
        if player.isInjured or player.fitness < self.fitness_threshold:
            return False
        
        # Calculate injury proximity
        injury_proximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
        
        # Very conservative - skip if injury risk is elevated
        if injury_proximity > self.injury_threshold:
            return False
        
        # Calculate tournament risk
        tournament_risk = season.get_tournament_risk(tournament, player)
        
        # Skip high-risk tournaments unless it's a Grand Slam
        if tournament_risk > 0.1 and tournament.type != "GrandSlam":
            return False
        
        # For Grand Slams, be slightly less conservative
        if tournament.type == "GrandSlam" and injury_proximity > 0.4:
            return False
        
        # Tournament importance consideration
        importance = {
            "GrandSlam": 10,
            "Master1000": 7,
            "ATP500": 4,
            "ATP250": 2
        }
        
        # Only play if expected value is high enough given risk
        expected_points = season.get_skill_based_expected_points(player, tournament)
        risk_adjusted_value = expected_points * importance[tournament.type] * (1 - tournament_risk)
        
        # Conservative threshold
        threshold = {
            "GrandSlam": 50,
            "Master1000": 30,
            "ATP500": 20,
            "ATP250": 15
        }
        
        return risk_adjusted_value > threshold[tournament.type]
