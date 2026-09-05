#!/usr/bin/env python3
"""Direct full-graph colourability under positive activation assumptions."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_graph():
    prior = REPO / 'hadwiger_nelson_parts509_pool_obstruction574'
    manifest = json.loads((prior / 'manifest.json').read_text())
    for name, digest in manifest['inputs'].items():
        require(sha256((REPO / name).read_bytes()).hexdigest() == digest, name)
    raw = (prior / 'certificate.json').read_bytes()
    require(sha256(raw).hexdigest() == manifest['certificate_sha256'], 'H certificate hash')
    spec = importlib.util.spec_from_file_location(
        'exact_geometry', REPO / 'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    geom = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geom)
    den, points, universe, pool, all_edges = geom.read_geometry()
    cert = json.loads(raw)
    selected = cert['pool_labels']
    labels = list(range(374)) + selected
    keep = set(labels)
    edges = [e for e in all_edges if set(e) <= keep]
    require(len(keep) == 574 and len(edges) == 2707, 'graph order or size')
    digest = sha256(''.join(f'{a},{b}\n' for a, b in edges).encode()).hexdigest()
    require(digest == '37d330b472e101c001e04aca6a1dc52ddf4f048d025adce0794f4e521682f575', 'edge hash')
    return labels, edges, cert


def encode(labels, edges, selectable, triangle=()):
    require(len(set(labels)) == len(labels), 'duplicate vertex')
    selectable = sorted(selectable)
    require(set(selectable) <= set(labels), 'activation labels')
    require(len(set(triangle)) == len(triangle) and len(triangle) in (0, 3), 'triangle format')
    require(set(triangle) <= set(labels) - set(selectable), 'pins must be required vertices')
    edge_set = {tuple(sorted(e)) for e in edges}
    require(all(tuple(sorted((a, b))) in edge_set for i, a in enumerate(triangle)
                for b in triangle[i+1:]), 'pin triangle')
    colours = {v: [4*i+c+1 for c in range(4)] for i, v in enumerate(labels)}
    activation = {v: 4*len(labels)+i+1 for i, v in enumerate(selectable)}
    rows = [([-activation[v]] if v in activation else []) + colours[v] for v in labels]
    rows += [[-colours[a][c], -colours[b][c]] for a, b in edges for c in range(4)]
    rows += [[colours[v][c]] for c, v in enumerate(triangle)]
    return rows, dict(colours=colours, activation=activation,
                      variables=4*len(labels)+len(selectable), clauses=len(rows))


def decode(labels, edges, meta, model, selected):
    positive = {v for v in model if v > 0}
    c = {v: next(i for i, lit in enumerate(meta['colours'][v]) if lit in positive)
         for v in selected}
    require(all(c[a] != c[b] for a, b in edges if a in c and b in c), 'improper decoded colouring')
    return ''.join(str(c[v]) if v in c else '.' for v in labels)


def dimacs(rows, variables):
    return (f'p cnf {variables} {len(rows)}\n' +
            ''.join(' '.join(map(str, row))+' 0\n' for row in rows)).encode()
