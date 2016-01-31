import csv
from operator import itemgetter

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
        print(self.ladder)


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
