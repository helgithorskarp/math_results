"""Independent scalar, rank/port and unbounded-closure certificate checker."""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = ['max6', 'max8', 'min1', 'high576', 'test80', 'q6', 'q9', 'union', 'min_hits_capped2']
INITIAL = (6, 8, 1, 576, 80, 0, 0, 0, 0)
PAIRS = tuple(itertools.combinations(range(10), 2))


def scalar(values, gates):
    values = list(values)
    for a, b in gates:
        values[a], values[b] = min(values[a], values[b]), max(values[a], values[b])
    return values


def mask(row):
    return sum(v << i for i, v in enumerate(row))


def independent_step(state, pair):
    p6, p8, pmin, high, test, q6, q9, union, r = state
    # Execute five distinct scalar rows. The fourth and fifth contain two
    # ones, so neither is replaced by an OR of one-hot output trajectories.
    rows = [[int(i == p6) for i in range(10)],
            [int(i == p8) for i in range(10)],
            [int(i != pmin) for i in range(10)],
            [(high >> i) & 1 for i in range(10)],
            [(test >> i) & 1 for i in range(10)]]
    a, b = pair
    q6 += bool(rows[0][a] or rows[0][b])
    q9 += (a == 9 or b == 9)
    low = not (rows[2][a] and rows[2][b])
    union += bool(rows[3][a] or rows[3][b] or low)
    r = min(2, r + low)
    if q6 > 2 or q9 > 1 or union > 4:
        return None
    rows = [scalar(row, [pair]) for row in rows]
    return (rows[0].index(1), rows[1].index(1), rows[2].index(0),
            mask(rows[3]), mask(rows[4]), q6, q9, union, r)


def validate_closure(certificate):
    assert certificate['wires'] == 10 and certificate['fields'] == FIELDS
    assert certificate['initial'] == list(INITIAL)
    assert certificate['bounds'] == dict(q6=2, q9=1, union=4)
    assert certificate['excluded_target'] == dict(max6=9, max8=9, min1=0, high576=768,
                                                 test80=768, min_hits_capped2=2)
    rows = [tuple(row) for row in certificate['states']]
    states = set(rows)
    assert len(states) == len(rows) and INITIAL in states
    transitions = allowed = 0
    for s in rows:
        assert len(s) == 9 and all(type(v) is int for v in s)
        p6, p8, pmin, high, test, q6, q9, union, r = s
        assert 6 <= p6 <= 9 and 8 <= p8 <= 9 and pmin in (0, 1)
        assert 0 <= high < 1024 and high.bit_count() == 2 and high & 512
        assert 0 <= test < 1024 and test.bit_count() == 2 and not (test & 15)
        assert 0 <= q6 <= 2 and 0 <= q9 <= 1 and 0 <= union <= 4 and 0 <= r <= 2
        assert (p6, p8, pmin, high, test, r) != (9, 9, 0, 768, 768, 2), ('Accepting state', s)
        for pair in PAIRS:
            nxt = independent_step(s, pair)
            transitions += 1
            if nxt is not None:
                allowed += 1
                assert nxt in states, ('Missing successor', s, pair, nxt)
    return dict(states=len(states), attempted_transitions=transitions, allowed_transitions=allowed)


def check_prefix(fixture):
    assert fixture['wires'] == 10
    assert len(fixture['prefix']) == 14 and len(fixture['after']) == 3
    assert sorted(fixture['prefix_output_order']) == list(range(11))
    assert len(fixture['control20']) == 20
    image = set()
    for state in range(2048):
        values = [(state >> i) & 1 for i in range(11)]
        result = scalar(values, fixture['prefix'])
        result = [result[i] for i in fixture['prefix_output_order']]
        result = scalar(result, fixture['after'])
        assert result[10] == max(values)
        image.add(mask(result[:10]))
        assert scalar(result[:10], fixture['control20']) + [result[10]] == sorted(values)
    assert image == set(fixture['states']) and len(image) == 127
    assert {16, 64, 256, 512, 80, 576, 640, 1021}.issubset(image)
    assignment_checks = 0
    for witness in fixture['witnesses']:
        high, low = set(witness['fixed_high']), set(witness['fixed_low'])
        assert not high & low
        free = [i for i in range(11) if i not in high | low]
        assert len(free) == witness['middle_count']
        assert witness['cap'] == 35 - fixture['lower_sizes'][str(len(free))] - witness['deleted']
        for assignment in itertools.product((0, 1), repeat=len(free)):
            # Marker colors drive the deletion/port route; actual free bits
            # are executed independently, including comparisons of equal bits.
            values = [2 if i in high else -1 if i in low else assignment[free.index(i)]
                      for i in range(11)]
            colors = [2 if i in high else 0 if i in low else 1 for i in range(11)]
            ports = [None if i in high | low else free.index(i) for i in range(11)]
            retained = []
            deleted = 0
            for section_index, section in enumerate((fixture['prefix'], fixture['after'])):
                for a, b in section:
                    outside = colors[a] != 1 or colors[b] != 1
                    deleted += outside
                    if not outside:
                        retained.append((ports[a], ports[b]))
                    if colors[a] > colors[b]:
                        colors[a], colors[b] = colors[b], colors[a]
                        ports[a], ports[b] = ports[b], ports[a]
                    values[a], values[b] = min(values[a], values[b]), max(values[a], values[b])
                if section_index == 0:
                    order = fixture['prefix_output_order']
                    values = [values[i] for i in order]
                    colors = [colors[i] for i in order]
                    ports = [ports[i] for i in order]
            assert deleted == witness['deleted']
            assert sum((v == 2) << i for i, v in enumerate(colors[:10])) == witness['x']
            assert sum((v != 0) << i for i, v in enumerate(colors[:10])) == witness['y']
            assert colors[10] == 2
            residual = scalar(assignment, retained)
            assert [residual[p] for p in ports if p is not None] == [v for v in values if v in (0, 1)]
            assignment_checks += 1
    bounds = {(w['x'], w['y']): w['cap'] for w in fixture['witnesses']}
    assert bounds == {(64, 1023): 2, (512, 1023): 1, (576, 1021): 4}
    return dict(original_inputs=2048, pruned_free_assignments=assignment_checks,
                prefix_image_size=len(image), known_control_gates=len(fixture['control20']))


def control():
    # This six-gate word satisfies all relaxed terminal targets, with two
    # minimum passages and mixed union five. It is not a K sorting network.
    word = [(0, 1), (0, 2), (4, 8), (6, 8), (8, 9), (6, 8)]
    rows = [[int(i == 6) for i in range(10)], [int(i == 8) for i in range(10)],
            [int(i != 1) for i in range(10)],
            [int(i in (6, 9)) for i in range(10)], [int(i in (4, 6)) for i in range(10)]]
    q6 = q9 = union = r = 0
    for a, b in word:
        q6 += bool(rows[0][a] or rows[0][b])
        q9 += 9 in (a, b)
        low = not (rows[2][a] and rows[2][b])
        union += bool(rows[3][a] or rows[3][b] or low)
        r += low
        rows = [scalar(row, [(a, b)]) for row in rows]
    assert (rows[0].index(1), rows[1].index(1), rows[2].index(0), mask(rows[3]), mask(rows[4]),
            q6, q9, union, r) == (9, 9, 0, 768, 768, 2, 1, 5, 2)
    return dict(sharp_relaxed_union=union, minimum_passages=r, scope='Auxiliary targets only')


def check_refill_invariants():
    before_six = [pair for pair in PAIRS if 6 not in pair and 9 not in pair]
    before_root_or_refill = [pair for pair in PAIRS if 8 not in pair and 9 not in pair]
    transitions = 0
    # Before the first passage of one-hot6, its coordinate6 is untouched.
    # Row80 is exactly the one-hot4 row together with that inert one.
    for p4 in (4, 5, 7, 8):
        single = [int(i == p4) for i in range(10)]
        two = [int(i in (p4, 6)) for i in range(10)]
        for pair in before_six:
            out_single, out_two = scalar(single, [pair]), scalar(two, [pair])
            assert out_single.index(1) in (4, 5, 7, 8)
            assert mask(out_two) == mask(out_single) | 64
            transitions += 1
    assert mask(scalar([int(i in (6, 8)) for i in range(10)], [(6, 8)])) == 320
    # Between (6,8) and (8,9), and between (8,9) and the unique refill,
    # the other one can occupy only6/7. Both finite sets are closed.
    for upper in (8, 9):
        for other in (6, 7):
            row = [int(i in (other, upper)) for i in range(10)]
            for pair in before_root_or_refill:
                out = scalar(row, [pair])
                assert mask(out) in ((1 << upper) | 64, (1 << upper) | 128)
                transitions += 1
    for other in (6, 7):
        row = [int(i in (other, 8)) for i in range(10)]
        assert mask(scalar(row, [(8, 9)])) == (1 << other) | 512
    refill_tests = 0
    for other in (6, 7):
        row = [int(i in (other, 9)) for i in range(10)]
        for a in range(8):
            out = scalar(row, [(a, 8)])
            assert out[8] == int(a == other)
            refill_tests += 1
    assert transitions == 224 and refill_tests == 16
    earlier_seven = 0
    for state in (640, 768):
        row = [(state >> i) & 1 for i in range(10)]
        for pair in PAIRS:
            if 9 in pair:
                continue
            out = mask(scalar(row, [pair]))
            assert out in (640, 768)
            if state == 640 and out == 768:
                assert pair == (7, 8)
            earlier_seven += 1
        assert mask(scalar(row, [(8, 9)])) == state
        assert mask(scalar(row, [(6, 8)])) == state
    assert earlier_seven == 72
    return dict(closed_invariant_transitions=transitions, forced_endpoint_rows=3,
                final_refill_tests=refill_tests, necessary_refill_lower_endpoints=[6, 7],
                earlier_seven_invariant_transitions=earlier_seven, earlier_seven_endpoint_rows=4)


def main():
    if not __debug__:
        raise RuntimeError("Run without Python optimization: assertions are part of the checker")
    fixture = json.loads((HERE / 'fixture.json').read_text())
    cert = json.loads((HERE / 'closure.json').read_text())
    result = dict(agent='six-sorting-2', role='researcher', status='VERIFIED')
    result.update(check_prefix(fixture))
    result.update(validate_closure(cert))
    result['refill_invariants'] = check_refill_invariants()
    result['positive_control'] = control()
    bad = dict(cert)
    excluded = [6, 8, 1, 576, 80, 1, 0, 1, 0]
    assert excluded in cert['states']
    bad['states'] = [row for row in cert['states'] if row != excluded]
    try:
        validate_closure(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Missing reachable state was accepted')
    bad = dict(cert)
    bad['states'] = cert['states'] + [[9, 9, 0, 768, 768, 2, 1, 4, 2]]
    try:
        validate_closure(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Accepting state was accepted')
    result['negative_certificate_controls'] = 2
    result['certificate_sha256'] = hashlib.sha256((HERE / 'closure.json').read_bytes()).hexdigest()
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
