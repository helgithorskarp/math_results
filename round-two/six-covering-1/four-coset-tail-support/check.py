"""Complete exact seven-resource profiles; standard-library Python only."""
from argparse import ArgumentParser
from itertools import combinations_with_replacement
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def partitions(prefix=(0,), high=0):
    if len(prefix) == 7:
        yield prefix
        return
    for copy in range(min(high + 1, 4) + 1):
        yield from partitions(prefix + (copy,), max(high, copy))


def profile(mask_by_copy, full):
    one = two = four = 0
    for mask in mask_by_copy:
        carry1 = one & mask
        one ^= mask
        carry2 = two & carry1
        two ^= carry1
        four ^= carry2
    return tuple(((one if k & 1 else full ^ one) &
                  (two if k & 2 else full ^ two) &
                  (four if k & 4 else full ^ four)).bit_count() for k in range(6))


def best_score(histogram, size):
    left, score = size, 0
    for multiplicity in range(5, -1, -1):
        take = min(left, histogram[multiplicity])
        left -= take
        score += take * multiplicity
    need(left == 0, 'hole count exceeds the actual candidate target')
    return score


def compute():
    from math import gcd
    S = [t for t in range(180) if t % 9 != 6]
    full = sum(1 << t for t in S)
    need(len(S) == 160, 'wrong literal target')
    free = [d for d in range(2, 721) if 720 % d == 0 and d not in (2, 4)]
    capacities = []
    for d in free:
        e = d // gcd(d, 4)
        counts = [sum(t % e == r for t in S) for r in range(e)]
        capacities.append({'cofactor': d, 'effective_modulus': e, 'capacity': max(counts)})
    seven = (8, 3, 6, 12, 5, 10, 20)
    mass = sum(row['capacity'] for row in capacities)
    other_mass = sum(row['capacity'] for row in capacities if row['cofactor'] not in seven)
    masks = {(e, r): sum(1 << t for t in S if t % e == r)
             for e in (2, 3, 5) for r in range(e)}
    allocations = tuple(partitions())
    need(len(allocations) == 855 and len(set(allocations)) == 855,
         'copy allocation domain is incomplete/repeated')
    histograms, phase_count, case_count = {}, 0, 0
    for b in range(2):
        for A in combinations_with_replacement(range(3), 3):
            for C in combinations_with_replacement(range(5), 3):
                phase_count += 1
                phase_masks = [masks[2, b]] + [masks[3, a] for a in A] + [masks[5, c] for c in C]
                for allocation in allocations:
                    unions = [0] * 5
                    for copy, mask in zip(allocation, phase_masks):
                        unions[copy] |= mask
                    histogram = profile(unions, full)
                    need(sum(histogram) == len(S), 'profile loses candidate points')
                    if histogram not in histograms:
                        histograms[histogram] = {'B': b, 'A': list(A), 'C': list(C),
                                                  'copies': list(allocation)}
                    case_count += 1
    scores, witnesses = [], []
    for size in range(115, 121):
        histogram = max(histograms, key=lambda h: best_score(h, size))
        score = best_score(histogram, size)
        scores.append({'holes': size, 'maximum_hits': score})
        witnesses.append({'holes': size, 'histogram': list(histogram), **histograms[histogram]})
    result = {'candidate_target_size': len(S), 'free_resource_mass': mass,
              'other_twenty_resource_mass': other_mass,
              'canonical_phase_multisets': phase_count, 'canonical_copy_partitions': len(allocations),
              'phase_partition_cases': case_count, 'necessary_hole_upper_bound': 115,
              'selected_seven_top_scores': scores,
              'resource_capacities': capacities,
              'distinct_multiplicity_histograms': len(histograms), 'profile_maximizers': witnesses,
              'tail_completion_asserted': False, 'global_L_min_8_bound_changed': False}
    need(mass == 600 and other_mass == 244, 'resource capacity inventory differs')
    for row in scores[1:]:
        need(row['maximum_hits'] + other_mass < 5 * row['holes'], 'claimed strict upper cap fails')
    return result


def validate(result, expected):
    for key, value in expected.items():
        need(key in result and result[key] == value, 'frozen expected field differs: ' + key)


def main():
    parser = ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    expected = json.loads((HERE / 'expected.json').read_text())
    result = compute()
    validate(result, expected)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('resource_capacities', 'profile_maximizers')}))


if __name__ == '__main__':
    main()
