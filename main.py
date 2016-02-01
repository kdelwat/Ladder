import csv
from operator import itemgetter
from tabulate import tabulate
import random
import math

DRAW = 0
WIN = 1
LOSS = 2

output = []


class Ladder:

    def __init__(self, rounds, teams, points={WIN: 2, DRAW: 1, LOSS: 0}):
        self.rounds = rounds
        self.points = points
        self.init_ladder(teams)

    def init_ladder(self, teams):
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


def cricket(team1, team2):
    if team1['Strength'] == team2['Strength']:
        result = DRAW
        winner = team1['Name']
        loser = team2['Name']
    elif team1['Strength'] > team2['Strength']:
        result = WIN
        winner = team1['Name']
        loser = team2['Name']
    else:
        result = WIN
        winner = team2['Name']
        loser = team1['Name']

    winning_runs = random.randint(120, 180)
    winning_score = str(random.randint(5, 10)) + '/' + str(winning_runs)
    if result == DRAW:
        losing_score = str(random.randint(5, 10)) + '/' + str(winning_runs)
    else:
        losing_score = str(random.randint(5, 10)) + '/' + str(random.randint(80, winning_runs))

    stats = {'Winning Score': winning_score,
             'Losing Score': losing_score}
    return (result, winner, loser, stats)


def play(team1, team2, game, ladder):
    print(team1)
    print(team2)
    result = game(team1, team2)
    if ladder is not None:
        ladder.record_result(result)
    return result


def rotate_except_first(l):
    new = [l[0], l[-1]]
    for i in range(2, len(l)):
        new.append(l[i-1])
    return new


def elimination(teams):
    number_of_rounds = int(math.log(len(teams), 2))

    for n in range(number_of_rounds):
        matches = loop_matches(teams)

        # Play all matches in round
        results = [play(match[0], match[1], cricket, None) for match in matches]

        for result in results:
            store(result, "Finals " + str(round + 1))

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


def round_robin(teams):
    '''Generate a round-robin fixture using the algorithm from
       https://en.wikipedia.org/wiki/Round-robin_tournament'''
    if len(teams) % 2 != 0:
        teams.append('BYE')

    number_of_rounds = len(teams) - 1
    rounds = []
    for i in range(number_of_rounds):
        matches = loop_matches(teams)
        rounds.append(matches)
        teams = rotate_except_first(teams)
    return rounds


def load_teams(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        teams = [team for team in reader]
    for team in teams:
        team['Strength'] = int(team['Strength'])
    return teams


def store(result, round_no):
    print("Storing", result)
    row = {'Round': round_no}
    if result[0] == DRAW:
        row['Winner'] = result[1] + ', ' + result[2]
        row['Loser'] = '-'
    else:
        row['Winner'] = result[1]
        row['Loser'] = result[2]
    for stat, value in result[3].items():
        row[stat] = value

    output.append(row)


def output_data(filename):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=["Round", "Winner", "Loser", "Winning Score", "Losing Score"])
        writer.writeheader()
        writer.writerows(output)


def play_fixture(fixture, ladder):
    for no, round in enumerate(fixture):
        for match in round:
            result = play(match[0], match[1], cricket, ladder)
            store(result, no + 1)


def simple_simulate(teams, structure, finals_structure, final_n=4):
    # Simulate a league using the given teams, structure, finals structure,
    # and number of league winners to move on to the finals.
    fixture = structure(teams)
    ladder = Ladder(len(fixture), teams)

    play_fixture(fixture, ladder)

    ladder.print_ladder()

    finalist_names = [team['Name'] for team in ladder.top(final_n)]
    finalists = [team for team in teams if team['Name'] in finalist_names]

    print(finals_structure(finalists))
    output_data('out.csv')

teams = load_teams('data.csv')
simple_simulate(teams, round_robin, elimination)
