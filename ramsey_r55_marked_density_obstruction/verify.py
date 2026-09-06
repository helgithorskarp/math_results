"""Independent fixed-size/set checker; imports no producer or earlier checker."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = [
    ('H', 'ramsey_r55_root20_anchor_realization/GRAPH.json',
     '8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf'),
    ('O', 'ramsey_r55_opposite22_realization/GRAPH.json',
     'e7f6086e6f99edcf47f5f931106bdfc294703e9a74aa8eb1caad60978917f355'),
    ('cases', 'ramsey_r55_marked_pair_decomposition/cases.json',
     'c5dfb2f121e8b85fb4078f622257d4a6d924a3f81e055ded9f214d5ed9c89ef9'),
]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def graph(doc):
    require(type(doc) is dict and set(doc) == {'n', 'red_edges'}, 'graph fields')
    n = doc['n']
    require(type(n) is int and 0 <= n <= 22, 'graph order')
    require(type(doc['red_edges']) is list, 'edge list')
    pairs = []
    for edge in doc['red_edges']:
        require(type(edge) is list and len(edge) == 2 and all(type(v) is int for v in edge), 'edge type')
        u, v = edge
        require(0 <= u < v < n, 'edge range')
        pairs.append((u, v))
    require(pairs == sorted(set(pairs)), 'edge order/duplicate')
    return n, set(pairs)


def clique(vertices, edges):
    return all(pair in edges for pair in itertools.combinations(sorted(vertices), 2))


def mask(vertices):
    return sum(1 << v for v in vertices)


def literal_maxima(vertices, edges, size):
    """All triangle-free size-sets, plus every obstruction at size+1."""
    triangles = [frozenset(t) for t in itertools.combinations(sorted(vertices), 3) if clique(t, edges)]
    maxima = []
    for t in itertools.combinations(sorted(vertices), size):
        subset = set(t)
        if not any(q <= subset for q in triangles):
            maxima.append(mask(t))
    rejected = 0
    for t in itertools.combinations(sorted(vertices), size + 1):
        subset = set(t)
        require(any(q <= subset for q in triangles), 'unobstructed larger triangle-free set')
        rejected += 1
    require(maxima, 'missing lower-bound witness')
    return sorted(maxima), rejected


def reconstruct():
    docs, digests = {}, {}
    for key, path, digest in SOURCES:
        data = (HERE.parent / path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == digest, f'{key} identity')
        docs[key] = json.loads(data)
        digests[key] = digest
    nh, eh = graph(docs['H'])
    no, eo = graph(docs['O'])
    require((nh, no) == (20, 22), 'orders')
    # Fixed-size subsets and literal four-cliques, not the producer's clique DP.
    k4 = [mask(q) for q in itertools.combinations(range(no), 4) if clique(q, eo)]
    domain = []
    examined14 = 0
    for q in itertools.combinations(range(no), 14):
        m = mask(q)
        examined14 += 1
        if not any(m & bad == bad for bad in k4):
            domain.append(m)
    domain.sort()
    require(len(domain) == 5, 'five complete size14 neighborhoods')
    universe = set(range(no))
    cases = []
    entries = []
    examined9 = 0
    for s1 in domain:
        vertices = {v for v in range(no) if s1 >> v & 1}
        maxima, rejected = literal_maxima(vertices, eo, 8)
        examined9 += rejected
        # Coverage makes the ten nonneighbors of a a ten-subset of S1.
        local_cases = []
        for nonneighbors in itertools.combinations(sorted(vertices), 10):
            s0_vertices = universe - set(nonneighbors)
            s0 = mask(s0_vertices)
            if any(s0 & bad == bad for bad in k4):
                continue
            common = vertices & s0_vertices
            require(len(common) == 4, 'coverage intersection')
            if any(clique(t, eo) for t in itertools.combinations(sorted(common), 3)):
                continue
            local_cases.append(s0)
        for s0 in sorted(local_cases):
            cases.append({'id': len(cases), 'S0': f'{s0:06x}', 'S1': f'{s1:06x}'})
        e = sum(pair in eo for pair in itertools.combinations(sorted(vertices), 2))
        entries.append({'S1': f'{s1:06x}', 'red_edges': e, 'triangle_free_maximum': 8,
                        'all_triangle_free_maximizers': [f'{t:06x}' for t in maxima],
                        'marked_cases': len(local_cases), 'density_upper_at_common4': 9 + e + 4 + 4 * 8})
    require(json.dumps(cases, sort_keys=True) == json.dumps(docs['cases'], sort_keys=True), 'entry-level case coverage')
    neighbors = {v for v in range(nh) if tuple(sorted((1, v))) in eh}
    require(neighbors == {0, 16, 17, 18, 19}, 'literal H neighbors of b')
    e_h = sum(pair in eh for pair in itertools.combinations(sorted(neighbors), 2))
    require(e_h == 4 and len(neighbors) == 5, 'literal H constants')
    bounds = []
    for case in cases:
        # Reconstruct the actual fixed graph induced by N_red(b), vertex by vertex.
        # Its labels are r=0, H=1..20, O=21..42; only four-by-fourteen edges remain free.
        s0, s1 = int(case['S0'], 16), int(case['S1'], 16)
        verts = [0] + [1 + h for h in sorted(neighbors)] + [21 + o for o in range(no) if s1 >> o & 1]
        known, free = 0, 0
        for u, v in itertools.combinations(verts, 2):
            if u == 0:
                known += int(v <= 20)
            elif v <= 20:
                known += int((u - 1, v - 1) in eh)
            elif u >= 21:
                known += int((u - 21, v - 21) in eo)
            elif u == 1:
                known += (s0 >> (v - 21)) & 1
            else:
                free += 1
        entry = next(row for row in entries if row['S1'] == case['S1'])
        upper = (len(neighbors) - 1) * entry['triangle_free_maximum']
        require(free == 56 and 92 > known + upper, 'strict density obstruction')
        bounds.append(dict(case, known_neighborhood_red_edges=known, cross_edge_variables=free,
                           cross_red_edges_required=92 - known, cross_red_edges_upper=upper,
                           density_upper=known + upper, deficit=92 - known - upper))
    expected = {
        'scope': 'fixed H20/O22; root red H blue O; marked cross degrees 12,14; union O; no red K5',
        'required_red_neighborhood_edges_at_b': 92, 'input_sha256': digests,
        'H_neighbors_of_b': sorted(neighbors), 'H_red_edges_on_neighbors_of_b': e_h,
        'root_to_H_neighbors_of_b_red_edges': len(neighbors),
        'remaining_H_neighbors_of_b': sorted(neighbors - {0}),
        'fixed_density_base': e_h + len(neighbors), 'S1_entries': entries, 'case_bounds': bounds,
        'all_100_cases_excluded_with_density92': True,
        'uniform_density_upper': max(row['density_upper'] for row in bounds),
        'full_degree_profile_excluded': False, 'unrestricted_fixed_core_gluing': 'UNRESOLVED',
    }
    report = {'accepted': True, 'four_cliques_of_O': len(k4), 'size14_subsets_examined': examined14,
              'size14_sets_entry_matched': len(domain), 'triangle_free_size8_sets_entry_matched':
              sum(len(row['all_triangle_free_maximizers']) for row in entries),
              'size9_sets_obstructed': examined9, 'markings_entry_matched': len(cases),
              'density_equations_reconstructed_from_fixed_graph': len(bounds),
              'uniform_density_upper': expected['uniform_density_upper'],
              'required_density': 92, 'independent_peer_review': False}
    return expected, report


def check_certificate(doc, expected):
    # Serialized comparison rejects integer/bool aliases as well as missing/extra fields.
    require(json.dumps(doc, sort_keys=True) == json.dumps(expected, sort_keys=True), 'certificate mismatch')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    expected, report = reconstruct()
    check_certificate(json.loads(args.certificate.read_text()), expected)
    with args.report.open('x') as out:
        out.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
