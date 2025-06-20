from .tournament_strategy import TournamentStrategy

class BigEventFocus(TournamentStrategy):
    def __init__(self):
        super().__init__("Big Event Focus")

    def should_play_tournament(self, player, tournament, season):
        # Skip if injured or unfit
        if player.isInjured or player.fitness < 0.15:
            return False

        # Only play Grand Slams and Masters 1000
        return tournament.type in ["GrandSlam", "Master1000"]