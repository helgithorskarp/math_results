"""Exact streaming screens for two one-parent monochromatic BASE routes.

No inferred feasibility, no phase normalization, no solver. Optional complete
seven-resource and conditioned-marginal screens use fixed bounded storage.
All eligible original seven-phase vectors are processed, even on cache eviction.
"""
from hashlib import sha256
from itertools import product
import json
import struct
import sys

P = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
BASE = tuple(n for n in range(8, 2521) if 2520 % n == 0
             and n not in {m for m, a in P})
CORE = (15, 24, 36, 72)
EXTRA = (18, 20, 28)


def case(color, joint=False):
    initial = [x for x in range(2520) if all(x % n != a for n, a in P)]
    required = [x for x in initial if not (x % 8 == 4 and x % 3 == color)]
    masks = {}
    caps = []
    for n in BASE:
        buckets = [0] * n
        for j, x in enumerate(required):
            buckets[x % n] |= 1 << j
        masks[n] = buckets
        caps.append([n, max(b.bit_count() for b in buckets)])
    outside = sum(c for n, c in caps if n not in CORE)
    threshold = len(required) - outside
    left = [(a, b, masks[15][a] | masks[24][b])
            for a, b in product(range(15), range(24))]
    right = [(c, d, masks[36][c] | masks[72][d])
             for c, d in product(range(36), range(72))]
    count = retained = 0
    maximum = -1
    witness = None
    retained_rows = []
    histogram = {}
    digest = sha256()
    for a, b, L in left:
        for c, d, R in right:
            gain = (L | R).bit_count()
            digest.update(struct.pack('<H', gain))
            count += 1
            histogram[gain] = histogram.get(gain, 0) + 1
            if gain > maximum:
                maximum, witness = gain, [a, b, c, d]
            if gain >= threshold:
                retained += 1
                if joint:
                    retained_rows.append(([a, b, c, d], L | R))
    if count != 933120 or sum(histogram.values()) != count:
        raise ValueError('Incomplete original core phase enumeration')
    direct = sum(any(x % n == a for n, a in zip(CORE, witness)) for x in required)
    if direct != maximum:
        raise ValueError('Literal original-phase maximizing witness differs')
    record = {'color': color, 'initial_points': len(initial),
            'required_points': len(required), 'base_capacities': caps,
            'all_individual_capacity': sum(c for n, c in caps),
            'outside_core_capacity': outside, 'necessary_core_threshold': threshold,
            'all_original_core_vectors': count, 'maximum_core_union': maximum,
            'core_maximizer': witness, 'retained_core_vectors': retained,
            'all_core_gains_sha256': digest.hexdigest(),
            'core_gain_histogram': sorted(histogram.items()),
            'four_resource_total_capacity': maximum + outside,
            'four_resource_screen_excludes': maximum + outside < len(required),
            'conditional_seven_resource_screen_run': False,
            'BASE_or_cover_realization_claimed': False}
    if joint and retained:
        if retained > 300:
            raise RuntimeError('Existing bounded joint plan exceeded: no exclusion')
        added = [(e, f, g, masks[18][e] | masks[20][f] | masks[28][g])
                 for e, f, g in product(range(18), range(20), range(28))]
        joint_digest = sha256()
        joint_max = -1
        joint_witness = None
        joint_count = 0
        other29 = sum(c for n, c in caps if n not in CORE + EXTRA)
        threshold7 = len(required) - other29
        cache = {}
        cache_hits = cache_misses = peak_cache = 0
        top7_count = 0
        marginal_digest = sha256()
        worst = None
        outside_labels = [n for n in BASE if n not in CORE + EXTRA]
        for phases, union in retained_rows:
            for e, f, g, more in added:
                actual_union = union | more
                gain = actual_union.bit_count()
                joint_digest.update(struct.pack('<H', gain))
                joint_count += 1
                if gain > joint_max:
                    joint_max, joint_witness = gain, phases + [e, f, g]
                if gain >= threshold7:
                    top7_count += 1
                    if actual_union in cache:
                        marginal = cache[actual_union]
                        cache_hits += 1
                    else:
                        marginal = tuple(max((mask & ~actual_union).bit_count()
                                             for mask in masks[n])
                                         for n in outside_labels)
                        cache_misses += 1
                        if len(cache) == 300:
                            del cache[next(iter(cache))]
                        cache[actual_union] = marginal
                        peak_cache = max(peak_cache, len(cache))
                    total = gain + sum(marginal)
                    phase7 = phases + [e, f, g]
                    marginal_digest.update(struct.pack('<38H', *phase7, gain,
                                                        *marginal, total))
                    if worst is None or total > worst['total_capacity']:
                        worst = {'phases': phase7, 'union_gain': gain,
                                 'conditional_capacities': list(zip(outside_labels, marginal)),
                                 'total_capacity': total,
                                 'strict_deficit': len(required) - total}
        if joint_count != retained * 10080:
            raise ValueError('Incomplete original seven-resource conditional screen')
        direct7 = sum(any(x % n == a for n, a in zip(CORE + EXTRA, joint_witness))
                      for x in required)
        if direct7 != joint_max:
            raise ValueError('Literal original seven-phase witness differs')
        record.update({'conditional_seven_resource_screen_run': True,
                       'conditional_seven_original_vectors': joint_count,
                       'conditional_seven_maximum': joint_max,
                       'conditional_seven_maximizer': joint_witness,
                       'all_conditional_seven_gains_sha256': joint_digest.hexdigest(),
                       'outside_seven_capacity': other29,
                       'conditional_total_capacity': joint_max + other29,
                       'strict_conditional_deficit': len(required) - joint_max - other29,
                       'conditional_screen_excludes': joint_max + other29 < len(required),
                       'necessary_seven_threshold': threshold7,
                       'near_maximum_seven_vectors': top7_count,
                       'streaming_marginal_complete': True,
                       'streaming_marginal_original_vectors': top7_count,
                       'streaming_marginal_cache_cap': 300,
                       'streaming_marginal_peak_cache_entries': peak_cache,
                       'streaming_marginal_cache_hits': cache_hits,
                       'streaming_marginal_cache_misses': cache_misses,
                       'all_streaming_marginal_rows_sha256': marginal_digest.hexdigest(),
                       'worst_marginal_record': worst,
                       'streaming_marginal_max_total': worst['total_capacity'] if worst else None,
                       'streaming_marginal_min_deficit': worst['strict_deficit'] if worst else None,
                       'streaming_marginal_screen_excludes': bool(worst and worst['strict_deficit'] > 0)})
        if cache_hits + cache_misses != top7_count or peak_cache > 300:
            raise ValueError('Streaming original-phase count/cache invariant')
    return record


if __name__ == '__main__':
    if sys.argv[1:] not in ([], ['--joint']):
        raise ValueError('Only optional --joint is supported')
    print(json.dumps({'agent': 'six-covering-3', 'role': 'researcher',
                      'scope': 'Two literal P/BASE one-parent color cases; no all-P/A4 exclusion',
                      'prefix': P, 'core': CORE, 'extra': EXTRA, 'base': BASE,
                      'cases': [case(c, joint=bool(sys.argv[1:])) for c in (1, 2)]}, sort_keys=True))
