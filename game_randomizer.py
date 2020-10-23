from random import sample
import csv
from dataclasses import dataclass
from ast import literal_eval
from itertools import groupby
from functools import partial
import sys

@dataclass
class Game:
    name: str
    owner: str
    weight: int
    max_players: int
    known: bool
    preset: bool
    veto: bool

# filter functions
no_veto = lambda games: (g for g in games if not g.veto)
max_players = lambda max_num, games: (g for g in games if g.max_players > max_num)
by_weight = lambda weight, games: (g for g in games if g.weight == weight)
known = lambda games: (g for g in games if g.known)
unknown = lambda games: (g for g in games if not g.known)

def pipe(first, *args):
    for fn in args:
        first = fn(first)
    return first

def read_csv(filename='games.csv'):
    csv_translator = [str, str, str, int, literal_eval, literal_eval, literal_eval]
    result=[]
    with open(filename, newline='') as csvfile:
        next(csvfile, None)
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            data = [t(v) for (v, t) in zip(row, csv_translator)]
            result.append(Game(*data))
    return result

def format_random(items, num_games):
    return '\r\n'.join('- ' + g.name for g in sample(items, num_games))

def main(player_count):

    all_games = read_csv()    

    no_veto_no_single = pipe(all_games, known, no_veto, partial(max_players, 2), list)
    no_veto_no_single.sort(key=lambda g: g.weight)
    games_by_weight = groupby(no_veto_no_single, lambda g: g.weight)

    heavy_to_learn = pipe(all_games, unknown, no_veto, partial(by_weight, 'Heavy'), list)
    medium_to_learn = pipe(all_games, unknown, no_veto, partial(by_weight, 'Medium'), list)

    print(f"Selecting random games for {player_count} players.")
    print("")

    num_games = 2 if player_count <= 8 else 3

    for weight, games in games_by_weight:
        possible = list(games)
        selected = format_random(possible, num_games)
        print(f"Your {weight} game choices are (out of {len(possible)}):\r\n{selected}\r\n")

    print(f"\r\nYour medium games to learn are:\r\n{format_random(medium_to_learn, 2)}")
    print(f"\r\nYour heavy games to learn are:\r\n{format_random(heavy_to_learn, 2)}")

if __name__ == '__main__':
    PLAYER_COUNT = 6 if len(sys.argv) == 1 else int(sys.argv[1])
    main(PLAYER_COUNT)
