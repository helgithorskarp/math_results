"""Universal linear-count pendant completion, with no seed certificate.

See LINEAR_PENDANT_COMPLETION.md. Stores O(N+r) integer labels and a fixed
number of rational parameters; entries use a closed four-block formula.
"""
from fractions import Fraction as F
from affine_pendant_completion import geometry, add_pendants


def require(condition, message):
    if not condition:
        raise ValueError(message)


def completion(family, center, count=None):
    s, old_star, old_outside = geometry(family, center)
    t = len(family) - s
    r = t + 1 if count is None else count
    require(isinstance(r, int) and not isinstance(r, bool) and r >= t + 1,
            "This sufficient linear-count recipe requires r>=N-s+1")
    k, b, N = s + r, t + r, len(family) + 2 * r
    delta = t - s
    require(r >= 2 and t >= s >= 1 and delta >= 0, "Downset deletion bound failed")
    points = tuple(1 << (max(family).bit_length() + j) for j in range(r))
    spokes = tuple(p | (1 << center) for p in points)
    augmented = add_pendants(family, center, r)
    groups = {a: 'S' for a in old_star}
    groups.update({a: 'E' for a in [0] + old_outside})
    groups.update({a: 'Z' for a in spokes})
    groups.update({a: 'P' for a in points})
    position = {a: j for j, a in enumerate(points)}
    position.update({a: j for j, a in enumerate(spokes)})
    u, v = F(1, r), F(k, b * r)
    w, y = F(r * r - s * t, b * r * (r - 1)), F(r - t, r * (r - 1))
    mu = F(delta, b)
    eta = min(u, v, w)
    upper_gap = 2 * eta / (N - 1) ** 2
    repair_norm = 2 * s + 4 * (b - 2)
    epsilon = min(F(1, 15 * b * repair_norm), upper_gap / (2 * repair_norm),
                  v / (2 * s), u / 2)
    if delta:
        epsilon = min(epsilon, mu / (2 * r), mu * y / 2)

    def labels(a, d):
        require(isinstance(a, int) and not isinstance(a, bool)
                and isinstance(d, int) and not isinstance(d, bool)
                and a in groups and d in groups, "Entry outside indexed integer family")
        return groups[a], groups[d]

    def raw_entry(a, d):
        ga, gd = labels(a, d)
        pair = {ga, gd}
        if pair == {'S', 'P'}:
            return u
        if pair == {'Z', 'E'}:
            return v
        if pair == {'Z', 'P'}:
            return w if position[a] != position[d] else F(0)
        if pair == {'E', 'P'}:
            return mu / r
        if ga == gd == 'P' and a != d:
            return mu * y
        return F(0)

    def repair_entry(a, d):
        ga, gd = labels(a, d)
        cross = 0
        if (a == 0 and gd == 'S') or (d == 0 and ga == 'S'):
            cross = 1
        elif {a, d} == {spokes[0], points[1]}:
            cross = s
        elif (a == points[1] and gd == 'S') or (d == points[1] and ga == 'S'):
            cross = -1
        elif {a, d} == {0, spokes[0]}:
            cross = -s
        outside = 0
        if a == d == 0:
            outside = -2 * (b - 2)
        elif {a, d} == {0, points[0]}:
            outside = b - 2
        elif a == 0 and gd in ('E', 'P') and d not in (0, points[0]):
            outside = 1
        elif d == 0 and ga in ('E', 'P') and a not in (0, points[0]):
            outside = 1
        elif a == points[0] and gd in ('E', 'P') and d not in (0, points[0]):
            outside = -1
        elif d == points[0] and ga in ('E', 'P') and a not in (0, points[0]):
            outside = -1
        return F(cross + outside)

    def entry(a, d):
        return raw_entry(a, d) + epsilon * repair_entry(a, d)

    return dict(family=augmented, original_family=list(family), center=center,
                original_s=s, original_N=len(family), t=t, count=r,
                s=k, b=b, N=N, delta=delta, points=points, spokes=spokes,
                u=u, v=v, w=w, y=y, mu=mu, eta=eta, upper_gap=upper_gap,
                repair_norm=repair_norm, epsilon=epsilon,
                raw_entry=raw_entry, repair_entry=repair_entry, entry=entry)


def dense_entries(record, mode='final', limit=64):
    require(record['N'] <= limit, "Dense validation exceeds explicit order limit")
    require(mode in ('final', 'raw', 'repair'), "Unknown matrix mode")
    oracle = record[{'final': 'entry', 'raw': 'raw_entry', 'repair': 'repair_entry'}[mode]]
    return [[oracle(a, d) for d in record['family']] for a in record['family']]
