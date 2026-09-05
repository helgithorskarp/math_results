#!/usr/bin/env python3
"""Literal-graph phase audit and independent finite clause semantics."""
from itertools import combinations, product, permutations
from pathlib import Path
import argparse
import hashlib
import json
import random

import model


def literal_graph(phase):
    words = model.core_words(phase)
    return {(a, b): (True if a//3 == b//3 else bool(words[a//3, b//3][(b-a) % 3]))
            for a, b in combinations(range(12), 2)}


def graph_phase(graph, mapping):
    def edge(a, b):
        return graph[tuple(sorted((mapping[a], mapping[b])))]
    for j in range(1, 4):
        block = mapping[3*j:3*j+3]
        for shift in range(3):
            mapping[3*j:3*j+3] = block[shift:] + block[:shift]
            word = [edge(0, 3*j+t) for t in range(3)]
            if word == sorted(word, reverse=True):
                break
        else:
            raise ValueError('no normalized core word')
    phase = []
    for i, j in ((1, 2), (1, 3), (2, 3)):
        word = tuple(int(edge(3*i, 3*j+t)) for t in range(3))
        pattern = (1, 0, 0) if (i, j) == (2, 3) else (1, 1, 0)
        phase.append(next(s for s in range(3) if pattern[s:]+pattern[:s] == word))
    return tuple(phase)


def phase_audit():
    """Rebuild all classes using actual 12-vertex permutations, no formula relabel."""
    phases = list(product(range(3), repeat=3))
    groups = []
    representatives = []
    comparisons = 0
    for phase in phases:
        graph = literal_graph(phase)
        model.require(all(sum(graph[tuple(sorted((v, w)))] for w in range(12) if w != v) == 7
                          for v in range(12)), 'not 7-regular')
        model.require(not any(len({graph[e] for e in combinations(vs, 2)}) == 1
                              for vs in combinations(range(12), 5)), 'bad minority core')
        orbit = set()
        for perm in permutations(range(4)):
            if {frozenset((perm[0], perm[1])), frozenset((perm[2], perm[3]))} != model.MATCHING:
                continue
            for sign in (-1, 1):
                mapping = [3*perm[i] + (sign*t) % 3 for i in range(4) for t in range(3)]
                got = graph_phase(graph, mapping)
                model.require(got == model.relabel(phase, perm, sign), 'phase action mismatch')
                sigma = [3*(v//3)+(v+1) % 3 for v in range(12)]
                model.require(all(mapping[sigma[v]] == 3*(mapping[v]//3)+(mapping[v]+sign) % 3
                                  for v in range(12)), 'not a normalizer')
                normal = literal_graph(got)
                model.require(all(normal[a, b] == graph[tuple(sorted((mapping[a], mapping[b])))]
                                  for a, b in combinations(range(12), 2)), 'literal graph lost')
                orbit.add(got)
                comparisons += 1
        groups.append(orbit)
        representatives.append(min(orbit))
    # Equality of entire orbit sets, and explicit disjointness/coverage.
    for i, phase in enumerate(phases):
        model.require(all(groups[phases.index(t)] == groups[i] for t in groups[i]), 'orbit closure')
    observed = [{'phase': list(r), 'members': [list(t) for t in sorted(groups[phases.index(r)])]}
                for r in sorted(set(representatives))]
    model.require(observed == model.classes(), 'phase class census mismatch')
    model.require(sorted(len(r['members']) for r in observed) == [1, 2, 4, 4, 8, 8], 'phase class sizes')
    return {'normalized_phases': len(phases), 'classes': observed, 'literal_relabelings': comparisons,
            'all_27_cores_7_regular_and_ramsey': True}


def pair_ids():
    sigma = [3*(v//3)+(v+1) % 3 if v < 30 else v for v in range(43)]
    unseen = set(combinations(range(43), 2))
    orbits = []
    while unseen:
        e = min(unseen)
        orbit = set()
        while e not in orbit:
            orbit.add(e)
            e = tuple(sorted(sigma[v] for v in e))
        unseen.difference_update(orbit)
        orbits.append(sorted(orbit))
    cross = sorted([o for o in orbits if o[0][1] < 30 and o[0][0]//3 != o[0][1]//3], key=lambda o: o[0])
    fixed = sorted([o for o in orbits if o[0][0] >= 30], key=lambda o: o[0])
    links = sorted([o for o in orbits if o[0][0] < 30 <= o[0][1]], key=lambda o: (o[0][1], o[0][0]))
    model.require((len(orbits), len(cross), len(fixed), len(links)) == (353, 135, 78, 130), 'pair orbits')
    return {e: i for i, orbit in enumerate(cross + fixed + links, 1) for e in orbit}


def semantic_tail(case):
    """Enumerate falsifying truth-table assignments using actual edge orbits."""
    ids = pair_ids()
    clauses = []
    checks = 0
    for i, j in combinations(range(4), 2):
        bits = [ids[3*i, 3*j+t] for t in range(3)]
        wanted = 1 if {i, j} in ({0, 1}, {2, 3}) else 2
        local = [tuple(b if not ((m >> t) & 1) else -b for t, b in enumerate(bits))
                 for m in range(8) if m.bit_count() != wanted]
        for m in range(8):
            values = {b: bool((m >> t) & 1) for t, b in enumerate(bits)}
            model.require(all(any(values[abs(l)] == (l > 0) for l in c) for c in local)
                          == (m.bit_count() == wanted), 'exact weight semantics')
            checks += 1
        clauses.extend(local)
    for i in range(4):
        row = []
        for j in range(4, 10):
            bits = [ids[3*i, 3*j+t] for t in range(3)]
            z = 28951 + 6*i+j-4
            row.append(z)
            local = [tuple(bits), tuple(-b for b in bits)]
            for m in range(8):
                local.append(tuple(b if not ((m >> t) & 1) else -b for t, b in enumerate(bits))
                             + (z if m.bit_count() == 1 else -z,))
            for m, zv in product(range(8), (False, True)):
                values = {b: bool((m >> t) & 1) for t, b in enumerate(bits)} | {z: zv}
                model.require(all(any(values[abs(l)] == (l > 0) for l in c) for c in local)
                              == (m.bit_count() in (1, 2) and zv == (m.bit_count() == 1)), 'mixed gate semantics')
                checks += 1
            clauses.extend(local)
        local = [tuple(row)] + [tuple(-z for z in five) for five in combinations(row, 5)]
        for values in product((False, True), repeat=6):
            assignment = dict(zip(row, values))
            model.require(all(any(assignment[abs(l)] == (l > 0) for l in c) for c in local)
                          == (1 <= sum(values) <= 4), 'row count semantics')
            checks += 1
        clauses.extend(local)
    for j in range(1, 10):
        for t in range(3):
            clauses.append((ids[0, 3*j+t] * (1 if t < case['weights'][j-1] else -1),))
    graph = literal_graph(case['phase'])
    for i, j in ((1, 2), (1, 3), (2, 3)):
        for t in range(3):
            clauses.append((ids[3*i, 3*j+t] * (1 if graph[3*i, 3*j+t] else -1),))
    result = sorted(tuple(sorted(c)) for c in clauses)
    model.require(len(result) == 334 and len(set(result)) == 334, 'tail count/duplicates')
    model.require(result == sorted(tuple(sorted(c)) for c in model.tail(case)), 'semantic tail mismatch')
    return result, checks


def check_formula(base, cnf, case):
    model.require(model.file_info(base)['sha256'] == model.BASE_SHA, 'base digest')
    with base.open('rb') as a, cnf.open('rb') as b:
        model.require(a.readline() == model.BASE_HEADER, 'base header')
        model.require(b.readline() == b'p cnf 28974 927334\n', 'case header')
        while block := a.read(1024*1024):
            model.require(b.read(len(block)) == block, 'modified parent clause')
        tail = b.read().decode().splitlines()
    clauses = []
    for line in tail:
        values = list(map(int, line.split()))
        model.require(values and values[-1] == 0 and all(values[:-1]), 'malformed tail')
        clauses.append(tuple(sorted(values[:-1])))
    expected, _ = semantic_tail(case)
    model.require(sorted(clauses) == expected, 'case tail mismatch')
    return model.file_info(cnf)


def audit():
    manifest = json.loads((model.ROOT / 'dependencies.json').read_text())
    for relative, digest in manifest['files'].items():
        model.require(model.file_info(model.ROOT.parent / relative)['sha256'] == digest, 'dependency mismatch: '+relative)
    result = phase_audit()
    cases = model.cases()
    model.require(len(cases) == 24 and {c['anchor'] for c in cases} == {64, 65, 67, 69}, 'case cover')
    result['cases'] = cases
    result['truth_assignments_per_tail'] = semantic_tail(cases[0])[1]
    for case in cases[1:]:
        semantic_tail(case)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit()
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(json.dumps({'phase_classes': len(result['classes']), 'cases': len(result['cases']),
                      'literal_relabelings': result['literal_relabelings'],
                      'truth_assignments_per_tail': result['truth_assignments_per_tail']}))
