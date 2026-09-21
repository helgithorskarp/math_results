#!/usr/bin/env python3
"""Exact finite corroboration of the universal proof; standard library only."""
import itertools
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def hull(points):
    points = sorted(points)
    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lower, upper = [], []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1] if len(points) > 1 else points


def endpoint_ranks(points):
    """Enumerate all subsets and compute their hull, independent of profiles."""
    N = len(points)
    require(N >= 2 and list(points) == sorted(points), 'point ordering')
    require(len({p[0] for p in points}) == N, 'distinct first coordinates')
    for a, b, c in itertools.combinations(points, 3):
        require((b[0]-a[0])*(c[1]-a[1]) != (b[1]-a[1])*(c[0]-a[0]),
                'general position')
    s = [[0]*N for _ in points]
    for mask in range(1, 1 << N):
        ids = [i for i in range(N) if mask >> i & 1]
        if len(ids) > 1 and len(hull([points[i] for i in ids])) == len(ids):
            s[ids[0]][ids[-1]] = max(s[ids[0]][ids[-1]], len(ids))
    return s


def profiles(n, s):
    """All feasible ACTIVE profiles. Inactive y_first=x_last=0.

    Uses only original pair and local constraints, not the new certificate.
    The active x_i bound n-1 follows from its pair with the final vertex.
    For fixed X, independent ranges enumerate EVERY feasible Y.
    """
    N = len(s)
    for x in itertools.product(range(n), repeat=N-1):
        bounds = []
        for j in range(1, N):
            bound = min(n+1-s[h][j]-x[h] for h in range(j))
            if j < N-1:
                bound = min(bound, n+1-x[j])
            bounds.append(bound)
        if min(bounds) < 0:
            continue
        for y in itertools.product(*(range(b+1) for b in bounds)):
            yield x, y


def value(n, x, y):
    # x indexes vertices 0..N-2; y indexes vertices 1..N-1.
    return (sum(math.comb(n, r) for r in range(x[0]+1))
            + sum(math.comb(x[i]+y[i-1], x[i]) for i in range(1, len(x)))
            + sum(math.comb(n, r) for r in range(y[-1]+1)))


def equality_profile(n, x, y):
    for i in range(1, len(x)):
        d = x[i]-x[i-1]
        if d not in (1, 2) or y[i-1] != n+d-1-x[i]:
            return False
    return x[-1]+y[-1] == n-1


def certificate(n, x, y):
    t = [x[0]]
    for a in x[1:]:
        t.append(max(a, t[-1]+1))
    if any(t[j-1]+y[j-1] > n-1 for j in range(1, len(x)+1)):
        return None
    if any(t[i]+y[i-1] > n+1 for i in range(1, len(x))):
        return None
    gaps = [math.comb(n, r) for r in range(t[-1]+1, n-y[-1])]
    terms = []
    for i in range(1, len(x)):
        raised = math.comb(t[i]+y[i-1], t[i])
        gain = raised-math.comb(x[i]+y[i-1], x[i])
        slack = sum(math.comb(n, r) for r in range(t[i-1]+1, t[i]+1))-raised
        require(gain >= 0 and slack >= 0, 'negative certificate term')
        terms.append([gain, slack])
    deficit = sum(gaps) + sum(sum(v) for v in terms)
    require(deficit == (1 << n)-value(n, x, y), 'deficit identity')
    return {'envelope': t, 'gap': sum(gaps), 'terms': terms, 'deficit': deficit}


def interval_condition(x, s):
    """Use the latest envelope maximizer, a specified sufficient choice."""
    N = len(s)
    for j in range(1, N):
        h = max(range(j), key=lambda a: (x[a]-a, a))
        if s[h][j] != j-h+1:
            return False
    return True


def main():
    result = {'status': 'VERIFIED', 'convex_profiles': 0,
              'convex_equality_profiles': 0, 'convex_cases': [],
              'geometric_profiles': 0, 'interval_certificates': 0,
              'numerical_certificates': 0}
    # The convex rank array is itself checked from geometry at every size.
    for N in range(2, 7):
        points = [(i, i*i) for i in range(N)]
        s = endpoint_ranks(points)
        require(all(s[h][j] == j-h+1 for h in range(N) for j in range(h+1, N)),
                'convex endpoint ranks')
        for n in range(N-1, 7):
            count = equal = 0
            for x, y in profiles(n, s):
                B = value(n, x, y)
                require(B <= 1 << n, 'convex-seed excess')
                require((B == 1 << n) == equality_profile(n, x, y), 'equality classification')
                require(interval_condition(x, s), 'convex interval condition')
                require(certificate(n, x, y) is not None, 'convex certificate')
                count += 1
                equal += (B == 1 << n)
            require(equal > 0, 'attainment')
            result['convex_profiles'] += count
            result['convex_equality_profiles'] += equal
            result['convex_cases'].append({'n': n, 'N': N, 'profiles': count, 'equal': equal})
    nonconvex = [(0, 0), (2, 2), (3, 1), (5, 7)]
    s = endpoint_ranks(nonconvex)
    require(len(hull(nonconvex)) == 3 and s[0][3] == 3, 'nonconvex fixture')
    for n in range(2, 7):
        for x, y in profiles(n, s):
            B = value(n, x, y)
            cert = certificate(n, x, y)
            geometric = interval_condition(x, s)
            if geometric:
                require(cert is not None, 'interval hypothesis implies certificate')
                result['interval_certificates'] += 1
            if cert is not None:
                require(B <= 1 << n, 'certified nonconvex excess')
                require((B == 1 << n) == equality_profile(n, x, y), 'certificate equality')
                result['numerical_certificates'] += 1
            result['geometric_profiles'] += 1
    # Certificate failure is not an excess: the 4-point nonconvex seed itself.
    x = y = (0, 0, 0)
    require((x, y) in set(profiles(2, s)), 'scope example feasibility')
    require(not interval_condition(x, s) and certificate(2, x, y) is None,
            'scope example must fail sufficient certificate')
    require(value(2, x, y) == 4 and not equality_profile(2, x, y),
            'convex-only equality scope')
    result['scope_control'] = {'points': nonconvex, 'n': 2, 'X_active': x,
                               'Y_active': y, 'B': 4, 'certificate': None}
    # Exact positive example on a nonconvex seed, with local intervals only.
    x, y = (0, 1, 2), (2, 1, 0)
    require((x, y) in set(profiles(3, s)), 'local positive feasibility')
    require(interval_condition(x, s) and value(3, x, y) == 8, 'local positive')
    result['nonconvex_positive'] = certificate(3, x, y)
    # Independent counting of all binomial levels and every local inequality.
    local = 0
    for n in range(1, 11):
        histogram = [0]*(n+1)
        for word in itertools.product((0, 1), repeat=n):
            histogram[sum(word)] += 1
        require(histogram == [math.comb(n, r) for r in range(n+1)], 'word levels')
        for a in range(n):
            for b in range(a+1, n):
                for y in range(min(n-1-a, n+1-b)+1):
                    assigned = sum(histogram[a+1:b+1])
                    require(math.comb(b+y, b) <= assigned, 'local allocation')
                    require((math.comb(b+y, b) == assigned) ==
                            (b-a in (1, 2) and y == n+(b-a)-1-b), 'local equality')
                    local += 1
    result['binary_word_local_checks'] = local
    data = (json.dumps(result, indent=2, sort_keys=True)+'\n').encode()
    expected = Path(__file__).with_name('expected.json')
    if expected.exists():
        require(data == expected.read_bytes(), 'expected output mismatch')
    print(data.decode(), end='')


if __name__ == '__main__':
    main()
