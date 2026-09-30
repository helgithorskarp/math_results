"""Independent actual-progression checks of the fixed-binary upper relaxation."""
import json
from itertools import product
from time import monotonic
from distinct_top_points import prepare, exact_budget
from fixed_binary_cluster import cluster_bound, evidence


def require(ok, message):
    if not ok:
        raise ValueError(message)


def literal_top_bound(state, cluster):
    N, B, T, A = state['N'], state['B'], state['T'], state['known']
    u = state['u']
    w = [state['v'][x % state['Q']] for x in range(N)]
    q0 = A[B] % T
    alpha1 = (A[B] + T) % B
    outside, inside = {}, {}
    for n in state['S']:
        if n == B:
            continue
        d = n // B
        outside[d] = max((sum(u[a::n]) + sum(w[a::n]) for a in range(n) if a % B % T != q0), default=0)
        inside[d] = max(sum(u[a::n]) + 2 * sum(w[a::n]) for a in range(alpha1, n, B))
    totals = []
    for mask in range(1 << len(cluster)):
        selected = [d for i, d in enumerate(cluster) if mask >> i & 1]
        best = -1
        for actual_phases in product(*(range(alpha1, B * d, B) for d in selected)):
            union = set()
            value = 0
            for d, a in zip(selected, actual_phases):
                points = range(a, N, B * d)
                union.update(points)
                value += sum(u[x] for x in points)
            value += 2 * sum(w[x] for x in union)
            best = max(best, value)
        totals.append(best + sum(outside[d] for i, d in enumerate(cluster) if not mask >> i & 1))
    result = max(totals) + sum(max(outside[n // B], inside[n // B]) for n in state['S'] if n != B and n // B not in cluster)
    return result


def main():
    t = monotonic()
    fixtures = []
    for C, u in [(9, [0] * 36), (9, [0] * 18 + [1] + [0] * 17), (15, [0] * 60)]:
        P = [3, 9] if C == 9 else [3, 5, 15]
        s = prepare(4, C, 2, [(4, 0)], u, [1] + [0] * (2 * C - 1))
        k = exact_budget(s)['sharp_budget']
        bound = cluster_bound(s, P)['top_upper_budget']
        require(k <= bound and bound == literal_top_bound(s, P), 'Cluster fixture or units')
        fixtures.append({'C': C, 'exact_point_budget': k, 'cluster_upper': bound})
    require([x['cluster_upper'] for x in fixtures] == [2, 4, 2], 'Strict cluster fixtures')

    cover = [(2, 0), (3, 0), (4, 1), (6, 3), (12, 7), (9, 2), (18, 5), (36, 35)]
    count = negative = known_positive = 0
    for A in [[(4, 1)], [(4, 1), (2, 0)], [(4, 1), (2, 0), (3, 0)], [(4, 1), (2, 0), (3, 0), (6, 3), (9, 2), (18, 5)]]:
        for v in [[1] * 18] + [[int(x == j) for x in range(18)] for j in range(18)]:
            u = [int(not any(x % n == a for n, a in A)) * (x % 7) for x in range(36)]
            s = prepare(4, 9, 2, A, u, v)
            e = evidence(s, [3, 9])
            require(e['gap'] <= 0, 'False genuine-cover exclusion')
            require(e['top_bound']['top_upper_budget'] == literal_top_bound(s, [3, 9]), 'Literal cluster budget')
            count += 1
            negative += e['demand'] < 0
            known_positive += any(v[x % 18] for x in range(1, 36, 4))
            zero = prepare(4, 9, 2, A, [0] * 36, v)
            ze = evidence(zero, [3, 9])
            require(ze['gap'] <= 0 and ze['top_bound']['top_upper_budget'] == literal_top_bound(zero, [3, 9]), 'Zero-u affine boundary')
            count += 1
            negative += ze['demand'] < 0
            known_positive += any(v[x % 18] for x in range(1, 36, 4))

    # Weight period smaller than T*C and a prescribed eight resource.
    cover24 = [(2, 0), (3, 0), (4, 1), (6, 1), (8, 3), (12, 11)]
    require(all(any(x % n == a for n, a in cover24) for x in range(24)), 'Cover24')
    for b in [1, 2, 4]:
        for A in [[(8, 3)], [(8, 3), (2, 0), (3, 0)]]:
            for j in range(b * 3):
                v = [int(x == j) for x in range(b * 3)]
                u = [int(not any(x % n == a for n, a in A)) * (x % 5) for x in range(24)]
                s = prepare(8, 3, b, A, u, v)
                e = evidence(s, [3])
                require(e['gap'] <= 0 and e['top_bound']['top_upper_budget'] == literal_top_bound(s, [3]), 'Small-period genuine-cover bound')
                count += 1
    require(negative > 0 and known_positive > 0, 'Effective-demand and known-top boundaries')
    result = {'agent': 'six-covering-2', 'role': 'researcher', 'all_passed': True,
              'fixtures': fixtures, 'genuine_cover_cases': count, 'negative_effective_demands': negative,
              'positive_prescribed_coarsest_cases': known_positive,
              'seconds': monotonic() - t,
              'scope': 'Exact evaluation of a valid upper relaxation, not exact optimization of the full point-charge budget'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
