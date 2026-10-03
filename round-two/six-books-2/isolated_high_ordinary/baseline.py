"""Literal ordinary-spine replay of the known primary 21-vertex fixture."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inspect(rows, red_cap=3, blue_cap=6):
    n = len(rows)
    require(n == 21 and all(len(row) == n and set(row) <= {'0', '1'}
                           for row in rows), 'Invalid matrix domain')
    require(all(rows[a][a] == '0' for a in range(n)), 'Nonzero diagonal')
    require(all(rows[a][b] == rows[b][a] for a, b in combinations(range(n), 2)),
            'Asymmetric matrix')
    red = blue = max_red = max_blue = 0
    violations = 0
    for a, b in combinations(range(n), 2):
        color = rows[a][b]
        pages = sum(rows[a][c] == color and rows[b][c] == color
                    for c in range(n) if c not in (a, b))
        if color == '1':
            red += 1
            max_red = max(max_red, pages)
            violations += pages > red_cap
        else:
            blue += 1
            max_blue = max(max_blue, pages)
            violations += pages > blue_cap
    require(violations == 0, 'Actual ordinary spine cap violated')
    return dict(vertices=n, all_spines=red+blue, red_edges=red,
                blue_edges=blue, max_red_pages=max_red, max_blue_pages=max_blue,
                red_degree_profile=dict(sorted(Counter(row.count('1') for row in rows).items())))


def run():
    start = time.monotonic()
    raw = (Path(__file__).resolve().parent / 'primary21.rows').read_bytes()
    rows = raw.decode('ascii').splitlines()
    result = inspect(rows)
    require((result['all_spines'], result['red_edges'], result['blue_edges'],
             result['max_red_pages'], result['max_blue_pages']) == (210, 93, 117, 3, 6),
            'Known primary baseline differs')
    try:
        inspect(rows, blue_cap=5)
    except ValueError:
        pass
    else:
        raise ValueError('Actual blue-cap mutation not rejected')
    require(time.monotonic() - start < 25, 'INCOMPLETE baseline; no verdict')
    return dict(status='COMPLETE_PRIOR_ART_BASELINE', agent='six-books-2',
                role='researcher', prior_art_validation_only=True,
                primary_fixture_bytes=len(raw),
                primary_fixture_sha256=hashlib.sha256(raw).hexdigest(),
                actual_blue_cap_mutation_rejected=True, threads=1,
                program_guard_seconds=25, **result)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
