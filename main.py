import csv
from operator import itemgetter
from tabulate import tabulate

DRAW = 0
WIN = 1
LOSS = 2


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
            raise KeyError('Team not found in ladder!')

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

    def print_ladder(self):
        printable = [['Name', 'Win', 'Loss', 'Draw', 'Points']]

        for row in self.ladder:
            printable.append([row['Name'],
                              row['Win'],
                              row['Loss'],
                              row['Draw'],
                              row['Points']])

        print(tabulate(printable, headers="firstrow"))


def cricket(team1, team2):
    if team1['Strength'] == team2['Strength']:
        return (DRAW, team1, team2)
    elif team1['Strength'] > team2['Strength']:
        winner = team1['Name']
        loser = team2['Name']
    else:
        winner = team2['Name']
        loser = team1['Name']
    return (WIN, winner, loser)


def play(team1, team2, game):
    result = game(team1, team2)
    ladder.record_result(result)


def rotate_except_first(l):
    new = [l[0], l[-1]]
    for i in range(2, len(l)):
        new.append(l[i-1])
    return new


def round_robin(teams):
    '''Generate a round-robin fixture using the algorithm from
       https://en.wikipedia.org/wiki/Round-robin_tournament'''
    if len(teams) % 2 != 0:
        teams.append("BYE")

    number_of_rounds = len(teams) - 1
    rounds = []
    for i in range(number_of_rounds):
        # Split the list of teams into two halves and them zip them in matches.
        # For example, 1 2 3 4 5 6, or:
        # 1 2 3
        # 6 5 4
        # Would become,
        # (1, 6), (2, 5), (3, 4)
        matches = list(zip(teams[:len(teams)//2], reversed(teams[len(teams)//2:])))

        rounds.append(matches)
        teams = rotate_except_first(teams)
    return rounds


def load_teams(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        return [team for team in reader]

teams = load_teams('data.csv')
ladder = Ladder(3, teams)
play(teams[0], teams[1], cricket)
play(teams[3], teams[4], cricket)
ladder.sort_ladder()
ladder.print_ladder()

print(round_robin(['A', 'B', 'C', 'D', 'E']))
