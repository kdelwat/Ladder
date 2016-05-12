import csv
import math
from operator import itemgetter
from tabulate import tabulate

from sports import cricket, football

DRAW = 0
WIN = 1
LOSS = 2

output = []
teams = []

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
            entry['Name'] = team['Name']
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
    result = game['function_name'](team1, team2, game['settings'])

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


def elimination(teams, game):
    # Play a simple elimination fixture for the given teams.

    number_of_rounds = int(math.log(len(teams), 2))

    for n in range(number_of_rounds):
        matches = loop_matches(teams)

        # Play all matches in round
        results = [play(match[0], match[1], game) for match in matches]

        for result in results:
            store(result, 'Finals ' + str(n + 1))

            # Output match
            print('\n' + result[1] + ' vs ' + result[2])
            print('Winner:', result[1])

            # Eliminate losing teams
            teams = [team for team in teams if team['Name'] != result[2]]

    return teams


def loop_matches(teams):
    # Split the list of teams into two halves and them zip them in matches.
    # For example, 1 2 3 4 5 6, or:
    # 1 2 3
    # 6 5 4
    # Would become,
    # (1, 6), (2, 5), (3, 4)
    return list(zip(teams[:len(teams)//2], reversed(teams[len(teams)//2:])))


def round_robin(teams, n=2):
    # Generate a round-robin fixture using the algorithm from
    # https://en.wikipedia.org/wiki/Round-robin_tournament. Teams
    # will play each other n times.

    # Add a dummy team to support byes in competitions with an uneven number
    # of teams.
    if len(teams) % 2 != 0:
        teams.append('BYE')

    number_of_rounds = len(teams) - 1
    rounds = []

    for _ in range(n):
        for r in range(number_of_rounds):
            matches = loop_matches(teams)
            rounds.append(matches)
            teams = rotate_except_first(teams)

    return rounds


def convert_to_int(n):
    try:
        return int(n)
    except ValueError:
        return n


def load_teams(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        teams = [team for team in reader]

    # Convert data to integer if possible.
    for team in teams:
        for key in team:
            team[key] = convert_to_int(team[key])

    return teams

def add_teams(table):
    '''Recieves a table from the GUI and converts it into a list of team 
    dictionaries.'''
    
    # Isolate field list
    fields = table.pop(0)
    
    # Loop through teams, converting each to dictionary and adding them to 
    # global teams list
    for row in table:
        team = {}

        for field in zip(fields, row):
            team[field[0]] = field[1]

        teams.append(team)

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


def simple_simulate(teams=teams, game=football, structure=round_robin, finals_structure=elimination, final_n=4):
    '''Simulate a league using the given teams, game, structure, finals
    structure, and number of league winners to move on to the finals.'''
    fixture = structure(teams)
    ladder = Ladder(len(fixture), teams)
    
    # Sanitise settings by converting all fields possible to int.
    for key in game['settings']:
        game['settings'][key] = convert_to_int(game['settings'][key])
        
    play_fixture(fixture, ladder, game)

    ladder.print_ladder()

    finalist_names = [team['Name'] for team in ladder.top(final_n)]
    finalists = [team for team in teams if team['Name'] in finalist_names]

    finals_structure(finalists, game)
    output_data('out.csv')

# teams = load_teams('data.csv')

# simple_simulate(teams, football, round_robin, elimination)