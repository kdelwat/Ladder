**Warning: this is highly WIP! Please don't use if you're afraid of losing
functionality or data!**

# Ladder

A real simulator for fake sports. Teams can be defined using arbitrary values,
and are then played off against each other in a league, including a main season
and finals series. A summary of results is outputted in the interface, and a CSV
file named `out.csv` is created detailing the outcomes of all games played.

![An example session](https://i.imgur.com/4FjCTUv.png)

## Installation Instructions

1. Clone the repository with `git clone https://github.com/kdelwat/Ladder.git`.
2. Ensure the dependencies are installed.
3. Navigate to the repository folder and run `python main.py`.
4. Open `http://127.0.0.1:8081/` in your browser.

## Dependencies

- Python 3
- [tabulate](https://pypi.python.org/pypi/tabulate/0.7.5)
- [remi](https://github.com/dddomodossola/remi)

## Usage

The GUI itself should be fairly self-explanatory. The "Load Teams" button accepts a CSV file describing the league's teams in the following format:

```
Name,Strength
Melbourne Stars,8
Melbourne Renegades,5
Sydney Thunder,10
Sydney Sixers,6
Adelaide Strikers,7
Hobart Hurricanes,4
Brisbane Heat,5
Perth Scorchers,7
```

It is important to note that, apart from name, *any* field can be used to
provide information about teams, as long as the chosen sport supports that
field.

## Extending

The main benefit of using *Ladder* is its extensibility. New sports can be
created quickly.

In `sports.py`, the sport is defined as a function. The basic template for a sport is as follows:

```python
def basic_game(team1, team2, teams, settings):
    # A template for all games. The game must take two team dictionaries.

    # If the game is won by a team, the result is set to the WIN constant.
    # If the game is drawn, the result is set to the DRAW constant.
    result = WIN

    # If the game has a winner, the winner is set to the name of the winning
    # team and the loser to the name of the losing team. In the event of a
    # draw, order does not matter, but both variables must still be filled.
    winner = team1
    loser = team2

    # All extra game statistics are stored in the stats dictionary. The key for
    # each entry is the name of the statistic.
    stats = {}

    # The game must return this information in the following tuple format.
    return (result, winner, loser, stats)
```

The new function must then be added to the `games` dictionary at the bottom of the file, in the following form:

```python
'Name': {'parameters': [],
         'function_name': fn,
         'settings': {}}

```

In this form,

- `Name` is the human-readable name of the sport which will be automatically
  added to the selection dropdown.
- `parameters` is a list of parameters included for each team. For cricket, the
  default is `['Name', 'Strength']`, but this can be changed to suit any data.
- `function_name` is the simulation function itself.
- `settings` is a dictionary, where each key-value pair is an option and its
  value.

A simple example of a full sport is displayed below.

```python
def football(team1, team2, teams, settings):
    '''Simulate a game of football (soccer).'''

    if teams[team1]['Strength'] == teams[team2]['Strength']:
        result = DRAW
        winner = team1
        loser = team2
    else:
        result = WIN
        if teams[team1]['Strength'] > teams[team2]['Strength']:
            winner = team1
            loser = team2
        else:
            winner = team2
            loser = team1

    # Generate winner statistics
    winning_goals = random.randint(1, 3)

    if result == DRAW:
        losing_goals = winning_goals
    else:
        losing_goals = random.randint(0, winning_goals - 1)

    stats = {'Winning Score': winning_goals,
             'Losing Score': losing_goals}

    return ((result, winner, loser, stats), teams)

games = {'Football (soccer)': {'parameters': ['Name', 'Strength', 'Goals'],
                               'function_name': football,
                               'settings': {'max_goals': '3',
                                            'min_goals': '1'}}}
```