"""Exact conservative P35 row producer. Actual author six-code-1, researcher.

No solver or peer executable. Physical and ordinary trust bridges: PROOF.md.
"""
from collections import Counter
import hashlib
import itertools as it
import json
import time

FIELDS = ('e','k','q','eligible','h','g1_S','psi','corrected_margin',
          'ss_excess','I5','hub_weight')

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()

def rows_and_physical_bridge(data):
    need(type(data) is dict and len(data['stars']) == 23, 'complete literal23-star carrier')
    rows, original, bridges = [], [], []
    for fi, blocks in enumerate(data['stars']):
        need(len(blocks) == 20 and len({tuple(sorted(b)) for b in blocks}) == 20,
             'twenty distinct blocks')
        need(all(len(b) == 4 and len(set(b)) == 4 and
                 all(type(p) is int and 0 <= p < 17 for p in b) for b in blocks),
             'literal four-subsets of17')
        multiplicities = Counter(p for block in blocks for p in block)
        covered = Counter(tuple(sorted(pair)) for block in blocks
                          for pair in it.combinations(block, 2))
        need(len(covered) == 120 and max(covered.values()) == 1, 'simple pair ownership')
        missing = {pair for pair in it.combinations(range(17), 2) if pair not in covered}
        delta = [5 - multiplicities[p] for p in range(17)]
        high = tuple(p for p in range(17) if delta[p] > 0)
        HH = {pair for pair in missing if all(p in high for p in pair)}
        need(min(delta) >= 0 and sum(delta) == 5 and len(missing) == 16,
             'physical deficit/leave domain')
        need(len(HH) == len(high) - 1, 'high-high leave identity')
        need(all(sum(p in edge for edge in missing) == 1 + 3*delta[p]
                 for p in range(17)), 'physical leave degrees')
        need(all(any(delta[p] > 0 for p in edge) for edge in missing), 'no low-low leave')
        isolated = {p for p in high if all(p not in edge for edge in HH)}
        for size in range(len(high) + 1):
            for marks in it.combinations(high, size):
                sat = tuple(p for p in high if p not in marks)
                e, k = 5 - len(high), len(marks)
                q = sum(any(p in marks for p in edge) for edge in HH)
                eligible = bool(isolated.intersection(marks))
                g1 = sum(delta[p] == 1 for p in sat)
                sigma = sum(delta[p] - 1 for p in sat)
                weight = sum(delta[p] for p in marks)
                psi = g1 if not e and eligible else -g1 if e and not eligible else 0
                indicator = int(e == 0 and k == 5)
                margin = psi - 3*(k - e - q)
                coordinates = (e,k,q,eligible,len(high),g1,psi,
                               margin+3*indicator,sigma,indicator,weight)
                need(coordinates[7] >= 0 and e == weight-k+sigma,
                     'corrected coefficient and weighted-support identity')
                rows.append(dict(fixture=fi, hub_high=list(marks), coordinates=list(coordinates)))
                original.append(dict(fixture=fi,hub_high=list(marks),h=len(high),e=e,k=k,q=q,
                                     eligible=eligible,g1_S=g1,ss_excess=sigma,hub_weight=weight,
                                     psi=psi,margin=margin))
                if e == k == 1 and q == 0:
                    need(eligible and len(sat) == 3 and len(marks) == 1,
                         'one actual isolated deficient hub and three saturated support neighbors')
                    need(set(it.combinations(sat,2)) == HH,
                         'EVERY saturated neighbor wedge is an actual high-high leave')
                    need(sum(delta[p] for p in sat) + delta[marks[0]] == 5,
                         'weighted bridge counts deficit weight as well as support')
                    bridges.append(dict(fixture=fi,hub=marks[0],neighbors=list(sat),
                                        saturated_pair_deficits=[delta[p] for p in sat],
                                        hub_deficit=delta[marks[0]],ss_excess=sigma))
    rows.sort(key=lambda r:(r['fixture'],r['hub_high']))
    original.sort(key=lambda r:(r['fixture'],r['hub_high']))
    need(len(rows) == 426 and sum(r['coordinates'][9] for r in rows) == 8,
         'all426 marks and eight retained exceptional unit rows')
    return rows, bridges

def arithmetic():
    cases = []
    # From9367: T>=1, Q>=4N5, and2T+2X+4tau+Q-N5<=7.
    for N5 in range(2):
        for T,X,tau in it.product(range(1,4),range(3),range(2)):
            for Q in range(4*N5,8+N5):
                if 2*T+2*X+4*tau+Q-N5 > 7:
                    continue
                E = 11-T-2*tau-Q
                K = 15-E+2*X
                budget = 3*(E+Q+N5-K)
                need(min(E,K,budget) >= 0, 'necessary scalar nonnegativity')
                cases.append(dict(T=T,X=X,tau=tau,N5=N5,Q=Q,E=E,K=K,
                                  margin_budget=budget))
    need(len(cases) == 27 and sum(c['N5'] for c in cases) == 5,
         'complete arithmetic domain')
    return cases

def certificate(types, vector):
    rows = [t for t, count in zip(types, vector) for _ in range(count)]
    U = [t for t in rows if t[0] == 0]
    A = [t for t in U if not t[3]]
    C = [t for t in rows if t[0] > 0 and not t[3]]
    B = [t for t in rows if t[0] > 0 and t[3]]
    D = sum(t[4] - t[1] for t in U)
    I = sum(min(t[4] - t[1], len(A) - 1) for t in A)
    C1, C2 = (sum(t[i] for t in C) for i in (5, 8))
    B2 = sum(t[8] for t in B)
    R = sum(t[1] == 0 for t in U)
    K0C = sum(t[1] == 0 for t in C)
    if D > I + C1:
        reason = 'UNIT_NEIGHBOR_CAPACITY'
    elif R > 0 and B and C1 + C2 < R + len(B):
        reason = 'DISTINCT_RADIUS_TWO_CROSSINGS'
    elif (D == I + C1 and B and (C2 == 0 or B2 == 0)
          and R + K0C > 0):
        reason = 'ALL_COLORS_CLOSED_PARTITION'
    else:
        reason = 'OPEN'
    return dict(reason=reason, D=D, I=I, C1=C1, C2=C2, B2=B2,
                unit_roots_k0=R, ineligible_nonunit_roots_k0=K0C,
                unit_rows=len(U), ineligible_unit_rows=len(A),
                ineligible_nonunit_rows=len(C), eligible_nonunit_rows=len(B))

def produce(types, case):
    E, K, Q, X, budget = (case[f] for f in ('E', 'K', 'Q', 'X', 'margin_budget'))
    zero = {
        'U0': (0, 0, 0, False, 5, 5, 0, 0, 0, 0, 0),
        'U1': (0, 1, 0, True, 5, 4, 4, 1, 0, 0, 1),
        'A': (1, 0, 0, False, 4, 3, -3, 0, 1, 0, 0),
        'B': (1, 1, 0, True, 4, 3, 0, 0, 0, 0, 2),
        'C': (1, 1, 0, True, 4, 2, 0, 0, 1, 0, 1),
        'D': (2, 0, 0, False, 3, 1, -1, 5, 2, 0, 0),
    }
    need({t for t in types if t[2] == 0} == set(zero.values()),
         'Complete six zero-charge types, including deficit-two carrier')
    index = {t: j for j, t in enumerate(types)}
    positive = [t for t in types if 0 < t[2] <= Q and t[7] <= budget and t[8] <= 2 * X]
    patterns, nodes, begin = [], 0, time.monotonic()

    def visit(first, used, counts):
        nonlocal nodes
        nodes += 1
        need(nodes <= 100000 and time.monotonic() - begin <= 10,
             'INCOMPLETE frozen100000-state/10s census guard')
        n, e, k, q, sigma, exceptional, mu = used
        if q == Q:
            if exceptional != case['N5']:
                return
            n0, e0, k0, s0, mu0 = 13 - n, E - e, K - k, 2 * X - sigma, budget - mu
            for d in range(min(e0 // 2, s0 // 2, mu0 // 5) + 1):
                for a in range(s0 - 2 * d + 1):
                    c, b = s0 - 2 * d - a, e0 - s0
                    u1 = k0 - e0 + 2 * d + a
                    u0 = n0 - e0 + d - u1
                    if min(a, b, c, d, u1, u0) < 0 or u1 + 5 * d > mu0:
                        continue
                    v = list(counts)
                    for name, count in [('U0', u0), ('U1', u1), ('A', a),
                                        ('B', b), ('C', c), ('D', d)]:
                        v[index[zero[name]]] = count
                    totals = (sum(v),) + tuple(sum(c * t[i] for c, t in zip(v, types))
                                               for i in (0, 1, 2, 8, 9))
                    need(totals == (13, E, K, Q, 2 * X, case['N5']) and
                         sum(c * t[7] for c, t in zip(v, types)) <= budget,
                         'All complete vectors satisfy exact totals')
                    patterns.append(tuple(v))
            return
        for j in range(first, len(positive)):
            t = positive[j]
            new = (n + 1, e + t[0], k + t[1], q + t[2], sigma + t[8],
                   exceptional + t[9], mu + t[7])
            if any(a > b for a, b in zip(new, (13, E, K, Q, 2 * X, case['N5'], budget))):
                continue
            counts[index[t]] += 1
            visit(j, new, counts)
            counts[index[t]] -= 1

    visit(0, (0,) * 7, [0] * len(types))
    need(len(set(patterns)) == len(patterns), 'No repeated full count vector')
    return sorted(patterns), nodes


def conservative_rows(data, rows):
    selected = []
    for row in rows:
        multiplicity = Counter(p for block in data['stars'][row['fixture']] for p in block)
        hubs = set(row['hub_high'])
        if all(5-multiplicity[a] <= (3 if a in hubs else 2) for a in range(17)):
            selected.append(row)
    return selected
