# A library of sport implementations.

import random

DRAW = 0
WIN = 1
LOSS = 2
     
def basic_game(team1, team2):
    # A template for all games. The game must take two team dictionaries.

    # If the game is won by a team, the result is set to the WIN constant.
    # If the game is drawn, the result is set to the DRAW constant.
    result = WIN

    # If the game has a winner, the winner is set to the name of the winning
    # team and the loser to the name of the losing team. In the event of a
    # draw, order does not matter, but both variables must still be filled.
    winner = team1['Name']
    loser = team2['Name']

    # All extra game statistics are stored in the stats dictionary. The key for
    # each entry is the name of the statistic.
    stats = {}

    # The game must return this information in the following tuple format.
    return (result, winner, loser, stats)

def cricket(team1, team2):
    # Simulate a game of cricket.
    if team1['Strength'] == team2['Strength']:
        result = DRAW
        winner = team1['Name']
        loser = team2['Name']
    else:
        result = WIN
        if team1['Strength'] > team2['Strength']:
            winner = team1['Name']
            loser = team2['Name']
        else:
            winner = team2['Name']
            loser = team1['Name']

    # Generate winner statistics
    winning_runs = random.randint(120, 180)
    winning_wickets = random.randint(5, 10)
    winning_score = str(winning_wickets) + '/' + str(winning_runs)

    if result == DRAW:
        losing_runs = winning_runs
    else:
        losing_runs = random.randint(80, winning_runs)

    losing_wickets = random.randint(5, 10)
    losing_score = str(losing_wickets) + '/' + str(losing_runs)

    stats = {'Winning Score': winning_score,
             'Losing Score': losing_score}

    return (result, winner, loser, stats)

def football(team1, team2):
    # Simulate a game of football (soccer).
    if team1['Strength'] == team2['Strength']:
        result = DRAW
        winner = team1['Name']
        loser = team2['Name']
    else:
        result = WIN
        if team1['Strength'] > team2['Strength']:
            winner = team1['Name']
            loser = team2['Name']
        else:
            winner = team2['Name']
            loser = team1['Name']

    # Generate winner statistics
    winning_goals = random.randint(1, 3)

    if result == DRAW:
        losing_goals = winning_goals
    else:
        losing_goals = random.randint(0, winning_goals - 1)

    stats = {'Winning Score': winning_goals,
             'Losing Score': losing_goals}

    return (result, winner, loser, stats)

# Define default characteristics of each game.
games = {'Cricket': {'parameters': ['Name', 'Strength'],
                     'function_name':cricket,
                     'settings': {'max_runs':'180',
                                  'min_runs':'120'}},
         'Football (soccer)': {'parameters': ['Name', 'Strength', 'Goals'],
                               'function_name':football,
                               'settings': {'max_goals':'3',
                                            'min_goals':'1'}}}