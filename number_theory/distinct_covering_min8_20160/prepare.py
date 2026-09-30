"""Convert a search output into a checked covering, deleting redundant classes."""
import argparse
import json
import math
from pathlib import Path
from verify import verify


def prepare(path):
    rows = [tuple(map(int, line.split())) for line in path.read_text().splitlines()]
    if not rows:
        raise ValueError('empty search output')
    L = math.lcm(*(m for a, m in rows))
    data = {'format_version': 1, 'lcm': L, 'congruences': rows}
    verify(data)  # INCONCLUSIVE search output cannot become a construction.
    count = [0] * L
    for a, m in rows:
        for x in range(a, L, m):
            count[x] += 1
    kept = set(rows)
    for a, m in sorted(rows, key=lambda pair: pair[1], reverse=True):
        if m == 8:
            continue
        if all(count[x] >= 2 for x in range(a, L, m)):
            kept.remove((a, m))
            for x in range(a, L, m):
                count[x] -= 1
    pairs = sorted(kept, key=lambda pair: pair[1])
    result = {'format_version': 1, 'lcm': math.lcm(*(m for a, m in pairs)), 'congruences': pairs}
    verify(result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(prepare(args.input), indent=2) + '\n')
