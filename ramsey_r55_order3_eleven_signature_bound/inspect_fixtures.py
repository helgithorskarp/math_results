#!/usr/bin/env python3
"""Independently check the complete action and core in the three public fixtures."""
from itertools import combinations
from pathlib import Path
import argparse
import json
import audit


def inspect(root):
    rows = []
    for index, expected in ((8, '100100100'), (11, '100110110'), (13, '110110101')):
        path = root / f'core{index}.edges'
        row = audit.inspect(path)
        edges = {tuple(map(int, line.split())) for line in path.read_text().splitlines()[1:]}
        def rotate(v):
            return 3*(v//3)+(v % 3+1) % 3 if v < 9 else v
        for a, b in combinations(range(19), 2):
            moved = tuple(sorted((rotate(a), rotate(b))))
            audit.require(((a, b) in edges) == (moved in edges), 'fixture action failure')
        audit.require(row['core_words'] == expected, 'core orbit representatives')
        audit.require(all((a, b) in edges for i in range(3) for a, b in combinations(range(3*i, 3*i+3), 2)),
                      'internal red triangles')
        rows.append(dict(index=index, action_pairs=171, **row))
    return dict(fixtures=rows, complete_action_checks=513)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--fixtures', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    report = inspect(a.fixtures)
    a.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print('PASS three full 19-vertex graphs, all core orbits and all 513 action pairs')
