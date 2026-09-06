"""Find an actual forbidden five-set in a specified switched Paley49 subgraph."""
import argparse
import json
from itertools import combinations
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def extract(doc):
    need(isinstance(doc, dict) and set(doc) == {'points', 'switch'}, 'input schema')
    points, spin = doc['points'], doc['switch']
    need(isinstance(points, list) and len(points) == 43 and all(type(x) is int and 0 <= x < 49 for x in points), '43 field points')
    need(len(set(points)) == 43, 'distinct field points')
    need(isinstance(spin, list) and len(spin) == 43 and all(type(x) is int and x in (0, 1) for x in spin), '43 switch bits')
    selected_bit = int(spin.count(1) > spin.count(0))
    half = [i for i, b in enumerate(spin) if b == selected_bit][:22]
    a = [[0]*43 for _ in range(43)]
    for i, j in combinations(range(43), 2):
        x = points[i] % 7-points[j] % 7
        y = points[i]//7-points[j]//7
        a[i][j] = a[j][i] = int(pow((x*x-3*y*y) % 7, 3, 7) == 1) ^ spin[i] ^ spin[j]
    for q in combinations(half, 5):
        colors = {a[i][j] for i, j in combinations(q, 2)}
        if len(colors) == 1:
            return {'n': 43, 'edges': [[i, j] for i, j in combinations(range(43), 2) if a[i][j]],
                    'color': colors.pop(), 'witness': list(q)}
    raise ValueError('no witness: contradicts the 22-point lemma or an implementation assumption')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('input', type=Path)
    args = ap.parse_args()
    print(json.dumps(extract(json.loads(args.input.read_text())), separators=(',', ':')))
