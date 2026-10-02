"""Separate physical-bit/full-factor oracle. six-code-1, researcher.

No producer, expected result, specialized zero-charge equation, solver or
peer program is imported. All count vectors are reconstructed exactly.
"""
from functools import lru_cache
import itertools as it
import time

def need(ok, message):
    if not ok:
        raise ValueError(message)

def physical_rows(data):
    stars = data['stars']
    need(len(stars) == 23, 'All generic classes')
    all_rows, filtered = [], []
    for fi, star in enumerate(stars):
        need(len(star) == 20 and all(len(b) == len(set(b)) == 4 and
             all(type(p) is int and 0 <= p < 17 for p in b) for b in star),
             'Physical point domain')
        masks = [sum(1 << p for p in b) for b in star]
        need(len(set(masks)) == 20, 'Distinct quadruples')
        replication = [(sum(bool(b & (1 << p)) for b in masks)) for p in range(17)]
        delta = [5 - r for r in replication]
        high = [p for p in range(17) if delta[p]]
        need(min(delta) >= 0 and sum(delta) == 5, 'Actual point deficits')
        leave = [0] * 17
        for a in range(17):
            for b in range(a + 1, 17):
                mask = (1 << a) | (1 << b)
                owners = sum((block & mask) == mask for block in masks)
                need(owners <= 1, 'Simple physical pair ownership')
                if not owners:
                    leave[a] |= 1 << b
                    leave[b] |= 1 << a
        high_mask = sum(1 << p for p in high)
        need(sum(x.bit_count() for x in leave) == 32 and
             all(leave[p].bit_count() == 1 + 3 * delta[p] for p in range(17)) and
             all(not (leave[p] & ~high_mask) for p in range(17) if not delta[p]),
             'Physical leave identity including no low-low pair')
        # Subset bits have a fixed canonical order independent of combinations.
        for subset in range(1 << len(high)):
            H = [p for j, p in enumerate(high) if subset >> j & 1]
            hmask = sum(1 << p for p in H)
            smask = high_mask ^ hmask
            h, k, e = len(high), len(H), 5 - len(high)
            q = sum(bool(hmask & ((1 << a) | (1 << b))) for a in high for b in high
                    if a < b and (leave[a] >> b & 1))
            eligible = any(not (leave[p] & high_mask) for p in H)
            one = sum(delta[p] == 1 for p in range(17) if smask >> p & 1)
            excess = sum(delta[p] - 1 for p in range(17) if smask >> p & 1)
            charge = one if e == 0 and eligible else -one if e and not eligible else 0
            exceptional = int(e == 0 and k == 5)
            margin = charge - 3 * (k - e - q - exceptional)
            coordinates = [e, k, q, eligible, h, one, charge, margin,
                           excess, exceptional, sum(delta[p] for p in H)]
            record = dict(fixture=fi, hub_high=H, coordinates=coordinates)
            all_rows.append(record)
            if all(delta[p] <= (3 if hmask >> p & 1 else 2) for p in range(17)):
                filtered.append(record)
    return sorted(all_rows, key=lambda r: (r['fixture'], r['hub_high'])), sorted(
        filtered, key=lambda r: (r['fixture'], r['hub_high']))

def all_cases():
    # Rectangular literal range, retaining both N5 values before selecting zero.
    out = []
    for N5, T, X, tau, Q in it.product(range(2), range(1, 4), range(3), range(2), range(9)):
        if Q < 4 * N5 or 2 * T + 2 * X + 4 * tau + Q - N5 > 7:
            continue
        E = 11 - T - 2 * tau - Q
        K = 15 - E + 2 * X
        mu = 3 * (E + Q + N5 - K)
        need(min(E, K, mu) >= 0, 'Literal scalar domain')
        out.append(dict(T=T, X=X, tau=tau, N5=N5, Q=Q,
                        E=E, K=K, margin_budget=mu))
    return out

def coefficient_vectors(types, case):
    target = (13, case['E'], case['K'], case['Q'], 2 * case['X'],
              case['N5'], case['margin_budget'])
    charges = [(1, t[0], t[1], t[2], t[8], t[9], t[7]) for t in types]
    length = len(target)
    order = [i for i, w in enumerate(charges) if all(a <= b for a, b in zip(w, target))]
    # Factor order is a permutation; it does not select a carrier or a count cap.
    order.sort(key=lambda i: charges[i], reverse=True)
    weights = [charges[i] for i in order]
    states, begin = 0, time.monotonic()
    suffix_min, suffix_max = [], []
    for j in range(len(weights)):
        suffix_min.append(tuple(min(w[i] for w in weights[j:]) for i in range(1, length)))
        suffix_max.append(tuple(max(w[i] for w in weights[j:]) for i in range(1, length)))

    @lru_cache(None)
    def coefficient(j, remaining):
        nonlocal states
        states += 1
        need(states <= 100000 and time.monotonic() - begin <= 10,
             'INCOMPLETE frozen coefficient100000-state/10s guard')
        if j == len(weights):
            return ((),) if remaining[:-1] == (0,) * (length - 1) else ()
        n = remaining[0]
        if any(remaining[i] < n * suffix_min[j][i - 1] for i in range(1, length)):
            return ()
        if any(remaining[i] > n * suffix_max[j][i - 1] for i in range(1, length - 1)):
            return ()
        w = weights[j]
        maximum = min(remaining[i] // w[i] for i in range(length) if w[i])
        result = []
        for count in range(maximum + 1):
            residual = tuple(a - count * b for a, b in zip(remaining, w))
            for tail in coefficient(j + 1, residual):
                result.append((count,) + tail)
        return tuple(result)

    out = []
    for v in coefficient(0, target):
        full = [0] * len(types)
        for i, count in zip(order, v):
            full[i] = count
        out.append(tuple(full))
    need(len(set(out)) == len(out), 'One formal monomial for each full count vector')
    return sorted(out), states


def direct_capacity(types, vector):
    """A separate vertex/colored-endpoint reconstruction of every certificate."""
    vertices = []
    for position in range(len(types)):
        t = types[position]
        need(t[5] + t[8] == t[4] - t[1], 'Deficits1/2 are SUPPORT colors')
        for _ in range(vector[position]):
            vertices.append(dict(unit=t[0] == 0, eligible=bool(t[3]),
                                 one=t[5], two=t[8], root=t[1] == 0))
    U = [v for v in vertices if v['unit']]
    A = [v for v in U if not v['eligible']]
    C = [v for v in vertices if not v['unit'] and not v['eligible']]
    B = [v for v in vertices if not v['unit'] and v['eligible']]
    D = sum(v['one'] for v in U)
    internal = 0
    for v in A:
        capacity = len(A) - 1
        if capacity > v['one']:
            capacity = v['one']
        internal += capacity
    C1 = sum(v['one'] for v in C)
    C2 = sum(v['two'] for v in C)
    B2 = sum(v['two'] for v in B)
    R = len([v for v in U if v['root']])
    RC = len([v for v in C if v['root']])
    failure = 'OPEN'
    if D - internal - C1 > 0:
        failure = 'UNIT_NEIGHBOR_CAPACITY'
    elif R != 0 and len(B) != 0 and C1 + C2 - R - len(B) < 0:
        failure = 'DISTINCT_RADIUS_TWO_CROSSINGS'
    elif (D - internal == C1 and len(B) > 0 and
          (not C2 or not B2) and R + RC > 0):
        failure = 'ALL_COLORS_CLOSED_PARTITION'
    return dict(reason=failure, D=D, I=internal, C1=C1, C2=C2, B2=B2,
                unit_roots_k0=R, ineligible_nonunit_roots_k0=RC,
                unit_rows=len(U), ineligible_unit_rows=len(A),
                ineligible_nonunit_rows=len(C), eligible_nonunit_rows=len(B))
