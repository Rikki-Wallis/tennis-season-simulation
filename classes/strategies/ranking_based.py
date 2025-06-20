from .tournament_strategy import TournamentStrategy


class RankingBased(TournamentStrategy):
    """Strategy: Adjust tournament selection based on current ranking"""
    def __init__(self):
        super().__init__("Ranking Based")

    def should_play_tournament(self, player, tournament, season):
        # Basic health checks
        if player.isInjured or player.fitness < 0.15:
            return False
        
        # Get current ranking
        ranking = player.ranking
        
        # Top 10 players: Focus on big events, be selective
        if ranking <= 10:
            return self._top_10_strategy(player, tournament, season)
        
        # Ranked 11-50: Play most Masters and ATP 500s, selective on 250s
        elif ranking <= 50:
            return self._mid_tier_strategy(player, tournament, season)
        
        # Ranked 51-100: Play most tournaments to accumulate points
        elif ranking <= 100:
            return self._climbing_strategy(player, tournament, season)
        
        # Outside top 100: Play everything possible to break through
        else:
            return self._breakthrough_strategy(player, tournament, season)

    def _top_10_strategy(self, player, tournament, season):
        """Strategy for top 10 players"""
        # Prioritize Grand Slams and Masters
        if tournament.type in ["GrandSlam", "Master1000"]:
            return True
        
        # Be selective with ATP 500s
        if tournament.type == "ATP500":
            # Only play if fitness is good and injury risk is low
            injury_proximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
            return player.fitness > 0.7 and injury_proximity < 0.3
        
        # Skip most ATP 250s unless very low risk
        if tournament.type == "ATP250":
            injury_proximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
            return player.fitness > 0.8 and injury_proximity < 0.2
        
        return False

    def _mid_tier_strategy(self, player, tournament, season):
        """Strategy for players ranked 11-50"""
        # Play all Grand Slams and Masters
        if tournament.type in ["GrandSlam", "Master1000"]:
            return True
        
        # Play most ATP 500s
        if tournament.type == "ATP500":
            injury_proximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
            return injury_proximity < 0.5
        
        # Be somewhat selective with ATP 250s
        if tournament.type == "ATP250":
            injury_proximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
            expected_points = season.get_skill_based_expected_points(player, tournament)
            return injury_proximity < 0.4 and expected_points > 20
        
        return False

    def _climbing_strategy(self, player, tournament, season):
        """Strategy for players ranked 51-100"""
        # Play all big events
        if tournament.type in ["GrandSlam", "Master1000"]:
            return True
        
        # Play ATP 500s unless high injury risk
        if tournament.type == "ATP500":
            injury_proximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
            return injury_proximity < 0.6
        
        # Play most ATP 250s - need points to climb
        if tournament.type == "ATP250":
            injury_proximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
            return injury_proximity < 0.5 and player.fitness > 0.3
        
        return False

    def _breakthrough_strategy(self, player, tournament, season):
        """Strategy for players outside top 100"""
        # Play everything possible - need to accumulate points
        injury_proximity = player.injuryRisk / player.injuryThreshold if player.injuryThreshold > 0 else 0
        
        # Only skip if injury risk is very high
        if injury_proximity > 0.7:
            return False
        
        # Minimum fitness requirement
        if player.fitness < 0.2:
            return False
        
        return True