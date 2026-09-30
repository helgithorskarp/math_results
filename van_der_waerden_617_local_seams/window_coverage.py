#!/usr/bin/env python3
"""Exact phase-rectangle coverage, ordered by balanced window radius."""
import argparse
import json
import time

P = 617
K = 7


def run(maximum):
    start = time.monotonic()
    squares = {x*x % P for x in range(1, P)}
    q = [-1] + [0 if x in squares else 1 for x in range(1, P)]
    phase_masks = [[sum(1 << s for s in range(P) if q[(x+s) % P] == b)
                    for x in range(P)] for b in (0, 1)]
    full_phase = (1 << P) - 1
    full_pairs = (1 << (2*P)) - 1
    rows = [0] * P
    progressions = []
    for d in range(1, (2*maximum-1)//6+1):
        for a in range(max(P-maximum, P-6*d), min(P, P+maximum-6*d)):
            radius = max(P-a, a+6*d-P+1)
            progressions.append((radius, d, a))
    progressions.sort()
    histogram = {}
    survivor_lists = {}
    tested = 0
    last_radius = 0
    covered = 0
    for radius, d, a in progressions:
        if radius != last_radius:
            if last_radius:
                remaining = 2*P*P - covered
                if remaining < 1000:
                    survivors = []
                    for s, row in enumerate(rows):
                        bits = full_pairs ^ row ^ (1 << s)
                        while bits:
                            bit = bits & -bits; bits ^= bit
                            index = bit.bit_length()-1
                            survivors.append([s, index % P, index // P])
                    survivor_lists[str(last_radius)] = survivors
            last_radius = radius
        tested += 1
        points = [a+j*d for j in range(K)]
        left = [x for x in points if x < P]
        right = [x-P for x in points if x >= P]
        for b in (0, 1):
            lm = full_phase
            for x in left: lm &= phase_masks[b][x]
            rm = [full_phase, full_phase]
            for x in right:
                rm[0] &= phase_masks[b][x]
                rm[1] &= phase_masks[1-b][x]
            rectangle = rm[0] | (rm[1] << P)
            while lm:
                bit = lm & -lm; lm ^= bit
                s = bit.bit_length()-1
                new = rectangle & (full_pairs ^ rows[s])
                count = new.bit_count()
                if count:
                    histogram[str(radius)] = histogram.get(str(radius), 0) + count
                    covered += count
                    rows[s] |= new
        if covered == P*(2*P-1):
            assert all((full_pairs ^ row) == 1 << s for s, row in enumerate(rows))
            threshold = radius
            break
    else:
        threshold = None
    return {
        'maximum_radius': maximum,
        'crossing_ap_candidates': len(progressions),
        'crossing_aps_processed': tested,
        'normalized_cases': 2*P*P,
        'incompatible_cases': P*(2*P-1),
        'covered_incompatible_cases': covered,
        'least_uniform_pole_free_radius': threshold,
        'first_obstruction_radius_histogram': histogram,
        'near_threshold_survivors': survivor_lists,
        'seconds': time.monotonic()-start,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--maximum', type=int, default=105)
    args = parser.parse_args()
    if not 1 <= args.maximum <= P:
        parser.error('radius must be in [1,617]')
    print(json.dumps(run(args.maximum), indent=2))
