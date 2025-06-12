from player import Player
import random

def init_players(numPlayers):
    # Create lists of first names and last names
    first_names = [
    "Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin", "Lucas",
    "Henry", "Alexander", "Daniel", "Matthew", "Jack", "Sebastian", "Logan",
    "Michael", "Ethan", "Jacob", "Mason", "David", "Samuel", "Joseph", "John",
    "Owen", "Luke", "Gabriel", "Anthony", "Isaac", "Dylan", "Andrew" ]

    last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson" ]
    
    # Initiating empty list to store player objects
    players = []
    nameDict = {}
    
    # Creating players with different random stats
    for _ in numPlayers:
        
        # Make sure that player name is unique
        while True:
            playerName = f'{random.choice(first_names)} {random.choice(last_names)}'
            
            if playerName not in nameDict:
                players.append(Player(playerName))
                nameDict[playerName] = 0
                break

    return players