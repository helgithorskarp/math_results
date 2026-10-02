"""Scope/schema damages, exact worst-row control, and a genuine toy cover.

The numerical stage1 damages rerun the complete AP checker. Structural
damages test its frame validator; these do not replace the four-stage audit.
"""
from copy import deepcopy
from pathlib import Path
import json

from affine import normalizer, normalize
from check_stage import run, validate


def require(condition, message):
    if not condition:
        raise ValueError(message)


def audit():
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

    frame_changes = {
        'wrong_period': lambda b: b.update(period=10080),
        'wrong_literal_twelve': lambda b: b['prefix'][-1].__setitem__(1, 3),
        'missing_twelve': lambda b: b['prefix'].pop(),
        'wrong_parent': lambda b: b.update(parent=2),
        'missing_original21': lambda b: b['original_base_labels'].remove(21),
        'duplicate_original15': lambda b: b['original_base_labels'].__setitem__(1, 15),
        'aliased_original16': lambda b: b['original_base_labels'].__setitem__(0, 16),
        'wrong_selected_original20': lambda b: b['fixed_order'].__setitem__(4, 28),
        'wrong_required1116': lambda b: b.update(required=1116),
        'pooled_original18_singleton3': lambda b: b['canonical18'].remove(3),
        'missing_stage': lambda b: b['stages'].pop(),
        'skipped_root_pair': lambda b: b['stages'][0].update(records=59),
        'skipped_original24_phase': lambda b: b['stages'][1].update(records=621),
        'dropped_retained_parent': lambda b: b['stages'][0]['retained_phase_vectors'].pop(),
        'wrong_actual_marginal_inventory': lambda b: b['stages'][3]['remaining_originals'].remove(21),
        'wrong_maximum_witness': lambda b: b['stages'][3]['maximum_row'].__setitem__(-1, 1117),
    }
    for name, change in frame_changes.items():
        reject(name, change, validate)
    numerical_changes = {
        'wrong_all_root_row_hash': lambda b: b['stages'][0].update(all_rows38H_sha256='0' * 64),
        'wrong_root_required_point_hash': lambda b: b['stages'][0].update(required_points_sha256='0' * 64),
        'wrong_root_union_gain': lambda b: b['stages'][0]['union_gain_range'].__setitem__(
            0, b['stages'][0]['union_gain_range'][0] + 1),
        'wrong_root_maximum_marginal': lambda b: b['stages'][0]['maximum_row'].__setitem__(3, 0),
    }
    for name, change in numerical_changes.items():
        reject(name, change, lambda b: run(1, b))
    p = [(8, 0), (9, 0), (10, 1), (14, 1), (12, 10)]
    labels = [n for n in range(8, 2521)
              if 2520 % n == 0 and n not in (8, 9, 10, 12, 14)]
    # Definition-level remainder counts; no bitmask and no producer import.
    R = {x for x in range(2520) if x % 8 != 4 and all(x % n != a for n, a in p)}
    caps = [max(sum(x in R for x in range(a, 2520, n)) for a in range(n))
            for n in labels]
    require(len(R) == 1118 and sum(caps) == 1256,
            'Unconditioned density control: it does not exclude this route')
    f, phases = [15, 18, 24, 36, 20], [2, 3, 2, 30, 3]
    U = {x for x in R if any(x % n == a for n, a in zip(f, phases))}
    rest = R - U
    marginal = [max(sum(x in rest for x in range(a, 2520, n)) for a in range(n))
                for n in labels if n not in f]
    row = [*phases, len(U), *marginal, len(U) + sum(marginal)]
    require(row == c['stages'][3]['maximum_row'] and len(U) == 448
            and sum(marginal) == 668, 'Literal final maximum-row control')
    # A genuine full distinct cover of the integers with period12. Every
    # partial-prefix marginal upper bound must retain its actual completion.
    toy = [(2, 0), (3, 0), (4, 1), (6, 5), (12, 7)]
    require(all(any(x % n == a for n, a in toy) for x in range(12)), 'Toy full cover')
    toy_bounds = []
    covered = set()
    for i in range(len(toy) + 1):
        if i:
            n, a = toy[i - 1]
            covered.update(range(a, 12, n))
        residual = set(range(12)) - covered
        bound = len(covered) + sum(max(sum(x in residual for x in range(a, 12, n))
                                      for a in range(n)) for n, _ in toy[i:])
        require(bound >= 12, 'Marginal screen discarded the actual toy full cover')
        toy_bounds.append(bound)
    bad_phases = [[n, 0] for n in labels]
    bad_phases[0][1] = 15
    try:
        normalize(bad_phases)
    except ValueError:
        rejected.append('out_of_domain_original15_normalization')
    else:
        raise ValueError('Normalizer accepted out-of-domain original phase')
    for a, b in ((-1, 0), (0, 18)):
        try:
            normalizer(a, b)
        except ValueError:
            rejected.append('out_of_domain_normalizer_' + str((a, b)))
        else:
            raise ValueError('Pair normalizer accepted invalid original phase')
    return dict(agent='six-covering-3', role='researcher', controls=rejected,
                unconditioned_required=1118, unconditioned_capacity=1256,
                literal_final_gain=448, literal_remaining_capacity=668,
                toy_full_distinct_cover=True, toy_prefix_upper_bounds=toy_bounds,
                full_four_stage_audit_still_required=True, native_solver=False)


if __name__ == '__main__':
    print(json.dumps(audit(), sort_keys=True))
