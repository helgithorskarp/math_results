"""New original positive spanning tree, both endpoints and whole entry audits."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
from original import audit, build, canonical, require
from sparse import point_at
from check_original import audit_new


def check_tree(base, matrices, edges):
    require(len(matrices) == 2 and len(edges) == 254, 'two entire endpoints and ALL254 tree edges')
    require({e['child'] for e in edges} == set(range(1, 255)), 'each original nonempty vertex once')
    parent = {e['child']: e['parent'] for e in edges}
    for e in edges:
        v, u = e['child'], e['parent']
        require(type(v) is int and type(u) is int and 0 <= u < 255 and u != v,
                'actual original tree indices')
        require(set(base['members'][u]).isdisjoint(base['members'][v]), 'actual supported tree edge')
        require(len(e['endpoint_weights']) == 2, 'both original endpoint edge weights')
        weights = [L[u][v]/200 for L in matrices]
        require([str(x) for x in weights] == e['endpoint_weights'] and
                min(weights) >= F(617, 1310720), 'every stated tree weight bound to actual entries')
        seen = {v}; depth = 0
        while v:
            v = parent[v]; depth += 1
            require(v not in seen and depth <= 2, 'whole connected tree, path length at most two')
            seen.add(v)
    c = min(F(x) for e in edges for x in e['endpoint_weights'])
    require(c == F(617, 1310720), 'exact whole tree weight minimum')
    return c


def run():
    base = build(json.loads(Path(__file__).with_name('COEFFICIENTS.json').read_bytes())); audit(base)
    matrices = []; models = []
    for tau in (F(0), F(1, 128)):
        _, T, L = point_at(base, tau, return_matrices=True)
        models.append(audit_new(base, tau, T, L)); matrices.append(L)
    hub = base['members'].index((3,))
    edges = [{'child': v, 'parent': 0 if matrices[0][0][v] > 0 else hub,
              'endpoint_weights': [str(L[0 if matrices[0][0][v] > 0 else hub][v]/200)
                                   for L in matrices]} for v in range(1, 255)]
    c = check_tree(base, matrices, edges)
    return {'agent': 'six-downset-2', 'role': 'researcher', 'N': 255, 's': 55, 'h': 200,
            'complete_new_original_endpoint_models': models,
            'entire_tree': edges, 'tree_edge_count': 254, 'hub_index': hub,
            'max_path_to_actual_empty': 2, 'uniform_tree_weight_lower_bound': str(c),
            'uniform_original_M_upper_gap': str(c/510),
            'uniform_original_cap_nonzero_floor': str(200*c/510),
            'whole_REAL_interval': ['0', '1/128'],
            'ordinary_affine_tree_Laplacian_bridges_unformalized': True,
            'independently_reviewed': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--record', required=True)
    result = run(); raw = canonical(result)+b'\n'; Path(p.parse_args().record).write_bytes(raw)
    print(json.dumps({k: v for k, v in result.items() if k != 'entire_tree'}))
