#!/usr/bin/env python3
"""A fixed 532-point cost-capped pilot inside the actual-composition family."""
from hashlib import sha256
import importlib.util
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


def build():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, digest in manifest['inputs'].items():
        require(sha256((REPO / name).read_bytes()).hexdigest() == digest, ('input hash', name))
    require(sha256((HERE / 'base_colouring.json').read_bytes()).hexdigest() == manifest['base_colouring_sha256'], 'base colour hash')
    source = load(REPO / 'hadwiger_nelson_parts509_partner_compatibility/data.py', 'partner_data')
    data = source.build()
    require(data['facts'] == json.loads((REPO / 'hadwiger_nelson_parts509_partner_compatibility/expected.json').read_text()), 'parent geometry')
    original = set(range(509)) - {40}
    base = json.loads((HERE / 'base_colouring.json').read_text())
    require(base['omitted_original'] == 40 and len(base['colouring']) == 508 and set(base['colouring']) <= set('0123'), 'base colouring domain')
    colour = dict(zip(sorted(original), map(int, base['colouring'])))
    adj = {v: set() for v in data['vertices'] + data['S']}
    for u, v in data['all_edges']:
        adj[u].add(v)
        adj[v].add(u)
        if u in original and v in original:
            require(colour[u] != colour[v], 'base original colouring')
    eligible = [v for v in data['vertices'] if v >= 509 and len(adj[v] & set(range(509))) <= 6]
    blocked = [v for v in eligible if {colour[u] for u in adj[v] & original} == {0, 1, 2, 3}]
    require(len(eligible) == 538 and len(blocked) == 5, 'completion selection dimensions')
    chosen = set(blocked)
    order = []
    while len(chosen) < 24:
        v = max(set(eligible) - chosen, key=lambda v: (len(adj[v] & chosen), len(adj[v] & original), -v))
        order.append(v)
        chosen.add(v)
    U = sorted((set(range(374)) - {40}) | chosen)
    vertices = sorted(set(U) | set(data['S']))
    selected_edges = [(u, v) for u, v in data['all_edges'] if u in vertices and v in vertices]
    formula = source.composition(data)
    header, *lines = formula.decode().splitlines()
    clauses = [list(map(int, line.split()[:-1])) for line in lines]
    universe = sorted(data['vertices'] + data['S'])
    position = {v: i for i, v in enumerate(universe)}
    activation = {v: 4 * len(universe) + i + 1 for i, v in enumerate(data['vertices'])}
    facts = dict(seed_vertices=len(vertices), seed_block_vertices=len(U), seed_edges=len(selected_edges),
                 seed_original_vertices=508, seed_completion_vertices=24, eligible_completions=len(eligible),
                 original_omission=40, seed_blockers=blocked, greedy_addition_order=order,
                 completion_labels=sorted(chosen), target_block_vertices=373,
                 seed_edge_sha256=sha256(''.join(f'{u},{v}\n' for u, v in selected_edges).encode()).hexdigest(),
                 parent_activation_sha256=sha256(formula).hexdigest(), parent_activation_variables=int(header.split()[2]),
                 parent_activation_clauses=len(clauses))
    data.update(seed_U=U, seed_vertices=vertices, seed_edges=selected_edges,
                full_adj=adj, activation=activation, position=position, clauses=clauses, facts=facts)
    return data


def direct(data, U, colours=4):
    vertices = sorted(set(U) | set(data['S']))
    pos = {v: i for i, v in enumerate(vertices)}
    edges = [(u, v) for u, v in data['all_edges'] if u in pos and v in pos]
    var = lambda v, c: colours * pos[v] + c + 1
    clauses = [[var(v, c) for c in range(colours)] for v in vertices]
    clauses += [[-var(u, c), -var(v, c)] for u, v in edges for c in range(colours)]
    clauses += [[var(0, 0)]]
    raw = (f'p cnf {colours * len(vertices)} {len(clauses)}\n' +
           ''.join(' '.join(map(str, row)) + ' 0\n' for row in clauses)).encode()
    return raw, vertices, edges


def check_colouring(data, U, colouring, colours=4):
    vertices = sorted(set(U) | set(data['S']))
    require(len(colouring) == len(vertices) and set(colouring) <= set(map(str, range(colours))), 'colour domain')
    mapped = dict(zip(vertices, map(int, colouring)))
    checks = 0
    for u, v in data['all_edges']:
        if u in mapped and v in mapped:
            require(mapped[u] != mapped[v], ('monochromatic unit edge', u, v))
            checks += 1
    return checks


def decode(data, U, model):
    positive = {v for v in model if v > 0}
    vertices = sorted(set(U) | set(data['S']))
    colouring = ''.join(str(next(c for c in range(4) if 4 * data['position'][v] + c + 1 in positive)) for v in vertices)
    check_colouring(data, U, colouring)
    return dict(U=sorted(U), colouring=colouring)
