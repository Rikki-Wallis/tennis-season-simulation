from season import Season
from player import Player
import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from strategies.big_event_focus import BigEventFocus
from strategies.injury_avoider import InjuryAvoider
from strategies.original import Original
from strategies.play_everything import PlayEverything
from strategies.ranking_based import RankingBased



"""

The following functions are general functions that help set up the simulation environment

"""



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
    for _ in range(numPlayers):
        
        # Make sure that player name is unique
        while True:
            playerName = f'{random.choice(first_names)} {random.choice(last_names)}'
            
            if playerName not in nameDict:
                players.append(Player(playerName))
                nameDict[playerName] = 0
                break

    return players


def assign_strategies(players, original=False):
    if original == True:
        for player in players:
            player.set_strategy(Original())
    else:
        # Strategies
        strategies = [BigEventFocus(), InjuryAvoider(), Original(), PlayEverything(), RankingBased()]

        i = 0 
        for player in players:
            player.set_strategy(strategies[i])
            
            if i == 4:
                i = 0
            else:
                i += 1
        




"""

The following functions are all used to plot for simulation 1

"""




class AggregatedPlayerStats:
    """Class to hold aggregated statistics across multiple simulations"""
    def __init__(self, name, ranking_position):
        self.name = name
        self.ranking_position = ranking_position
        self.serveStrength = 0
        self.returnStrength = 0
        self.form = 0
        self.injuryThreshold = 0
        self.injuryProbability = 0

def create_aggregated_rankings(all_rankings, method='average'):
    """
    Create aggregated rankings using either average or median statistics
    
    Args:
        all_rankings: List of lists, each containing Player objects from one simulation
        method: 'average' or 'median'
    
    Returns:
        List of AggregatedPlayerStats objects sorted by ranking position
    """
    num_players = len(all_rankings[0])
    num_simulations = len(all_rankings)
    
    # Collect all stats for each ranking position across simulations
    position_stats = {i: {
        'serve_strength': [],
        'return_strength': [],
        'form': [],
        'injury_threshold': [],
        'injury_probability': [],
        'names': []
    } for i in range(num_players)}
    
    # Gather stats for each position across all simulations
    for sim_rankings in all_rankings:
        for pos, player in enumerate(sim_rankings):
            position_stats[pos]['serve_strength'].append(player.serveStrength)
            position_stats[pos]['return_strength'].append(player.returnStrength)
            position_stats[pos]['form'].append(player.form)
            position_stats[pos]['injury_threshold'].append(player.injuryThreshold)
            position_stats[pos]['injury_probability'].append(player.injuryProbability)
            position_stats[pos]['names'].append(player.name)
    
    # Create aggregated player objects
    aggregated_rankings = []
    
    for pos in range(num_players):
        # Get most common name for this position (or use a generic name)
        most_common_name = max(set(position_stats[pos]['names']), 
                             key=position_stats[pos]['names'].count)
        
        agg_player = AggregatedPlayerStats(f"Pos_{pos+1}_{most_common_name}", pos)
        
        if method == 'average':
            agg_player.serveStrength = np.mean(position_stats[pos]['serve_strength'])
            agg_player.returnStrength = np.mean(position_stats[pos]['return_strength'])
            agg_player.form = np.mean(position_stats[pos]['form'])
            agg_player.injuryThreshold = np.mean(position_stats[pos]['injury_threshold'])
            agg_player.injuryProbability = np.mean(position_stats[pos]['injury_probability'])
        elif method == 'median':
            agg_player.serveStrength = np.median(position_stats[pos]['serve_strength'])
            agg_player.returnStrength = np.median(position_stats[pos]['return_strength'])
            agg_player.form = np.median(position_stats[pos]['form'])
            agg_player.injuryThreshold = np.median(position_stats[pos]['injury_threshold'])
            agg_player.injuryProbability = np.median(position_stats[pos]['injury_probability'])
        
        aggregated_rankings.append(agg_player)
    
    return aggregated_rankings

def visualize_individual_stats_by_ranking(actualRankings, title_suffix=""):
    """Break down individual statistics by ranking position"""
    
    # Extract individual stats for each ranking position
    serve_strength = [player.serveStrength for player in actualRankings]
    return_strength = [player.returnStrength for player in actualRankings]
    form = [player.form for player in actualRankings]
    injury_threshold = [player.injuryThreshold for player in actualRankings]
    injury_probability = [player.injuryProbability for player in actualRankings]
    
    # Create subplots for each stat - REDUCED SIZE
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))  # Reduced from (18, 12)
    fig.suptitle(f'Individual Statistics by Ranking Position {title_suffix}', fontsize=12)
    
    # Serve Strength
    axes[0, 0].plot(range(len(actualRankings)), serve_strength, color='blue', alpha=0.7)
    axes[0, 0].set_title('Serve Strength', fontsize=10)
    axes[0, 0].set_xlabel('Ranking Position', fontsize=9)
    axes[0, 0].set_ylabel('Serve Strength', fontsize=9)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].tick_params(labelsize=8)
    
    # Return Strength
    axes[0, 1].plot(range(len(actualRankings)), return_strength, color='green', alpha=0.7)
    axes[0, 1].set_title('Return Strength', fontsize=10)
    axes[0, 1].set_xlabel('Ranking Position', fontsize=9)
    axes[0, 1].set_ylabel('Return Strength', fontsize=9)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].tick_params(labelsize=8)
    
    # Form
    axes[0, 2].plot(range(len(actualRankings)), form, color='orange', alpha=0.7)
    axes[0, 2].set_title('Form', fontsize=10)
    axes[0, 2].set_xlabel('Ranking Position', fontsize=9)
    axes[0, 2].set_ylabel('Form', fontsize=9)
    axes[0, 2].grid(True, alpha=0.3)
    axes[0, 2].tick_params(labelsize=8)
    
    # Injury Threshold
    axes[1, 0].plot(range(len(actualRankings)), injury_threshold, color='red', alpha=0.7)
    axes[1, 0].set_title('Injury Threshold', fontsize=10)
    axes[1, 0].set_xlabel('Ranking Position', fontsize=9)
    axes[1, 0].set_ylabel('Injury Threshold', fontsize=9)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].tick_params(labelsize=8)
    
    # Injury Probability
    axes[1, 1].plot(range(len(actualRankings)), injury_probability, color='purple', alpha=0.7)
    axes[1, 1].set_title('Injury Probability', fontsize=10)
    axes[1, 1].set_xlabel('Ranking Position', fontsize=9)
    axes[1, 1].set_ylabel('Injury Probability', fontsize=9)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].tick_params(labelsize=8)
    
    # Combined Score
    combined_score = [(player.serveStrength + player.returnStrength) * player.form * 
                     player.injuryThreshold * (1 - player.injuryProbability) 
                     for player in actualRankings]
    axes[1, 2].plot(range(len(actualRankings)), combined_score, color='black', alpha=0.7)
    axes[1, 2].set_title('Combined Score', fontsize=10)
    axes[1, 2].set_xlabel('Ranking Position', fontsize=9)
    axes[1, 2].set_ylabel('Combined Score', fontsize=9)
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].tick_params(labelsize=8)
    
    plt.tight_layout()
    plt.show()

def create_ranking_tier_analysis(actualRankings, tier_size=50):
    """Analyze statistics by ranking tiers"""
    
    # Create tiers
    tiers = []
    tier_labels = []
    
    for i in range(0, len(actualRankings), tier_size):
        tier_players = actualRankings[i:i+tier_size]
        tiers.append(tier_players)
        tier_labels.append(f'Rank {i+1}-{min(i+tier_size, len(actualRankings))}')
    
    # Calculate statistics for each tier
    stats_by_tier = {
        'serve_strength': [],
        'return_strength': [],
        'form': [],
        'injury_threshold': [],
        'injury_probability': [],
        'combined_score': []
    }
    
    for tier in tiers:
        stats_by_tier['serve_strength'].append(np.mean([p.serveStrength for p in tier]))
        stats_by_tier['return_strength'].append(np.mean([p.returnStrength for p in tier]))
        stats_by_tier['form'].append(np.mean([p.form for p in tier])*20)
        stats_by_tier['injury_threshold'].append(np.mean([p.injuryThreshold for p in tier])*100)
        stats_by_tier['injury_probability'].append(np.mean([p.injuryProbability for p in tier])*100)
        stats_by_tier['combined_score'].append(np.mean([
            (p.serveStrength + p.returnStrength) * p.form * p.injuryThreshold * (1 - p.injuryProbability) 
            for p in tier
        ]))
    
    # Create bar chart - REDUCED SIZE
    fig, ax = plt.subplots(figsize=(10, 6))  # Reduced from (15, 8)
    x = np.arange(len(tier_labels))
    width = 0.12
    
    bars1 = ax.bar(x - 2.5*width, stats_by_tier['serve_strength'], width, label='Serve Strength', alpha=0.8)
    bars2 = ax.bar(x - 1.5*width, stats_by_tier['return_strength'], width, label='Return Strength', alpha=0.8)
    bars3 = ax.bar(x - 0.5*width, stats_by_tier['form'], width, label='Form', alpha=0.8)
    bars4 = ax.bar(x + 0.5*width, stats_by_tier['injury_threshold'], width, label='Injury Threshold', alpha=0.8)
    bars5 = ax.bar(x + 1.5*width, stats_by_tier['injury_probability'], width, label='Injury Probability', alpha=0.8)
    
    ax.set_xlabel('Ranking Tiers', fontsize=10)
    ax.set_ylabel('Average Statistic Value', fontsize=10)
    ax.set_title('Average Statistics by Ranking Tier', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(tier_labels, rotation=45, fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=8)
    
    plt.tight_layout()
    plt.show()

def create_distribution_plots(actualRankings, top_n=50):
    """Compare distributions of top N vs bottom N players"""
    
    top_players = actualRankings[:top_n]
    bottom_players = actualRankings[-top_n:]
    
    # REDUCED SIZE
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))  # Reduced from (18, 12)
    fig.suptitle(f'Distribution Comparison: Top {top_n} vs Bottom {top_n} Players', fontsize=12)
    
    stats = [
        ('serveStrength', 'Serve Strength'),
        ('returnStrength', 'Return Strength'),
        ('form', 'Form'),
        ('injuryThreshold', 'Injury Threshold'),
        ('injuryProbability', 'Injury Probability')
    ]
    
    for i, (stat_attr, stat_name) in enumerate(stats):
        row, col = i // 3, i % 3
        
        top_values = [getattr(p, stat_attr) for p in top_players]
        bottom_values = [getattr(p, stat_attr) for p in bottom_players]
        
        axes[row, col].hist(top_values, alpha=0.7, label=f'Top {top_n}', bins=15, color='blue')
        axes[row, col].hist(bottom_values, alpha=0.7, label=f'Bottom {top_n}', bins=15, color='red')
        axes[row, col].set_title(stat_name, fontsize=10)
        axes[row, col].set_xlabel(stat_name, fontsize=9)
        axes[row, col].set_ylabel('Frequency', fontsize=9)
        axes[row, col].legend(fontsize=8)
        axes[row, col].grid(True, alpha=0.3)
        axes[row, col].tick_params(labelsize=8)
    
    # Combined score distribution
    top_combined = [(p.serveStrength + p.returnStrength) * p.form * 
                   p.injuryThreshold * (1 - p.injuryProbability) for p in top_players]
    bottom_combined = [(p.serveStrength + p.returnStrength) * p.form * 
                      p.injuryThreshold * (1 - p.injuryProbability) for p in bottom_players]
    
    axes[1, 2].hist(top_combined, alpha=0.7, label=f'Top {top_n}', bins=15, color='blue')
    axes[1, 2].hist(bottom_combined, alpha=0.7, label=f'Bottom {top_n}', bins=15, color='red')
    axes[1, 2].set_title('Combined Score', fontsize=10)
    axes[1, 2].set_xlabel('Combined Score', fontsize=9)
    axes[1, 2].set_ylabel('Frequency', fontsize=9)
    axes[1, 2].legend(fontsize=8)
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].tick_params(labelsize=8)
    
    plt.tight_layout()
    plt.show()

def create_serve_vs_return_scatter(actualRankings):
    """Scatter plot of serve vs return strength colored by ranking"""
    
    serve_strength = [p.serveStrength for p in actualRankings]
    return_strength = [p.returnStrength for p in actualRankings]
    rankings = list(range(len(actualRankings)))
    
    # REDUCED SIZE
    plt.figure(figsize=(8, 6))  # Reduced from (12, 8)
    scatter = plt.scatter(serve_strength, return_strength, c=rankings, 
                         cmap='viridis', alpha=0.7, s=50)
    plt.colorbar(scatter, label='Ranking Position')
    plt.xlabel('Serve Strength', fontsize=10)
    plt.ylabel('Return Strength', fontsize=10)
    plt.title('Serve Strength vs Return Strength (Colored by Ranking)', fontsize=12)
    
    # Add diagonal line to show balanced players
    min_val = min(min(serve_strength), min(return_strength))
    max_val = max(max(serve_strength), max(return_strength))
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', alpha=0.5, label='Balanced Line')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.tick_params(labelsize=9)
    plt.tight_layout()
    plt.show()

def create_rolling_average_plot(actualRankings, window_size=20):
    """Create rolling average plots for smoother trend visualization"""
    
    def rolling_average(data, window):
        return [np.mean(data[max(0, i-window//2):i+window//2+1]) for i in range(len(data))]
    
    serve_strength = [p.serveStrength for p in actualRankings]
    return_strength = [p.returnStrength for p in actualRankings]
    form = [p.form for p in actualRankings]
    
    serve_rolling = rolling_average(serve_strength, window_size)
    return_rolling = rolling_average(return_strength, window_size)
    form_rolling = rolling_average(form, window_size)
    
    # REDUCED SIZE
    plt.figure(figsize=(12, 8))  # Reduced from (15, 10)
    
    plt.subplot(2, 2, 1)
    plt.plot(serve_strength, alpha=0.3, color='blue', label='Raw Data')
    plt.plot(serve_rolling, color='blue', linewidth=2, label=f'Rolling Average (window={window_size})')
    plt.title('Serve Strength by Ranking', fontsize=10)
    plt.xlabel('Ranking Position', fontsize=9)
    plt.ylabel('Serve Strength', fontsize=9)
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tick_params(labelsize=8)
    
    plt.subplot(2, 2, 2)
    plt.plot(return_strength, alpha=0.3, color='green', label='Raw Data')
    plt.plot(return_rolling, color='green', linewidth=2, label=f'Rolling Average (window={window_size})')
    plt.title('Return Strength by Ranking', fontsize=10)
    plt.xlabel('Ranking Position', fontsize=9)
    plt.ylabel('Return Strength', fontsize=9)
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tick_params(labelsize=8)
    
    plt.subplot(2, 2, 3)
    plt.plot(form, alpha=0.3, color='orange', label='Raw Data')
    plt.plot(form_rolling, color='orange', linewidth=2, label=f'Rolling Average (window={window_size})')
    plt.title('Form by Ranking', fontsize=10)
    plt.xlabel('Ranking Position', fontsize=9)
    plt.ylabel('Form', fontsize=9)
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tick_params(labelsize=8)
    
    plt.subplot(2, 2, 4)
    plt.plot(serve_rolling, label='Serve Strength', linewidth=2)
    plt.plot(return_rolling, label='Return Strength', linewidth=2)
    plt.plot(form_rolling, label='Form', linewidth=2)
    plt.title('All Stats Comparison (Rolling Averages)', fontsize=10)
    plt.xlabel('Ranking Position', fontsize=9)
    plt.ylabel('Stat Value', fontsize=9)
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tick_params(labelsize=8)
    
    plt.tight_layout()
    plt.show()

def create_comprehensive_analysis(all_predicted_rankings, all_actual_rankings, method='average'):
    """
    Create comprehensive analysis using aggregated data from all simulations
    
    Args:
        all_predicted_rankings: List of lists containing predicted rankings from all simulations
        all_actual_rankings: List of lists containing actual rankings from all simulations
        method: 'average' or 'median' for aggregation
    """
    print(f"\nCreating comprehensive analysis using {method} across all simulations...")
    
    # Create aggregated rankings
    agg_predicted = create_aggregated_rankings(all_predicted_rankings, method)
    agg_actual = create_aggregated_rankings(all_actual_rankings, method)
    
    # Run all visualization functions with aggregated data
    print("1. Individual stats by ranking...")
    visualize_individual_stats_by_ranking(agg_actual, f"({method.title()} across all simulations)")
    
    print("2. Ranking tier analysis...")
    create_ranking_tier_analysis(agg_actual)
    
    print("5. Serve vs return scatter...")
    create_serve_vs_return_scatter(agg_actual)
    
    print("6. Rolling average plot...")
    create_rolling_average_plot(agg_actual)


"""
Simulation 2 plotting functions
"""



f"""
Simulation 2 plotting functions
"""



from collections import defaultdict

def analyze_strategy_performance(all_actual_rankings, title_suffix=""):
    """
    Analyze how different strategies perform in terms of rankings
    
    Args:
        all_actual_rankings: List of lists containing actual rankings from all simulations
        title_suffix: Additional text for plot titles
    """
    
    # Dictionary to store results for each strategy
    strategy_results = defaultdict(list)
    strategy_rankings = defaultdict(list)
    
    # Collect data from all simulations
    for sim_rankings in all_actual_rankings:
        for rank, player in enumerate(sim_rankings):
            strategy_name = type(player.strategy).__name__
            strategy_results[strategy_name].append(rank + 1)  # Rankings start from 1
            strategy_rankings[strategy_name].append(player)
    
    return strategy_results, strategy_rankings

def plot_strategy_ranking_distributions(strategy_results, title_suffix=""):
    """Create box plots showing ranking distributions for each strategy"""
    
    # REDUCED SIZE
    plt.figure(figsize=(8, 6))  # Reduced from (12, 8)
    
    strategies = list(strategy_results.keys())
    ranking_data = [strategy_results[strategy] for strategy in strategies]
    
    box_plot = plt.boxplot(ranking_data, labels=strategies, patch_artist=True)
    
    # Color the boxes differently
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']
    for patch, color in zip(box_plot['boxes'], colors[:len(strategies)]):
        patch.set_facecolor(color)
    
    plt.title(f'Ranking Distribution by Strategy {title_suffix}', fontsize=12)
    plt.xlabel('Strategy', fontsize=10)
    plt.ylabel('Final Ranking Position', fontsize=10)
    plt.xticks(rotation=45, fontsize=9)
    plt.yticks(fontsize=9)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_strategy_performance_metrics(strategy_results, title_suffix=""):
    """Create bar charts showing average ranking and other metrics for each strategy"""
    
    strategies = list(strategy_results.keys())
    avg_rankings = [np.mean(strategy_results[strategy]) for strategy in strategies]
    median_rankings = [np.median(strategy_results[strategy]) for strategy in strategies]
    std_rankings = [np.std(strategy_results[strategy]) for strategy in strategies]
    
    # REDUCED SIZE
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))  # Reduced from (15, 12)
    fig.suptitle(f'Strategy Performance Metrics {title_suffix}', fontsize=12)
    
    # Average ranking (lower is better)
    axes[0, 0].bar(strategies, avg_rankings, color='skyblue', alpha=0.7)
    axes[0, 0].set_title('Average Ranking by Strategy', fontsize=10)
    axes[0, 0].set_ylabel('Average Ranking', fontsize=9)
    axes[0, 0].tick_params(axis='x', rotation=45, labelsize=8)
    axes[0, 0].tick_params(axis='y', labelsize=8)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Median ranking (lower is better)
    axes[0, 1].bar(strategies, median_rankings, color='lightgreen', alpha=0.7)
    axes[0, 1].set_title('Median Ranking by Strategy', fontsize=10)
    axes[0, 1].set_ylabel('Median Ranking', fontsize=9)
    axes[0, 1].tick_params(axis='x', rotation=45, labelsize=8)
    axes[0, 1].tick_params(axis='y', labelsize=8)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Standard deviation of rankings (consistency)
    axes[1, 0].bar(strategies, std_rankings, color='lightcoral', alpha=0.7)
    axes[1, 0].set_title('Ranking Consistency by Strategy\n(Lower = More Consistent)', fontsize=9)
    axes[1, 0].set_ylabel('Standard Deviation of Rankings', fontsize=8)
    axes[1, 0].tick_params(axis='x', rotation=45, labelsize=8)
    axes[1, 0].tick_params(axis='y', labelsize=8)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Top 50 percentage
    top_50_percentages = []
    for strategy in strategies:
        rankings = strategy_results[strategy]
        top_50_count = sum(1 for rank in rankings if rank <= 50)
        percentage = (top_50_count / len(rankings)) * 100
        top_50_percentages.append(percentage)
    
    axes[1, 1].bar(strategies, top_50_percentages, color='gold', alpha=0.7)
    axes[1, 1].set_title('Percentage of Players in Top 50', fontsize=10)
    axes[1, 1].set_ylabel('Percentage (%)', fontsize=9)
    axes[1, 1].tick_params(axis='x', rotation=45, labelsize=8)
    axes[1, 1].tick_params(axis='y', labelsize=8)
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def comprehensive_strategy_analysis(all_actual_rankings, title_suffix=""):
    """
    Run all strategy analysis functions
    
    Args:
        all_actual_rankings: List of lists containing actual rankings from all simulations with different strategies
        title_suffix: Additional text for plot titles
    """
    
    print("Analyzing strategy performance...")
    strategy_results, strategy_rankings = analyze_strategy_performance(all_actual_rankings, title_suffix)
    
    print("1. Creating ranking distribution plots...")
    plot_strategy_ranking_distributions(strategy_results, title_suffix)
    
    print("2. Creating performance metrics...")
    plot_strategy_performance_metrics(strategy_results, title_suffix)
    
    return strategy_results, strategy_rankings


""" 
Simulation 1:
This simulation is set to all players having the original strategy for tournament selection.
This will help me get plots and answer the question how does skill effect rankings at the
end of the season?
"""

# Main simulation code
simSteps = 50
tempPredicted = []
tempActual = []
all_predicted_rankings = []  # Store actual player objects for each simulation
all_actual_rankings = []     # Store actual player objects for each simulation

# Getting data by simulating season
for i in range(simSteps):   
    print(f'\n\n\n\n Simulation Step {i}')
    # Create new players
    newPlayers = init_players(200)
    assign_strategies(newPlayers, True)
    
    # Copy new players list
    predictedRankings = [player for player in newPlayers]
    
    # Calculate predicted rankings (sorted by servingStrength + returningStrength)
    predictedRankings.sort(key = lambda player: (player.serveStrength + player.returnStrength)*player.form*player.injuryThreshold*(1-player.injuryProbability), reverse=True)
    
    # Simulate season
    newSeason = Season(newPlayers)
    newSeason.simulate_season()
    
    all_actual_rankings.append(newSeason.rankings)
    all_predicted_rankings.append(predictedRankings)

create_comprehensive_analysis(all_predicted_rankings, all_actual_rankings)


"""
Simulation 2:
every one will use different strategies now
"""

# Main simulation code
simSteps = 50
tempPredicted = []
tempActual = []
all_predicted_rankings = []  # Store actual player objects for each simulation
all_actual_rankings = []     # Store actual player objects for each simulation

# Getting data by simulating season
for i in range(simSteps):   
    print(f'\n\n\n\n Simulation Step {i}')
    # Create new players
    newPlayers = init_players(200)
    assign_strategies(newPlayers)
    
    # Copy new players list
    predictedRankings = [player for player in newPlayers]
    
    # Calculate predicted rankings (sorted by servingStrength + returningStrength)
    predictedRankings.sort(key = lambda player: (player.serveStrength + player.returnStrength)*player.form*player.injuryThreshold*(1-player.injuryProbability), reverse=True)
    
    # Simulate season
    newSeason = Season(newPlayers)
    newSeason.simulate_season()
    
    all_actual_rankings.append(newSeason.rankings)
    all_predicted_rankings.append(predictedRankings)

comprehensive_strategy_analysis(all_actual_rankings, "(Multi-Strategy Simulation)")