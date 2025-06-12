"""
Test File
"""

import numpy as np
from player import Player
from game import Game


def test_player():
    # Reset the ID counter
    Player.idCounter = 0

    # Create a new player
    p1 = Player("Test Player")

    # Test identity
    assert p1.name == "Test Player"
    assert p1.playerID == 0

    # Test type and rough ranges (normal distribution)
    assert isinstance(p1.serveStrength, float)
    assert isinstance(p1.returnStrength, float)
    assert 20 <= p1.serveStrength <= 100
    assert 10 <= p1.returnStrength <= 80

    # Test initial stats
    assert p1.gamesPlayed == 0
    assert p1.rankingPoints == 0
    for val in p1.tournamentsWon.values():
        assert val == 0

    # Test incrementing tournament wins
    p1.increment_tournament_win("ATP 500")
    assert p1.tournamentsWon["ATP 500"] == 1
    p1.increment_tournament_win("ATP 500")
    assert p1.tournamentsWon["ATP 500"] == 2

    # Test incrementing points
    p1.increment_points(250)
    assert p1.rankingPoints == 250
    p1.increment_points(100)
    assert p1.rankingPoints == 350

    # Test incrementing games played
    p1.increment_games_played()
    assert p1.gamesPlayed == 1
    p1.increment_games_played()
    assert p1.gamesPlayed == 2

    # Test unique ID
    p2 = Player("Second Player")
    assert p2.playerID == 1


def test_game():
# Create two dummy players with fixed attributes
    class DummyPlayer:
        def __init__(self, name, serveStrength, returnStrength, form=1.0):
            self.name = name
            self.serveStrength = serveStrength
            self.returnStrength = returnStrength
            self.form = form

    server = DummyPlayer("Server", serveStrength=80, returnStrength=30)
    returner = DummyPlayer("Returner", serveStrength=60, returnStrength=40)

    # Create Game instance
    game = Game(server, returner)

    # Check that markov chain and index are generated correctly
    assert isinstance(game.markovChain, np.ndarray)
    assert isinstance(game.markovChainIndex, dict)
    assert "0-0" in game.markovChainIndex
    assert "Hold" in game.markovChainIndex
    assert "Break" in game.markovChainIndex

    # Test that simulate_game sets a winner from server or returner
    winners = set()
    for _ in range(50):
        game.simulate_game()
        assert game.winner in (server, returner)
        winners.add(game.winner.name)

    # Expect at least both players can win sometimes
    assert "Server" in winners
    assert "Returner" in winners

    # Test absorption probabilities matrix properties
    B, transient_indices, absorbing_indices = game.compute_absorption_probabilities(game.markovChain)
    # Each row sums to 1 (absorbing probabilities sum to 1)
    for row in B:
        assert np.isclose(np.sum(row), 1), "Absorption probabilities row must sum to 1"

def test_set():
    pass


def test_match():
    pass


def test_tiebreak():
    pass


def test_tournament():
    pass


def test_season():
    pass


if __name__ == "__main__":
    test_player()
    test_game()
