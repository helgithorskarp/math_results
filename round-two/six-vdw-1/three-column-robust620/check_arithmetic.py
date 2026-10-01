"""Exact coordinate/repetition arithmetic for the stated conditional corollaries."""
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def run():
    frequencies = [0]*620
    for x in range(3704):
        frequencies[x % 620] += 1
    require(frequencies == [6]*604+[5]*16, 'interval repetition counts')
    by_field = {r: [] for r in range(31)}
    for lower in range(310):
        upper = lower+310
        require(lower % 31 == upper % 31 and (upper-lower) % 20 == 10, 'antipodal CRT pair')
        require(frequencies[lower]+frequencies[upper] >= 11, 'paired interval mismatch cost')
        by_field[lower % 31].append((lower, upper))
    require(all(len(pairs) == 10 for pairs in by_field.values()), 'field-column pair count')
    minima = [min(frequencies[a]+frequencies[b] for a, b in pairs) for pairs in by_field.values()]
    require(sum(sorted(minima)[:4]) == 44, 'four distinct fields mismatch floor')
    for s in range(10):
        disjoint = set()
        for r in range(31):
            actual = [x for x in range(620) if x % 31 == r and x % 20 in [s, s+10]]
            require(len(actual) == 2 and (actual[1]-actual[0]) == 310, 'nonanti baseline equal-pair support')
            require(not disjoint.intersection(actual), 'overlapping field pairs')
            disjoint.update(actual)
        require(len(disjoint) == 62, '31 disjoint equal baseline pairs')
    result = {'status': 'COMPLETE_CRT_REPETITION_AND_CONDITIONAL_DISTANCE_ARITHMETIC',
              'period': 620, 'target_N': 3704, 'antipodal_pairs': 310,
              'minimum_changed_fields_if_valid': 4, 'period_bit_floor_if_valid': 8,
              'periodic_target_edit_floor_if_valid': 44,
              'nonanti_baseline_period_floor': 31, 'nonanti_baseline_target_floor': 155,
              'minimum_pair_repetition_cost': 11,
              'premise': 'The new outside-three-field-residues theorem, plus step310 antipodality of a valid period620 word. No existence or sharpness claim.'}
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    run()
