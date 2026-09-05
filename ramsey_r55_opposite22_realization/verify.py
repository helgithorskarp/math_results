"""Independent replay: explicitly delete every edge and recurse on clique intersections.

No producer import and no use of its single-hole reduction for acceptance.
"""
import argparse
import base64
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def source(doc):
    need(type(doc['n']) is int and doc['n'] == 22, 'order')
    raw = base64.b64decode(doc['red_parent_graph6_base64'], validate=True)
    need(len(raw) == 40 and raw[0] == 85 and all(63 <= x <= 126 for x in raw), 'graph6 bytes')
    need((raw[-1] - 63) & 7 == 0, 'nonzero padding')
    rows = [0] * 22
    offset = 0
    for v in range(1, 22):
        for u in range(v):
            if ((raw[1 + offset // 6] - 63) >> (5 - offset % 6)) & 1:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
            offset += 1
    need(sum(x.bit_count() for x in rows) == 228, 'parent count')
    need(type(doc['red_deletions']) is list and len(doc['red_deletions']) == 6, 'deletions')
    for pair in doc['red_deletions']:
        need(type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair), 'deletion type')
        u, v = pair
        need(0 <= u < v < 22 and (rows[u] >> v) & 1, 'missing or invalid deletion')
        rows[u] ^= 1 << v
        rows[v] ^= 1 << u
    need(sum(x.bit_count() for x in rows) == 216, 'source count')
    return rows


def graph_rows(doc, n):
    need(set(doc) == {'n', 'red_edges'} and type(doc['n']) is int and doc['n'] == n, 'graph fields/order')
    need(type(doc['red_edges']) is list, 'edge list')
    rows = [0] * n
    for pair in doc['red_edges']:
        need(type(pair) is list and len(pair) == 2 and all(type(x) is int for x in pair), 'edge type')
        u, v = pair
        need(0 <= u < v < n and not ((rows[u] >> v) & 1), 'loop/range/duplicate')
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return rows


def complement(rows):
    full = (1 << len(rows)) - 1
    return [full ^ (1 << v) ^ row for v, row in enumerate(rows)]


def clique_list(rows, k):
    out = []
    def visit(prefix, available, remaining):
        if not remaining:
            out.append(prefix)
            return
        while available.bit_count() >= remaining:
            bit = available & -available
            available ^= bit
            v = bit.bit_length() - 1
            visit(prefix + [v], available & rows[v], remaining - 1)
    visit([], (1 << len(rows)) - 1, k)
    return out


def check(doc, result, graph, handoff):
    rows = source(doc)
    need(not clique_list(rows, 4) and not clique_list(complement(rows), 5), 'invalid source')
    edges = [(u, v) for u in range(22) for v in range(u + 1, 22) if (rows[u] >> v) & 1]
    cases, survivors = [], []
    for u, v in edges:
        child = rows.copy()
        child[u] ^= 1 << v
        child[v] ^= 1 << u
        r4 = clique_list(child, 4)
        b5 = clique_list(complement(child), 5)
        need(not r4, 'deletion created red K4')
        cases.append({'deleted_edge': [u, v], 'red_K4': len(r4), 'blue_K5': len(b5),
                      'first_blue_K5': min(b5) if b5 else None})
        if not b5:
            survivors.append([u, v])
    need(json.dumps(result['cases'], sort_keys=True) == json.dumps(cases, sort_keys=True)
         and json.dumps(result['surviving_deletions']) == json.dumps(survivors), 'case-level mismatch')
    need(bool(survivors) and json.dumps(result['chosen_deletion']) == json.dumps(survivors[0]), 'chosen survivor')
    expected = rows.copy()
    u, v = survivors[0]
    expected[u] ^= 1 << v
    expected[v] ^= 1 << u
    expected = complement(expected)
    opposite = graph_rows(graph, 22)
    need(opposite == expected, 'opposite edge list mismatch')
    need(not clique_list(opposite, 5) and not clique_list(complement(opposite), 4), 'opposite forbidden clique')
    # A new blue-universal root has no red incidences.
    rooted = opposite + [0]
    need(not clique_list(rooted, 5) and not clique_list(complement(rooted), 5), 'rooted forbidden clique')
    constants = {'parent_red_edges': 114, 'source_red_edges': 108,
                 'source_red_K4': 0, 'source_blue_K5': 0, 'five_sets_scanned': 26334,
                 'opposite_red_edges': 124, 'opposite_blue_edges': 107,
                 'opposite_red_K5': 0, 'opposite_blue_K4': 0,
                 'blue_root_extension_order': 23, 'blue_root_extension_red_K5': 0,
                 'blue_root_extension_blue_K5': 0}
    need(all(type(result[k]) is int and result[k] == val for k, val in constants.items()), 'result scalar')
    need(sum(x.bit_count() for x in opposite) == 248, 'opposite edge count')
    hp = HERE.parent / 'ramsey_r55_root20_anchor_realization/GRAPH.json'
    hb = hp.read_bytes()
    need(hashlib.sha256(hb).hexdigest() == '8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf', 'H identity')
    h = graph_rows(json.loads(hb), 20)
    need(not clique_list(h, 4) and not clique_list(complement(h), 5), 'H forbidden clique')
    hd, od = [r.bit_count() for r in h], [r.bit_count() for r in opposite]
    hc = [19 - hd[v] if v < 2 else 20 - hd[v] for v in range(20)]
    oc = [21 - d for d in od]
    want = {'H20_graph_sha256': hashlib.sha256(hb).hexdigest(), 'H20_red_degrees': hd,
            'O22_red_degrees': od, 'O22_blue_degrees': oc,
            'H20_required_cross_red_degrees': hc, 'O22_required_cross_red_degrees': oc,
            'cross_red_edges': 214, 'cross_pairs_unfixed': 440,
            'root_red_degree': 20, 'target_red_edge_total': 450,
            'target_red_degrees': [20] * 3 + [21] * 40}
    need(all(json.dumps(handoff[k]) == json.dumps(val) for k, val in want.items()), 'handoff mismatch')
    need(sum(hc) == sum(oc) == 214 and 92 + 124 + 20 + 214 == 450, 'edge debts')
    need(hc[:2] == [12, 14] and (h[0] & h[1]) == 0 and h[0] & 2, 'marked H structure')
    return {'status': 'VERIFIED', 'explicit_deletion_graphs_checked': len(cases),
            'entry_level_records_matched': len(cases), 'survivors': len(survivors),
            'selected_opposite_graph_checked': True, 'blue_root_extension_checked': True,
            'H20_rechecked': True, 'cross_debts_checked': True,
            'gluing_feasibility_tested': False, 'target_graph_found': False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, default=HERE / 'INPUT.json')
    p.add_argument('--work', type=Path, default=HERE)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    docs = [json.loads(a.input.read_text())] + [json.loads((a.work / n).read_text())
                                               for n in ('result.json', 'GRAPH.json', 'HANDOFF.json')]
    report = check(*docs)
    a.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
