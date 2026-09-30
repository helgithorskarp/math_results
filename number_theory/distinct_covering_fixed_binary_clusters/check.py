"""Exact, solver-free source checks. Actual author: six-covering-2 researcher."""
import hashlib
import io
import json
from contextlib import redirect_stdout
from itertools import product
from math import prod, gcd
from pathlib import Path
import point_controls
import cluster_controls
from distinct_top_points import prepare
from fixed_binary_cluster import evidence

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_boxes(N, axes, boxes):
    require(prod(axes) == N and all(gcd(a, b) == 1 for i, a in enumerate(axes) for b in axes[:i]), 'CRT axes')
    for row in boxes:
        require(len(row) == len(axes) + 1 and all(type(x) is int for x in row), 'Integer box shape')
        require(row[-1] > 0 and all(0 < mask < 1 << axis for mask, axis in zip(row, axes)), 'Positive box and masks')


def decode_literal(N, axes, boxes):
    validate_boxes(N, axes, boxes)
    values = [0] * N
    for x in range(N):
        selected = [row[-1] for row in boxes if all(mask >> (x % axis) & 1 for mask, axis in zip(row, axes))]
        require(len(selected) <= 1, 'Overlapping literal boxes')
        if selected:
            values[x] = selected[0]
    return values


def decode_crt(N, axes, boxes):
    validate_boxes(N, axes, boxes)
    values = [0] * N
    coefficients = [(N // axis) * pow(N // axis, -1, axis) for axis in axes]
    for row in boxes:
        coordinates = [[a for a in range(axis) if mask >> a & 1] for mask, axis in zip(row, axes)]
        for point in product(*coordinates):
            x = sum(a * c for a, c in zip(point, coefficients)) % N
            require(values[x] == 0, 'Overlapping CRT boxes')
            values[x] = row[-1]
    return values


def histograms(values, resources):
    result = {}
    for n in resources:
        population = [0] * n
        for x, w in enumerate(values):
            population[x % n] += w
        result[n] = max(population)
    return result


def controls(module):
    output = io.StringIO()
    with redirect_stdout(output):
        module.main()
    data = json.loads(output.getvalue())
    data.pop('seconds')
    require(data['all_passed'], 'Failed exact controls')
    return data


def compute():
    document = (ROOT / 'input.json').read_bytes()
    data = json.loads(document)
    require(data['author'] == 'six-covering-2' and data['role'] == 'researcher', 'Input authorship')
    N, axes, A = data['N'], data['CRT_axes'], data['known']
    require((N, data['B'], data['C'], data['b'], data['minimum']) == (15120, 16, 945, 8, 8), 'Declared application')
    require(data['u_multiplier'] == data['v_multiplier'] == 1, 'Declared integer component factors')
    require(data['v_definition'] == 'v(x mod7560)=w(x)+w(x+7560), 0<=x<7560', 'Declared periodic vector')
    w = decode_literal(N, axes, data['base_boxes'])
    require(w == decode_crt(N, axes, data['base_boxes']), 'Independent box decoders disagree')
    Q = N // 2
    u = w
    v = [w[x] + w[x + Q] for x in range(Q)]
    state = prepare(data['B'], data['C'], data['b'], A, u, v, minimum=data['minimum'])
    e = evidence(state, data['cluster'])
    # Ordinary actual-progressions version uses no production CRT coset or
    # group-budget routine, and keeps the cluster union literally.
    literal_top = cluster_controls.literal_top_bound(state, data['cluster'])
    require(literal_top == e['top_bound']['top_upper_budget'], 'Independent literal top bound')
    S = set(state['S'])
    R = [n for n in range(8, N + 1) if N % n == 0 and n not in dict(A)]
    outside = [n for n in R if n not in S]
    physical = [u[x] + v[x % Q] for x in range(N)]
    maxima = histograms(physical, outside)
    require(maxima == e['outside_capacities'], 'All physical outside maxima')
    costs = {n: sum(v[x % Q] for x in range(N) if x % n == a) for n, a in A if n not in S}
    require(costs == e['known_outside_periodic_footprints'], 'Known-outside costs')
    demand = sum(physical) - sum(costs.values())
    require(demand == e['demand'] and demand > sum(maxima.values()) + literal_top, 'No strict conditional cut')
    residual = [value if all(x % n != a for n, a in A) else 0 for x, value in enumerate(physical)]
    residual_maxima = histograms(residual, R)
    require(sum(residual) == e['ordinary_residual_demand'] and sum(residual_maxima.values()) == e['ordinary_residual_capacity'], 'Ordinary same-vector units')
    require(sum(residual) <= sum(residual_maxima.values()), 'Same-vector comparison')
    known_top_weight = sum(v[x % Q] for x in range(N) if x % 16 == dict(A)[16])
    require(known_top_weight > 0 and all(c == 0 for c in costs.values()), 'Known-top support boundary')
    no_cluster = evidence(state, [])
    require(no_cluster['top_bound']['top_upper_budget'] == cluster_controls.literal_top_bound(state, []), 'No-cluster comparison')
    alternative = data['ordinary_alternative']
    aw = decode_literal(N, axes, alternative['boxes'])
    require(aw == decode_crt(N, axes, alternative['boxes']), 'Alternative box decoders')
    require(all(aw[x] == 0 for x in range(N) if any(x % n == a for n, a in A)), 'Alternative support')
    ac = sum(histograms(aw, R).values())
    require(sum(aw) == alternative['demand'] and ac == alternative['capacity'] and sum(aw) > ac, 'Different ordinary vector is not a strict cut')
    malformed = 0
    for boxes in [data['base_boxes'] + data['base_boxes'][:1], [[-1, 1, 1, 1, 1]], [[1, 1, 1, 1, -1]]]:
        try:
            decode_literal(N, axes, boxes)
        except ValueError:
            malformed += 1
        else:
            raise ValueError('Malformed boxes accepted')
    application = {'N': N, 'known_classes': len(A), 'base_boxes': len(data['base_boxes']),
                   'periodic_weight_on_prescribed_16': known_top_weight,
                   'demand': demand, 'known_outside_periodic_cost': sum(costs.values()),
                   'outside_resources': len(outside), 'outside_actual_phases': sum(outside),
                   'outside_maxima_sha256': hashlib.sha256(json.dumps(sorted(maxima.items()), separators=(',', ':')).encode()).hexdigest(),
                   'outside_capacity': sum(maxima.values()), 'cluster_top_upper': literal_top,
                   'total_capacity': e['capacity'], 'strict_gap': e['gap'],
                   'cluster_phase_cases': prod(d + 1 for d in data['cluster']),
                   'no_cluster_top_upper': no_cluster['top_bound']['top_upper_budget'],
                   'no_cluster_strict_gap': no_cluster['gap'],
                   'ordinary_residual_demand': sum(residual), 'ordinary_residual_capacity': sum(residual_maxima.values()),
                   'all_unused_resources': len(R), 'all_unused_actual_phases': sum(R),
                   'alternative_ordinary_demand': sum(aw), 'alternative_ordinary_capacity': ac,
                   'malformed_box_rejections': malformed}
    result = {'agent': 'six-covering-2', 'role': 'researcher', 'all_passed': True,
              'input_sha256': hashlib.sha256(document).hexdigest(), 'application': application,
              'point_controls': controls(point_controls), 'cluster_controls': controls(cluster_controls),
              'scope': 'Written lemmas and a complete fixed-prefix integer cut; both smaller global periods remain open and no numerical L_min(8) improvement'}
    return result


if __name__ == '__main__':
    result = compute()
    require(result == json.loads((ROOT / 'expected.json').read_text()), 'Expected exact evidence differs')
    print(json.dumps(result, indent=2))
