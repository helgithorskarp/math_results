"""Independent set-based audit of the modulus-539 fibre certificate.

Run from any directory with Python 3.11+: python3 -B audit.py.
No imports from the reviewed source are used.
"""

from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "schur6_composite_multiplier_obstructions"
Z11 = frozenset(range(11))


def pair(x):
    return min(x, 7 - x) - 1


def add(x, y):
    return frozenset((a + b) % 11 for a in x for b in y)


def fibres(row):
    return {a: row[pair(a)] if a <= 3 else frozenset((-b) % 11 for b in row[pair(a)])
            for a in range(1, 7)}


def valid(row):
    f = fibres(row)
    return all(not (add(f[a], f[b]) & f[(a + b) % 7])
               for a, b in product(range(1, 7), repeat=2) if (a + b) % 7)


def rows_by_sizes(sizes):
    # The first adjacent size-four doubling pair determines the next fibre.
    i = next(j for j in range(3) if sizes[j] == sizes[(j + 1) % 3] == 4)
    j = (i + 1) % 3
    k = 3 - i - j
    found = []
    for x in map(frozenset, combinations(range(11), 4)):
        sx = add(x, x)
        if len(sx) != 7:
            continue
        y = Z11 - sx
        if i in (1, 2):
            y = frozenset((-t) % 11 for t in y)
        for z in map(frozenset, combinations(range(11), sizes[k])):
            row = [None, None, None]
            row[i], row[j], row[k] = x, y, z
            if valid(row):
                found.append(tuple(row))
    return found


def size_profiles():
    # Cauchy-Davenport gives |X+Y| >= min(11, |X|+|Y|-1).
    admissible = []
    for row in product(range(12), repeat=3):
        for a, b in product(range(1, 7), repeat=2):
            c = (a + b) % 7
            if c:
                u, v, w = (row[pair(t)] for t in (a, b, c))
                if u and v and min(11, u + v - 1) + w > 11:
                    break
        else:
            admissible.append(row)
    aset = set(admissible)
    profiles = set()
    for x in admissible:
        for y in admissible:
            z = tuple(11 - x[i] - y[i] for i in range(3))
            if z in aset:
                profiles.add(tuple(sorted((x, y, z))))
    return len(admissible), sorted(profiles)


def check_words():
    out = {}
    for row in json.loads((SOURCE / "witnesses.json").read_text()):
        n = row["modulus"]
        word = [int(x) for x in row["word"]]
        assert len(word) == n - 1 and set(word) == set(range(row["colours"]))
        for x in range(1, n):
            assert word[x - 1] == word[n - x - 1]
            assert word[row["multiplier"] * x % n - 1] == row["permutation"][word[x - 1]]
            for y in range(x, n):
                z = (x + y) % n
                if z:
                    assert not (word[x - 1] == word[y - 1] == word[z - 1])
        out[row["name"]] = (n, row["colours"])
    return out


def main():
    count, profiles = size_profiles()
    assert count == 206 and len(profiles) == 7
    dense = {sizes: rows_by_sizes(sizes)
             for sizes in ((4, 4, 4), (3, 4, 4), (4, 3, 4), (4, 4, 3))}
    assert {str(k): len(v) for k, v in dense.items()} == {
        '(4, 4, 4)': 5, '(3, 4, 4)': 30, '(4, 3, 4)': 30, '(4, 4, 3)': 30}
    assert all(0 not in s for row in dense[4, 4, 4] for s in row)
    covers = 0
    last = set(dense[4, 4, 3])
    for x in dense[3, 4, 4]:
        for y in dense[4, 3, 4]:
            if any(x[i] & y[i] for i in range(3)):
                continue
            z = tuple(Z11 - x[i] - y[i] for i in range(3))
            covers += z in last
    assert covers == 0
    print(json.dumps({'admissible_size_rows': count, 'profiles': profiles,
                      'dense_counts': {str(k): len(v) for k, v in dense.items()},
                      'balanced_covers': covers, 'witnesses': check_words()},
                     sort_keys=True))


if __name__ == '__main__':
    main()
