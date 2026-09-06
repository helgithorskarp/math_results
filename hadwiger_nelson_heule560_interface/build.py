#!/usr/bin/env python3
"""Exact existential projection of one fixed four-colouring interface."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'hadwiger_nelson_heule632_pair_pilot'))
import build as geometry_source


def read_inputs():
    plan = json.loads((HERE / 'plan.json').read_text())
    for name, digest in plan['input_files'].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError('input hash: ' + name)
    boundary = json.loads((ROOT / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    colour = json.loads((ROOT / 'hadwiger_nelson_heule560_degree_family/certificate.json').read_text())['cover_colouring']
    _, edges, _ = geometry_source.geometry()
    mandatory = set(boundary['mandatory_vertices'])
    optional = boundary['optional_vertices']
    lists = {v: set(range(4)) for v in optional}
    for u, v in edges:
        if u in mandatory and v in mandatory and colour[u] == colour[v]:
            raise ValueError('mandatory colouring')
        if u in lists and v in mandatory:
            lists[u].discard(int(colour[v]))
        if v in lists and u in mandatory:
            lists[v].discard(int(colour[u]))
    return plan, optional, lists, [(u, v) for u, v in edges if u in lists and v in lists]


def minimize(clauses):
    """Canonical subsumption-free equivalent CNF."""
    result = []
    for row in sorted(set(clauses), key=lambda c: (len(c), tuple(sorted(c)))):
        if any(-v in row for v in row):
            continue
        if not any(old <= row for old in result):
            result.append(row)
    return result


def project(optional, lists, edges, limits):
    selector = {v: i + 1 for i, v in enumerate(optional)}
    colour_var = {}
    fresh = len(optional)
    for v in optional:
        for c in sorted(lists[v]):
            fresh += 1
            colour_var[v, c] = fresh
    # At least one colour when selected. No at-most-one or reverse activation
    # clauses are needed: choose any true colour; absent vertices may be false.
    clauses = [frozenset([-selector[v]] + [colour_var[v, c] for c in lists[v]])
               for v in optional]
    clauses += [frozenset((-colour_var[u, c], -colour_var[v, c]))
                for u, v in edges for c in lists[u] & lists[v]]
    initial = len(clauses)
    live = set(colour_var.values())
    trace = []
    start = time.monotonic()
    while live:
        if time.monotonic() - start > limits['seconds_per_stage']:
            raise RuntimeError('projection time boundary')
        occurrence = {x: [0, 0] for x in live}
        for row in clauses:
            for lit in row:
                if abs(lit) in live:
                    occurrence[abs(lit)][lit < 0] += 1
        x = min(live, key=lambda a: (occurrence[a][0] * occurrence[a][1], sum(occurrence[a]), a))
        pos = [r - {x} for r in clauses if x in r]
        neg = [r - {-x} for r in clauses if -x in r]
        if len(pos) * len(neg) > limits['max_resolvent_pairs_per_step']:
            raise RuntimeError('resolvent boundary')
        clauses = minimize([r for r in clauses if x not in r and -x not in r] +
                           [a | b for a in pos for b in neg])
        if len(clauses) > limits['max_live_clauses']:
            raise RuntimeError('clause boundary')
        trace.append([x, len(pos), len(neg), len(clauses)])
        live.remove(x)
    if any(lit >= 0 or -lit > len(optional) for row in clauses for lit in row):
        raise ValueError('non-selector projection literal')
    forbidden = sorted([sorted(optional[-lit - 1] for lit in row) for row in clauses], key=lambda r: (len(r), r))
    return forbidden, {'initial_clauses': initial, 'colour_variables': len(colour_var),
                       'elimination_trace': trace, 'peak_live_clauses': max([initial] + [r[3] for r in trace])}


def counts_by_union(forbidden, n):
    """Inclusion-exclusion, merging identical unions after each hyperedge."""
    weights = {frozenset(): 1}
    for row in forbidden:
        nxt = dict(weights)
        for union, sign in weights.items():
            key = union | frozenset(row)
            nxt[key] = nxt.get(key, 0) - sign
        weights = {key: val for key, val in nxt.items() if val}
        if len(weights) > 1000000:
            raise RuntimeError('inclusion-exclusion boundary')
    return [sum(sign * math.comb(n - len(union), k - len(union))
                for union, sign in weights.items() if len(union) <= k)
            for k in range(n + 1)], len(weights)


def covers_and_colourings(optional, lists, edges, forbidden, limits):
    transversals = [frozenset()]
    start = time.monotonic()
    for row in forbidden:
        transversals = minimize([t if t & set(row) else t | {v}
                                for t in transversals for v in row])
        if len(transversals) > limits['max_transversals']:
            raise RuntimeError('transversal boundary')
    fixed = json.loads((ROOT / 'hadwiger_nelson_heule560_degree_family/certificate.json').read_text())['cover_colouring']
    mandatory = json.loads((ROOT / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())['mandatory_vertices']
    adjacency = {v: set() for v in optional}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    witnesses = []
    for omitted in sorted(transversals, key=lambda t: (len(t), sorted(t))):
        domains = {v: set(lists[v]) for v in optional if v not in omitted}
        assigned = {}

        def search():
            if time.monotonic() - start > limits['seconds_per_stage']:
                raise RuntimeError('cover colouring boundary')
            if len(assigned) == len(domains):
                return True
            available = {v: domains[v] - {assigned[n] for n in adjacency[v] if n in assigned}
                         for v in domains if v not in assigned}
            v = min(available, key=lambda v: (len(available[v]), -len(adjacency[v]), v))
            for c in sorted(available[v]):
                assigned[v] = c
                if search():
                    return True
            assigned.pop(v, None)
            return False

        if not search():
            raise ValueError('projected feasible cover has no colouring')
        text = ['.'] * 632
        for v in mandatory:
            text[v] = fixed[v]
        for v, c in assigned.items():
            text[v] = str(c)
        witnesses.append({'omitted_optional': sorted(omitted), 'colouring': ''.join(text)})
    return witnesses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    plan, optional, lists, edges = read_inputs()
    forbidden, trace = project(optional, lists, edges, plan['limits'])
    counts, unions = counts_by_union(forbidden, len(optional))
    certificate = {'optional_vertices': optional, 'lists': {str(v): sorted(lists[v]) for v in optional},
                   'optional_edges': edges, 'minimal_nonextending_sets': forbidden,
                   'extending_counts_by_optional_size': counts,
                   'maximal_extending_cover_colourings': covers_and_colourings(optional, lists, edges, forbidden, plan['limits'])}
    (args.out / 'certificate.json').write_text(json.dumps(certificate, separators=(',', ':'), sort_keys=True) + '\n')
    report = {'projection': trace, 'inclusion_exclusion_union_count': unions,
              'minimal_obstructions': len(forbidden), 'extending_16': counts[16],
              'remaining_16': math.comb(68, 16) - counts[16],
              'elapsed_seconds': time.monotonic() - start}
    (args.out / 'build_report.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'projection'}, indent=2))
    print('Minimal nonextending sets:', forbidden)


if __name__ == '__main__':
    main()
