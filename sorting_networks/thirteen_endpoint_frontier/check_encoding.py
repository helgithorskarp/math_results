"""Exact small-word controls for transitions and touch-count constraints."""
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent / 'thirteen_prefix_frontier'))
from filtered_encoding import Encoding


def model(word, x, y=None):
    row = [x >> i & 1 for i in range(3)] if y is None else [
        2 if x >> i & 1 else 1 if y >> i & 1 else 0 for i in range(3)]
    high = low = mixed = 0
    for a, b in word:
        high += bool(row[a] or row[b])
        low += not (row[a] and row[b])
        mixed += row[a] != 1 or row[b] != 1
        if row[a] > row[b]:
            row[a], row[b] = row[b], row[a]
    return row, high, low, mixed


def encoding(m):
    return Encoding(3, m, constants=True, intervals=False,
                    pure_sides=False, disjoint_lex=False)


def main():
    pairs = list(itertools.combinations(range(3), 2))
    sorting = touch = mixed = 0
    for word in itertools.product(pairs, repeat=3):
        enc = encoding(3)
        for x in range(8):
            enc.add_row(x)
        expected = all(model(word, x)[0] == sorted(model([], x)[0]) for x in range(8))
        assert enc.solver.solve(assumptions=enc.assume_gates(word)) == expected
        enc.solver.delete(); sorting += 1
        for x in range(8):
            for polarity, count in ((1, model(word, x)[1]), (0, model(word, x)[2])):
                for bound in (count, count - 1):
                    enc = encoding(3); enc.add_row(x, final_sorted=False)
                    enc.touch_bound(x, bound, polarity)
                    assert enc.solver.solve(assumptions=enc.assume_gates(word)) == (count <= bound)
                    enc.solver.delete(); touch += 1
    for word in itertools.product(pairs, repeat=2):
        for x in range(8):
            for y in range(8):
                if x & ~y:
                    continue
                count = model(word, x, y)[3]
                for bound in (count, count - 1):
                    enc = encoding(2)
                    enc.add_row(x, final_sorted=False); enc.add_row(y, final_sorted=False)
                    enc.mixed_touch_bound(x, y, bound)
                    assert enc.solver.solve(assumptions=enc.assume_gates(word)) == (count <= bound)
                    enc.solver.delete(); mixed += 1
    print(json.dumps({'three_wire_sorting_words': sorting,
                      'one_threshold_controls': touch, 'mixed_controls': mixed,
                      'status': 'Exact forced-word controls passed.'}))


if __name__ == '__main__':
    main()
