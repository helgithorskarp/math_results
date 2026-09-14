#!/usr/bin/env python3
"""Every unit-edge-preserving partial translation of the point606 core is global."""
from collections import defaultdict
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RAD = (1, 3, 5, 15, 11, 33, 55, 165)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def load_points():
    for name, h in json.loads((HERE/'inputs.json').read_text()).items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == h, ('input hash', name))
    path = REPO/'hadwiger_nelson_point606_criticality_gate/verify.py'
    spec = importlib.util.spec_from_file_location('point606_input', path)
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    all_points, _, _, _ = source.load_inputs()
    cert = json.loads((path.parent/'certificate.json').read_text())
    labels = [v for v in list(range(585))+[606] if v not in cert['deleted_labels']]
    points = [all_points[v] for v in labels]
    require(len(points) == len(set(points)) == 530, 'source point set')
    return points


def norm(p, q):
    out = [0]*8
    for axis in range(2):
        d = [a-b for a, b in zip(p[axis], q[axis], strict=True)]
        for i in range(8):
            out[0] += RAD[i]*d[i]*d[i]
            for j in range(i+1, 8):
                out[i ^ j] += 2*RAD[i & j]*d[i]*d[j]
    return tuple(out)


def canonical_direction(p, q):
    d = tuple(b-a for x, y in zip(p, q, strict=True)
              for a, b in zip(x, y, strict=True))
    require(any(d), 'zero direction')
    return max(d, tuple(-x for x in d))


def geometry(points):
    edges, groups = [], defaultdict(list)
    for a, b in combinations(range(len(points)), 2):
        if norm(points[a], points[b]) == (288**2,)+(0,)*7:
            edges.append((a, b))
            groups[canonical_direction(points[a], points[b])].append((a, b))
    directions = sorted(groups)
    return edges, [groups[d] for d in directions]


def spanning_tree(n, edges):
    adjacency = [[] for _ in range(n)]
    for a, b in edges:
        require(0 <= a < b < n, 'edge domain')
        adjacency[a].append(b)
        adjacency[b].append(a)
    parent = [-1]*n
    parent[0] = 0
    todo = [0]
    for v in todo:
        for u in adjacency[v]:
            if parent[u] == -1:
                parent[u] = v
                todo.append(u)
    return parent if len(todo) == n else None


def compute():
    points = load_points()
    edges, groups = geometry(points)
    require(len(edges) == 2648 and len(groups) == 36, 'source geometry')
    tests, checked_tree_edges = 0, 0
    smallest, largest = len(edges), 0
    trace = sha256()
    for i, j in combinations(range(len(groups)), 2):
        retained = sorted(e for k, group in enumerate(groups) if k not in (i, j)
                          for e in group)
        tree = spanning_tree(len(points), retained)
        require(tree is not None, ('disconnected direction deletion', i, j))
        allowed = set(retained)
        require(all(tuple(sorted((v, tree[v]))) in allowed for v in range(1, len(points))),
                'tree edge membership')
        checked_tree_edges += len(points)-1
        trace.update((' '.join(map(str, [i, j]+tree))+'\n').encode())
        smallest = min(smallest, len(retained))
        largest = max(largest, len(retained))
        tests += 1
    return dict(all_checks=True, source_vertices=len(points), source_unit_edges=len(edges),
                complete_source_pair_checks=len(points)*(len(points)-1)//2,
                unoriented_unit_directions=len(groups), direction_pair_deletions=tests,
                all_retained_graphs_connected=True, tree_edge_memberships=checked_tree_edges,
                minimum_retained_edges=smallest, maximum_retained_edges=largest,
                source_edge_sha256=sha256(''.join(f'{a} {b}\n' for a, b in edges).encode()).hexdigest(),
                tree_stream_sha256=trace.hexdigest(),
                all_edge_preserving_partial_translations_global=True,
                minimum_image_order_in_declared_class=530,
                capped_image_exists=False, record_candidate=False,
                imported_non_four_proof_required=False)


if __name__ == '__main__':
    result = compute()
    require(result == json.loads((HERE/'EXPECTED.json').read_text()), 'expected result')
    print(json.dumps(result, sort_keys=True))
