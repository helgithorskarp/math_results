"""Independent literal-AP audit of the complete streaming one-parent color screen.

Imports no producer. Reverse loops fill canonical arrays at physical positions.
All eligible original vectors are replayed; cache eviction never drops a phase.
"""
import hashlib
import json
from pathlib import Path
import struct
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def independent_case(color):
    initial = [x for x in range(2520)
               if x % 8 != 0 and x % 9 != 0 and x % 10 != 1
               and x % 14 != 1 and x % 12 != 10]
    points = [x for x in initial if x % 8 != 4 or x % 3 != color]
    required = sum(1 << x for x in points)
    labels = [n for n in range(8, 2521)
              if 2520 % n == 0 and n not in (8, 9, 10, 12, 14)]
    M = {n: [sum(1 << x for x in range(a, 2520, n)) & required
             for a in range(n)] for n in labels}
    capacities = [[n, max(mask.bit_count() for mask in M[n])] for n in labels]
    F = (15, 24, 36, 72)
    E = (18, 20, 28)
    outside = sum(c for n, c in capacities if n not in F)
    threshold = len(points) - outside
    raw = bytearray(2 * 933120)
    accepted = []
    maximum, witness, visited = -1, None, 0
    histogram = {}
    for d in range(71, -1, -1):
        for c in range(35, -1, -1):
            CD = M[72][d] | M[36][c]
            for b in range(23, -1, -1):
                BCD = CD | M[24][b]
                for a in range(14, -1, -1):
                    U = BCD | M[15][a]
                    gain = U.bit_count()
                    index = ((a * 24 + b) * 36 + c) * 72 + d
                    struct.pack_into('<H', raw, 2 * index, gain)
                    visited += 1
                    histogram[gain] = histogram.get(gain, 0) + 1
                    phase = [a, b, c, d]
                    if gain > maximum or (gain == maximum and phase < witness):
                        maximum, witness = gain, phase
                    if gain >= threshold:
                        accepted.append((phase, U))
    accepted.sort(key=lambda pair: pair[0])
    require(visited == 933120 and sum(histogram.values()) == visited,
            'Incomplete independent original core enumeration')
    require(sum(any(x % n == a for n, a in zip(F, witness)) for x in points)
            == maximum, 'Literal original four-phase witness')
    # Independently verify every per-original capacity by direct remainder buckets.
    for n, capacity in capacities:
        buckets = [0] * n
        for x in points:
            buckets[x % n] += 1
        require(max(buckets) == capacity, 'Literal individual capacity')
    record = {'color': color, 'initial_points': len(initial),
              'required_points': len(points), 'base_capacities': capacities,
              'all_individual_capacity': sum(c for n, c in capacities),
              'outside_core_capacity': outside, 'necessary_core_threshold': threshold,
              'all_original_core_vectors': visited, 'maximum_core_union': maximum,
              'core_maximizer': witness, 'retained_core_vectors': len(accepted),
              'all_core_gains_sha256': hashlib.sha256(raw).hexdigest(),
              'core_gain_histogram': sorted(histogram.items()),
              'four_resource_total_capacity': maximum + outside,
              'four_resource_screen_excludes': maximum + outside < len(points),
              'conditional_seven_resource_screen_run': False,
              'BASE_or_cover_realization_claimed': False}
    if accepted:
        require(len(accepted) <= 300, 'Existing retained-core storage cap')
        other29 = sum(c for n, c in capacities if n not in F + E)
        threshold7 = len(points) - other29
        joint = bytearray(2 * len(accepted) * 10080)
        best7, witness7, count7, near_count = -1, None, 0, 0
        for slot in range(len(accepted) - 1, -1, -1):
            phase, U = accepted[slot]
            for g in range(27, -1, -1):
                UG = U | M[28][g]
                for f in range(19, -1, -1):
                    UGF = UG | M[20][f]
                    for e in range(17, -1, -1):
                        actual = UGF | M[18][e]
                        gain = actual.bit_count()
                        index = slot * 10080 + (e * 20 + f) * 28 + g
                        struct.pack_into('<H', joint, 2 * index, gain)
                        count7 += 1
                        phases = phase + [e, f, g]
                        if gain > best7 or (gain == best7 and phases < witness7):
                            best7, witness7 = gain, phases
                        if gain >= threshold7:
                            near_count += 1
        require(count7 == len(accepted) * 10080, 'Incomplete independent joint enumeration')
        require(sum(any(x % n == a for n, a in zip(F + E, witness7)) for x in points)
                == best7, 'Literal original seven-phase witness')
        # Scan the independently filled gain array in canonical index order.
        # All marginal masks are recomputed at physical positions; the producer
        # uses compressed positions and memoizes capacity tuples instead.
        digest = hashlib.sha256()
        seen = {}
        hits = misses = peak = processed = 0
        worst = None
        remaining_labels = [n for n in labels if n not in F + E]
        for index in range(count7):
            gain = struct.unpack_from('<H', joint, 2 * index)[0]
            if gain < threshold7:
                continue
            slot, suffix = divmod(index, 10080)
            e, suffix = divmod(suffix, 560)
            f, g = divmod(suffix, 28)
            phase, old_union = accepted[slot]
            union = old_union | M[18][e] | M[20][f] | M[28][g]
            require(union.bit_count() == gain and union & ~required == 0,
                    'Canonical physical-union reconstruction')
            leftover = required ^ union
            marginal = tuple(max((mask & leftover).bit_count() for mask in M[n])
                             for n in remaining_labels)
            total = gain + sum(marginal)
            phases = phase + [e, f, g]
            digest.update(struct.pack('<38H', *phases, gain, *marginal, total))
            processed += 1
            if union in seen:
                hits += 1
            else:
                misses += 1
                if len(seen) == 300:
                    del seen[next(iter(seen))]
                seen[union] = True
                peak = max(peak, len(seen))
            if worst is None or total > worst['total_capacity']:
                worst = {'phases': phases, 'union_gain': gain,
                         'conditional_capacities': list(zip(remaining_labels, marginal)),
                         'total_capacity': total, 'strict_deficit': len(points) - total}
        require(processed == near_count and hits + misses == processed and peak <= 300,
                'Complete streaming vector/cache count')
        if worst:
            # Direct remainder buckets check EVERY marginal capacity at the
            # displayed worst vector, independently of all bitmask arithmetic.
            leftovers = [x for x in points if all(x % n != a
                         for n, a in zip(F + E, worst['phases']))]
            for n, capacity in worst['conditional_capacities']:
                bucket = [0] * n
                for x in leftovers:
                    bucket[x % n] += 1
                require(max(bucket) == capacity, 'Literal conditional capacity')
        record.update({'conditional_seven_resource_screen_run': True,
                       'conditional_seven_original_vectors': count7,
                       'conditional_seven_maximum': best7,
                       'conditional_seven_maximizer': witness7,
                       'all_conditional_seven_gains_sha256': hashlib.sha256(joint).hexdigest(),
                       'outside_seven_capacity': other29,
                       'conditional_total_capacity': best7 + other29,
                       'strict_conditional_deficit': len(points) - best7 - other29,
                       'conditional_screen_excludes': best7 + other29 < len(points),
                       'necessary_seven_threshold': threshold7,
                       'near_maximum_seven_vectors': near_count,
                       'streaming_marginal_complete': True,
                       'streaming_marginal_original_vectors': processed,
                       'streaming_marginal_cache_cap': 300,
                       'streaming_marginal_peak_cache_entries': peak,
                       'streaming_marginal_cache_hits': hits,
                       'streaming_marginal_cache_misses': misses,
                       'all_streaming_marginal_rows_sha256': digest.hexdigest(),
                       'worst_marginal_record': worst,
                       'streaming_marginal_max_total': worst['total_capacity'] if worst else None,
                       'streaming_marginal_min_deficit': worst['strict_deficit'] if worst else None,
                       'streaming_marginal_screen_excludes': bool(worst and worst['strict_deficit'] > 0)})
    return record


def validate_frame(candidate):
    require(set(candidate) == {'agent', 'role', 'scope', 'prefix', 'core', 'extra', 'base', 'cases'},
            'Incomplete or extra certificate fields')
    require(candidate['agent'] == 'six-covering-3' and candidate['role'] == 'researcher'
            and candidate['scope'] == 'Two literal P/BASE one-parent color cases; no all-P/A4 exclusion',
            'Wrong authorship or certificate scope')
    inventory = [n for n in range(8, 2521)
                 if 2520 % n == 0 and n not in (8, 9, 10, 12, 14)]
    require(candidate['prefix'] == [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]],
            'Wrong literal P')
    require(candidate['base'] == inventory and candidate['core'] == [15, 24, 36, 72]
            and candidate['extra'] == [18, 20, 28], 'Wrong original-resource inventory')
    require([c['color'] for c in candidate['cases']] == [1, 2], 'Complete two-color frame')


def compare(candidate, records):
    validate_frame(candidate)
    require(records == candidate['cases'], 'Full independent record mismatch')


def controls(candidate, records):
    """Damage actual input/certificate fields after one complete independent replay."""
    damages = []

    def damage(name, change):
        bad = json.loads(json.dumps(candidate))
        change(bad)
        try:
            compare(bad, records)
        except (ValueError, KeyError, TypeError):
            damages.append(name)
        else:
            raise ValueError('Accepted damaged actual certificate: ' + name)

    damage('wrong_prefix_phase', lambda x: x['prefix'][4].__setitem__(1, 2))
    damage('missing_original_base', lambda x: x['base'].pop())
    damage('duplicate_original_base', lambda x: x['base'].__setitem__(1, 15))
    damage('wrong_original_core', lambda x: x['core'].__setitem__(0, 30))
    damage('wrong_original_extra', lambda x: x['extra'].__setitem__(2, 56))
    damage('missing_color_case', lambda x: x['cases'].pop())
    damage('wrong_required_set_size', lambda x: x['cases'][0].__setitem__('required_points', 1294))
    damage('wrong_four_resource_threshold', lambda x: x['cases'][0].__setitem__('necessary_core_threshold', 315))
    damage('wrong_seven_resource_threshold', lambda x: x['cases'][0].__setitem__('necessary_seven_threshold', 580))
    damage('dropped_core_vector', lambda x: x['cases'][0].__setitem__('retained_core_vectors', 239))
    damage('dropped_seven_vector', lambda x: x['cases'][0].__setitem__('conditional_seven_original_vectors', 2419199))
    damage('dropped_marginal_vector', lambda x: x['cases'][0].__setitem__('streaming_marginal_original_vectors', 863))
    damage('incomplete_stream', lambda x: x['cases'][0].__setitem__('streaming_marginal_complete', False))
    damage('wrong_conditional_maximum', lambda x: x['cases'][0].__setitem__('streaming_marginal_max_total', 1191))
    damage('wrong_original_worst_phase', lambda x: x['cases'][0]['worst_marginal_record']['phases'].__setitem__(0, 3))
    damage('wrong_worst_marginal', lambda x: x['cases'][0]['worst_marginal_record']['conditional_capacities'][0].__setitem__(1, 55))
    damage('wrong_all_core_digest', lambda x: x['cases'][1].__setitem__('all_core_gains_sha256', '0' * 64))
    damage('wrong_all_joint_digest', lambda x: x['cases'][0].__setitem__('all_conditional_seven_gains_sha256', '0' * 64))
    damage('wrong_all_marginal_digest', lambda x: x['cases'][0].__setitem__('all_streaming_marginal_rows_sha256', '0' * 64))
    damage('unconditional103_field', lambda x: x.__setitem__('unconditional103_hole_bound', True))
    return damages


def audit(path, run_controls=False):
    candidate = json.loads(Path(path).read_text())
    validate_frame(candidate)
    records = [independent_case(color) for color in (1, 2)]
    records = json.loads(json.dumps(records))
    compare(candidate, records)
    require(records[1]['all_individual_capacity'] == 1283
            and records[1]['required_points'] == 1293,
            'Color2 elementary deficit not verified')
    require(records[0]['conditional_total_capacity'] == 1295
            and records[0]['streaming_marginal_max_total'] == 1190
            and records[0]['streaming_marginal_original_vectors'] == 864
            and records[0]['streaming_marginal_complete'],
            'Complete color1 marginal frontier differs')
    return {'agent': 'six-covering-3', 'role': 'researcher',
            'complete_individual_core_and_joint_screens': True,
            'all_original_core_vectors': sum(r['all_original_core_vectors'] for r in records),
            'all_conditional_seven_vectors': records[0]['conditional_seven_original_vectors'],
            'all_original_individual_phase_capacities_remainder_checked': True,
            'color2_one_parent_BASE_slice_excluded': True,
            'color1_one_parent_BASE_slice_excluded': True,
            'color1_marginal_frontier_complete': True,
            'all_streaming_marginal_vectors': records[0]['streaming_marginal_original_vectors'],
            'all_streaming_marginal_rows_sha256': records[0]['all_streaming_marginal_rows_sha256'],
            'conditional_marginal_max_total': records[0]['streaming_marginal_max_total'],
            'conditional_marginal_deficit': records[0]['streaming_marginal_min_deficit'],
            'unconditional103_hole_bound_claimed': False,
            'full_records_sha256': hashlib.sha256(json.dumps(records, sort_keys=True,
                                         separators=(',', ':')).encode()).hexdigest(),
            'same_author_independent_algorithm': True,
            'independent_external_review': False,
            'formalization': False,
            'certificate_damage_controls': controls(candidate, records) if run_controls else []}


if __name__ == '__main__':
    arguments = sys.argv[1:]
    run_controls = '--controls' in arguments
    if run_controls:
        arguments.remove('--controls')
    require(len(arguments) <= 1 and not any(a.startswith('--') for a in arguments),
            'Usage: audit.py [expected.json] [--controls]')
    path = arguments[0] if arguments else Path(__file__).with_name('expected.json')
    print(json.dumps(audit(path, run_controls), sort_keys=True))
