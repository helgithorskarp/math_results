"""Produce a solver-free, fixed-core marked-neighborhood density certificate."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = {
    'H': ('ramsey_r55_root20_anchor_realization/GRAPH.json',
          '8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf'),
    'O': ('ramsey_r55_opposite22_realization/GRAPH.json',
          'e7f6086e6f99edcf47f5f931106bdfc294703e9a74aa8eb1caad60978917f355'),
    'cases': ('ramsey_r55_marked_pair_decomposition/cases.json',
              'c5dfb2f121e8b85fb4078f622257d4a6d924a3f81e055ded9f214d5ed9c89ef9'),
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def decode(doc):
    need(type(doc) is dict and set(doc) == {'n', 'red_edges'}, 'graph fields')
    n = doc['n']
    need(type(n) is int and 0 <= n <= 22, 'graph order')
    need(type(doc['red_edges']) is list, 'edge list')
    adj, previous = [0] * n, [-1, -1]
    for edge in doc['red_edges']:
        need(type(edge) is list and len(edge) == 2 and all(type(x) is int for x in edge), 'edge types')
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


def edges_in(adj, mask):
    return sum((adj[v] & mask).bit_count() for v in range(len(adj)) if mask >> v & 1) // 2


def triangle_free_maxima(dp, mask):
    best, maxima, t = -1, [], mask
    while True:
        if dp[t] <= 2:
            size = t.bit_count()
            if size > best:
                best, maxima = size, [t]
            elif size == best:
                maxima.append(t)
        if not t:
            break
        t = (t - 1) & mask
    return best, sorted(maxima)


def load_inputs():
    docs = {}
    for key, (path, digest) in INPUTS.items():
        data = (HERE.parent / path).read_bytes()
        need(hashlib.sha256(data).hexdigest() == digest, f'{key} identity')
        docs[key] = json.loads(data)
    return docs


def calculate(docs):
    h, o = decode(docs['H']), decode(docs['O'])
    need(len(h) == 20 and len(o) == 22, 'production orders')
    full = (1 << 22) - 1
    dp = clique_dp(o)
    domain = {12: [], 14: []}
    for mask, omega in enumerate(dp):
        if omega <= 3 and mask.bit_count() in domain:
            domain[mask.bit_count()].append(mask)
    cases = []
    for s1 in domain[14]:
        for s0 in domain[12]:
            if s0 | s1 == full and dp[s0 & s1] <= 2:
                cases.append({'id': len(cases), 'S0': f'{s0:06x}', 'S1': f'{s1:06x}'})
    need(json.dumps(cases, sort_keys=True) == json.dumps(docs['cases'], sort_keys=True), 'exact inherited cases')
    a, b = 0, 1
    nh = h[b]
    need(nh & 1 and nh.bit_count() == 5 and h[a].bit_count() == 7, 'marked H degrees')
    others = [v for v in range(20) if v != a and nh >> v & 1]
    need(others == [16, 17, 18, 19], 'remaining H neighbors of b')
    base = nh.bit_count() + edges_in(h, nh)
    entries = []
    for s1 in domain[14]:
        tau, maxima = triangle_free_maxima(dp, s1)
        e = edges_in(o, s1)
        entries.append({
            'S1': f'{s1:06x}', 'red_edges': e,
            'triangle_free_maximum': tau,
            'all_triangle_free_maximizers': [f'{t:06x}' for t in maxima],
            'marked_cases': sum(int(c['S1'], 16) == s1 for c in cases),
            'density_upper_at_common4': base + e + 4 + len(others) * tau,
        })
    by_s1 = {row['S1']: row for row in entries}
    bounds = []
    for case in cases:
        row = by_s1[case['S1']]
        known = base + row['red_edges'] + 4
        upper = len(others) * row['triangle_free_maximum']
        bounds.append(dict(case, known_neighborhood_red_edges=known,
                           cross_edge_variables=4 * 14,
                           cross_red_edges_required=92 - known,
                           cross_red_edges_upper=upper,
                           density_upper=known + upper,
                           deficit=92 - known - upper))
    need(len(cases) == 100 and all(row['deficit'] > 0 for row in bounds), 'whole selected branch closes')
    return {
        'scope': 'fixed H20/O22; root red H blue O; marked cross degrees 12,14; union O; no red K5',
        'required_red_neighborhood_edges_at_b': 92,
        'input_sha256': {key: value[1] for key, value in INPUTS.items()},
        'H_neighbors_of_b': [v for v in range(20) if nh >> v & 1],
        'H_red_edges_on_neighbors_of_b': edges_in(h, nh),
        'root_to_H_neighbors_of_b_red_edges': nh.bit_count(),
        'remaining_H_neighbors_of_b': others,
        'fixed_density_base': base,
        'S1_entries': entries,
        'case_bounds': bounds,
        'all_100_cases_excluded_with_density92': True,
        'uniform_density_upper': max(row['density_upper'] for row in bounds),
        'full_degree_profile_excluded': False,
        'unrestricted_fixed_core_gluing': 'UNRESOLVED',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = calculate(load_inputs())
    with args.output.open('x') as out:
        out.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'cases': len(result['case_bounds']), 'density_upper': result['uniform_density_upper'],
                      'required': 92, 'excluded': True}), flush=True)


if __name__ == '__main__':
    main()
