#!/usr/bin/env python3
"""Verify a subgraph size bound from explicit single-deletion colourings.

Uses exact geometry and positive witnesses only; no solver is imported.
"""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_colouring(labels, edges, deleted, colours):
    require(type(deleted) is int and deleted in labels, 'deleted vertex label')
    require(type(colours) is str and len(colours) == len(labels), 'colour string length')
    require(set(colours) <= set('.0123'), 'colour alphabet')
    require([labels[i] for i, c in enumerate(colours) if c == '.'] == [deleted], 'deletion marker')
    c = dict(zip(labels, colours, strict=True))
    checked = 0
    for a, b in edges:
        if deleted not in (a, b):
            require(c[a] != c[b], f'improper edge {a},{b} after deleting {deleted}')
            checked += 1
    return checked


def compute():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, digest in manifest['inputs'].items():
        require(sha256((REPO / name).read_bytes()).hexdigest() == digest, f'input hash: {name}')
    raw = (HERE / 'certificate.json').read_bytes()
    require(sha256(raw).hexdigest() == manifest['certificate_sha256'], 'new certificate hash')
    cert = json.loads(raw)
    old = json.loads((REPO / 'hadwiger_nelson_parts509_pool_obstruction574/certificate.json').read_text())
    table = json.loads((REPO / 'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())
    spec = importlib.util.spec_from_file_location(
        'integer_geometry', REPO / 'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py')
    geometry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geometry)
    denominator, points, universe, pool, all_edges = geometry.read_geometry()
    X = old['pool_labels']
    require(X == sorted(set(X)) and len(X) == 200 and set(X) <= set(pool), 'X definition')
    labels = list(range(374)) + X
    H = set(labels)
    require(len(H) == 574 and len({points[v] for v in labels}) == 574, 'distinct graph vertices')
    require(cert['labels'] == labels, 'new certificate label order')
    edges = [e for e in all_edges if set(e) <= H]
    digest = sha256(''.join(f'{a},{b}\n' for a, b in edges).encode()).hexdigest()
    require(digest == '37d330b472e101c001e04aca6a1dc52ddf4f048d025adce0794f4e521682f575', 'H edge hash')
    require([r['vertex'] for r in old['deletions']] == X, 'old deletion coverage')
    edge_checks = 0
    for row in old['deletions']:
        index = row['pattern']
        require(type(index) is int and 0 <= index < len(table['classes']), 'old L witness index')
        left = table['classes'][index]['witness_colouring_L']
        require(len(left) == 374 and set(left) <= set('0123'), 'old L witness format')
        edge_checks += check_colouring(labels, edges, row['vertex'], left + row['pool_colours'])
    new_labels = [r['vertex'] for r in cert['deletions']]
    require(new_labels == list(range(309)), 'new deletion coverage')
    for row in cert['deletions']:
        edge_checks += check_colouring(labels, edges, row['vertex'], row['colours'])
    forced = set(X) | set(new_labels)
    require(len(forced) == 509, 'distinct forced vertices')
    return dict(graph_vertices=len(labels), graph_edges=len(edges), coordinate_denominator=denominator,
                edge_sha256=digest, old_pool_deletion_colourings=200,
                new_L_deletion_colourings=309, distinct_forced_vertices=len(forced),
                verified_retained_edge_incidences=edge_checks,
                all_subgraphs_through_order=len(forced)-1,
                all_such_subgraphs_four_colourable=True,
                untested_L_vertices=list(range(309,374)),
                solver_or_UNSAT_certificate_required=False,
                status='EVERY AT-MOST-508-VERTEX SUBGRAPH OF H574 IS FOUR-COLOURABLE')


def main():
    result = compute()
    require(result == json.loads((HERE/'expected.json').read_text()), 'expected facts mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
