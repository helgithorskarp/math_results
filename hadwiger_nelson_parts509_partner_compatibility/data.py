#!/usr/bin/env python3
"""Exact fixed-partner lists and complete composition activation encoding."""
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dimacs(variables, clauses):
    return (f'p cnf {variables} {len(clauses)}\n' +
            ''.join(' '.join(map(str, row)) + ' 0\n' for row in clauses)).encode()


def list_cnf(masks, edges):
    require(len(masks) == 135 and all(type(m) is int and 0 <= m < 16 for m in masks), 'list masks')
    colour = lambda v, c: 4 * (v - 374) + c + 1
    clauses = [[colour(v, c) for c in range(4)] for v in range(374, 509)]
    clauses += [[-colour(u, c), -colour(v, c)] for u, v in edges for c in range(4)]
    clauses += [[-colour(v, c)] for v, m in zip(range(374, 509), masks) for c in range(4) if not m & (1 << c)]
    return dimacs(540, clauses)


def check_S(colouring, masks, edges):
    require(len(colouring) == 135 and set(colouring) <= set('0123'), 'S colour domain')
    cols = dict(zip(range(374, 509), map(int, colouring)))
    require(all(m & (1 << cols[v]) for v, m in zip(range(374, 509), masks)), 'S available list')
    require(all(cols[u] != cols[v] for u, v in edges), 'S unit edge')
    return cols


def composition(data):
    """No query is run: active U iff a proper colouring of UD(U union S) exists."""
    vertices = sorted(data['vertices'] + data['S'])
    pos = {v: i for i, v in enumerate(vertices)}
    col = lambda v, c: 4 * pos[v] + c + 1
    act = {v: 4 * len(vertices) + i + 1 for i, v in enumerate(data['vertices'])}
    clauses = [[-act[v]] + [col(v, c) for c in range(4)] for v in data['vertices']]
    clauses += [[col(v, c) for c in range(4)] for v in data['S']]
    clauses += [[-col(u, c), -col(v, c)] for u, v in data['all_edges'] for c in range(4)]
    clauses += [[act[v]] for v in data['interface']] + [[col(0, 0)]]
    return dimacs(4 * len(vertices) + len(act), clauses)


def build():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, digest in manifest['inputs'].items():
        require(sha256((REPO / name).read_bytes()).hexdigest() == digest, ('input hash', name))
    require(sha256((HERE / 'fixtures.json').read_bytes()).hexdigest() == manifest['fixture_sha256'], 'fixture hash')
    old = load(REPO / 'hadwiger_nelson_parts509_rigid_block_core_pilot/engine.py', 'rigid_engine')
    data = old.build()
    require(data['facts'] == json.loads((REPO / 'hadwiger_nelson_parts509_rigid_block_core_pilot/expected.json').read_text()), 'ambient preflight')
    other = load(REPO / 'hadwiger_nelson_parts509_point613_closure_review1/independent_check.py', 'other_field')
    S = list(range(374, 509))
    unit = (288 * 288,) + (0,) * 7
    S_edges = [(u, v) for u, v in combinations(S, 2)
               if other.squared_distance(data['points'][u], data['points'][v]) == unit]
    cross = [(u, v) for u in data['vertices'] for v in S
             if other.squared_distance(data['points'][u], data['points'][v]) == unit]
    interface_input = json.loads((REPO / 'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())
    old_cross = [e for e in cross if e[0] < 374]
    require(len(S_edges) == 552 and [list(e) for e in old_cross] == interface_input['cross_edges_L_S'], 'old composition geometry')
    require(len({data['points'][v] for v in data['vertices'] + S}) == 1111, 'composition collision')
    witnesses = json.loads((HERE / 'fixtures.json').read_text())
    cases = []
    checks = 0
    patterns_seen = set()
    for row in witnesses:
        require(row['omitted'] == sorted(set(row['omitted'])) and set(row['omitted']) <= set(data['vertices']), 'omission domain')
        labels = sorted(set(data['vertices']) - set(row['omitted']))
        require(len(labels) == len(row['colouring']) and set(row['colouring']) <= set('0123'), 'T colour domain')
        cols = dict(zip(labels, map(int, row['colouring'])))
        require(cols[0] == 0 and set(data['interface']) <= set(labels), 'mandatory interface')
        require(40 not in cols and row['deleted_trial_vertex'] not in cols, 'omitted trial vertices')
        for u, v in data['edges']:
            if u in cols and v in cols:
                require(cols[u] != cols[v], 'saved T colouring')
                checks += 1
        pattern = tuple(cols[v] for v in data['nonorigin'])
        require(list(pattern) == row['pattern'] and pattern not in data['allowed'], 'saved boundary pattern')
        for kind, chosen in [('interface', old_cross), ('full', cross)]:
            if kind == 'interface' and pattern in patterns_seen:
                continue
            masks = [15] * 135
            for u, v in chosen:
                if u in cols:
                    masks[v - 374] &= ~(1 << cols[u])
            cases.append(dict(kind=kind, query=row['query'], masks=masks,
                              cnf_sha256=sha256(list_cnf(masks, S_edges)).hexdigest()))
        patterns_seen.add(pattern)
    require(len(witnesses) == 49 and len(patterns_seen) == 44 and len(cases) == 93, 'saved case coverage')
    data.update(S=S, S_edges=S_edges, cross=cross, old_cross=old_cross, witnesses=witnesses, cases=cases,
                all_edges=sorted(set(tuple(sorted(e)) for e in data['edges'] + S_edges + cross)))
    composed = composition(data)
    facts = dict(ambient_T_vertices=976, S_vertices=135, full_vertices=1111, T_edges=6406,
                 S_edges=len(S_edges), original_cross_edges=len(old_cross), all_cross_edges=len(cross),
                 additional_cross_edges=len(cross) - len(old_cross), full_edges=len(data['all_edges']),
                 exact_new_S_pair_checks=len(S) * (len(S) - 1) // 2,
                 exact_cross_pair_checks=len(data['vertices']) * len(S), saved_witnesses=49,
                 distinct_interface_patterns=44, compatibility_cases=len(cases),
                 distinct_list_instances=len({r['cnf_sha256'] for r in cases}), saved_witness_edge_checks=checks,
                 composition_cnf_variables=4 * 1111 + 976,
                 composition_cnf_clauses=len(composed.splitlines()) - 1,
                 composition_cnf_sha256=sha256(composed).hexdigest(), composition_cnf_bytes=len(composed),
                 composition_cnf_solved=False)
    data['facts'] = facts
    return data
