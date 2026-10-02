"""Deterministic positive coloring certificates; failed search proves nothing.

Adapted from six-code-3's published good_cohort_z_residuals/generate.py.
All colors here are newly generated; no previous color arrays are imported.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

BRIDGE_PIN = '2f20d52b0f2ea96b3008cbafdb0e2878ef87918a3d62f2a5c470c26d9e2c0fb3'

def need(test, message):
    if not test:
        raise ValueError(message)

def color(adjacency, priority):
    colors = [-1] * len(adjacency)
    seen = [0] * len(adjacency)
    todo = set(range(len(adjacency)))
    degree = [a.bit_count() for a in adjacency]
    while todo:
        v = max(todo, key=lambda i: (seen[i].bit_count(), degree[i], priority[i]))
        c = 0
        while seen[v] >> c & 1:
            c += 1
        colors[v] = c
        todo.remove(v)
        neighbors = adjacency[v]
        while neighbors:
            bit = neighbors & -neighbors
            seen[bit.bit_length()-1] |= 1 << c
            neighbors ^= bit
    return colors

def generate(bridge):
    rows = bridge['raw_positive_maps']
    need(len(rows) == 50, 'frozen raw carrier population differs')
    entries = []
    for index, row in enumerate(rows):
        begin = time.monotonic()
        centers = {17, row['first'][1][2]}
        candidates = [sum(1 << p for p in q)
                      for q in itertools.combinations(sorted(set(range(18))-centers), 5)]
        candidates = [m for m in candidates
                      if all((m & w).bit_count() <= 2 for w in row['word_masks'])]
        adjacency = [0] * len(candidates)
        edges = 0
        for i, j in itertools.combinations(range(len(candidates)), 2):
            if (candidates[i] & candidates[j]).bit_count() <= 2:
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
                edges += 1
        best = color(adjacency, [-i for i in range(len(candidates))])
        for trial in range(64):
            if max(best) < 28:
                break
            need(time.monotonic()-begin <= 5, 'INCOMPLETE5s product search guard')
            priority = list(range(len(candidates)))
            random.Random(20261001+1000*index+trial).shuffle(priority)
            trial_colors = color(adjacency, priority)
            if max(trial_colors) < max(best):
                best = trial_colors
        need(time.monotonic()-begin <= 5, 'INCOMPLETE5s product guard')
        need(len(best) == len(candidates), 'color domain differs')
        need(all(best[i] != best[j] for i, j in itertools.combinations(range(len(candidates)), 2)
                 if adjacency[i] >> j & 1), 'improper generated positive colors')
        capacity = max(best)+1
        entries.append(dict(index=index, product_index=row['product_index'],
                            candidate_count=len(candidates), edges=edges,
                            candidate_sha256=hashlib.sha256(json.dumps(candidates, separators=(',', ':')).encode()).hexdigest(),
                            colors=best, capacity=capacity, upper_bound=36+capacity,
                            triangle_count=len(row['triangle_points']), first_fixture=row['first'][0]))
    return dict(agent='six-code-3', role='researcher',
                scope='All50 normalized unit-second-yv4 interfaces with isolated deficient first u; source u-v leave cases retained. No triangle premise or global selector. Proper-color upper bounds only; no optimality or sharpness.',
                entries=entries)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bridge', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    raw = Path(args.bridge).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == BRIDGE_PIN, 'raw carrier pin differs')
    result = generate(json.loads(raw))
    Path(args.output).write_text(json.dumps(result, sort_keys=True, separators=(',', ':'))+'\n')
    print(json.dumps(dict(status='GENERATED_POSITIVE_CERTIFICATES', interfaces=len(result['entries']),
                         maximum_upper_bound=max(e['upper_bound'] for e in result['entries']))))

if __name__ == '__main__':
    main()
