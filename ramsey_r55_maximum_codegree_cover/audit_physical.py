"""Audit the joined input against four direct, fully fixed physical frames.

The parser projects an actual DIMACS file under each choice. The reference
enumerates K5s in each fixed frame independently of physical.substitution().
Equal ordered hashes and counts check the exact four-way input interface.
"""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time
from graphs import frame, require


def record(h, values):
    h.update((' '.join(map(str, values)) + ' 0\n').encode('ascii'))


def projected_file(path, a_choice, seed_choice):
    h = sha256()
    count = 0
    raw_count = 0
    with path.open() as f:
        header = f.readline().split()
        require(header[:3] == ['p', 'cnf', '785'], 'DIMACS header')
        for line in f:
            values = list(map(int, line.split()))
            require(values and values[-1] == 0 and 0 not in values[:-1], 'clause')
            values.pop()
            require(all(1 <= abs(x) <= 785 for x in values), 'variable range')
            raw_count += 1
            out = []
            satisfied = False
            for x in values:
                if abs(x) <= 2:
                    value = a_choice if abs(x) == 1 else seed_choice
                    if value == (x > 0):
                        satisfied = True
                else:
                    out.append(x)
            if not satisfied:
                require(out, 'empty projected clause')
                record(h, out)
                count += 1
        require(raw_count == int(header[3]), 'DIMACS clause count')
    return {'clauses': count, 'ordered_clause_sha256': h.hexdigest()}


def fixed_reference(seed, kind):
    a = frame(seed, kind)
    h = sha256()
    count = 0
    for vertices in combinations(range(43), 5):
        pairs = list(combinations(vertices, 2))
        for color in (1, 0):
            if any(((a[u] >> v) & 1) != color for u, v in pairs if v < 16):
                continue
            values = [(v * (v - 1) // 2 + u - 117) * (-1 if color else 1)
                      for u, v in pairs if v >= 16]
            require(values, 'bad fixed frame')
            values.sort(key=abs)
            record(h, values)
            count += 1
    return {'clauses': count, 'ordered_clause_sha256': h.hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cnf', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    results = []
    for seed in ('5', '6'):
        for kind in ('A', 'T'):
            actual = projected_file(args.cnf, kind == 'A', seed == '5')
            expected = fixed_reference(seed, kind)
            require(actual == expected, f'physical input mismatch: {seed}/{kind}')
            results.append({'seed': seed, 'kind': kind, **actual})
    print(json.dumps({'status': 'ALL_FOUR_COMPLETE_PHYSICAL_INPUTS_MATCH',
                      'frames': results, 'seconds': time.monotonic() - started,
                      'terminal_physical_decisions': 0}, indent=2))


if __name__ == '__main__':
    main()
