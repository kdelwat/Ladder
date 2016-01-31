import csv

DRAW = 0
WIN = 1
LOSS = 2


class Ladder:

    def __init__(self, rounds, teams, points={WIN: 2, DRAW: 1, LOSS: 0}):
        self.rounds = rounds
        self.points = points
        self.init_ladder(teams)

    def init_ladder(self, teams):
        self.ladder = {}
        for team in teams:
            entry = {}
            entry['Win'] = 0
            entry['Loss'] = 0
            entry['Draw'] = 0
            entry['Points'] = 0
            self.ladder[team['Name']] = entry

    def record_result(self, result):
        if result[0] == WIN:
            self.ladder[result[1]]['Win'] += 1
            self.ladder[result[1]]['Points'] = self.points[WIN]

            self.ladder[result[2]]['Loss'] += 1
            self.ladder[result[2]]['Points'] = self.points[LOSS]

        elif result[0] == DRAW:
            self.ladder[result[1]]['Draw'] += 1
            self.ladder[result[1]]['Points'] = self.points[DRAW]

            self.ladder[result[2]]['Draw'] += 1
            self.ladder[result[2]]['Points'] = self.points[DRAW]

        else:
            raise ValueError('Result type not supported!')

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
ladder.print_ladder()
