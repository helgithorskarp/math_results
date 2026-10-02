"""Certificate/stream damages, definition-level rows, and lift/TAIL controls."""
from copy import deepcopy
from math import gcd
from pathlib import Path
import argparse
import json

from check import run, validate


def require(condition, message):
    if not condition:
        raise ValueError(message)


def audit(scratch):
    c = json.loads(Path(__file__).with_name('certificate.json').read_text())
    rejected = []

    def reject(name, change, checker):
        bad = deepcopy(c)
        change(bad)
        try:
            checker(bad)
        except (ValueError, KeyError, TypeError, IndexError):
            rejected.append(name)
        else:
            raise ValueError('Damage admitted: ' + name)

    structural = {
        'wrong_period': lambda b: b.update(period=10080),
        'different_H_fourteen': lambda b: b['prefix'][3].__setitem__(1, 0),
        'wrong_literal_twelve': lambda b: b['prefix'][-1].__setitem__(1, 3),
        'omitted_twelve': lambda b: b['prefix'].pop(),
        'boolean_original_phase': lambda b: b['prefix'][2].__setitem__(1, True),
        'missing_original21': lambda b: b['original_base_labels'].remove(21),
        'duplicate_original15': lambda b: b['original_base_labels'].__setitem__(1, 15),
        'aliased_original16': lambda b: b['original_base_labels'].__setitem__(0, 16),
        'pooled_original18_singleton3': lambda b: b['pair_phase_domains'][1].remove(3),
        'pooled_original18_singleton12': lambda b: b['pair_phase_domains'][1].remove(12),
        'canonical_pairs_substituted': lambda b: b.update(records_per_parent=60),
        'raw_original15_phase14_missing': lambda b: b['pair_phase_domains'][0].pop(),
        'boolean_raw_phase': lambda b: b['pair_phase_domains'][0].__setitem__(1, True),
        'missing_parent7': lambda b: b['cases'].pop(),
        'duplicated_parent': lambda b: b['cases'][1].update(parent=1),
        'skipped_raw_pair': lambda b: b['cases'][0].update(records=269),
        'missing_remaining_original21': lambda b: b['remaining_originals'].remove(21),
        'wrong_phase_action_count': lambda b: b['cases'][0].update(remaining_phase_actions=9245),
        'inflated_deficit': lambda b: b['cases'][0].update(universal_outside_holes_at_least=3),
    }
    for name, change in structural.items():
        reject(name, change, validate)
    records = scratch / 'parent1-normal.records'
    numerical = {
        'wrong_all_record_hash': lambda b: b['cases'][0].update(all_rows38H_sha256='0' * 64),
        'wrong_required_point_hash': lambda b: b['cases'][0].update(required_points_sha256='0' * 64),
        'wrong_maximum_original20_marginal': lambda b: b['cases'][0]['maximum_row'].__setitem__(3, 0),
        'wrong_gain_range': lambda b: b['cases'][0]['union_gain_range'].__setitem__(
            0, b['cases'][0]['union_gain_range'][0] + 1),
    }
    for name, change in numerical.items():
        reject(name, change, lambda b: run(1, b, records))
    encoded = records.read_bytes()
    stream_damages = {
        'omitted_last_pair': encoded[:-76],
        'duplicated_last_pair': encoded + encoded[-76:],
        'reordered_first_pairs': encoded[76:152] + encoded[:76] + encoded[152:],
        'damaged_first_marginal': encoded[:6] + bytes([encoded[6] ^ 1]) + encoded[7:],
    }
    for name, data in stream_damages.items():
        damaged = scratch / ('damage-' + name + '.records')
        damaged.write_bytes(data)
        try:
            run(1, c, damaged)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Damaged raw stream admitted: ' + name)
    p = [(8, 0), (9, 0), (10, 1), (14, 1), (12, 10)]
    labels = [n for n in range(8, 2521)
              if 2520 % n == 0 and n not in (8, 9, 10, 12, 14)]
    literal_rows = []
    for parent, phases in [(1, [2, 6]), (2, [2, 3])]:
        R = {x for x in range(2520) if x % 8 != parent
             and all(x % n != a for n, a in p)}
        U = {x for x in R if x % 15 == phases[0] or x % 18 == phases[1]}
        residual = R - U
        marginal = [max(len(residual.intersection(range(a, 2520, n))) for a in range(n))
                    for n in labels if n not in (15, 18)]
        row = [*phases, len(U), *marginal, len(U) + sum(marginal)]
        case = next(v for v in c['cases'] if v['parent'] == parent)
        require(row == case['maximum_row'], 'Definition-level worst row differs')
        require(case['unconditioned_upper'] >= len(R), 'Unconditioned control would exclude')
        literal_rows.append(dict(parent=parent, gain=len(U), remaining_sum=sum(marginal),
                                 bound=row[-1], deficit=len(R) - row[-1]))
    # A genuine full distinct period12 cover. Actual completion must survive
    # every ordinary marginal bound, including the empty/final prefixes.
    toy = [(2, 0), (3, 0), (4, 1), (6, 5), (12, 7)]
    require(all(any(x % n == a for n, a in toy) for x in range(12)), 'Toy is not a cover')
    toy_bounds = []
    covered = set()
    for j in range(len(toy) + 1):
        if j:
            n, a = toy[j - 1]
            covered.update(range(a, 12, n))
        residual = set(range(12)) - covered
        bound = len(covered) + sum(max(len(residual.intersection(range(a, 12, n)))
                                      for a in range(n)) for n, _ in toy[j:])
        require(bound >= 12, 'Bound discarded an actual completion')
        toy_bounds.append(bound)
    eligible = {n for n in range(8, 10081) if 10080 % n == 0}
    base = {n for n in range(8, 2521) if 2520 % n == 0}
    tail = {multiple * d for multiple in (16, 32) for d in range(1, 316) if 315 % d == 0}
    require(len(eligible) == 65 and len(base) == 41 and len(tail) == 24
            and base.isdisjoint(tail) and base | tail == eligible,
            'Original BASE/TAIL split is not exhaustive and disjoint')
    # Explain the repeated full-record hashes without using this symmetry
    # to discard any of the six independently enumerated parent domains.
    transports = []
    for e in (1, 3, 5, 7):
        candidates = [u for u in range(2520) if u % 315 == 1 and u % 8 == e]
        require(len(candidates) == 1 and gcd(candidates[0], 2520) == 1,
                'CRT multiplier is not a unique unit')
        u = candidates[0]
        require(u % 15 == 1 and u % 18 == 1, 'Selected original phases moved')
        require(all({u * x % 2520 for x in range(a, 2520, n)}
                    == set(range(a, 2520, n)) for n, a in p),
                'Literal prefix class moved')
        require(all(len({u * a % n for a in range(n)}) == n for n in labels),
                'Original phase action is not bijective')
        for r in (1, 2, 3, 4, 5, 6, 7):
            source = {x for x in range(2520) if x % 8 != r
                      and all(x % n != a for n, a in p)}
            target = {x for x in range(2520) if x % 8 != e * r % 8
                      and all(x % n != a for n, a in p)}
            require({u * x % 2520 for x in source} == target, 'Required set transport failed')
        transports.append([e, u])
    lifts = 0
    for n in labels:
        for a in range(n):
            lifted = {x + j * 2520 for x in range(a, 2520, n) for j in range(4)}
            literal = set(range(a, 10080, n))
            require(lifted == literal, 'Four-lift BASE AP identity failed')
            lifts += len(literal)
    tail_points = 0
    for n in tail:
        require(n % 8 == 0, 'TAIL crosses parents')
        for a in range(n):
            for x in range(a, 10080, n):
                require(x % 8 == a % 8, 'Literal TAIL AP has another parent')
                tail_points += 1
    return dict(agent='six-covering-3', role='researcher', rejected_controls=rejected,
                controls=len(rejected), definition_level_maximum_rows=literal_rows,
                toy_full_distinct_cover=True, toy_prefix_upper_bounds=toy_bounds,
                original_BASE_TAIL_partition=[41, 24, 65],
                CRT_multipliers=transports, parent_orbits=[[0], [1, 3, 5, 7], [2, 6], [4]],
                all_original_BASE_AP_lift_points=lifts,
                all_original_TAIL_AP_parent_points=tail_points,
                other_parent4_dependency_audit_still_required=True,
                external_review_claimed=False, native_solver=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.scratch), sort_keys=True))
