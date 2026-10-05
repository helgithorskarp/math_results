"""six-reviewer-1: independent original q18 chart audit. Stdlib only.
No author data, programs, factors or expected-output file is loaded.
Integer numerators represent twice each proper/actual generator.
"""
import argparse
from collections import Counter, deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json


def require(ok, label):
    if not ok:
        raise ValueError(label)


def add(d, key, value):
    d[key] = d.get(key, 0) + value
    if d[key] == 0:
        del d[key]


def edge(u, v):
    return (min(u, v), max(u, v))


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()


def geometry():
    groups = [1 << i for i in range(21)]
    vertices = {0}
    for size in (1, 2, 3):
        for bits in combinations(groups, size):
            m = sum(bits)
            if size < 3 or ((m & 7).bit_count() >= 2 and not
                            (m & 7 == 6 and m & sum(groups[3:12]))):
                vertices.add(m)
    d = sorted(vertices)
    proper = d[1:]
    star = {m for m in proper if m & 1}
    nonstar = set(proper) - star
    zz = {sum(p) for p in combinations(groups[3:12], 2)}
    ww = {sum(p) for p in combinations(groups[12:21], 2)}
    bw = {6 | w for w in groups[12:21]}
    bad = zz | ww | bw
    nn = [[], [], []]
    for u, v in combinations(sorted(nonstar), 2):
        if not u & v:
            nn[int(u in bad) + int(v in bad)].append((u, v))
    ns = sorted(edge(u, v) for u in nonstar for v in star - {1} if not u & v)
    require(len(d) == 278 and len(star) == 58 and len(bad) == 81,
            'original carrier')
    sizes = [sum(bool(m & b) for m in d) for b in groups]
    require(sizes == [58, 49, 49] + [23]*9 + [24]*9, 'all point stars')
    require([len(z) for z in nn] == [7885, 9009, 2628] and len(ns) == 10280,
            'complete coordinate partition')
    return d, star, bad, nn, ns


def pivots(bad, e2):
    adjacency = {v: [] for v in bad}
    for u, v in e2:
        adjacency[u].append(v)
        adjacency[v].append(u)
    for a in adjacency.values():
        a.sort()
    order, seen, todo = [], {24}, deque([24])
    while todo:
        u = todo.popleft()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
                order.append(edge(u, v))
    require(seen == bad and len(order) == 80, 'original spanning tree')
    chord = (12288, 49152)
    require(chord in e2 and chord not in order, 'odd original chord')
    return order + [chord]


def solve_twice(bad, pivot, rhs):
    """Solve A*x=2*rhs by peeling leaves then solving the triangle.
    Arbitrary integers, no Gauss-Jordan/Bareiss or author inverse.
    """
    neighbors = {v: {} for v in bad}
    for j, (u, v) in enumerate(pivot):
        neighbors[u][v] = j
        neighbors[v][u] = j
    remaining = {v: 2*rhs.get(v, 0) for v in bad}
    solution = [0]*len(pivot)
    leaves = deque(sorted(v for v in bad if len(neighbors[v]) == 1))
    peeled = 0
    while leaves:
        u = leaves.popleft()
        if len(neighbors[u]) != 1:
            continue
        v, j = next(iter(neighbors[u].items()))
        solution[j] = remaining[u]
        remaining[v] -= remaining[u]
        del remaining[u]
        del neighbors[v][u]
        neighbors[u].clear()
        peeled += 1
        if len(neighbors[v]) == 1:
            leaves.append(v)
    cycle = sorted(remaining)
    require(peeled == 78 and cycle == [24, 12288, 49152], 'triangle reduction')
    for u, v in combinations(cycle, 2):
        w = next(x for x in cycle if x not in (u, v))
        value = remaining[u] + remaining[v] - remaining[w]
        require(value % 2 == 0, 'integral twice inverse')
        solution[neighbors[u][v]] = value // 2
    return solution


def inverse(bad, pivot, damage):
    b = sorted(bad)
    columns = [solve_twice(bad, pivot, {v: 1}) for v in b]
    q = [[columns[i][j] for i in range(81)] for j in range(81)]
    if damage == 'inverse':
        q[0][0] += 1
    byv = {v: i for i, v in enumerate(b)}
    for i, u in enumerate(b):
        incident = [j for j, e in enumerate(pivot) if u in e]
        for k in range(81):
            require(sum(q[j][k] for j in incident) == 2*int(i == k),
                    'left inverse')
    for j, row in enumerate(q):
        for k, (u, v) in enumerate(pivot):
            require(row[byv[u]] + row[byv[v]] == 2*int(j == k), 'right inverse')
    require(set(x for row in q for x in row) <= {-2, -1, 0, 1, 2},
            'inverse entry bound')
    return q, byv


def lift_rows(h):
    rows = Counter()
    for (u, v), value in h.items():
        rows[u] += value
        rows[v] += value
    actual = dict(h)
    for u, value in rows.items():
        if value:
            actual[(0, u)] = -value
    loop = sum(rows.values())
    if loop:
        actual[(0, 0)] = loop
    return actual


def lift_outer(h):
    actual = {}
    for (u, v), value in h.items():
        add(actual, (u, v), value)
        add(actual, (0, u), -value)
        add(actual, (0, v), -value)
        add(actual, (0, 0), 2*value)
    return actual


def audit(damage=None):
    d, star, bad, nn, ns = geometry()
    set_e0, set_e1 = set(nn[0]), set(nn[1])
    pivot = pivots(bad, nn[2])
    q, byv = inverse(bad, pivot, damage)
    pset = set(pivot)
    badfree = [e for e in nn[2] if e not in pset]
    gauge = nn[0][0]
    require(gauge == (2, 4), 'good original gauge')
    goodfree = nn[0][1:]
    selected = set(badfree + goodfree + ns)
    require(len(selected) == 20711 and not selected & pset and gauge not in selected,
            'selected original coordinates')
    columns = []
    for u, v in badfree:
        h = {(u, v): 2}
        for j, p in enumerate(pivot):
            add(h, p, -q[j][byv[u]] - q[j][byv[v]])
        columns.append(('bad', (u, v), h))
    for e in goodfree:
        columns.append(('good', e, {e: 2, gauge: -2}))
    for e in ns:
        u = e[0] if e[0] not in star else e[1]
        columns.append(('star', e, {e: 2, edge(u, 1): -2}))
    if damage == 'bad_degree':
        add(columns[0][2], pivot[0], 1)
    elif damage == 'good_mass':
        add(columns[len(badfree)][2], gauge, 1)
    elif damage == 'anchor':
        h = columns[-1][2]
        u = next(v for v in columns[-1][1] if v not in star)
        del h[edge(u, 1)]
    elif damage == 'missing_column':
        columns.pop()
    totals = Counter()
    envelope = Counter()
    actual_envelope = Counter()
    stream = sha256()
    counts = Counter()
    max_bad_terms = max_bad_mass = 0
    allowed_proper = {e for e in combinations(d[1:], 2) if not e[0] & e[1]}
    for typ, chosen, h in columns:
        require(all(e in allowed_proper for e in h), 'proper support')
        require({e: value for e, value in h.items() if e in selected} == {chosen: 2},
                'coordinate left inverse')
        kernel, degree = Counter(), Counter()
        good_sum = 0
        for (u, v), value in h.items():
            if v in star:
                kernel[u] += value
            if u in star:
                kernel[v] += value
            if u in bad and v in bad:
                degree[u] += value
                degree[v] += value
            if (u, v) in set_e0:
                good_sum += value
        require(not any(kernel.values()), 'proper star kernel')
        require(not any(degree.values()), 'bad degree equations')
        require(good_sum == 0, 'good mass equation')
        require(not any(e in set_e1 for e in h), 'cross coordinates')
        actual = lift_rows(h)
        if damage == 'empty_lift' and chosen == badfree[0]:
            add(actual, (0, 0), 1)
        require(actual == lift_outer(h), 'complete actual lift')
        require(all(not u & v for u, v in actual), 'actual support')
        require(actual.get((0, 0), 0) == 0 and
                all(actual.get((0, u), 0) == 0 for u in bad), 'all forced floors')
        rows = Counter()
        for (u, v), value in actual.items():
            rows[u] += value
            if v != u:
                rows[v] += value
        require(all(rows[v] == 0 for v in d), 'every actual stochastic row')
        counts[typ] += 1
        counts['proper_positions'] += len(h)
        counts['actual_positions'] += len(actual)
        mass = sum(abs(v) for v in h.values())
        if typ == 'bad':
            max_bad_terms = max(max_bad_terms, len(h))
            max_bad_mass = max(max_bad_mass, mass)
        totals[typ] += mass
        totals['all'] += mass
        for e, value in h.items():
            envelope[e] += abs(value)
        for e, value in actual.items():
            actual_envelope[e] += abs(value)
        stream.update(canon([typ, list(chosen), [[*e, v] for e, v in sorted(h.items())],
                             [[*e, v] for e, v in sorted(actual.items())]]) + b'\n')
    require(counts['bad'] == 2547 and counts['good'] == 7884 and counts['star'] == 10280,
            'all independent columns')
    nnmax = max(envelope[e] for e in nn[0]+nn[1]+nn[2]) // 2
    actmax = max(actual_envelope.values()) // 2
    properbudget = F(totals['all'], 2)
    require(envelope[gauge] == 2*nnmax and actual_envelope[(0,1)] == 2*actmax,
            'original maximum positions')
    require(max_bad_terms <= 8 and max_bad_mass <= 16, 'individual bad column bound')
    require(nnmax == 7884 and actmax == 10280 and properbudget == 49850,
            'complete envelope bounds')
    # Exact inequalities pay continuum statements in the written proof.
    eta = F(1, 2**60)
    rho = F(1, 2**74)
    require(nnmax*rho < eta/2 and actmax*rho < eta and
            properbudget*rho < F(1,512), 'original real cube budgets')
    neweta = F(1, 2**20)
    newrho = neweta / 10280
    newfloor = F(39,4096) - properbudget*newrho
    require(newfloor > F(39,8192) and
            neweta-nnmax*newrho > 0 and 9*neweta-actmax*newrho == 8*neweta,
            'refined real cube budgets')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'counts':dict(sorted(counts.items())),
            'proper_absolute_edge_sums':{k:str(F(v,2)) for k,v in sorted(totals.items())},
            'inverse_entry_counts':{str(k):v for k,v in sorted(Counter(x for r in q for x in r).items())},
            'inverse_sha256':sha256(canon(q)).hexdigest(),
            'all_full_inverse_product_positions':13122,
            'maximum_bad_terms':max_bad_terms, 'maximum_bad_absolute_edge_sum':str(F(max_bad_mass,2)),
            'all_original_columns_and_lifts_sha256':stream.hexdigest(),
            'complete_proper_envelope_sha256':sha256(canon([[*e,v] for e,v in sorted(envelope.items())])).hexdigest(),
            'complete_actual_envelope_sha256':sha256(canon([[*e,v] for e,v in sorted(actual_envelope.items())])).hexdigest(),
            'proper_envelope_positions':len(envelope),
            'actual_envelope_positions':len(actual_envelope),
            'NN_maximum':nnmax,'actual_maximum':actmax,
            'original_rho':str(rho),'refined_rho':str(newrho),
            'refined_NN_sign_margin':str(neweta-nnmax*newrho),
            'refined_unforced_M_surplus':str(8*neweta/220),
            'refined_proper_floor':str(newfloor),
            'refined_actual_gap':str(newfloor/220),
            'retained_premises':['10308 original center/equality geometry',
                                 '10324 enlarged center/equality geometry for refinement only'],
            'ordinary_bridges_unformalized':True,'no_author_executable_or_data_input':True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--damage', choices=['inverse','bad_degree','good_mass','anchor',
                                            'missing_column','empty_lift'])
    args = parser.parse_args()
    print(json.dumps(audit(args.damage),sort_keys=True,indent=2))
