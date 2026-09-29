"""Produce compact pruning/path certificates, without a solver."""
import argparse
import itertools
import json
from pathlib import Path


LOWER = [0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35]


def apply(x, network):
    x = list(x)
    for a, b in network:
        x[a], x[b] = min(x[a], x[b]), max(x[a], x[b])
    return x


def image(n, network, order):
    result = set()
    for x in range(1 << n):
        out = apply([(x >> i) & 1 for i in range(n)], network)
        result.add(sum(out[p] << j for j, p in enumerate(order)))
    return sorted(result)


def prune(n, network, fixed_inputs, output_order):
    ports = [None if i in fixed_inputs else sum(j not in fixed_inputs for j in range(i))
             for i in range(n)]
    retained = []
    steps = []
    for k, (a, b) in enumerate(network):
        if ports[a] is not None and ports[b] is not None:
            retained.append([ports[a], ports[b]])
        else:
            steps.append(k)
            if ports[a] is None:
                ports[a], ports[b] = ports[b], None
    return {'fixed_inputs': list(fixed_inputs), 'deleted_steps': steps,
            'output_holes': [j for j, p in enumerate(output_order) if ports[p] is None],
            'retained_network': retained,
            'output_order': [ports[p] for p in output_order if ports[p] is not None]}


def static_data(network, order):
    best = {}
    for markers in itertools.product((-1, 0, 1), repeat=11):
        values = list(markers)
        retained = 0
        for a, b in network:
            retained += values[a] == values[b] == 0
            values[a], values[b] = min(values[a], values[b]), max(values[a], values[b])
        out = [values[p] for p in order]
        if out != sorted(out):
            continue
        interval = out.count(-1), 11 - out.count(1)
        if retained < best.get(interval, (100, None))[0]:
            best[interval] = retained, list(markers)
    intervals = [{'interval': [a, b], 'prefix_retained': retained,
                  'size_lower': LOWER[b-a] - retained, 'input_markers': markers}
                 for (a, b), (retained, markers) in sorted(best.items()) if b-a >= 2]
    maximum = {}
    minimum = {}
    for bits in range(2048):
        x = [bits >> i & 1 for i in range(11)]
        plus = minus = 0
        for a, b in network:
            plus += bool(x[a] or x[b])
            minus += not (x[a] and x[b])
            x[a], x[b] = min(x[a], x[b]), max(x[a], x[b])
        out = sum(x[p] << j for j, p in enumerate(order))
        if plus > maximum.get(out, (-1, None))[0]:
            maximum[out] = plus, bits
        if minus > minimum.get(out, (-1, None))[0]:
            minimum[out] = minus, bits
    thresholds = []
    for weight in range(1, 11):
        state = ((1 << weight) - 1) << (11 - weight)
        D, maximum_input = maximum[state]
        E, minimum_input = minimum[state]
        H = 35 - LOWER[11-weight] - D
        G = 35 - LOWER[weight] - E
        thresholds.append({'state': state, 'weight': weight,
                           'maximum_input_mask': maximum_input, 'maximum_prefix_deleted': D,
                           'minimum_input_mask': minimum_input, 'minimum_prefix_deleted': E,
                           'max_touch_bound': H, 'min_touch_bound': G,
                           'cut_crossing_bound': H + G - 21})
    return intervals, thresholds


def build(fixture):
    P = fixture['incumbent'][:fixture['prefix_length']]
    original = prune(13, P, fixture['target10']['original_fixed_maxima'], list(range(13)))
    network, order = original['retained_network'], original['output_order']
    assert len(network) == 14 and original['output_holes'] == [10, 12]
    cut = prune(11, network, [fixture['target10']['maximum_input']], order)
    states = image(11, network, order)
    targets = [{'name': 'X/10', 'wires_before_projection': 11, 'prefix': network,
                'prefix_output_order': order, 'states': states, 'completion_budget': 21,
                'full_budget': 35, 'maximum_pruning': cut, 'route_bound': 3,
                'positive_suffix': fixture['target10']['known_22_suffix']}]
    for case in fixture['commuted_cases']:
        prefix = P + case['tournament']
        fixed = [i for i in range(13) if case['maximum_input_mask'] >> i & 1]
        cut = prune(13, prefix, fixed, list(range(13)))
        targets.append({'name': f"Y{case['case']}", 'wires_before_projection': 13,
                        'prefix': prefix, 'prefix_output_order': list(range(11)),
                        'states': image(13, prefix, list(range(11))),
                        'completion_budget': 20, 'full_budget': 44,
                        'maximum_pruning': cut, 'route_bound': 3,
                        'positive_suffix': case['known_21_suffix']})
    intervals, thresholds = static_data(network, order)
    pairs = [[a, b] for a in range(6, 11) for b in range(a+2, 11)]
    return {'agent': 'six-sorting-2', 'role': 'researcher', 'schema': 1,
            'known_lower_bounds': LOWER, 'shortcut_types': pairs, 'targets': targets,
            'capacity_demo': {'target': 'X/10', 'comparator_multiset': fixture['capacity_demo_multiset'],
                              'interval_bounds': intervals, 'threshold_bounds': thresholds}}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    result = build(json.loads((root / 'fixture.json').read_text()))
    if args.check:
        assert result == json.loads((root / 'certificate.json').read_text()), 'certificate mismatch'
    else:
        (root / 'certificate.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'targets': [(t['name'], len(t['states']), t['completion_budget'], t['route_bound'])
                                 for t in result['targets']],
                      'shortcut_types': result['shortcut_types'],
                      'interval_bounds': len(result['capacity_demo']['interval_bounds'])}))
