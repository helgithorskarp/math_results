#!/usr/bin/env python3
"""Exact supplementary checks and a generated non-co-sunflower witness."""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
import random

from rounding import (add_clique_triangles, centered_lp, edge_coloring,
                      local_saturation, lp_data, residual_bound, round_centered,
                      saturated_gap_bound, verify_coloring, verify_lp, verify_packing)


def reject(action):
    try:
        action()
    except AssertionError:
        return
    raise AssertionError('negative control was accepted')


def direct_integer_centered(k, sets, multiplicities):
    """Enumerate actual matchings for each individual center; no LP rows."""
    es = list(combinations(range(k), 2))
    edge_id = {e: j for j, e in enumerate(es)}
    @lru_cache(None)
    def matchings(vertices):
        if not vertices:
            return (0,)
        v, *rest = vertices
        result = set(matchings(tuple(rest)))
        for u in rest:
            bit = 1 << edge_id[min(u, v), max(u, v)]
            result.update(bit | mask for mask in matchings(tuple(w for w in rest if w != u)))
        return tuple(sorted(result))
    reachable = {0}
    for s, m in zip(sets, multiplicities):
        choices = matchings(tuple(sorted(s)))
        for _ in range(m):
            reachable = {a | b for a in reachable for b in choices if not a & b}
    return max(map(int.bit_count, reachable), default=0)


def explicit_fractional_check(k, sets, multiplicities, result):
    """Expand every LP variable into weights on actual graph triangles."""
    loads = Counter()
    offset = k
    offsets = []
    for m in multiplicities:
        offsets.append(offset)
        offset += m
    mass = Q(0)
    for (i, u, v), weight in zip(result['variables'], result['primal']):
        for center in range(offsets[i], offsets[i] + multiplicities[i]):
            w = weight / multiplicities[i]
            for e in combinations(sorted((u, v, center)), 2):
                loads[e] += w
            mass += w
    assert mass == result['value'] and all(w <= 1 for w in loads.values())


def coloring_audit():
    counts = []
    for k in range(7):
        es = list(combinations(range(k), 2))
        for mask in range(1 << len(es)):
            sub = [e for j, e in enumerate(es) if mask >> j & 1]
            edge_coloring(k, sub)
        counts.append(1 << len(es))
    rng = random.Random(571705)
    for case in range(60):
        k = 8 + case % 25
        probability = (1 + case % 9) / 10
        es = [e for e in combinations(range(k), 2) if rng.random() < probability]
        edge_coloring(k, es)
    reject(lambda: verify_coloring(3, [(0, 1), (0, 2)], {(0, 1): 0, (0, 2): 0}))
    return dict(exhaustive_graph_counts=counts, seeded_larger_graphs=60)


def lp_audit():
    instances = []
    for k in range(2, 8):
        for size in range(2, k + 1):
            for m in range(1, size):
                instances.append((k, [tuple(range(size))], [m]))
    subsets = [s for size in range(2, 5) for s in combinations(range(4), size)]
    for ss in combinations(subsets, 2):
        instances.append((4, list(ss), [1, 1]))
        instances.append((4, list(ss), [len(s) - 1 for s in ss]))
    rng = random.Random(571706)
    for case in range(100):
        k = 3 + case % 5
        available = [s for size in range(2, k + 1) for s in combinations(range(k), size)]
        ss = rng.sample(available, min(len(available), 1 + case % 4))
        mm = [rng.randrange(1, len(s)) for s in ss]
        instances.append((k, ss, mm))
    stats = Counter()
    max_actual_gap = Q(0)
    trace = sha256()
    for k, ss, mm in instances:
        result = centered_lp(k, ss, mm)
        explicit_fractional_check(k, ss, mm, result)
        centered, details = round_centered(k, ss, mm, result)
        full = add_clique_triangles(k, centered)
        verify_packing(k, ss, mm, full)
        assert len(full) >= residual_bound(k, len(centered))
        assert len(full) >= residual_bound(k, max(Q(0), result['value'] - Q(3 * sum(map(len, ss)), 2)))
        E = sum(len(s) * m for s, m in zip(ss, mm))
        saturated = 2 * result['value'] == E
        if local_saturation(k, ss, mm):
            assert saturated
            stats['local_saturation_certificates'] += 1
        stats['spoke_saturated_lp_optima'] += saturated
        stats['lp_pairs'] += 1
        stats['pivots'] += result['pivots']
        stats['instances_with_fractional_assignments'] += details['fractional_base_edges'] > 0
        stats['instances_requiring_color_discard'] += details['coloring_loss'] > 0
        if k <= 5:
            actual = direct_integer_centered(k, ss, mm)
            assert len(centered) <= actual <= result['value']
            assert actual >= result['value'] - Q(3 * sum(map(len, ss)), 2)
            max_actual_gap = max(max_actual_gap, result['value'] - actual)
            stats['definition_level_integer_optima'] += 1
        trace.update(repr((k, ss, mm, str(result['value']), len(centered), len(full), details)).encode())
    # Theorem 1 is also valid for arbitrary base graphs, not just cliques.
    for case in range(24):
        k = 3 + case % 4
        ss = [tuple(range(k)), tuple(range(k - 1))]
        mm = [1 + case % 2, 1]
        base = [e for e in combinations(range(k), 2) if rng.randrange(3)]
        result = centered_lp(k, ss, mm, base)
        centered, _ = round_centered(k, ss, mm, result, base)
        verify_packing(k, ss, mm, centered, base)
        stats['arbitrary_base_lp_pairs'] += 1
    # A primal/dual optimal pair that is NOT extreme must be rejected.
    es, degrees, vs, _, _ = lp_data(7, [tuple(range(7))], [3])
    nonextreme = dict(variables=vs, primal=[Q(1, 2)] * len(vs),
                     dual=[Q(0)] * len(es) + [Q(1, 2)] * len(degrees), value=Q(21, 2))
    reject(lambda: verify_lp(7, [tuple(range(7))], [3], nonextreme))
    # Feasibility, duality, and packing decoding negative controls.
    result = centered_lp(3, [(0, 1, 2)], [2])
    corrupted = dict(result, primal=[Q(2)] + result['primal'][1:])
    reject(lambda: verify_lp(3, [(0, 1, 2)], [2], corrupted))
    corrupted = dict(result, dual=[Q(0)] * len(result['dual']))
    reject(lambda: verify_lp(3, [(0, 1, 2)], [2], corrupted))
    reject(lambda: verify_packing(3, [(0, 1, 2)], [2], [(3, 0, 1), (3, 0, 1)]))
    blocked = centered_lp(4, [(0, 1, 2), (0, 1, 3)], [2, 2])
    assert blocked['value'] == 5
    assert not local_saturation(4, [(0, 1, 2), (0, 1, 3)], [2, 2])
    stats['negative_controls'] = 4
    return dict(stats, maximum_small_actual_integrality_gap=str(max_actual_gap),
                deterministic_trace_sha256=trace.hexdigest(),
                nonsaturation_example=dict(clique_order=4, centered_lp='5', half_spokes='6'))


def dense_matching(vertices, available):
    """Perfect matching when the induced minimum degree is >= half its order."""
    vertices = list(vertices)
    assert len(vertices) % 2 == 0
    edge = lambda u, v: (min(u, v), max(u, v))
    assert all(sum(edge(u, v) in available for v in vertices if v != u) >= len(vertices) // 2
               for u in vertices)
    unmatched, pairs = set(vertices), []
    while unmatched:
        pair = next(((u, v) for u, v in combinations(sorted(unmatched), 2)
                     if edge(u, v) in available), None)
        if pair is None:
            break
        u, v = pair
        pairs.append(edge(u, v))
        unmatched -= {u, v}
    while unmatched:
        u, v = sorted(unmatched)[:2]
        if edge(u, v) in available:
            pairs.append(edge(u, v))
        else:
            for j, (a, b) in enumerate(pairs):
                if edge(u, a) in available and edge(v, b) in available:
                    pairs[j:j + 1] = [edge(u, a), edge(v, b)]
                    break
                if edge(u, b) in available and edge(v, a) in available:
                    pairs[j:j + 1] = [edge(u, b), edge(v, a)]
                    break
            else:
                raise AssertionError('dense matching augmentation failed')
        unmatched -= {u, v}
    assert len(pairs) * 2 == len(vertices) and len({v for e in pairs for v in e}) == len(vertices)
    assert set(pairs) <= available
    return pairs


def large_witness():
    k = 280
    ss = [tuple(range(140)), tuple(range(70, 210)), tuple(range(140, 280))]
    mm = [34, 34, 34]
    assert local_saturation(k, ss, mm)
    unions = [len(set(a) | set(b)) for a, b in combinations(ss, 2)]
    assert unions == [210, 280, 210]
    available = set(combinations(range(k), 2))
    centered, center = [], k
    for s, m in zip(ss, mm):
        for _ in range(m):
            pairs = dense_matching(s, available)
            centered.extend((center, u, v) for u, v in pairs)
            available -= set(pairs)
            center += 1
    assert len(centered) == 7140
    packing = add_clique_triangles(k, centered)
    verify_packing(k, ss, mm, packing)
    weights = [sum(m for s, m in zip(ss, mm) if v in s) for v in range(k)]
    order = sorted(range(k), key=lambda v: (-weights[v], v))
    E = sum(weights)
    q = k * (k - 1) // 2
    prefix = [0]
    for v in order:
        prefix.append(prefix[-1] + weights[v])
    ell = min(range(k + 1), key=lambda ell: q - ell * (k - ell) + E - prefix[ell])
    opposite = set(order[:ell])
    cover = [e for e in combinations(range(k), 2) if (e[0] in opposite) == (e[1] in opposite)]
    offset = k
    for s, m in zip(ss, mm):
        cover.extend((v, c) for c in range(offset, offset + m) for v in s if v not in opposite)
        offset += m
    expected_cover = q - ell * (k - ell) + E - prefix[ell]
    assert len(cover) == len(set(cover)) == expected_cover
    assert 2 * len(packing) - len(cover) >= saturated_gap_bound(k, 3) == Q(3549, 44)
    canonical = '\n'.join(','.join(map(str, t)) for t in sorted(tuple(sorted(t)) for t in packing)) + '\n'
    return dict(clique_order=k, independent_vertices=sum(mm), neighborhood_sizes=list(map(len, ss)),
                multiplicities=mm, pairwise_union_sizes=unions, centered_triangles=len(centered),
                total_packing=len(packing), cut_cover=len(cover), cut_clique_side=ell,
                witnessed_integer_margin=2 * len(packing) - len(cover),
                theorem_rational_margin='3549/44', theorem_integer_margin=81,
                packing_sha256=sha256(canonical.encode()).hexdigest())


def algebra_audit():
    cases = 0
    for r in range(21):
        for u in range(31):
            k = 80 * r + 40 + u
            expanded = (Q(u * u, 66) + (Q(4 * r, 3) + Q(47, 66)) * u
                        + Q(16 * r * r, 3) + Q(28 * r, 3) + Q(205, 44))
            assert saturated_gap_bound(k, r) == expanded > 0
            cases += 1
    # Check the square-completion identity on rational data.
    for k in (2, 3, 5, 17, 280):
        for r in range(6):
            for j in range(41):
                t = Q(j, 40)
                raw = k * k * (Q(1, 12) - t / 2 + Q(11, 12) * t * t) - 4 * r * k * t
                low = Q(k * k, 66) - Q(12 * r * k, 11) - Q(48 * r * r, 11)
                square = Q(11 * k * k, 12) * (t - Q(3, 11) - Q(24 * r, 11 * k)) ** 2
                assert raw - low == square
                cases += 1
    return dict(exact_identity_cases=cases)


def sharpness_audit():
    cases = 0
    for k in range(3, 64, 2):
        es = list(combinations(range(k), 2))
        colors = {e: sum(e) % k for e in es}
        verify_coloring(k, es, colors)
        assert set(Counter(colors.values()).values()) == {(k - 1) // 2}
        packing = [(k + c, u, v) for (u, v), c in colors.items() if c < k - 1]
        verify_packing(k, [tuple(range(k))], [k - 1], packing)
        assert len(packing) == (k - 1) * ((k - 1) // 2)
        assert Q(len(es)) - len(packing) == Q(k - 1, 2)
        cases += 1
    return dict(odd_complete_split_controls=cases, largest_clique=63,
                exact_centered_gap='(k-1)/2; one type, m=k-1, odd k')


if __name__ == '__main__':
    output = dict(status='PASS', evidence='supplementary exact audit; universal proof in PROOF.md',
                  coloring=coloring_audit(), lp_rounding=lp_audit(),
                  algebra=algebra_audit(), sharpness=sharpness_audit(),
                  large_witness=large_witness())
    print(json.dumps(output, indent=2, sort_keys=True))
