"""Strictly-unbalanced pendant completion at r=N-s, and every larger count.

The boundary branch lifts a singular raw lower mode with a restricted repair.
Above the boundary, reuse the independently published linear-count recipe.
See BOUNDARY_PENDANT_COMPLETION.md. Standard-library exact arithmetic only.
"""
from fractions import Fraction as F
import linear_pendant_completion as linear
from affine_pendant_completion import geometry, add_pendants


def require(condition, message):
    if not condition:
        raise ValueError(message)


def completion(family, center, count=None):
    s, old_star, old_outside = geometry(family, center)
    t = len(family) - s
    require(t > s >= 1, 'This nonnegative boundary recipe requires N>2s')
    r = t if count is None else count
    require(isinstance(r, int) and not isinstance(r, bool) and r >= t,
            'This sufficient recipe requires an integer r>=N-s')
    if r > t:
        record = linear.completion(family, center, r)
        record.update(construction='above-boundary', raw_lower_gap=F(2, 15),
                      lower_gap=F(1, 15), final_upper_gap=record['epsilon'])
        return record
    k, b, N = s + t, 2*t, len(family) + 2*t
    delta = t - s
    points = tuple(1 << (max(family).bit_length() + j) for j in range(t))
    spokes = tuple(p | (1 << center) for p in points)
    augmented = add_pendants(family, center, t)
    groups = {a: 'S' for a in old_star}
    groups.update({a: 'E' for a in [0] + old_outside})
    groups.update({a: 'Z' for a in spokes})
    groups.update({a: 'P' for a in points})
    position = {a: j for j, a in enumerate(points)}
    position.update({a: j for j, a in enumerate(spokes)})
    u, v, w = F(1, t), F(k, b*t), F(delta, b*(t-1))
    mu = F(delta, b)
    gap, repair_norm = F(8, 15), 2*s+4*(t-1)
    kappa = F(4*s*k, t*(t+3*s))
    epsilon = min(gap*kappa/(8*b*repair_norm**2), v/(2*s), u/2, mu/(2*t))

    def labels(a, d):
        require(isinstance(a, int) and not isinstance(a, bool)
                and isinstance(d, int) and not isinstance(d, bool)
                and a in groups and d in groups, 'Entry outside indexed integer family')
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
            return mu/t
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
            outside = -2*(t-1)
        elif {a, d} == {0, points[0]}:
            outside = t-1
        elif (a == 0 and gd == 'E' and d != 0) or (d == 0 and ga == 'E' and a != 0):
            outside = 1
        elif (a == points[0] and gd == 'E' and d != 0) or (d == points[0] and ga == 'E' and a != 0):
            outside = -1
        return F(cross+outside)

    def entry(a, d):
        return raw_entry(a, d)+epsilon*repair_entry(a, d)

    return dict(family=augmented, original_family=list(family), center=center,
        original_s=s, original_N=len(family), t=t, count=t, s=k, b=b, N=N,
        delta=delta, points=points, spokes=spokes, u=u, v=v, w=w, y=F(0), mu=mu,
        construction='boundary', raw_lower_gap=gap, repair_norm=repair_norm,
        kappa=kappa, epsilon=epsilon, lower_gap=b*epsilon*kappa/2,
        final_upper_gap=epsilon, raw_entry=raw_entry, repair_entry=repair_entry, entry=entry)


def dense_entries(record, mode='final', limit=64):
    return linear.dense_entries(record, mode=mode, limit=limit)
