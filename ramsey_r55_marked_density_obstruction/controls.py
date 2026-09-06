"""Finite proof-bridge, small-instance and rejection controls."""
import argparse
import copy
import itertools
import json
from pathlib import Path

import analyze
import verify


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rejected(function, *args):
    try:
        function(*args)
    except ValueError:
        return
    raise ValueError('negative control accepted')


def small_clique_controls():
    graphs, subsets, maxima_checks = 0, 0, 0
    for n in range(6):
        pairs = list(itertools.combinations(range(n), 2))
        for code in range(1 << len(pairs)):
            edges = [list(e) for i, e in enumerate(pairs) if code >> i & 1]
            doc = {'n': n, 'red_edges': edges}
            adj = analyze.decode(doc)
            _, edge_set = verify.graph(doc)
            dp = analyze.clique_dp(adj)
            for mask in range(1 << n):
                verts = [v for v in range(n) if mask >> v & 1]
                literal = max(k for k in range(len(verts) + 1)
                              if any(verify.clique(t, edge_set) for t in itertools.combinations(verts, k)))
                require(dp[mask] == literal, 'small exact clique number')
                subsets += 1
            best, masks = analyze.triangle_free_maxima(dp, (1 << n) - 1)
            reference, _ = verify.literal_maxima(set(range(n)), edge_set, best)
            require(masks == reference, 'small complete triangle-free maximizers')
            maxima_checks += 1
            graphs += 1
    return {'all_labeled_graphs_orders0_to5': graphs, 'subset_clique_numbers': subsets,
            'complete_triangle_free_maximizer_lists': maxima_checks}


def density_bridge_controls():
    # Root r=0; H={1,2,3} with a=1,b=2; O={4,5,6}. All four H graphs
    # containing ab, all eight O graphs, and all 512 cross matrices.
    h_pairs = [(1, 2), (1, 3), (2, 3)]
    o_pairs = [(4, 5), (4, 6), (5, 6)]
    cross = list(itertools.product(range(1, 4), range(4, 7)))
    tested = safe = witnesses_need_red_K5_hypothesis = nonzero_common = 0
    for hcode in range(4):
        eh = {(1, 2)} | {p for i, p in enumerate(h_pairs[1:]) if hcode >> i & 1}
        nh = {v for v in range(1, 4) if tuple(sorted((2, v))) in eh}
        for ocode in range(8):
            eo = {p for i, p in enumerate(o_pairs) if ocode >> i & 1}
            for xcode in range(512):
                edges = eh | eo | {(0, 1), (0, 2), (0, 3)}
                edges |= {p for i, p in enumerate(cross) if xcode >> i & 1}
                s = {v for v in range(4, 7) if (2, v) in edges}
                s0 = {v for v in range(4, 7) if (1, v) in edges}
                neighborhood = {v for v in range(7) if tuple(sorted((2, v))) in edges}
                actual = sum(e in edges for e in itertools.combinations(sorted(neighborhood), 2))
                e_h = sum(e in eh for e in itertools.combinations(sorted(nh), 2))
                e_s = sum(e in eo for e in itertools.combinations(sorted(s), 2))
                common = len(s & s0)
                other_cross = sum((v, o) in edges for v in nh - {1} for o in s)
                identity = len(nh) + e_h + e_s + common + other_cross
                require(actual == identity, 'literal density identity')
                tau = max(len(t) for k in range(len(s) + 1) for t in itertools.combinations(sorted(s), k)
                          if not any(verify.clique(q, eo) for q in itertools.combinations(t, 3)))
                bound = len(nh) + e_h + e_s + common + (len(nh) - 1) * tau
                no_red_K5 = not any(verify.clique(q, edges) for q in itertools.combinations(range(7), 5))
                if no_red_K5:
                    require(actual <= bound, 'red-K5-free density cap')
                    safe += 1
                elif actual > bound:
                    witnesses_need_red_K5_hypothesis += 1
                nonzero_common += int(common > 0)
                tested += 1
    require(witnesses_need_red_K5_hypothesis > 0 and nonzero_common > 0, 'nonvacuous bridge controls')
    return {'full_graphs': tested, 'red_K5_free_graphs': safe,
            'graphs_violating_bound_when_red_K5_hypothesis_dropped': witnesses_need_red_K5_hypothesis,
            'graphs_with_nonzero_common_term': nonzero_common}


def corruption_controls(certificate, expected):
    mutations = []
    for field, value in [('uniform_density_upper', 92), ('required_red_neighborhood_edges_at_b', 90),
                         ('all_100_cases_excluded_with_density92', 1), ('full_degree_profile_excluded', True),
                         ('fixed_density_base', 8), ('unrestricted_fixed_core_gluing', 'UNSAT')]:
        doc = copy.deepcopy(certificate)
        doc[field] = value
        mutations.append(doc)
    for field, value in [('known_neighborhood_red_edges', 57), ('cross_edge_variables', 55),
                         ('cross_red_edges_upper', 34), ('cross_red_edges_required', 32),
                         ('deficit', 0), ('id', 1), ('S1', '1276fe')]:
        doc = copy.deepcopy(certificate)
        doc['case_bounds'][0][field] = value
        mutations.append(doc)
    doc = copy.deepcopy(certificate)
    doc['case_bounds'].pop()
    mutations.append(doc)
    doc = copy.deepcopy(certificate)
    doc['S1_entries'].pop(0)
    mutations.append(doc)
    doc = copy.deepcopy(certificate)
    doc['S1_entries'][0]['triangle_free_maximum'] = 7
    mutations.append(doc)
    doc = copy.deepcopy(certificate)
    doc['S1_entries'][0]['all_triangle_free_maximizers'].pop()
    mutations.append(doc)
    doc = copy.deepcopy(certificate)
    doc['S1_entries'][0]['all_triangle_free_maximizers'][0] = '1276fe'
    mutations.append(doc)
    for doc in mutations:
        rejected(verify.check_certificate, doc, expected)
    malformed = [
        {'n': True, 'red_edges': []}, {'n': 2, 'red_edges': [[0, True]]},
        {'n': 2, 'red_edges': [[0, 1], [0, 1]]}, {'n': 2, 'red_edges': [[1, 0]]},
        {'n': 2, 'red_edges': [[0, 2]]}, {'n': 2, 'red_edges': [[0, 0]]},
        {'n': 3, 'red_edges': [[1, 2], [0, 1]]}, {'n': 2, 'red_edges': [], 'extra': 1},
    ]
    for doc in malformed:
        rejected(analyze.decode, doc)
        rejected(verify.graph, doc)
    return {'corrupt_certificates_rejected': len(mutations), 'malformed_graphs_rejected_by_both': len(malformed)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    expected, _ = verify.reconstruct()
    verify.check_certificate(certificate, expected)
    report = {'accepted': True, 'small_graphs': small_clique_controls(),
              'proof_bridge': density_bridge_controls(),
              'negative_controls': corruption_controls(certificate, expected)}
    with args.report.open('x') as out:
        out.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
