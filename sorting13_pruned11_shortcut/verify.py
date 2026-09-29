"""Independent scalar-marker and cut-capacity replay; no generator or solver imports."""
import json
import resource
import time
from collections import deque
from pathlib import Path


def compare(values, gates):
    values = values.copy()
    touched = []
    for k, (a, b) in enumerate(gates):
        if values[a] == 2 or values[b] == 2:
            touched.append(k)
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values, touched


def unpack(bits, n):
    return [bits >> i & 1 for i in range(n)]


def packed(values):
    return sum(value << i for i, value in enumerate(values))


def marked_inputs(markers):
    free = [i for i, marker in enumerate(markers) if marker == 0]
    for bits in range(1 << len(free)):
        values = [2 * marker for marker in markers]
        for j, i in enumerate(free):
            values[i] = bits >> j & 1
        yield values


def retained_count(values, gates):
    values = values.copy()
    count = 0
    for a, b in gates:
        count += values[a] in (0, 1) and values[b] in (0, 1)
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values, count


if __name__ == '__main__':
    start = time.monotonic()
    root = Path(__file__).resolve().parent
    cert = json.loads((root / 'certificate.json').read_text())
    fixture = json.loads((root / 'fixture.json').read_text())
    lower = [0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35]
    assert cert['known_lower_bounds'] == lower
    shortcuts = [(6,8), (6,9), (6,10), (7,9), (7,10), (8,10)]
    assert list(map(tuple, cert['shortcut_types'])) == shortcuts
    assert len(fixture['incumbent']) == 45 and fixture['prefix_length'] == 21
    P = fixture['incumbent'][:21]
    X = set()
    for bits in range(8192):
        values = unpack(bits, 13)
        incumbent, _ = compare(values, fixture['incumbent'])
        assert incumbent == sorted(values)
        out, _ = compare(values, P)
        assert out[12] == max(values)
        X.add(packed(out[:12]))
    assert len(X) == 157
    projection = {(x & 1023) | ((x >> 11) << 10) for x in X if x >> 10 & 1}
    targets = cert['targets']
    assert [t['name'] for t in targets] == ['X/10', 'Y1', 'Y2']
    assert set(targets[0]['states']) == projection and len(projection) == 136
    # Independently align the generalized fourteen-gate prefix with original P.
    fixed_original = fixture['target10']['original_fixed_maxima']
    assert fixed_original == [1, 5]
    t0 = targets[0]
    for bits in range(2048):
        free = unpack(bits, 11)
        values = []
        k = 0
        for i in range(13):
            if i in fixed_original:
                values.append(2)
            else:
                values.append(free[k]); k += 1
        direct, _ = compare(values, P)
        expected = [direct[i] for i in range(13) if i not in (10, 12)]
        assert direct[10] == direct[12] == 2
        out, _ = compare(free, t0['prefix'])
        assert [out[i] for i in t0['prefix_output_order']] == expected
    marker_checks = 0
    for target in targets:
        n = target['wires_before_projection']
        if n == 13:
            case = next(c for c in fixture['commuted_cases'] if target['name'] == f"Y{c['case']}")
            assert target['prefix'] == P + case['tournament']
            assert target['prefix_output_order'] == list(range(11))
            full_order = list(range(13))
        else:
            assert len(target['prefix']) == 14
            full_order = target['prefix_output_order']
        observed = set()
        for bits in range(1 << n):
            values = unpack(bits, n)
            out, _ = compare(values, target['prefix'])
            row = [out[i] for i in target['prefix_output_order']]
            observed.add(packed(row))
            sorted_row, _ = compare(row, target['positive_suffix'])
            assert sorted_row == sorted(row)
            if n == 13:
                complete, _ = compare(out, target['positive_suffix'])
                assert complete == sorted(values)
        assert sorted(observed) == target['states']
        assert len(target['states']) == {'X/10':136, 'Y1':146, 'Y2':145}[target['name']]
        assert len(target['positive_suffix']) == target['completion_budget'] + 1
        assert all(((1 << k)-1) << (11-k) in observed for k in range(12))
        assert 64 in observed
        cut = target['maximum_pruning']
        fixed = cut['fixed_inputs']
        assert len(fixed) == n - 10
        assert cut['output_holes'] == ([6] if n == 11 else [6,11,12])
        assert len(cut['deleted_steps']) == (3 if n == 11 else 12)
        assert len(cut['retained_network']) == (11 if n == 11 else 12)
        assert target['full_budget'] == len(target['prefix']) + target['completion_budget']
        assert target['route_bound'] == target['full_budget'] - len(cut['deleted_steps']) - lower[10] == 3
        for bits in range(1024):
            free = unpack(bits, 10)
            values = []
            k = 0
            for i in range(n):
                if i in fixed:
                    values.append(2)
                else:
                    values.append(free[k]); k += 1
            direct, touched = compare(values, target['prefix'])
            ordered = [direct[i] for i in full_order]
            assert [i for i, value in enumerate(ordered) if value == 2] == cut['output_holes']
            assert touched == cut['deleted_steps']
            kept = [value for value in ordered if value != 2]
            replay, _ = compare(free, cut['retained_network'])
            assert [replay[i] for i in cut['output_order']] == kept
            marker_checks += 1
    demo = cert['capacity_demo']
    multiset = list(map(tuple, demo['comparator_multiset']))
    assert len(multiset) == 21 and all(0 <= a < b < 11 for a, b in multiset)
    assert not set(multiset) & set(shortcuts)
    # Independent graph-distance certificate for the impossibility of every ordering.
    distance = {6:0}
    queue = deque([6])
    while queue:
        a = queue.popleft()
        for lo, hi in multiset:
            if lo == a and hi not in distance:
                distance[hi] = distance[a] + 1
                queue.append(hi)
    assert distance[10] == 4 > targets[0]['route_bound']
    static_marker_checks = 0
    for entry in demo['interval_bounds']:
        lo, hi = entry['interval']
        for values in marked_inputs(entry['input_markers']):
            out, count = retained_count(values, t0['prefix'])
            out = [out[i] for i in t0['prefix_output_order']]
            assert out[:lo] == [-2]*lo and out[hi:] == [2]*(11-hi)
            assert all(value in (0, 1) for value in out[lo:hi])
            assert count == entry['prefix_retained']
            static_marker_checks += 1
        assert entry['size_lower'] == lower[hi-lo] - entry['prefix_retained']
        assert sum(lo <= a < b < hi for a, b in multiset) >= entry['size_lower']
    assert len(demo['interval_bounds']) == 55
    for entry in demo['threshold_bounds']:
        weight, state = entry['weight'], entry['state']
        assert state == ((1 << weight)-1) << (11-weight)
        for polarity in ('maximum', 'minimum'):
            mask = entry[polarity + '_input_mask']
            markers = [(1 if mask >> i & 1 else 0) if polarity == 'maximum'
                       else (0 if mask >> i & 1 else -1) for i in range(11)]
            for values in marked_inputs(markers):
                out, count = retained_count(values, t0['prefix'])
                out = [out[i] for i in t0['prefix_output_order']]
                hole_pattern = sum((value == (2 if polarity == 'maximum' else -2)) << i
                                   for i, value in enumerate(out))
                assert hole_pattern == (state if polarity == 'maximum' else 2047 ^ state)
                assert count == 14 - entry[polarity + '_prefix_deleted']
                static_marker_checks += 1
        H = 35 - lower[11-weight] - entry['maximum_prefix_deleted']
        G = 35 - lower[weight] - entry['minimum_prefix_deleted']
        assert (H,G,H+G-21) == (entry['max_touch_bound'], entry['min_touch_bound'], entry['cut_crossing_bound'])
        assert sum(bool(state >> a & 1 or state >> b & 1) for a,b in multiset) <= H
        assert sum(not(state >> a & 1 and state >> b & 1) for a,b in multiset) <= G
        assert sum(a < 11-weight <= b for a,b in multiset) <= H + G - 21
    assert len(demo['threshold_bounds']) == 10
    positive_cuts = 0
    for mask in range(2048):
        capacity = sum(bool(mask >> a & 1) and not(mask >> b & 1) for a,b in multiset)
        demand = max((state & mask).bit_count() - ((((1 << state.bit_count())-1)
                     << (11-state.bit_count())) & mask).bit_count() for state in projection)
        assert capacity >= demand, (mask, capacity, demand)
        positive_cuts += demand > 0
    assert positive_cuts == 2034
    print(json.dumps({'status':'verified', 'targets':[(t['name'],len(t['states'])) for t in targets],
                      'route_bound':3, 'shortcut_types':6, 'maximum_marker_assignments':marker_checks,
                      'static_marker_assignments':static_marker_checks, 'interval_bounds':55,
                      'cut_subsets':2048, 'positive_demand_cuts':positive_cuts,
                      'demo_shortest_maximum_motion':4,
                      'seconds':time.monotonic()-start,
                      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
