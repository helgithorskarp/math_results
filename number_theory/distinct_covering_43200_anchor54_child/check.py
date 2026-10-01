"""All54 raw phases; literal physical integer checks, no solver or private input."""
import argparse
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from time import monotonic

HERE = Path(__file__).resolve().parent
N, Q, B, C, b = 43200, 10800, 64, 675, 16
ORDER = (8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 36, 40, 45, 48, 50, 75)
PARENT = (0, 0, 5, 10, 1, 4, 3, 17, 2, 3, 11, 30, 27, 28, 14, 33, 38)
AXES = (16, 27, 25)
REPRESENTATIVES = tuple(range(9)) + tuple(range(27, 36))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def validate(data):
    need(all(type(data[k]) is int and data[k] == v for k, v in
         [('N', N), ('Q', Q), ('B', B), ('C', C), ('b', b), ('extra_modulus', 54)]),
         'Unexpected implemented parameters')
    need(data['axes'] == list(AXES) and data['cluster'] == [3, 5]
         and all(type(v) is int for v in data['axes'] + data['cluster']), 'Unexpected axes or cluster')
    need(data['parent_moduli'] == list(ORDER) and data['parent_residues'] == list(PARENT)
         and all(type(v) is int for v in data['parent_moduli'] + data['parent_residues']),
         'Different prescribed prefix')
    basis = data['box_basis']
    need(bool(basis) and all(len(mask) == 3 and all(type(v) is int for v in mask)
         and all(0 < mask_i < 1 << axis for mask_i, axis in zip(mask, AXES)) for mask in basis),
         'Malformed literal Cartesian box basis')
    need(len({tuple(mask) for mask in basis}) == len(basis), 'Duplicate basis box')
    need(tuple(r['phase54'] for r in data['representatives']) == REPRESENTATIVES
         and all(type(r['phase54']) is int for r in data['representatives']),
         'Missing, duplicated or reordered representative')
    for row in data['representatives']:
        terms = row['weights']
        need(bool(terms) and all(len(term) == 2 and all(type(v) is int for v in term)
             and 0 <= term[0] < len(basis) and term[1] > 0 for term in terms),
             'Invalid sparse positive integer coefficients')
        need(len({term[0] for term in terms}) == len(terms), 'Repeated box within one vector')


@lru_cache(None)
def physical_coordinates():
    coordinates = {tuple(x % axis for axis in AXES): x for x in range(Q)}
    need(len(coordinates) == Q, 'The ordinary remainder axes are not bijective')
    return coordinates


@lru_cache(None)
def cofactor_coordinates():
    coordinates = {(x % 400, x % 27): x for x in range(Q)}
    need(len(coordinates) == Q, 'The ordinary cofactor/remainder table is not bijective')
    return coordinates


def weight(data, a):
    need(type(a) is int and 0 <= a < 54, 'Invalid raw phase')
    root = a % 9
    representative = root if root % 2 == a % 2 else root + 27
    row = next(r for r in data['representatives'] if r['phase54'] == representative)
    base = [0] * Q
    for index, value in row['weights']:
        masks = data['box_basis'][index]
        coordinates = [[v for v in range(axis) if mask >> v & 1] for mask, axis in zip(masks, AXES)]
        for key in product(*coordinates):
            x = physical_coordinates()[key]
            need(not base[x], 'Overlapping boxes')
            base[x] = value
    u, v = a % 27, representative % 27
    transformed = []
    for x in range(Q):
        leaf = x % 27
        target_leaf = v if leaf == u else u if leaf == v else leaf
        transformed.append(base[cofactor_coordinates()[x % 400, target_leaf]])
    need(any(transformed), 'Zero certificate')
    known = tuple(zip(ORDER, PARENT)) + ((54, a),)
    need(all(not w or all(x % m != phase for m, phase in known)
             for x, w in enumerate(transformed)), 'Positive weight on a prescribed class')
    return transformed


def evaluate(data, a):
    base = weight(data, a)
    vector = base * (N // Q)
    resources = [n for n in range(8, N + 1) if N % n == 0 and n not in ORDER + (54,)]
    top = {B * d for d in range(1, C + 1) if C % d == 0}
    need(top <= set(resources), 'A top resource is placed or unavailable')
    nonzero = [(x, w) for x, w in enumerate(vector) if w]
    capacities, H = {}, {}
    phase_hash = sha256()
    for n in resources:
        populations = [0] * n
        for x, w in nonzero:
            populations[x % n] += w
        capacities[n] = max(populations)
        phase_hash.update(json.dumps([n, populations], separators=(',', ':')).encode() + b'\n')
        if n in top and n != B:
            H[n // B] = [max(populations[t::b]) for t in range(b)]
    M = {d: capacities[B * d] for d in H}
    labels = []
    case_hash = sha256()
    for t in range(b):
        points = [(x, vector[x]) for x in range(t + B // 2, N, B) if vector[x]]
        values = []
        for s, r in product(range(-1, 3), range(-1, 5)):
            inside = [(d, v) for d, v in ((3, s), (5, r)) if v >= 0]
            outside = [d for d, v in ((3, s), (5, r)) if v < 0]
            mass = sum(w for x, w in points if any(x % d == v for d, v in inside))
            value = 2 * mass + sum(M[d] for d in outside)
            case_hash.update(json.dumps([t, [s, r], value], separators=(',', ':')).encode() + b'\n')
            values.append(value)
        labels.append(max(values) + sum(max(M[d], 2 * H[d][t]) for d in H if d not in (3, 5)))
    outside = sum(capacities[n] for n in resources if n not in top)
    total = outside + max(labels)
    result = {'phase54': a, 'demand': sum(vector), 'outside_capacity': outside,
              'top_budget': max(labels), 'total_capacity': total, 'strict_gap': sum(vector) - total,
              'resource_phase_values_sha256': phase_hash.hexdigest(),
              'union_case_values_sha256': case_hash.hexdigest(),
              'base_weight_sha256': sha256(json.dumps(base, separators=(',', ':')).encode()).hexdigest()}
    need(result['strict_gap'] > 0, 'No strict physical integer inequality')
    return result


def controls(data):
    edits = ('bad_period', 'missing_representative', 'duplicate_representative', 'bad_basis_index',
             'zero_weight', 'negative_weight', 'duplicate_weight_term', 'oversized_mask', 'overlap',
             'weight_on_parent', 'different_parent')
    for edit in edits:
        invalid = deepcopy(data)
        row = invalid['representatives'][0]
        if edit == 'bad_period':
            invalid['Q'] = 3600
        elif edit == 'missing_representative':
            invalid['representatives'].pop()
        elif edit == 'duplicate_representative':
            invalid['representatives'].append(deepcopy(row))
        elif edit == 'bad_basis_index':
            row['weights'][0][0] = len(invalid['box_basis'])
        elif edit == 'zero_weight':
            row['weights'][0][1] = 0
        elif edit == 'negative_weight':
            row['weights'][0][1] = -1
        elif edit == 'duplicate_weight_term':
            row['weights'].append(deepcopy(row['weights'][0]))
        elif edit == 'oversized_mask':
            invalid['box_basis'][0][1] = 1 << 27
        elif edit == 'overlap':
            index = len(invalid['box_basis'])
            invalid['box_basis'].append([(1 << axis) - 1 for axis in AXES])
            row['weights'].append([index, 1])
        elif edit == 'weight_on_parent':
            index = len(invalid['box_basis'])
            invalid['box_basis'].append([1, 1, 1])
            row['weights'] = [[index, 1]]
        elif edit == 'different_parent':
            invalid['parent_residues'][-1] = 39
        try:
            validate(invalid)
            weight(invalid, 0)
        except ValueError:
            continue
        raise ValueError('Malformed certificate accepted: ' + edit)
    return list(edits)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', type=int)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    raw = (HERE / 'input.json').read_bytes()
    data = json.loads(raw)
    validate(data)
    start = monotonic()
    if args.phase is not None:
        result = {'phase_result': evaluate(data, args.phase), 'parent_exclusion': False,
                  'whole_period_exclusion': False}
    else:
        results = []
        for a in range(54):
            need(monotonic() - start < 20, 'Incomplete raw54 check: unchanged20s cap')
            results.append(evaluate(data, a))
        events = ''.join(json.dumps(row, separators=(',', ':'), sort_keys=True) + '\n' for row in results).encode()
        resources = [n for n in range(8, N + 1) if N % n == 0 and n not in ORDER + (54,)]
        result = {'N': N, 'Q': Q, 'extra_modulus': 54, 'parent_moduli': list(ORDER),
                  'parent_residues': list(PARENT), 'input_sha256': sha256(raw).hexdigest(),
                  'stored_representative_count': 18, 'literal_box_basis_count': len(data['box_basis']),
                  'raw_phases_checked': 54, 'smallest_physical_gap': min(r['strict_gap'] for r in results),
                  'actual_resources_checked': 54 * len(resources),
                  'actual_phases_evaluated': 54 * sum(resources), 'cluster_union_cases': 54 * b * 24,
                  'ordered_phase_results_sha256': sha256(events).hexdigest(),
                  'parent_exclusion': True, 'whole_period_exclusion': False}
        need(result == json.loads((HERE / 'expected.json').read_text()), 'Exact result differs from saved literal evidence')
    rejected = controls(data) if args.controls else []
    print(json.dumps({'certificate': result, 'rejected_controls': rejected,
                      'elapsed_seconds': monotonic() - start, 'whole_cap_seconds': 20,
                      'independent_review': False}, indent=2))


if __name__ == '__main__':
    main()
