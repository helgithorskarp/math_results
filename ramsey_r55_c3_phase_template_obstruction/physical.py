#!/usr/bin/env python3
"""Physical graph and score audit, importing no optimizer or objective code."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

N = 43
ACTION = [3*(v//3)+(v+1)%3 for v in range(42)]+[42]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read_graph(path):
    lines = Path(path).read_text().splitlines()
    need(lines and lines[0] == '43', 'graph order')
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    need(all(len(e) == 2 and 0 <= e[0] < e[1] < N for e in edges), 'edge range')
    need(edges == sorted(set(edges)), 'canonical edge list')
    rows = [0]*N
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return rows


def edge_bytes(rows):
    return ('43\n'+''.join(f'{u} {v}\n' for u, v in combinations(range(N), 2)
                           if rows[u] & (1 << v))).encode()


def orbits():
    todo = set(combinations(range(N), 2))
    free, fixed = [], []
    while todo:
        u, v = min(todo)
        orbit = {tuple(sorted((u, v))), tuple(sorted((ACTION[u], ACTION[v]))),
                 tuple(sorted((ACTION[ACTION[u]], ACTION[ACTION[v]])))}
        need(orbit <= todo and len(orbit) == 3, 'physical orbit partition')
        todo -= orbit
        if v < 42 and u//3 == v//3:
            fixed.append((sorted(orbit), int(u < 21)))
        else:
            free.append(sorted(orbit))
    # Native IDs put the moving/moving orbits before all root contacts.
    free.sort(key=lambda orbit: (orbit[0][1] == 42, orbit[0]))
    need(len(free) == 287 and len(fixed) == 14, 'physical orbit counts')
    return free, fixed


def decode(word):
    need(len(word) == 287 and set(word) <= {'0', '1'}, 'complete orbit word')
    free, fixed = orbits()
    rows = [0]*N
    for orbit, red in fixed+[(orbit, int(b)) for orbit, b in zip(free, word)]:
        if red:
            for u, v in orbit:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
    return rows


def family(rows):
    need(len(rows) == N, 'row count')
    for u, v in combinations(range(N), 2):
        need(bool(rows[u] & (1 << v)) == bool(rows[ACTION[u]] & (1 << ACTION[v])), 'C3 invariance')
    free, fixed = orbits()
    for orbit, red in fixed:
        need(all(int(bool(rows[u] & (1 << v))) == red for u, v in orbit), 'internal triangle colors')
    word = ''.join(str(int(bool(rows[o[0][0]] & (1 << o[0][1])))) for o in free)
    need(decode(word) == rows, 'complete physical decode')
    return word


def cliques(rows, k, candidates=None, chosen=()):
    if not k:
        yield chosen
        return
    if candidates is None:
        candidates = (1 << len(rows))-1
    while candidates.bit_count() >= k:
        bit = candidates & -candidates
        candidates ^= bit
        u = bit.bit_length()-1
        yield from cliques(rows, k-1, candidates & rows[u], chosen+(u,))


def recursive_defects(rows):
    mask = (1 << len(rows))-1
    blue = [mask ^ row ^ (1 << u) for u, row in enumerate(rows)]
    return [list(cliques(color, 5)) for color in (blue, rows)]


def literal_defects(rows):
    result = [[], []]
    for q in combinations(range(len(rows)), 5):
        color = (rows[q[0]] >> q[1]) & 1
        if all(((rows[u] >> v) & 1) == color for u, v in combinations(q, 2)):
            result[color].append(q)
    return result


def initial_bits(seed):
    mask = (1 << 64)-1
    word = ''
    for _ in range(287):
        seed = (seed+0x9e3779b97f4a7c15) & mask
        z = seed
        z = ((z ^ (z >> 30))*0xbf58476d1ce4e5b9) & mask
        z = ((z ^ (z >> 27))*0x94d049bb133111eb) & mask
        z ^= z >> 31
        word += str(z % 2)
    return word


def audit(work, expected_restarts=None, expected_steps=None, seed_base=None):
    records = list(csv.DictReader((work/'restarts.tsv').open(), delimiter='\t'))
    need(records, 'empty restart file')
    if expected_restarts is not None:
        need(len(records) == expected_restarts, 'incomplete restart batch')
    report = []
    for i, record in enumerate(records):
        need(int(record['restart']) == i, 'restart coverage')
        if seed_base is not None:
            need(int(record['seed']) == seed_base+i, 'seed contract')
        if expected_steps is not None:
            need(int(record['steps_done']) == expected_steps or int(record['best']) == 0, 'incomplete restart')
        rows = decode(record['bits'])
        need(family(rows) == record['bits'], 'restart family')
        defects = recursive_defects(rows)
        counts = list(map(len, defects))
        need(sum(counts) == int(record['best']), 'recorded best score')
        initial = recursive_defects(decode(initial_bits(int(record['seed']))))
        need(sum(map(len, initial)) == int(record['initial']), 'initial physical score')
        need(0 <= int(record['best_step']) <= int(record['steps_done']), 'best-step range')
        report.append({'restart': i, 'seed': int(record['seed']), 'blue_red': counts,
                       'score': sum(counts), 'graph_sha256': sha256(edge_bytes(rows)).hexdigest()})
    first = min(range(len(records)), key=lambda i: report[i]['score'])
    rows = read_graph(work/'best.edges')
    need(rows == decode(records[first]['bits']), 'first best graph identity')
    need(family(rows) == records[first]['bits'], 'winner action and bits')
    bad = literal_defects(rows)
    need(bad == recursive_defects(rows), 'complete physical defect-list equality')
    target = not any(bad)
    status = json.loads((work/'status.json').read_text())
    need(status.get('complete') is True or (target and status.get('candidate_target') is True), 'run incomplete')
    return {'status': 'VERIFIED_EXPLICIT_C3_FOURTEEN_GRAPH', 'vertices': N,
        'physical_pairs': 903, 'physical_five_sets': 962598,
        'free_orbits': 287, 'fixed_internal_orbits': 14,
        'records': report, 'best_restart': first,
        'red_edges': sum(row.bit_count() for row in rows)//2,
        'degrees': [row.bit_count() for row in rows],
        'degree_histogram': dict(sorted(Counter(row.bit_count() for row in rows).items())),
        'best_score': sum(map(len, bad)), 'defects_blue_red': list(map(len, bad)),
        'complete_defects': bad, 'best_bits': records[first]['bits'],
        'graph_sha256': sha256(edge_bytes(rows)).hexdigest(),
        'ramsey_target': target, 'score_below_155': sum(map(len, bad)) < 155}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('work', type=Path)
    p.add_argument('--restarts', type=int)
    p.add_argument('--steps', type=int)
    p.add_argument('--seed-base', type=int)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = audit(a.work, a.restarts, a.steps, a.seed_base)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(result['status'], result['best_score'], result['defects_blue_red'], result['graph_sha256'])
