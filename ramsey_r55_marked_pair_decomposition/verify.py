"""Independent fixed-size enumeration and complement-first local graph replay."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
GRAPH = HERE.parent / 'ramsey_r55_opposite22_realization/GRAPH.json'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def decode(doc):
    need(set(doc) == {'n', 'red_edges'} and type(doc['n']) is int and 1 <= doc['n'] <= 25, 'graph fields/order')
    n = doc['n']
    need(type(doc['red_edges']) is list, 'edge list')
    seen, previous = set(), [-1, -1]
    for e in doc['red_edges']:
        need(type(e) is list and len(e) == 2 and all(type(v) is int for v in e), 'edge types')
        need(0 <= e[0] < e[1] < n and e > previous, 'edge range/order/duplicate')
        seen.add(tuple(e))
        previous = e
    return n, seen


def clique_masks(n, edges, k, red=True):
    return [sum(1 << v for v in q) for q in itertools.combinations(range(n), k)
            if all((e in edges) == red for e in itertools.combinations(q, 2))]


def make_local(n, edges, s0, s1):
    out = set()
    for u, v in itertools.combinations(range(n+3), 2):
        if v < 3:
            red = True
        elif u == 0:
            red = False
        elif u in (1, 2):
            red = bool((s0 if u == 1 else s1) >> (v-3) & 1)
        else:
            red = (u-3, v-3) in edges
        if red:
            out.add((u, v))
    return {'n': n+3, 'red_edges': [list(e) for e in sorted(out)]}


def k5_count(doc, red):
    n, edges = decode(doc)
    neighbors = [set(v for v in range(n) if v != u and
                     ((tuple(sorted((u, v))) in edges) == red)) for u in range(n)]
    def count(available, remaining):
        if remaining == 0:
            return 1
        if len(available) < remaining:
            return 0
        total = 0
        for v in sorted(available):
            total += count({w for w in available if w > v} & neighbors[v], remaining-1)
        return total
    return count(set(range(n)), 5)


def independent_domains(n, k4):
    domains = {}
    examined = {}
    for k in (12, 14, 15):
        accepted = []
        count = 0
        for subset in itertools.combinations(range(n), k):
            mask = sum(1 << v for v in subset)
            count += 1
            if all(mask & q != q for q in k4):
                accepted.append(mask)
        domains[k] = sorted(accepted)
        examined[k] = count
    return domains, examined


def independently_join(n, edges, domain14, k4):
    cases, bad, cover = [], [], 0
    full = (1 << n)-1
    for s1 in domain14:
        vertices = [v for v in range(n) if s1 >> v & 1]
        # Union=O iff D0=O\S0 is a ten-subset of S1. This independently
        # enumerates all possibilities without joining the producer's D12 list.
        for blue0 in itertools.combinations(vertices, 10):
            s0 = full ^ sum(1 << v for v in blue0)
            if any(s0 & q == q for q in k4):
                continue
            cover += 1
            common = [v for v in vertices if s0 >> v & 1]
            triangles = [list(q) for q in itertools.combinations(common, 3)
                         if all(e in edges for e in itertools.combinations(q, 2))]
            if triangles:
                bad.append({'S0': f'{s0:06x}', 'S1': f'{s1:06x}', 'red_triangle': min(triangles)})
            else:
                cases.append({'S0': f'{s0:06x}', 'S1': f'{s1:06x}'})
    cases.sort(key=lambda c: (int(c['S1'], 16), int(c['S0'], 16)))
    cases = [{'id': j, **c} for j, c in enumerate(cases)]
    bad.sort(key=lambda c: (int(c['S1'], 16), int(c['S0'], 16)))
    return cases, bad, cover


def check_boundary(path, cases):
    with path.open() as source:
        need(source.readline().split() == ['p', 'cnf', str(440+len(cases)), str(1+44*len(cases))], 'boundary header')
        need(list(map(int, source.readline().split())) == list(range(441, 441+len(cases)))+[0], 'selector disjunction')
        for j, c in enumerate(cases):
            for i in range(2):
                mask = int(c[f'S{i}'], 16)
                for v in range(22):
                    edge = 22*i+v+1
                    expected = [-(441+j), edge if mask >> v & 1 else -edge, 0]
                    need(list(map(int, source.readline().split())) == expected, 'selector implication')
        need(source.read() == '', 'boundary EOF')


def check(work):
    raw = GRAPH.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == 'e7f6086e6f99edcf47f5f931106bdfc294703e9a74aa8eb1caad60978917f355', 'O identity')
    n, edges = decode(json.loads(raw))
    need(n == 22 and len(edges) == 124, 'O dimensions')
    k4 = clique_masks(n, edges, 4)
    need(len(k4) == 111 and not clique_masks(n, edges, 5) and not clique_masks(n, edges, 4, False), 'O core check')
    domains, examined = independent_domains(n, k4)
    return check_data(work, n, edges, k4, domains, examined)


def check_data(work, n, edges, k4, domains, examined):
    """The controls reuse a once-reconstructed universe, never published counts."""
    need(len(domains[14]) > 0 and not domains[15], 'maximum induced red-K4-free order14')
    hashes = {}
    for k, masks in domains.items():
        data = b''.join(struct.pack('<I', m) for m in masks)
        need(data == (work/f'domain{k}.bin').read_bytes(), 'entry-level subset domain mismatch')
        hashes[str(k)] = hashlib.sha256(data).hexdigest()
    cases, bad, cover = independently_join(n, edges, domains[14], k4)
    actual_cases = json.loads((work/'cases.json').read_text())
    need(json.dumps(actual_cases, sort_keys=True) == json.dumps(cases, sort_keys=True), 'complete case list mismatch')
    result = json.loads((work/'result.json').read_text())
    exact = {'max_red_K4_free_induced_order': 14, 'domain_counts': {str(k):len(v) for k,v in domains.items()},
             'domain_sha256_u32le_sorted': hashes, 'all_maximizers': [f'{m:06x}' for m in domains[14]],
             'degree_and_cover_pairs_before_clique_checks': 320089770,
             'red_K4_free_cover_pairs': cover, 'rejected_common_triangle_pairs': bad,
             'local_R55_pairs': len(cases),
             'case_counts_by_S1': {f'{s:06x}':sum(int(c['S1'],16)==s for c in cases) for s in domains[14]},
             'unfixed_cross_edges_per_case': 396, 'boundary_primary_variables': 440,
             'boundary_constrained_primaries': 44, 'boundary_selectors': len(cases),
             'boundary_clauses': 1 + 44 * len(cases)}
    need(all(json.dumps(result[k], sort_keys=True) == json.dumps(v, sort_keys=True) for k,v in exact.items()), 'result field mismatch')
    for j, c in enumerate(cases):
        local = make_local(n, edges, int(c['S0'],16), int(c['S1'],16))
        need(k5_count(local, True) == k5_count(local, False) == 0, f'case {j} local graph failure')
        if j == 0:
            claimed = json.loads((work/'LOCAL_GRAPH.json').read_text())
            decode(claimed)
            need(json.dumps(local, sort_keys=True) == json.dumps(claimed, sort_keys=True), 'local witness graph mismatch')
    check_boundary(work/'boundary.cnf', cases)
    return {'status': 'VERIFIED', 'fixed_size_subsets_examined': {str(k): v for k,v in examined.items()},
            'domain_records_matched': {str(k):len(v) for k,v in domains.items()},
            'all_local25_graphs_checked': len(cases), 'marked_cases_matched': len(cases),
            'boundary_CNF_rows_matched': 1+44*len(cases),
            'boundary_sha256': hashlib.sha256((work/'boundary.cnf').read_bytes()).hexdigest(),
            'global_43_graph_found': False, 'global_feasibility_tested': False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    report = check(a.work)
    a.report.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
