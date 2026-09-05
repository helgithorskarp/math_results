#!/usr/bin/env python3
"""Generate a finite phase cover layered on the complete published formula."""
from itertools import combinations, product, permutations
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'ramsey_r55_order3_ten_cycle_obstruction'
PREVIOUS = ROOT.parent / 'ramsey_r55_order3_ten_cycle_anchor_sweep'
BASE_SHA = 'f01c990a1dae17fb7bc1cd633d785cd819ba9f4d1a1eeacd69b4034663af104e'
BASE_HEADER = b'p cnf 28950 927000\n'
PHASE_PAIRS = ((1, 2), (1, 3), (2, 3))
PAIRS = list(combinations(range(10), 2))
IDS = {p: tuple(range(1 + 3*i, 4 + 3*i)) for i, p in enumerate(PAIRS)}
MATCHING = {frozenset((0, 1)), frozenset((2, 3))}
ANCHORS = (64, 65, 67, 69)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def file_info(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while data := stream.read(1024 * 1024):
            digest.update(data)
    return {'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def weights():
    return json.loads((PARENT / 'anchor_r4.json').read_text())['weights']


def core_words(phase):
    words = {(0, 1): (1, 0, 0), (0, 2): (1, 1, 0), (0, 3): (1, 1, 0)}
    for pair, shift in zip(PHASE_PAIRS, phase):
        word = (1, 0, 0) if pair == (2, 3) else (1, 1, 0)
        words[pair] = word[shift:] + word[:shift]
    return words


def relabel(phase, perm, sign):
    """Permute matched cycles, optionally invert every moving cycle, rephase."""
    words = core_words(phase)

    def edge(i, u, j, v):
        a, b = perm[i], perm[j]
        u, v = sign*u, sign*v
        return words[a, b][(v-u) % 3] if a < b else words[b, a][(u-v) % 3]

    shifts = [0]
    for j in range(1, 4):
        shifts.append(next(s for s in range(3)
                           if [edge(0, 0, j, t+s) for t in range(3)]
                           == sorted([edge(0, 0, j, t+s) for t in range(3)], reverse=True)))
    answer = []
    for i, j in PHASE_PAIRS:
        word = tuple(edge(i, shifts[i], j, t+shifts[j]) for t in range(3))
        base = (1, 0, 0) if (i, j) == (2, 3) else (1, 1, 0)
        answer.append(next(s for s in range(3) if base[s:] + base[:s] == word))
    return tuple(answer)


def classes():
    perms = [p for p in permutations(range(4))
             if {frozenset((p[0], p[1])), frozenset((p[2], p[3]))} == MATCHING]
    orbits = {}
    for phase in product(range(3), repeat=3):
        orbit = {relabel(phase, p, sign) for p in perms for sign in (-1, 1)}
        orbits.setdefault(min(orbit), set()).update(orbit)
    return [{'phase': list(k), 'members': [list(t) for t in sorted(v)]}
            for k, v in sorted(orbits.items())]


def cases():
    return [{'index': 4*i+j, 'phase': row['phase'], 'anchor': a,
             'weights': weights()[a]}
            for i, row in enumerate(classes()) for j, a in enumerate(ANCHORS)]


def common_clauses():
    clauses = []
    nv = 28950
    # Truth-table exclusion gives exactly the specified block weight.
    for pair in combinations(range(4), 2):
        bits = IDS[pair]
        weight = 1 if frozenset(pair) in MATCHING else 2
        for values in product((0, 1), repeat=3):
            if sum(values) != weight:
                clauses.append([-b if x else b for b, x in zip(bits, values)])
    for i in range(4):
        row = []
        for j in range(4, 10):
            bits = IDS[i, j]
            clauses.extend([list(bits), [-b for b in bits]])
            nv += 1
            z = nv
            row.append(z)
            for values in product((0, 1), repeat=3):
                clauses.append([-b if x else b for b, x in zip(bits, values)]
                               + [z if sum(values) == 1 else -z])
        clauses.append(row)
        clauses.extend([[-z for z in five] for five in combinations(row, 5)])
    require(nv == 28974 and len(clauses) == 298, 'global layer dimensions')
    return clauses


def tail(case):
    clauses = common_clauses()
    clauses.extend([[b if t < case['weights'][j-1] else -b]
                    for j in range(1, 10) for t, b in enumerate(IDS[0, j])])
    words = core_words(case['phase'])
    clauses.extend([[b if value else -b] for pair in PHASE_PAIRS
                    for b, value in zip(IDS[pair], words[pair])])
    require(len(clauses) == 334, 'case layer dimensions')
    return clauses


def generate(base, destination, case):
    require(file_info(base)['sha256'] == BASE_SHA, 'parent digest mismatch')
    with base.open('rb') as source, destination.open('wb') as target:
        require(source.readline() == BASE_HEADER, 'parent header mismatch')
        target.write(b'p cnf 28974 927334\n')
        shutil.copyfileobj(source, target)
        target.write(''.join(' '.join(map(str, c)) + ' 0\n' for c in tail(case)).encode())
    return file_info(destination)
