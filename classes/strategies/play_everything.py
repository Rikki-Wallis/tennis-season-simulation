from .tournament_strategy import TournamentStrategy

class PlayEverything(TournamentStrategy):
    def __init__(self):
        super().__init__("Play Everything")
    
    def should_play_tournament(self, player, tournament, season):
        # Only skip if injured or critically unfit
        if player.isInjured or player.fitness < 0.1:
            return False
        return True