#!/usr/bin/env python3
"""six-reviewer-4 independent regular Book Ramsey codegree audit.

The core domain comes from flat nine-edge subsets on seven residual points.
Defect graphs come from every pairing of labeled incident stubs. Published
integer vectors are untrusted certificates, projected to the zero-sum plane;
no author module or expected record determines the enumerated domain.
"""
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations
from math import comb, factorial, gcd
from pathlib import Path
import argparse
import hashlib
import json


def require(value, message):
    if not value:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


EDGES = tuple(combinations(range(8), 2))
SLOT = {e: k for k, e in enumerate(EDGES)}


def adjacency(mask):
    rows = [set() for _ in range(8)]
    for k, (i, j) in enumerate(EDGES):
        if mask >> k & 1:
            rows[i].add(j)
            rows[j].add(i)
    return rows


def relabel(mask, point):
    return sum(1 << SLOT[tuple(sorted((point[i], point[j])))]
               for k, (i, j) in enumerate(EDGES) if mask >> k & 1)


def fixed_cardinality_cores():
    """Normalize N_F(0)={2,3}; all21 residual bits have exactly9 ones."""
    residual_edges = tuple(combinations(range(1, 8), 2))
    targets = (2, 2, 2, 3, 3, 3, 3)
    incidents = [sum(1 << k for k, e in enumerate(residual_edges) if i in e)
                 for i in range(1, 8)]
    normalized = set()
    visits = 0
    fixed = (1 << SLOT[(0, 2)]) | (1 << SLOT[(0, 3)])
    for chosen in combinations(range(21), 9):
        visits += 1
        mask = sum(1 << k for k in chosen)
        if any((mask & a).bit_count() != d for a, d in zip(incidents, targets)):
            continue
        full = fixed
        for k in chosen:
            full |= 1 << SLOT[residual_edges[k]]
        rows = adjacency(full)
        if any(rows[i] & rows[j] for i, j in EDGES if j in rows[i]):
            continue
        normalized.add(full)
    require(visits == comb(21, 9) == 293930, 'entire fixed-weight residual domain')
    require(len(normalized) == 120, 'normalized marked core census')
    domain = set()
    for pair in combinations(range(2, 8), 2):
        point = (0, 1)+pair+tuple(i for i in range(2, 8) if i not in pair)
        images = {relabel(mask, point) for mask in normalized}
        require(len(images) == 120 and not images & domain, '15 disjoint neighbor-pair classes')
        domain |= images
    require(len(domain) == 1800, 'full labeled marked core census')
    for mask in domain:
        rows = adjacency(mask)
        require(list(map(len, rows)) == [2, 2]+[3]*6 and 1 not in rows[0],
                'literal full degree and absent marked edge')
    return domain, visits


def orbit_closure(domain):
    generators = []
    for i in range(2, 7):
        point = list(range(8))
        point[i], point[i+1] = point[i+1], point[i]
        generators.append(point)
    remaining = set(domain)
    result = []
    while remaining:
        first = min(remaining)
        orbit, todo = {first}, deque([first])
        while todo:
            mask = todo.popleft()
            for point in generators:
                image = relabel(mask, point)
                require(image in domain, 'S6 orbit remains in independently generated domain')
                if image not in orbit:
                    orbit.add(image)
                    todo.append(image)
        require(orbit <= remaining, 'disjoint core orbits')
        remaining -= orbit
        result.append({'F_mask': first, 'orbit_size': len(orbit)})
    require(len(result) == 4 and sum(x['orbit_size'] for x in result) == 1800,
            'complete four-orbit cover')
    return result


def capacities(mask):
    """Build the full10-point local graph, using literal common-neighbor sets."""
    F = adjacency(mask)
    J = [{1, 2}]+[{j+1 for j in row} for row in F]+[set()]
    J[1].add(0)
    J[2].add(0)
    h = list(map(len, J))
    require(h == [2]+[3]*8+[0], 'full isolated/low/cubic local graph')
    S0 = []
    for i in range(9):
        row = []
        for j in range(9):
            if i == j:
                row.append(h[i]+2)
            else:
                row.append(h[i]+h[j]-(5 if j in J[i] else 2)-len(J[i] & J[j]))
        S0.append(row)
    return S0


@lru_cache(maxsize=64)
def stub_multigraphs(target):
    """All perfect matchings of labeled stubs, then quotient identical endpoints."""
    stubs = tuple(i for i, count in enumerate(target) for _ in range(count))
    require(len(stubs) in (10, 12), 'ten or twelve total incident stubs')
    out = set()
    terminal = 0

    def visit(left, edges):
        nonlocal terminal
        if not left:
            terminal += 1
            if any(i == j for i, j in edges):
                return
            count = Counter(edges)
            weighted = tuple((i, j, w) for (i, j), w in sorted(count.items()))
            out.add(weighted)
            return
        a = left[0]
        for pos in range(1, len(left)):
            b = left[pos]
            visit(left[1:pos]+left[pos+1:], edges+(tuple(sorted((a, b))),))
    visit(stubs, ())
    n = len(stubs)
    require(terminal == factorial(n)//(2**(n//2)*factorial(n//2)),
            'every labeled perfect stub matching')
    for weighted in out:
        rows = [sum(w for a, b, w in weighted if i in (a, b)) for i in range(9)]
        require(rows == list(target), 'weighted multigraph recovers incident degrees')
    return tuple(sorted(out))


def residual(S0, weights, group):
    # The two distinguished rows contain the isolated point and complementary
    # cubic subsets; its deleted coordinate is not among these nine columns.
    S = [row[:] for row in S0]
    for i, j, w in weights:
        S[i][j] -= w
        S[j][i] -= w
    group = set(group)
    for i in range(1, 9):
        for j in range(1, 9):
            if ((i-1 in group) == (j-1 in group)):
                S[i][j] -= 1
    return S


def project(vector):
    require(len(vector) == 9 and all(type(x) is int for x in vector) and any(vector),
            'integer certificate vector shape')
    total = sum(vector)
    result = [9*x-total for x in vector]
    divisor = 0
    for x in result:
        divisor = gcd(divisor, abs(x))
    require(divisor > 0, 'constant vectors cannot certify the positive constant mode')
    result = [x//divisor for x in result]
    if next(x for x in result if x) < 0:
        result = [-x for x in result]
    require(sum(result) == 0 and any(result), 'primitive zero-sum certificate')
    return result


def prepared(vector):
    return 4*sum(x*x for x in vector), [(i, j, 2*vector[i]*vector[j])
                                      for i, j in combinations(range(9), 2)
                                      if vector[i] and vector[j]]


def negative(S, plan):
    constant, terms = plan
    return constant+sum(S[i][j]*w for i, j, w in terms)


def run(certificate_path, export_path=None):
    domain, visits = fixed_cardinality_cores()
    orbits = orbit_closure(domain)
    original = json.loads(certificate_path.read_text())
    pools = {}
    for record in original:
        key = (record['F_mask'], record['case'])
        require(key not in pools and record['vectors'], 'unique nonempty certificate pools')
        pools[key] = [project(v) for v in record['vectors']]
    required = {(x['F_mask'], kind) for x in orbits for kind in ('five_five', 'six_four')}
    require(set(pools) == required, 'certificate keys match independently derived domain')
    input_vectors = sum(len(v) for v in pools.values())
    cases = []
    selected_pools = []
    witness_digest = hashlib.sha256()
    for core in orbits:
        mask = core['F_mask']
        S0 = capacities(mask)
        for kind in ('five_five', 'six_four'):
            pool = pools[(mask, kind)]
            plans = [prepared(v) for v in pool]
            groups = [g for g in combinations(range(8), 4 if kind == 'five_five' else 5)
                      if kind != 'five_five' or 0 in g]
            stream = hashlib.sha256()
            count = entry_failures = 0
            used = set()
            worst_witness = None
            for group in groups:
                target = (2,)+tuple(2+int(i < 2)-(1 if kind == 'five_five' else 2*int(i in group))
                                    for i in range(8))
                for weights in stub_multigraphs(target):
                    if any(w > S0[i][j] for i, j, w in weights):
                        continue
                    S = residual(S0, weights, group)
                    require(all(S[i][i] == 4 and sum(S[i]) == 16 for i in range(9)),
                            'literal residual diagonal and row sums')
                    values = [(j, negative(S, p)) for j, p in enumerate(plans)]
                    j, value = next(((j, x) for j, x in values if x < 0), (None, None))
                    require(j is not None, 'every necessary state has a negative zero-sum integer form')
                    used.add(j)
                    worst_witness = value if worst_witness is None else max(worst_witness, value)
                    witness_digest.update(encode([mask, kind, group, weights, j, value]))
                    stream.update(encode([mask, kind, group, weights, S]))
                    count += 1
                    entry_failures += int(any(x < 0 for row in S for x in row))
            cases.append({'F_mask': mask, 'case': kind, 'groups': len(groups), 'states': count,
                          'negative_entry_states': entry_failures, 'state_stream_sha256': stream.hexdigest(),
                          'vectors': len(pool), 'certificate_vectors_used': len(used),
                          'largest_chosen_negative_form': worst_witness})
            selected_pools.append({'F_mask': mask, 'case': kind,
                                   'vectors': [pool[i] for i in sorted(used)]})
    total = sum(c['states'] for c in cases)
    require(total == 46411 and sum(c['states'] for c in cases if c['case'] == 'five_five') == 44100,
            'complete all46,411 residual matrix census')
    weighted_total = sum(c['states']*o['orbit_size'] for c in cases for o in orbits
                         if c['F_mask'] == o['F_mask'])
    require(weighted_total == 20888640, 'exact labeled marked multiplicity')
    if export_path:
        export_path.write_bytes(encode(selected_pools))
    return {'agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'target_height': 8120, 'flat_residual_edge_sets': visits, 'normalized_cores': 120,
            'labeled_marked_F': len(domain), 'F_domain_sha256': hashlib.sha256(encode(sorted(domain))).hexdigest(),
            'core_records': orbits, 'cases': cases, 'states': total, 'labeled_marked_states': weighted_total,
            'negative_zero_sum_forms': total, 'input_certificate_vectors': input_vectors,
            'projected_vector_max_absolute_entry': max(abs(x) for vs in pools.values() for v in vs for x in v),
            'projected_vectors_sha256': hashlib.sha256(encode(sorted(pools.items()))).hexdigest(),
            'witness_stream_sha256': witness_digest.hexdigest(),
            'stub_degree_domains': stub_multigraphs.cache_info().currsize,
            'author_modules_imported': False, 'external_vector_certificate': True,
            'Ramsey_endpoint_decided': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vectors', type=Path, required=True)
    parser.add_argument('--check', type=Path)
    parser.add_argument('--compare-author', type=Path)
    parser.add_argument('--export-used', type=Path, help='export only the selected primitive zero-sum vectors')
    args = parser.parse_args()
    result = run(args.vectors, args.export_used)
    if args.check:
        require(encode(result) == encode(json.loads(args.check.read_text())), 'complete expected-output mismatch')
    if args.compare_author:
        author = json.loads(args.compare_author.read_text())
        for key in ('F_domain_sha256', 'core_records', 'labeled_marked_F', 'states', 'labeled_marked_states'):
            require(result[key] == author[key], 'author full-domain comparison: '+key)
        for actual, expected in zip(result['cases'], author['cases']):
            relevant = {k: v for k, v in expected.items() if k != 'vectors'}
            require({k: actual[k] for k in relevant} == relevant, 'author every-state full matrix stream')
        require(len(result['cases']) == len(author['cases']) == 8, 'all eight author subdomains')
        result['author_comparison'] = {'all_eight_full_matrix_streams_agree': True,
                                       'canonical_record_used_to_select_domain': False}
    print(json.dumps(result, sort_keys=True, indent=2))
