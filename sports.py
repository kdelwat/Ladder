# A library of sport implementations.

import random

DRAW = 0
WIN = 1
LOSS = 2

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
