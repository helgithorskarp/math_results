#!/usr/bin/env python3
"""Exact marked leave carrier for shortened (2,1,1,1) stars."""
from itertools import combinations, permutations
import hashlib
import json
from pathlib import Path

from paths import WORK as HERE
HIGH_PAIRS = tuple(combinations(range(4), 2))
HIGH_GROUP = [(0,) + p for p in permutations((1, 2, 3))]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def image(edges, permutation):
    return tuple(sorted(tuple(sorted((permutation[a], permutation[b]))) for a, b in edges))


def core_representatives():
    domain = [tuple(e for i, e in enumerate(HIGH_PAIRS) if bits >> i & 1)
              for bits in range(64) if 3 <= bits.bit_count() <= 5]
    representatives = sorted({min(image(core, g) for g in HIGH_GROUP) for core in domain},
                             key=lambda core: (len(core), core))
    seen = set()
    records = []
    for core in representatives:
        orbit = {image(core, g) for g in HIGH_GROUP}
        if not orbit <= set(domain) or orbit & seen or core != min(orbit):
            raise RuntimeError('bad marked core orbit')
        seen.update(orbit)
        records.append(dict(core=core, e=len(core), orbit_size=len(orbit)))
    if seen != set(domain) or len(domain) != 41 or [sum(len(q) == e for q in representatives)
                                                    for e in (3, 4, 5)] != [6, 4, 2]:
        raise RuntimeError('incomplete marked core carrier')
    # Separate construction: choose the covered edges, compare literal
    # adjacency matrices to previously retained graphs under every hub-fixing map.
    separate = []
    for covered_size in (3, 2, 1):
        for covered in combinations(HIGH_PAIRS, covered_size):
            remaining = set(HIGH_PAIRS) - set(covered)
            equivalent = False
            for saved in separate:
                for a, b, d in permutations((1, 2, 3)):
                    point = {0: 0, 1: a, 2: b, 3: d}
                    if all(((u, v) in remaining) ==
                           (tuple(sorted((point[u], point[v]))) in saved)
                           for u, v in HIGH_PAIRS):
                        equivalent = True
                        break
                if equivalent:
                    break
            if not equivalent:
                separate.append(remaining)
    canonical = sorted({min(image(q, g) for g in HIGH_GROUP) for q in separate},
                       key=lambda core: (len(core), core))
    if canonical != representatives:
        raise RuntimeError('independent marked core carrier differs')
    return records


def normalized_leave(core):
    e = len(core)
    m = e - 3
    need = [7, 4, 4, 4]
    cohorts = []
    edges = list(core)
    low = 4
    for high in range(4):
        count = need[high] - sum(high in edge for edge in core)
        cohort = list(range(low, low + count))
        edges += [(high, z) for z in cohort]
        cohorts.append(cohort)
        low += count
    matching = [(z, z + 1) for z in range(low, 17, 2)]
    edges += matching
    result = tuple(sorted(edges))
    if len(matching) != m or low + 2 * m != 17 or len(result) != 16 or len(set(result)) != 16:
        raise RuntimeError('bad normalized leave dimensions')
    if [sum(z in edge for edge in result) for z in range(17)] != [7, 4, 4, 4] + [1] * 13:
        raise RuntimeError('bad normalized leave degrees')
    return result, cohorts, matching


def matrix(leave):
    required = sorted(set(combinations(range(17), 2)) - set(leave))
    if len(required) != 120:
        raise RuntimeError('wrong covered-pair count')
    index = {edge: i for i, edge in enumerate(required)}
    rows = []
    for word in combinations(range(17), 4):
        pairs = list(combinations(word, 2))
        if all(edge in index for edge in pairs):
            rows.append((sum(1 << z for z in word), sorted(index[e] for e in pairs)))
    rows.sort()
    literal = []
    for mask in range(1 << 17):
        if mask.bit_count() != 4:
            continue
        points = [z for z in range(17) if mask >> z & 1]
        if not any((mask >> a & 1) and (mask >> b & 1) for a, b in leave):
            literal.append(mask)
    if literal != [word for word, _ in rows]:
        raise RuntimeError('literal candidate universe differs')
    if len(rows) > 1334:
        raise RuntimeError('native matrix capacity insufficient; no search verdict')
    return required, rows


def validate_star(words, leave):
    if len(words) != 20 or len(set(words)) != 20 or any(
            type(w) is not int or w < 0 or w >= 1 << 17 or w.bit_count() != 4 for w in words):
        raise RuntimeError('bad shortened star words')
    blocks = [frozenset(z for z in range(17) if w >> z & 1) for w in words]
    if any(len(a & b) > 1 for a, b in combinations(blocks, 2)):
        raise RuntimeError('shortened star pair conflict')
    covered = set().union(*(set(combinations(sorted(b), 2)) for b in blocks))
    if set(combinations(range(17), 2)) - covered != set(leave):
        raise RuntimeError('shortened star leave differs')
    if [sum(z in b for b in blocks) for z in range(17)] != [3, 4, 4, 4] + [5] * 13:
        raise RuntimeError('shortened star replication differs')


def build():
    cases = []
    for i, record in enumerate(core_representatives()):
        leave, cohorts, matching = normalized_leave(record['core'])
        required, rows = matrix(leave)
        cases.append(dict(index=i, **record, m=len(matching), leave=leave, cohorts=cohorts,
                          matching=matching, candidates=len(rows),
                          matrix_sha256=digest([required, rows])))
    return dict(agent='six-code-3', role='researcher', status='COMPLETE leave carrier; star feasibility unknown',
                high_core_labeled_domain=41, marked_leave_types=12, cases=cases)


if __name__ == '__main__':
    value = build()
    (HERE / 'leave_carrier.json').write_text(json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps({k: v for k, v in value.items() if k != 'cases'}))
    print(json.dumps([dict(index=q['index'], e=q['e'], core=q['core'], candidates=q['candidates'])
                      for q in value['cases']]))
