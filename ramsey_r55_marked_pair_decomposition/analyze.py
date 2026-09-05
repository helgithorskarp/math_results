"""Exact marked attachment decomposition by subset clique-number DP."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
GRAPH = HERE.parent / 'ramsey_r55_opposite22_realization/GRAPH.json'
GRAPH_SHA = 'e7f6086e6f99edcf47f5f931106bdfc294703e9a74aa8eb1caad60978917f355'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def decode(doc):
    need(set(doc) == {'n', 'red_edges'} and type(doc['n']) is int and 1 <= doc['n'] <= 22, 'graph fields/order')
    n = doc['n']
    need(type(doc['red_edges']) is list, 'edge list')
    previous = [-1, -1]
    adj = [0] * n
    for edge in doc['red_edges']:
        need(type(edge) is list and len(edge) == 2 and all(type(v) is int for v in edge), 'edge types')
        u, v = edge
        need(0 <= u < v < n and edge > previous, 'edge range/order/duplicate')
        adj[u] |= 1 << v
        adj[v] |= 1 << u
        previous = edge
    return adj


def clique_dp(adj):
    dp = bytearray(1 << len(adj))
    for mask in range(1, len(dp)):
        bit = mask & -mask
        rest = mask ^ bit
        v = bit.bit_length() - 1
        dp[mask] = max(dp[rest], 1 + dp[rest & adj[v]])
    return dp


def domain_hash(masks):
    return hashlib.sha256(b''.join(struct.pack('<I', m) for m in masks)).hexdigest()


def local_graph(adj, s0, s1):
    n = len(adj)
    edges = [[0, 1], [0, 2], [1, 2]]
    edges += [[v + 3, w + 3] for v, w in itertools.combinations(range(n), 2) if adj[v] >> w & 1]
    edges += [[i + 1, v + 3] for i, mask in enumerate((s0, s1)) for v in range(n) if mask >> v & 1]
    return {'n': n + 3, 'red_edges': sorted(edges)}


def boundary_rows(cases, n=22, total_primary=440):
    """100-way exact DNF with fresh selectors above all 440 cross primaries."""
    rows = [tuple(range(total_primary + 1, total_primary + len(cases) + 1))]
    for j, case in enumerate(cases):
        selector = total_primary + j + 1
        for i, name in enumerate(('S0', 'S1')):
            mask = int(case[name], 16)
            for v in range(n):
                lit = i * n + v + 1
                rows.append((-selector, lit if mask >> v & 1 else -lit))
    return rows


def calculate(adj):
    n = len(adj)
    need(n == 22, 'production order22')
    full = (1 << n) - 1
    dp = clique_dp(adj)
    # Direct local checks keep the proof independent of any numerical Ramsey bound.
    need(dp[full] == 4, 'O red clique number')
    blue = [full ^ row ^ (1 << v) for v, row in enumerate(adj)]
    need(not any(all(blue[u] >> v & 1 for u, v in itertools.combinations(q, 2))
                 for q in itertools.combinations(range(n), 4)), 'O blue K4')
    domains = {k: [] for k in (12, 14, 15)}
    maximum = 0
    for mask, omega in enumerate(dp):
        if omega <= 3:
            k = mask.bit_count()
            maximum = max(maximum, k)
            if k in domains:
                domains[k].append(mask)
    cases, rejected = [], []
    cover = 0
    for s1 in domains[14]:
        for s0 in domains[12]:
            if s0 | s1 != full:
                continue
            cover += 1
            common = s0 & s1
            need(common.bit_count() == 4, 'intersection count')
            if dp[common] >= 3:
                q = next(q for q in itertools.combinations(range(n), 3)
                         if all(common >> v & 1 for v in q)
                         and all(adj[u] >> v & 1 for u, v in itertools.combinations(q, 2)))
                rejected.append({'S0': f'{s0:06x}', 'S1': f'{s1:06x}', 'red_triangle': list(q)})
            else:
                cases.append({'id': len(cases), 'S0': f'{s0:06x}', 'S1': f'{s1:06x}'})
    need(bool(cases), 'no local witness; this run expects nonempty decomposition')
    report = {
        'scope': 'fixed O22, red anchor triangle, |S0|=12, |S1|=14, S0 union S1=O; exact local25 R55 attachments only',
        'max_red_K4_free_induced_order': maximum,
        'domain_counts': {str(k): len(v) for k, v in domains.items()},
        'domain_sha256_u32le_sorted': {str(k): domain_hash(v) for k, v in domains.items()},
        'all_maximizers': [f'{m:06x}' for m in domains[14]],
        'degree_and_cover_pairs_before_clique_checks': 320089770,
        'red_K4_free_cover_pairs': cover,
        'rejected_common_triangle_pairs': rejected,
        'local_R55_pairs': len(cases),
        'case_counts_by_S1': {f'{s:06x}': sum(int(c['S1'], 16) == s for c in cases) for s in domains[14]},
        'unfixed_cross_edges_per_case': 396,
        'boundary_primary_variables': 440, 'boundary_constrained_primaries': 44,
        'boundary_selectors': len(cases), 'boundary_clauses': 1 + 44 * len(cases),
        'global_43_vertex_feasibility': 'UNRESOLVED; no solver run in this decomposition',
    }
    witness = local_graph(adj, int(cases[0]['S0'], 16), int(cases[0]['S1'], 16))
    return report, cases, witness, domains


def save(path, doc):
    path.write_text(json.dumps(doc, indent=2) + '\n')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    a.work.mkdir(parents=True, exist_ok=False)
    data = GRAPH.read_bytes()
    need(hashlib.sha256(data).hexdigest() == GRAPH_SHA, 'input identity')
    report, cases, witness, domains = calculate(decode(json.loads(data)))
    for name, doc in [('result.json', report), ('cases.json', cases), ('LOCAL_GRAPH.json', witness)]:
        save(a.work / name, doc)
    for k, masks in domains.items():
        (a.work / f'domain{k}.bin').write_bytes(b''.join(struct.pack('<I', m) for m in masks))
    rows = boundary_rows(cases)
    with (a.work / 'boundary.cnf').open('w') as out:
        out.write(f'p cnf {440 + len(cases)} {len(rows)}\n')
        for row in rows:
            out.write(' '.join(map(str, row)) + ' 0\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
