class TournamentStrategy:
    def __init__(self, name):
        self.name = name
        
    def should_play_tournament(self, player, tournament, season):
        raise NotImplementedError
    