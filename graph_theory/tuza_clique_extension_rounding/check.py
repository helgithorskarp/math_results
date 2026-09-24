"""Definition-level certificate checks; all arithmetic is exact.

The producer supplies witnesses. This module independently rebuilds every
relevant incidence, flow margin, proper coloring, recoloring component and
triangle edge. No finite audit proves either imported existence theorem.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
import random

from constructions import (affine_kirkman, allocate_spokes, clique_stage,
                           construct_extension, equitable_coloring)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def check_design(design):
    need(bool(design) and bool(design[0]), 'empty design')
    n = 3*len(design[0])
    pairs = Counter()
    need(len(design) == (n-1)//2, 'wrong number of parallel classes')
    for parallel in design:
        points = []
        for triple in parallel:
            need(len(triple) == len(set(triple)) == 3, 'invalid design triple')
            need(all(type(x) is int and 0 <= x < n for x in triple), 'invalid design point')
            points.extend(triple)
            pairs.update(tuple(sorted(e)) for e in combinations(triple, 2))
        need(sorted(points) == list(range(n)), 'parallel class is not a partition')
    need(pairs == Counter({e: 1 for e in combinations(range(n), 2)}), 'design pair multiplicity')
    return n


def check_coloring(n, edges, palette, colored):
    need(len(colored) == len(edges), 'wrong coloring size')
    seen_edges, seen_incidence = set(), set()
    for a, b, color in colored:
        need((a, b) in edges and (a, b) not in seen_edges, 'wrong coloring edge')
        need(type(color) is int and 0 <= color < palette, 'color outside palette')
        seen_edges.add((a, b))
        for vertex in (a, b):
            need(0 <= vertex < n and (vertex, color) not in seen_incidence, 'adjacent colors repeat')
            seen_incidence.add((vertex, color))
    need(seen_edges == set(edges), 'missing coloring edge')


def check_equitable(n, edges, palette, cert):
    edges = set(edges)
    check_coloring(n, edges, palette, cert['initial'])
    current = {(a, b): c for a, b, c in cert['initial']}
    sizes = Counter(current.values())
    for hi, lo, listed in cert['trace']:
        need(hi != lo and sizes[hi]-sizes[lo] >= 2, 'invalid balancing direction')
        component = set(map(tuple, listed))
        need(component and len(component) == len(listed), 'bad recoloring component')
        need(component <= edges and all(current[e] in (hi, lo) for e in component), 'wrong path colors')
        vertices = set(component.pop())
        component = set(map(tuple, listed))
        reached_edges = set()
        while True:
            added = {e for e in edges if current[e] in (hi, lo) and vertices.intersection(e)}
            expanded = vertices | {x for e in added for x in e}
            reached_edges |= added
            if expanded == vertices:
                break
            vertices = expanded
        need(reached_edges == component, 'trace is not a whole alternating component')
        excess = sum(1 if current[e] == hi else -1 for e in component)
        need(excess == 1, 'wrong alternating path excess')
        before = sum(sizes[c]**2 for c in range(palette))
        for e in component:
            old = current[e]
            new = lo if old == hi else hi
            sizes[old] -= 1
            sizes[new] += 1
            current[e] = new
        need(sum(sizes[c]**2 for c in range(palette)) < before, 'nondecreasing recoloring potential')
        check_coloring(n, edges, palette, [(a, b, c) for (a, b), c in current.items()])
    final = [(a, b, current[a, b]) for a, b in sorted(edges)]
    need(final == cert['colored'], 'final coloring differs from trace')
    loads = [sizes[c] for c in range(palette)]
    need(max(loads)-min(loads) <= 1, 'unequal color-class sizes')
    return len(cert['trace'])


def check_allocation(available, columns, quota, selected):
    need(len(selected) == len(available), 'wrong number of allocation rows')
    fractions = [Fraction(0) for _ in range(columns)]
    counts = [0]*columns
    for row, chosen in zip(available, selected):
        need(len(chosen) == len(set(chosen)) == quota, 'wrong or repeated row allocation')
        need(set(chosen) <= row, 'allocation uses forbidden spoke')
        if quota:
            need(bool(row), 'empty positive row')
            for y in row:
                fractions[y] += Fraction(quota, len(row))
        for y in chosen:
            counts[y] += 1
    need(sum(fractions) == len(available)*quota, 'wrong fractional total')
    for y, value in enumerate(fractions):
        need(value.numerator//value.denominator <= counts[y] <=
             -(-value.numerator//value.denominator), 'column outside exact flow bounds')
    mean = Fraction(len(available)*quota, columns)
    return max(abs(value-mean) for value in counts)


def check_stage(s, sizes, u, v_masses, design, cert):
    order = check_design(design)
    need(cert['design_order'] == order and s <= order <= s+5, 'wrong padding')
    classes = (3*Fraction(u))//order
    need(cert['classes'] == classes, 'wrong number of selected classes')
    expected = [t for parallel in design[:classes] for t in parallel if max(t) < s]
    need(cert['triangles'] == expected, 'wrong deleted-point triangle family')
    need(Fraction(u)-7*s <= len(expected) <= u, 'internal triangle loss')
    used = Counter(tuple(sorted(e)) for t in expected for e in combinations(t, 2))
    need(all(v == 1 for v in used.values()), 'repeated internal triangle edge')
    remainder = set(combinations(range(s), 2))-set(used)
    degrees = [sum(x in e for e in remainder) for x in range(s)]
    need(max(degrees)-min(degrees) <= 2*(order-s), 'remainder degree spread')
    check_coloring(s, remainder, max(degrees)+1, cert['remainder_coloring'])
    coloring = {(a, b): c for a, b, c in cert['remainder_coloring']}
    occupied = [[set() for _ in range(s)] for _ in sizes]
    total_traces = 0
    actual_counts = []
    begin = 0
    for i, (size, mass, group) in enumerate(zip(sizes, v_masses, cert['groups'])):
        k = (2*Fraction(mass))//s
        need(group['palette_begin'] == begin and group['palette_count'] == k, 'wrong palette group')
        selected = {e for e, c in coloring.items() if begin <= c < begin+k}
        begin += k
        total_traces += check_equitable(s, selected, size, group)
        need(0 <= mass-len(selected) < 6*s, 'XXH count loss')
        local_degree = Counter(x for e in selected for x in e)
        for x in range(s):
            need(k-11 <= local_degree[x] <= k, 'palette group degree bound')
            need(local_degree[x] <= 2*Fraction(mass)/s, 'row exceeds original fractional spoke budget')
            need(abs(local_degree[x]-Fraction(2*len(selected), s)) <= 11, 'row discrepancy')
        for x, y, color in group['colored']:
            need(color not in occupied[i][x] and color not in occupied[i][y], 'XXH reused spoke')
            occupied[i][x].add(color)
            occupied[i][y].add(color)
        columns = Counter(y for row in occupied[i] for y in row)
        need(all(abs(columns[y]-Fraction(2*len(selected), size)) < 2 for y in range(size)), 'XXH column discrepancy')
        actual_counts.append(len(selected))
    return occupied, {'internal_triangles': len(expected), 'XXH_triangles': actual_counts,
                      'recoloring_paths': total_traces, 'remainder_degree_spread': max(degrees)-min(degrees)}


def check_extension(fixture, cert):
    sizes, s = fixture['sizes'], fixture['s']
    d, n = len(sizes), sum(sizes)
    offsets = [sum(sizes[:i]) for i in range(d)]
    classes = [i for i, size in enumerate(sizes) for _ in range(size)]
    need(fixture['u'] >= 0 and all(v >= 0 for v in fixture['v']), 'negative profile')
    need(3*fixture['u']+sum(fixture['v']) <= s*(s-1)//2, 'internal profile capacity')
    core_mass = Fraction(0)
    residual_spare_mass = Fraction(0)
    for (i, j), mass in fixture['w'].items():
        capacity = sizes[i]*(sizes[i]-1)//2 if i == j else sizes[i]*sizes[j]
        need(0 <= mass <= capacity, 'fractional core capacity')
        need(i in fixture['neighbors'] and j in fixture['neighbors'], 'unsupported fractional neighborhood')
        # A fresh nonzero core-only profile: put half the unused loop capacity
        # into triangles internal to each clique core class, the rest in spare.
        triangle_mass = Fraction(capacity-mass)/6 if i == j else Fraction(0)
        original_spare = capacity-mass-3*triangle_mass
        q = mass//s
        q = q if q >= fixture['cutoff'] else 0
        residual_spare = original_spare+mass-s*q
        need(triangle_mass >= 0 and residual_spare >= 0 and
             3*triangle_mass+residual_spare == capacity-s*q, 'residual core profile identity')
        core_mass += triangle_mass
        residual_spare_mass += residual_spare
    for i, size in enumerate(sizes):
        load = 2*fixture['v'][i] + sum((int(i == a)+int(i == b))*mass
                                     for (a, b), mass in fixture['w'].items())
        need(load <= s*size, 'fractional spoke capacity')
    occupied, stage_stats = check_stage(s, sizes, fixture['u'], fixture['v'],
                                      fixture['design'], cert['stage'])
    expected_triangles = [tuple(n+x for x in t) for t in cert['stage']['triangles']]
    for i, group in enumerate(cert['stage']['groups']):
        expected_triangles.extend((n+x, n+y, offsets[i]+color) for x, y, color in group['colored'])
    quotas = {e: Fraction(w)//s for e, w in fixture['w'].items()}
    quotas = {e: q if q >= fixture['cutoff'] else 0 for e, q in quotas.items()}
    need(dict((tuple(e), q) for e, q in cert['quotas']) == quotas, 'wrong rounded quotas')
    previous_q = 0
    used_core = set()
    type_degree = {e: Counter() for e in quotas}
    flow_discrepancies = []
    processed = set()
    sufficient_matching_checks = 0
    for step in cert['allocations']:
        e = tuple(step['edge_type'])
        i, j = e
        q = step['quota']
        need(e not in processed and q == quotas[e] and q >= previous_q > -1, 'wrong allocation order')
        processed.add(e)
        previous_q = q
        selected = {}
        expected_parts = [(i, 2*q)] if i == j else [(i, q), (j, q)]
        need([(r['part'], r['demand']) for r in step['spokes']] == expected_parts, 'wrong spoke sides')
        for record in step['spokes']:
            part, demand = record['part'], record['demand']
            available = [set(range(sizes[part]))-row for row in occupied[part]]
            discrepancy = check_allocation(available, sizes[part], demand, record['selected'])
            flow_discrepancies.append(discrepancy)
            selected[part] = record['selected']
            for x, row in enumerate(record['selected']):
                occupied[part][x].update(row)
        need(len(step['pairings']) == s, 'missing center matching')
        for x, matching in enumerate(step['pairings']):
            if i == j:
                both = sorted(offsets[i]+v for v in selected[i][x])
                left, right = set(both[:q]), set(both[q:])
            else:
                left = {offsets[i]+v for v in selected[i][x]}
                right = {offsets[j]+v for v in selected[j][x]}
            need(len(matching) == q and {a for a, b in matching} == left and
                 {b for a, b in matching} == right, 'not a perfect assigned matching')
            degrees = Counter(v for pair in used_core for v in pair)
            need(max((degrees[v] for v in left | right), default=0)*2 < q,
                 'fixture does not meet direct dense-matching condition')
            sufficient_matching_checks += 1
            for a, b in matching:
                pair = tuple(sorted((a, b)))
                need(pair not in used_core, 'reused core matching edge')
                used_core.add(pair)
                type_degree[e][a] += 1
                type_degree[e][b] += 1
                expected_triangles.append((n+x, a, b))
    need(processed == {e for e, q in quotas.items() if q > 0}, 'missing positive quota')
    need(expected_triangles == cert['triangles'], 'triangle list differs from component certificates')
    used_edges = set()
    for triangle in cert['triangles']:
        need(len(triangle) == len(set(triangle)) == 3, 'degenerate triangle')
        for a, b in combinations(sorted(triangle), 2):
            need(0 <= a < b < n+s, 'invalid triangle vertex')
            if b < n:
                e = tuple(sorted((classes[a], classes[b])))
                need(e in fixture['w'], 'nonedge in core triangle')
            elif a < n:
                need(classes[a] in fixture['neighbors'], 'nonedge spoke')
            need((a, b) not in used_edges, 'triangle edge repeated')
            used_edges.add((a, b))
    all_degrees = Counter(v for pair in used_core for v in pair)
    need(max(all_degrees.values(), default=0) <= s, 'core deletion degree exceeds s')
    B = 2**(d+2)
    max_type_discrepancy = Fraction(0)
    for (i, j), q in quotas.items():
        need(sum(type_degree[i, j].values()) == 2*s*q, 'wrong core type count')
        for part in {i, j}:
            mean = Fraction(s*q*(2 if i == j else 1), sizes[part])
            for vertex in range(offsets[part], offsets[part]+sizes[part]):
                discrepancy = abs(type_degree[i, j][vertex]-mean)
                max_type_discrepancy = max(max_type_discrepancy, discrepancy)
                need(discrepancy < B, 'unbalanced residual core type')
    fractional_external = fixture['u']+sum(fixture['v'])+sum(fixture['w'].values())
    loss = fractional_external-len(cert['triangles'])
    need(0 <= loss <= (7+6*d+len(fixture['w'])*(fixture['cutoff']+1))*s, 'exterior loss bound')
    if fixture['universal_elementary_bounds']:
        alpha = min(Fraction(size, n) for size in sizes)
        Q = 8*B*(11+d)
        need(fixture['cutoff'] == Q, 'wrong universal elementary cutoff')
        need(Fraction(s, n) <= min(alpha/Fraction(88), alpha/Fraction(16*d)), 'small-size elementary bounds fail')
    return {'name': fixture['name'], 'core_order': n, 'clique_order': s,
            'triangles': len(cert['triangles']), 'stage': stage_stats,
            'XHH_triangles': len(used_core), 'exact_external_loss': str(loss),
            'maximum_core_degree': max(all_degrees.values(), default=0),
            'maximum_type_discrepancy': str(max_type_discrepancy),
            'flow_column_discrepancies': list(map(str, flow_discrepancies)),
            'preserved_core_fractional_mass': str(core_mass),
            'residual_core_spare_mass': str(residual_spare_mass),
            'dense_matching_checks': sufficient_matching_checks,
            'matching_repairs': cert['matching_repairs'],
            'triangles_sha256': digest(cert['triangles']),
            'certificate_sha256': digest(cert),
            'universal_elementary_bounds': fixture['universal_elementary_bounds']}


def run():
    audit = {'status': 'PASS', 'scope': 'finite elementary bridge only; Kirkman and dense core existence remain imported'}
    designs = {d: affine_kirkman(d) for d in range(1, 5)}
    audit['affine_designs'] = [{'order': check_design(value), 'sha256': digest(value)} for value in designs.values()]
    stage_records = []
    for design in designs.values():
        order = 3*len(design[0])
        for s in range(max(1, order-5), order+1):
            for level in range(5):
                capacity = s*(s-1)//2
                u = Fraction(capacity*level, 12)
                remaining = capacity-3*u
                masses = [remaining*Fraction(2, 5), remaining*Fraction(1, 3)]
                sizes = [3*s+7, 5*s+1]
                cert = clique_stage(s, sizes, u, masses, design)
                _, summary = check_stage(s, sizes, u, masses, design, cert)
                stage_records.append([s, level, summary, digest(cert)])
    audit['clique_stages'] = {'instances': len(stage_records), 'records_sha256': digest(stage_records),
                              'recoloring_paths': sum(x[2]['recoloring_paths'] for x in stage_records)}
    flow_records = []
    for rows, cols in [(1, 1), (2, 3), (3, 3), (3, 4)]:
        for mask in range(1 << (rows*cols)):
            available = [{y for y in range(cols) if mask & (1 << (x*cols+y))} for x in range(rows)]
            for quota in range(1, min(map(len, available))+1):
                selected, stats = allocate_spokes(available, cols, quota)
                check_allocation(available, cols, quota, selected)
                flow_records.append([rows, cols, mask, quota, [sorted(row) for row in selected]])
    audit['exhaustive_flow_rounding'] = {'instances': len(flow_records), 'records_sha256': digest(flow_records)}
    coloring_records, coloring_paths = [], 0
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            edges = [e for i, e in enumerate(pairs) if mask & (1 << i)]
            degree = Counter(x for e in edges for x in e)
            for extra in [0, 2]:
                palette = max(degree.values(), default=0)+1+extra
                cert = equitable_coloring(n, edges, palette)
                coloring_paths += check_equitable(n, edges, palette, cert)
                coloring_records.append([n, mask, palette, digest(cert)])
    rng = random.Random(20260924)
    for n in range(7, 36):
        for density in [1, 2, 3]:
            edges = [e for e in combinations(range(n), 2) if rng.randrange(4) < density]
            palette = n+3
            cert = equitable_coloring(n, edges, palette)
            coloring_paths += check_equitable(n, edges, palette, cert)
            coloring_records.append([n, density, palette, digest(cert)])
    audit['equitable_coloring'] = {'instances': len(coloring_records), 'replayed_paths': coloring_paths,
                                  'seed': 20260924, 'records_sha256': digest(coloring_records)}
    parameter_records = []
    for d in range(1, 13):
        A, B = 11, 2**(d+2)
        Q = 8*B*(A+d)
        for delta in [0, 2, B//2, B-1]:
            for D in [Q, Q+1, 10*Q]:
                error = Fraction(2*A, 88)+Fraction(2*A*delta, D)
                need(error <= Fraction(1, 2), 'flow fractional discrepancy margin')
                matching = Fraction(Q, 8)+d*B
                need(matching <= Fraction(Q, 4), 'increasing-quota matching margin')
                parameter_records.append([d, delta, D, str(error), str(matching)])
    audit['parameter_endpoints'] = {'instances': len(parameter_records), 'records_sha256': digest(parameter_records)}
    growth_records = []
    for t in [88, 89, 100, 1000, 10000]:
        s, part = t**3, t**4
        n, internal = 2*part, s*(s-1)//2
        u, v = Fraction(internal, 6), Fraction(internal, 4)
        w = s*part-Fraction(internal, 2)
        need(3*u+2*v == internal and 2*v+w == s*part, 'growth-profile capacities')
        need(w <= part**2 and internal > n, 'growth profile not beyond linear deletion cost')
        need(Fraction(s, n) <= Fraction(1, 176), 'growth-profile size tolerance')
        q = w//s
        need(q >= 1664 and 0 <= w-s*q < s, 'growth-profile quota or loss')
        growth_records.append({'t': t, 'core_order': n, 'clique_order': s,
                               'internal_edges': internal, 'internal_edges_per_core_vertex': str(Fraction(internal, n)),
                               'XXX_mass': str(u), 'each_XXH_mass': str(v), 'XHH_mass': str(w),
                               'quota': q, 'XHH_rounding_loss': str(w-s*q)})
    audit['superlinear_internal_edge_profiles'] = {
        'scope': 'exact feasible fractional profiles and explicit parameter inequalities; no large packing is materialized',
        'profiles': growth_records, 'records_sha256': digest(growth_records)}
    fixtures = [
        {'name': 'clique_core_saturated_spokes', 'sizes': [3072], 'loops': [0], 'cross': [],
         's': 22, 'u': Fraction(77, 3), 'v': [Fraction(120)],
         'w': {(0, 0): Fraction(22*1530)+Fraction(1, 7)}, 'neighbors': [0],
         'design': designs[3], 'cutoff': 768, 'universal_elementary_bounds': True},
        {'name': 'two_clique_core_all_edge_types', 'sizes': [6000, 6100], 'loops': [0, 1], 'cross': [(0, 1)],
         's': 24, 'u': Fraction(276, 9), 'v': [Fraction(70), Fraction(80)],
         'w': {(0, 0): Fraction(24*1700)+Fraction(1, 2),
               (0, 1): Fraction(24*1750)+Fraction(1, 4),
               (1, 1): Fraction(24*1800)+Fraction(3, 4)}, 'neighbors': [0, 1],
         'design': designs[3], 'cutoff': 1664, 'universal_elementary_bounds': True},
        {'name': 'bipartite_core_with_clique_extension', 'sizes': [6000, 6200], 'loops': [], 'cross': [(0, 1)],
         's': 26, 'u': Fraction(325, 12), 'v': [Fraction(90), Fraction(100)],
         'w': {(0, 1): Fraction(26*2000)+Fraction(1, 3)}, 'neighbors': [0, 1],
         'design': designs[3], 'cutoff': 1664, 'universal_elementary_bounds': True},
    ]
    results, certificates = [], []
    for fixture in fixtures:
        cert = construct_extension(fixture['sizes'], fixture['loops'], fixture['cross'],
                                   fixture['s'], fixture['u'], fixture['v'], fixture['w'],
                                   fixture['design'], fixture['cutoff'])
        results.append(check_extension(fixture, cert))
        certificates.append(cert)
    audit['integrated_extensions'] = results
    rejected = []

    def reject(name, function):
        try:
            function()
        except ValueError:
            rejected.append(name)
        else:
            raise RuntimeError('negative control accepted: ' + name)

    bad_design = deepcopy(designs[2])
    bad_design[0][0] = bad_design[0][1]
    reject('nonpartition_parallel_class', lambda: check_design(bad_design))
    reject('forbidden_spoke', lambda: check_allocation([{0}, {1}], 2, 1, [{1}, {0}]))
    reject('wrong_row_degree', lambda: check_allocation([{0, 1}], 2, 1, [set()]))
    reject('column_overload', lambda: check_allocation([{0, 1, 2}]*2, 3, 1, [{0}, {0}]))
    reject('infeasible_row_quota', lambda: allocate_spokes([{0}], 2, 2))
    color_bad = equitable_coloring(4, [(0, 1), (1, 2)], 4)
    color_bad['initial'][1] = (1, 2, color_bad['initial'][0][2])
    reject('improper_initial_coloring', lambda: check_equitable(4, {(0, 1), (1, 2)}, 4, color_bad))
    bad = deepcopy(certificates[0])
    bad['triangles'].pop()
    reject('missing_triangle', lambda: check_extension(fixtures[0], bad))
    bad_quota = deepcopy(certificates[0])
    bad_quota['allocations'][0]['quota'] += 1
    reject('wrong_uniform_quota', lambda: check_extension(fixtures[0], bad_quota))
    bad_spoke = deepcopy(certificates[0])
    bad_spoke['allocations'][0]['spokes'][0]['selected'][0].pop()
    reject('missing_allocated_spoke', lambda: check_extension(fixtures[0], bad_spoke))
    bad_pair = deepcopy(certificates[0])
    pairings = bad_pair['allocations'][0]['pairings']
    pairings[0][1] = pairings[0][0]
    reject('repeated_matching_endpoint', lambda: check_extension(fixtures[0], bad_pair))
    audit['negative_controls'] = rejected
    return audit


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
