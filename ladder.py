import csv
import math
from operator import itemgetter
from tabulate import tabulate

import sports

DRAW = 0
WIN = 1
LOSS = 2

output = []
teams = {}


class Ladder:

    def __init__(self, rounds, teams, points={WIN: 2, DRAW: 1, LOSS: 0}):
        self.rounds = rounds
        self.points = points
        self.init_ladder(teams)

    def init_ladder(self, teams):
        # Create a blank ladder with an entry for each team, including W/L/D/P
        # statistics
        self.ladder = []

        for team in teams:
            entry = {}
            entry['Name'] = team
            entry['Win'] = 0
            entry['Loss'] = 0
            entry['Draw'] = 0
            entry['Points'] = 0
            self.ladder.append(entry)

    def record_result(self, result):
        if result[0] == WIN:
            self.record_win(result[1])
            self.record_loss(result[2])
        elif result[0] == DRAW:
            self.record_draw(result[1])
            self.record_draw(result[2])
        else:
            raise ValueError('Result type not supported!')

    def team_index(self, name):
        # Get the index of a team in the ladder by a given name.
        for index, team in enumerate(self.ladder):
            if team['Name'] == name:
                return index
        else:
            raise KeyError('Team ' + str(name) + ' not found in ladder!')

    def record_win(self, team):
        self.ladder[self.team_index(team)]['Win'] += 1
        self.ladder[self.team_index(team)]['Points'] += self.points[WIN]

    def record_loss(self, team):
        self.ladder[self.team_index(team)]['Loss'] += 1
        self.ladder[self.team_index(team)]['Points'] += self.points[LOSS]

    def record_draw(self, team):
        self.ladder[self.team_index(team)]['Draw'] += 1
        self.ladder[self.team_index(team)]['Points'] += self.points[DRAW]

    def sort_ladder(self):
        self.ladder.sort(key=itemgetter('Points'), reverse=True)

    def top(self, n):
        # Return top n teams in ladder.
        self.sort_ladder()
        return self.ladder[:n]

    def print_ladder(self):
        self.sort_ladder()
        printable = [['Name', 'Win', 'Loss', 'Draw', 'Points']]

        for row in self.ladder:
            printable.append([row['Name'],
                              row['Win'],
                              row['Loss'],
                              row['Draw'],
                              row['Points']])

        print(tabulate(printable, headers='firstrow'))


def play(team1, team2, game, ladder=None):
    # Return the result of a match played between two teams according to
    # the rules of a given game. If a ladder is supplied, the result is
    # recorded in the ladder.
    
    global teams
    
    # Get result and new teams dictionary back from game
    result, teams = game['function_name'](team1, team2, teams, game['settings'])

    if ladder is not None:
        ladder.record_result(result)

    return result


def rotate_except_first(l):
    # Rotate a list of teams excluding the first team.
    # For example,
    # 1 2 3 4 5 6 -> 1 6 2 3 4 5
    new = [l[0], l[-1]]
    for i in range(2, len(l)):
        new.append(l[i-1])
    return new


def elimination(teams, game, settings, ladder):
    '''Play a simple elimination fixture for the given teams.'''
    
    # Get the top n teams from the ladder to play in fixture
    final_n = settings['top_teams']

    finalists = [team['Name'] for team in ladder.top(final_n)]
    
    number_of_rounds = int(math.log(len(finalists), 2))

    for n in range(number_of_rounds):
        matches = loop_matches(finalists)

        # Play all matches in round
        results = [play(match[0], match[1], game) for match in matches]

        for result in results:
            store(result, 'Finals ' + str(n + 1))

            # Output match
            print('\n' + result[1] + ' vs ' + result[2])
            print('Winner:', result[1])

            # Eliminate losing teams
            finalists = [finalist for finalist in finalists if finalist != result[2]]

    return finalists


def loop_matches(teams):
    # Split the list of teams into two halves and them zip them in matches.
    # For example, 1 2 3 4 5 6, or:
    # 1 2 3
    # 6 5 4
    # Would become,
    # (1, 6), (2, 5), (3, 4)
    return list(zip(teams[:len(teams)//2], reversed(teams[len(teams)//2:])))


def round_robin(teams, settings):
    '''Generate a round-robin fixture using the algorithm from
    https://en.wikipedia.org/wiki/Round-robin_tournament. Teams
    will play each other n times.

    Add a dummy team to support byes in competitions with an uneven number
    of teams.'''
    
    # Get list of team names, adding BYE team if necessary
    team_names = list(teams.keys())
    
    if len(team_names) % 2 != 0:
        team_names.append('BYE')
    
    number_of_rounds = len(team_names) - 1
    rounds = []
    
    for _ in range(settings['revolutions']):
        for r in range(number_of_rounds):
            matches = loop_matches(team_names)
            rounds.append(matches)
            team_names = rotate_except_first(team_names)

    return rounds


def convert_to_int(n):
    try:
        return int(n)
    except ValueError:
        return n

def load_teams(filename):
    '''Load teams from csv file filename as array'''

    with open(filename) as f:
        reader = csv.reader(f)
        teams = [team for team in reader]

    return teams

def save_teams(team_array, filename):
    '''Saves team_array to filename.'''
    
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        
        for row in team_array:
            writer.writerow(row)
    
def add_teams(table):
    '''Recieves a table from the GUI and converts it into a list of team 
    dictionaries.'''

    # Isolate field list and remove name field
    fields = table.pop(0)
    fields.pop(0)
    
    # Loop through teams, converting each to dictionary and adding them to 
    # global teams list
    for row in table:
        name = row.pop(0)
        
        team_attributes = {}

        for field in zip(fields, row):
            team_attributes[field[0]] = convert_to_int(field[1])

        teams[name] = team_attributes


def store(result, round_no):
    # Format result into list and store in output buffer.
    row = {'Round': round_no}

    if result[0] == DRAW:
        row['Winner'] = result[1] + ', ' + result[2]
        row['Loser'] = '-'
    else:
        row['Winner'] = result[1]
        row['Loser'] = result[2]

    # Add all statistics.
    for stat, value in result[3].items():
        row[stat] = value

    output.append(row)


def output_data(filename):
    # Flush output buffer to filename.
    with open(filename, 'w') as f:
        # Add mandatory field names
        fieldnames = ['Round', 'Winner', 'Loser']

        # Add all other field names
        fieldnames.extend([field for field in output[0].keys()
                           if field not in fieldnames])

        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(output)


def play_fixture(fixture, ladder, game):
    # Take a given fixture of matches (a list of lists of matches).
    # Play each round, getting the result using the specified game
    # and store the result.
    for round_number, round_matches in enumerate(fixture):
        for match in round_matches:
            result = play(match[0], match[1], game, ladder)
            store(result, round_number + 1)


def clean_dictionary(dic):
    '''Convert each value in dictionary to int if possible.'''
    for key in dic:
        dic[key] = convert_to_int(dic[key])
    return dic

# Define default characteristics of each tournament and finals structure.
tournament_structures = {'Round Robin': {'function_name':round_robin,
                                         'settings': {'revolutions':'1'}}}

finals_structures = {'Elimination': {'function_name':elimination,
                                     'settings': {'top_teams':'4'}}}

def simple_simulate(teams=teams, game=sports.games['Cricket'], structure=tournament_structures['Round Robin'], finals_structure=finals_structures['Elimination'], final_n=4):
    '''Simulate a league using the given teams, game, structure, finals
    structure, and number of league winners to move on to the finals.'''

    # Sanitise settings by converting all fields possible to int.
    game['settings'] = clean_dictionary(game['settings'])
    structure['settings'] = clean_dictionary(structure['settings'])
    finals_structure['settings'] = clean_dictionary(finals_structure['settings'])    
        
    fixture = structure['function_name'](teams, structure['settings'])
    ladder = Ladder(len(fixture), teams)
    
    play_fixture(fixture, ladder, game)

    ladder.print_ladder()

    finalist_names = [team['Name'] for team in ladder.top(final_n)]
    finalists = [team for team in teams if team['Name'] in finalist_names]

    finals_structure['function_name'](finalists, game, finals_structure['settings'], ladder)
    
    output_data('out.csv')

def simulate_season(teams=teams, game=sports.games['Cricket'], structure=tournament_structures['Round Robin']):
    
    # Sanitise settings by converting all fields possible to int.
    game['settings'] = clean_dictionary(game['settings'])
    structure['settings'] = clean_dictionary(structure['settings'])
    
    fixture = structure['function_name'](teams, structure['settings'])

    ladder = Ladder(len(fixture), teams)
    
    play_fixture(fixture, ladder, game)

    ladder.print_ladder()
    
    output_data('out.csv')
    
    return ladder

def simulate_finals(ladder, teams=teams, game=sports.games['Cricket'], structure=finals_structures['Elimination']):
    
    # Sanitise settings by converting all fields possible to int.
    structure['settings'] = clean_dictionary(structure['settings'])
    
    structure['function_name'](teams, game, structure['settings'], ladder)
    
    output_data('out.csv')
    
# simple_simulate(teams, football, round_robin, elimination)


#teams = {'Melbourne Stars': {'Strength': 8},
# 'Melbourne Renegades': {'Strength': 5},
# 'Sydney Thunder': {'Strength': 10},
# 'Sydney Sixers': {'Strength': 6},
# 'Adelaide Strikers': {'Strength': 7},
# 'Hobart Hurricanes': {'Strength': 4},
# 'Brisbane Heat': {'Strength': 5},
# 'Perth Scorchers': {'Strength': 7}}

#ladder = simulate_season(teams=teams)
#simulate_finals(ladder, teams=teams)