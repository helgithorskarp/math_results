"""Exact single-deletion inventory; standard-library CPython, no solver."""
import argparse
import base64
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_PATH = HERE.parent / 'ramsey_r55_root20_anchor_realization/GRAPH.json'
H_SHA = '8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def pairs(q):
    return itertools.combinations(q, 2)


def decode(doc):
    n = doc['n']
    require(type(n) is int and n == 22, 'expected order 22')
    text = base64.b64decode(doc['red_parent_graph6_base64'], validate=True).decode('ascii')
    require(len(text) == 1 + (n * (n - 1) // 2 + 5) // 6, 'graph6 length')
    require(ord(text[0]) - 63 == n and all(63 <= ord(c) <= 126 for c in text), 'graph6 alphabet/header')
    bits = ''.join(format(ord(c) - 63, '06b') for c in text[1:])
    require(set(bits[n * (n - 1) // 2:]) <= {'0'}, 'graph6 padding')
    edges = {e for e, b in zip(((i, j) for j in range(1, n) for i in range(j)), bits) if b == '1'}
    parent_count = len(edges)
    deletions = doc['red_deletions']
    require(type(deletions) is list and len(deletions) == 6, 'six source deletions required')
    for edge in deletions:
        require(type(edge) is list and len(edge) == 2 and all(type(x) is int for x in edge), 'edge type')
        i, j = edge
        require(0 <= i < j < n and (i, j) in edges, 'invalid/repeated deletion')
        edges.remove((i, j))
    require(parent_count == 114 and len(edges) == 108, 'source edge count')
    return n, edges


def count(edges, n, k, red):
    return sum(all((e in edges) == red for e in pairs(q))
               for q in itertools.combinations(range(n), k))


def run(doc):
    n, edges = decode(doc)
    require(count(edges, n, 4, True) == 0, 'source red K4')
    critical = {edge: [] for edge in sorted(edges)}
    blue5 = 0
    for q in itertools.combinations(range(n), 5):
        red = [e for e in pairs(q) if e in edges]
        blue5 += not red
        if len(red) == 1:
            critical[red[0]].append(list(q))
    require(blue5 == 0, 'source blue K5')
    survivors = [list(e) for e, qs in critical.items() if not qs]
    require(bool(survivors), 'no survivor; do not manufacture a graph')
    chosen = survivors[0]
    child_red = edges - {tuple(chosen)}
    opposite_red = set(pairs(range(n))) - child_red
    require(len(opposite_red) == 124 and count(opposite_red, n, 4, False) == 0
            and count(opposite_red, n, 5, True) == 0, 'opposite core failure')
    rooted = set(opposite_red)  # new vertex n is blue to all old vertices
    rooted_counts = [count(rooted, n + 1, 5, color) for color in (True, False)]
    require(rooted_counts == [0, 0], 'rooted graph failure')
    report = {
        'scope': 'all 108 single red-edge deletions of the specified source graph; no quotient',
        'parent_red_edges': 114, 'source_red_edges': 108,
        'source_red_K4': 0, 'source_blue_K5': 0,
        'five_sets_scanned': 26334,
        'cases': [{'deleted_edge': list(e), 'red_K4': 0,
                   'blue_K5': len(qs), 'first_blue_K5': qs[0] if qs else None}
                  for e, qs in critical.items()],
        'surviving_deletions': survivors, 'chosen_deletion': chosen,
        'opposite_red_edges': 124, 'opposite_blue_edges': 107,
        'opposite_red_K5': 0, 'opposite_blue_K4': 0,
        'blue_root_extension_order': 23,
        'blue_root_extension_red_K5': rooted_counts[0],
        'blue_root_extension_blue_K5': rooted_counts[1],
    }
    graph = {'n': n, 'red_edges': [list(e) for e in sorted(opposite_red)]}
    h_bytes = H_PATH.read_bytes()
    require(hashlib.sha256(h_bytes).hexdigest() == H_SHA, 'H20 identity')
    h = json.loads(h_bytes)
    require(h['n'] == 20, 'H20 order')
    h_degrees = [sum(v in e for e in h['red_edges']) for v in range(20)]
    o_degrees = [sum(v in e for e in opposite_red) for v in range(n)]
    h_cross = [(19 if v < 2 else 20) - h_degrees[v] for v in range(20)]
    o_cross = [21 - d for d in o_degrees]
    require(sum(h_cross) == sum(o_cross) == 214, 'cross debt mismatch')
    handoff = {
        'scope': 'two valid local neighborhoods and necessary scalar/degree debts only; no gluing feasibility claim',
        'H20_graph_sha256': H_SHA, 'H20_red_degrees': h_degrees,
        'O22_red_degrees': o_degrees, 'O22_blue_degrees': o_cross,
        'H20_required_cross_red_degrees': h_cross,
        'O22_required_cross_red_degrees': o_cross,
        'cross_red_edges': 214, 'cross_pairs_unfixed': 440,
        'root_red_degree': 20, 'target_red_edge_total': 450,
        'target_red_degrees': [20, 20, 20] + [21] * 40,
        'outside_marking': 'unfixed: local H vertices 0 and 1 need cross degrees 12 and 14; requiring their union to be all O forces only-first/only-second/both sizes 8/10/4',
    }
    return report, graph, handoff


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=HERE / 'INPUT.json')
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    report, graph, handoff = run(json.loads(args.input.read_text()))
    for name, obj in [('result.json', report), ('GRAPH.json', graph), ('HANDOFF.json', handoff)]:
        save(args.work / name, obj)
    print(json.dumps({'cases': len(report['cases']), 'survivors': len(report['surviving_deletions']),
                      'chosen': report['chosen_deletion'], 'opposite_edges': [124, 107]}))


if __name__ == '__main__':
    main()
