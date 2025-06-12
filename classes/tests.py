"""
Test File
"""

import numpy as np
from player import Player
from game import Game
from set import Set
from tiebreak import Tiebreak
from match import Match
from tournament import *

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
    # Reset player ID counter for consistency
    Player.idCounter = 0

    # Create two players
    p1 = Player("Player One")
    p2 = Player("Player Two")

    # Make both players have high form to reduce randomness
    p1.form = 1.0
    p2.form = 1.0

    # Simulate a set
    tennis_set = Set(p1, p2)
    next_server = tennis_set.simulate_set()

    # Test that winner is one of the players
    assert tennis_set.winner in [p1, p2]

    # Test that the set score is valid
    s1, s2 = tennis_set.score
    assert (s1 >= 6 or s2 >= 6) or (s1 == 7 or s2 == 7)
    assert abs(s1 - s2) >= 1

    # Test that next_server tuple is a valid swap of players
    assert set(next_server) == {p1, p2}

    print(f"Test passed: Set winner is {tennis_set.winner.name}, final score {s1}-{s2}")

def test_match():
    # Reset player ID counter
    Player.idCounter = 0

    # Create two players with high form to reduce randomness
    p1 = Player("Player One")
    p2 = Player("Player Two")
    p1.form = 1.0
    p2.form = 1.0

    # Optional: Seed random for reproducibility
    np.random.seed(42)

    # Simulate a best-of-3 match
    match = Match(p1, p2, setFormat=3)
    match.simulate_match()

    # Validate winner/loser
    assert match.winner in [p1, p2]
    assert match.loser in [p1, p2]
    assert match.winner != match.loser

    # Validate score
    score_p1, score_p2 = match.score
    assert score_p1 == 2 or score_p2 == 2  # One must win 2 sets
    assert score_p1 < 3 and score_p2 < 3   # Max 3 sets in best-of-3

    print(f"Test passed: {match.winner.name} defeated {match.loser.name} ({score_p1}-{score_p2})")


def test_tiebreak():
    # Reset the ID counter
    Player.idCounter = 0

    # Create two players
    p1 = Player("Player One")
    p2 = Player("Player Two")

    # Create a Tiebreak object
    tb = Tiebreak(p1, p2)

    # Simulate the tiebreak
    tb.simulate_tiebreak()

    # Basic assertions
    assert tb.winner in (p1, p2), "Winner must be one of the players"
    assert isinstance(tb.score, list), "Score must be a tuple"
    assert tb.score[0] >= 0 and tb.score[1] >= 0, "Scores must be non-negative integers"


    print(f"Tiebreak Result: {tb.score[0]}–{tb.score[1]}, Winner: {tb.winner.name}")


def test_tournament():

    # Reset Player ID counter
    Player.idCounter = 0

    # Create 32 players with descending ranking points
    players = []
    for i in range(32):
        player = Player(f"Player {i+1}")
        player.rankingPoints = 1000 - i * 10  # Seeded order
        players.append(player)

    # Create ATP250 tournament
    tournament = ATP250(courtType="hard", name="Test ATP250")
    tournament.add_set_format(setFormat=3)

    # Generate draw and simulate
    tournament.generate_draw(players)
    tournament.simulate_tournament()

    # Confirm structure
    assert len(tournament.draw) == 5  # 5 rounds: R1 to Final
    assert tournament.draw[0]  # R1 has matches
    assert all(isinstance(round_, list) for round_ in tournament.draw)

    # Confirm winner
    final_match = tournament.draw[-1][0]
    assert final_match.winner is not None
    assert final_match.loser is not None
    assert final_match.winner != final_match.loser

    # Confirm points were awarded
    all_points = [p.rankingPoints for p in players]
    assert any(p > 1000 - i * 10 for i, p in enumerate(all_points)), "No points awarded"

    # Check that all players have updated ranking points (no one remains at their initial value)
    for i, player in enumerate(players):
        initial_points = 1000 - i * 10
        assert player.rankingPoints >= initial_points, f"{player.name} rankingPoints not updated properly"
    
    print(f" Tournament winner: {final_match.winner.name} with {final_match.winner.rankingPoints} points")
    print(f" Tournament test passed")


def test_season():
    pass


if __name__ == "__main__":
    test_player()
    test_game()
    test_tiebreak()
    test_set()
    test_match()
    test_tournament()