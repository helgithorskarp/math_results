"""Independent scalar, port, kernel-cover and unbounded-certificate audit.

Imports neither the generator nor a solver. Author: six-sorting-2, researcher.
"""
import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAIRS = tuple(itertools.combinations(range(8), 2))
FIELDS = ['max5', 'max6', 'min1', 'high160', 'two_ones', 'union128_254', 'union160_254']
INITIAL = [(5, 6, 1, 160, x, 0, 0) for x in (40, 48)]


def scalar(values, word):
    values = list(values)
    for a, b in word:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def mask(row):
    return sum(v << i for i, v in enumerate(row))


def run_prefix(values, f, after):
    out = scalar(values, f['prefix'])
    return scalar([out[i] for i in f['prefix_output_order']], after)


def check_witnesses(f, after, rows, start, end):
    checks = 0
    for w in rows:
        high, low = set(w['fixed_high']), set(w['fixed_low'])
        assert not high & low
        free = [i for i in range(11) if i not in high | low]
        assert len(free) == w['middle_count']
        assert w['cap'] == 35 - f['lower_sizes'][str(len(free))] - w['deleted']
        assignments = list(itertools.product((0, 1), repeat=len(free)))
        assignments += [tuple(range(len(free))), tuple(reversed(range(len(free))))]
        for assignment in assignments:
            values = [100 if i in high else -100 if i in low else assignment[free.index(i)]
                      for i in range(11)]
            colors = [2 if i in high else 0 if i in low else 1 for i in range(11)]
            ports = [None if i in high | low else free.index(i) for i in range(11)]
            retained, deleted = [], 0
            for section_index, section in enumerate((f['prefix'], after)):
                for a, b in section:
                    outside = colors[a] != 1 or colors[b] != 1
                    deleted += outside
                    if not outside:
                        retained.append((ports[a], ports[b]))
                    if colors[a] > colors[b]:
                        colors[a], colors[b] = colors[b], colors[a]
                        ports[a], ports[b] = ports[b], ports[a]
                    if values[a] > values[b]:
                        values[a], values[b] = values[b], values[a]
                if section_index == 0:
                    order = f['prefix_output_order']
                    values = [values[i] for i in order]
                    colors = [colors[i] for i in order]
                    ports = [ports[i] for i in order]
            assert deleted == w['deleted']
            assert sum((v == 2) << i for i, v in enumerate(colors[start:end])) == w['x']
            assert sum((v != 0) << i for i, v in enumerate(colors[start:end])) == w['y']
            replay = scalar(assignment, retained)
            assert [replay[p] for p in ports if p is not None] == [v for v in values if -100 < v < 100]
            checks += 1
    return checks


def check_minimum_cover(expected):
    # Unlike the closed-form generator, follow all three individual zero
    # routes through every support-touching comparator with witnessed caps.
    pairs = [p for p in itertools.combinations(range(10), 2)
             if 9 not in p or p == (8, 9)]

    @lru_cache(maxsize=None)
    def suffixes(positions, costs):
        if positions == (0, 0, 0):
            return ((),)
        result = []
        for a, b in pairs:
            if not any(p in (a, b) for p in positions):
                continue
            new_costs = tuple(c + int(p in (a, b)) for p, c in zip(positions, costs))
            if any(c > cap for c, cap in zip(new_costs, (2, 1, 4))):
                continue
            new_positions = tuple(a if p == b else p for p in positions)
            result += [((a, b),) + word for word in suffixes(new_positions, new_costs)]
        return tuple(result)

    words = suffixes((0, 1, 5), (0, 0, 0))
    assert len(words) == len(set(words)) == 43
    assert set(words) == {tuple(map(tuple, w)) for w in expected}
    assert {n: sum(len(w) == n for w in words) for n in (2, 3, 4)} == {2: 1, 3: 6, 4: 36}
    return suffixes.cache_info().currsize


def check_maximum_cover():
    # All binary merges of the five separate one-hot routes; no unary
    # merge is front-loaded. Final-wire and leaf5 budgets suffice.
    occupied_start = (3, 4, 5, 7, 8)
    words = []

    def visit(positions, q5, q8, word):
        if len(set(positions)) == 1:
            if positions[0] == 8:
                words.append(tuple(word))
            return
        for a, b in itertools.combinations(sorted(set(positions)), 2):
            next_q5 = q5 + int(positions[2] in (a, b))
            next_q8 = q8 + int(positions[4] in (a, b))
            if next_q5 > 2 or next_q8 > 1:
                continue
            visit(tuple(b if p == a else p for p in positions), next_q5, next_q8, word + [(a, b)])

    visit(occupied_start, 0, 0, [])
    expected = {((4, 7), (3, 7), (5, 7), (7, 8)),
                ((3, 7), (4, 7), (5, 7), (7, 8)),
                ((3, 4), (4, 7), (5, 7), (7, 8))}
    assert len(words) == 3 and set(words) == expected
    return expected


def transition(state, pair):
    p5, p6, pmin, high, test, u1, u2 = state
    rows = [[int(i == p5) for i in range(8)], [int(i == p6) for i in range(8)],
            [int(i != pmin) for i in range(8)], [(high >> i) & 1 for i in range(8)],
            [(test >> i) & 1 for i in range(8)]]
    top, bottom = [int(i == 7) for i in range(8)], [int(i != 0) for i in range(8)]
    a, b = pair
    low = not (bottom[a] and bottom[b])
    u1 += bool(top[a] or top[b] or low)
    u2 += bool(rows[3][a] or rows[3][b] or low)
    if u1 > 2 or u2 > 3:
        return None
    assert scalar(top, [pair]) == top and scalar(bottom, [pair]) == bottom
    rows = [scalar(row, [pair]) for row in rows]
    return (rows[0].index(1), rows[1].index(1), rows[2].index(0),
            mask(rows[3]), mask(rows[4]), u1, u2)


def check_closure(cert):
    assert cert['wires'] == 8 and cert['fields'] == FIELDS
    assert cert['initials'] == [list(s) for s in INITIAL]
    assert cert['bounds'] == dict(union128_254=2, union160_254=3)
    assert cert['excluded'] == dict(max5=7, max6=7, min1=0, high160=192, two_ones=192)
    states = {tuple(row) for row in cert['states']}
    assert len(states) == len(cert['states']) and set(INITIAL) <= states
    allowed = 0
    for s in states:
        assert len(s) == 7 and all(type(v) is int for v in s)
        p5, p6, pmin, high, test, u1, u2 = s
        assert 5 <= p5 <= 7 and p6 in (6, 7) and pmin in (0, 1)
        assert high in (160, 192) and 0 <= test < 256 and test.bit_count() == 2
        assert 0 <= u1 <= 2 and 0 <= u2 <= 3
        assert s[:5] != (7, 7, 0, 192, 192), ('Accepting state', s)
        for pair in PAIRS:
            nxt = transition(s, pair)
            if nxt is not None:
                allowed += 1
                assert nxt in states, ('Missing successor', s, pair, nxt)
    return dict(states=len(states), attempted_transitions=28*len(states), allowed_transitions=allowed)


def sharp_controls():
    for lower in (3, 4):
        word = [(0, 1), (lower, 6), (5, 6), (6, 7), (5, 6)]
        p5, p6, pmin, high, test = 5, 6, 1, 160, (1 << lower) | 32
        rows = [[int(i == p5) for i in range(8)], [int(i == p6) for i in range(8)],
                [int(i != pmin) for i in range(8)], [(high >> i) & 1 for i in range(8)],
                [(test >> i) & 1 for i in range(8)]]
        u1 = u2 = 0
        for a, b in word:
            u1 += a == 0 or b == 7
            u2 += bool(rows[3][a] or rows[3][b] or a == 0)
            rows = [scalar(row, [(a, b)]) for row in rows]
        assert (rows[0].index(1), rows[1].index(1), rows[2].index(0),
                mask(rows[3]), mask(rows[4]), u1, u2) == (7, 7, 0, 192, 192, 2, 4)
    return dict(auxiliary_words=2, first_union=2, relaxed_second_union=4,
                scope='Five row targets only; neither word is a completion sorter')


def main():
    if not __debug__:
        raise RuntimeError('Run without Python optimization')
    f = json.loads((HERE / 'fixture.json').read_text())
    cert = json.loads((HERE / 'closure.json').read_text())
    assert f['lower_sizes'] == {'5': 9, '6': 12, '7': 16, '9': 25, '11': 35}
    assert f['pure_minimum'] == [[0, 5], [0, 1]] and f['minimum_capacity'] == [2, 1, 4]
    kernel_hash = hashlib.sha256(json.dumps(f['minimum_kernel_words'], separators=(',', ':')).encode()).hexdigest()
    assert kernel_hash == f['minimum_kernel_sha256']
    minimum_states = check_minimum_cover(f['minimum_kernel_words'])
    maximum_words = check_maximum_cover()
    K, L, images = set(), set(), [set(), set(), set()]
    bubble = [(i, i+1) for limit in range(7, 0, -1) for i in range(limit)]
    for state in range(2048):
        values = [(state >> i) & 1 for i in range(11)]
        k = run_prefix(values, f, f['after'])
        assert k[10] == max(values)
        K.add(mask(k[:10]))
        assert scalar(k[:10], f['K_control20']) + [k[10]] == sorted(values)
        ell = scalar(k, f['pure_minimum'])
        assert ell[0] == min(values)
        L.add(mask(ell[1:10]))
        assert [ell[0]] + scalar(ell[1:10], f['L_control18']) + [ell[10]] == sorted(values)
        for c, case in enumerate(f['cases']):
            assert tuple(map(tuple, case['maximum_prefix'])) in maximum_words
            full = scalar(ell, [(a+1, b+1) for a, b in case['maximum_prefix']])
            assert full[0] == sorted(values)[0] and full[9:] == sorted(values)[-2:]
            images[c].add(mask(full[1:9]))
            assert [full[0]] + scalar(full[1:9], bubble) + full[9:] == sorted(values)
    assert K == set(f['K_states']) and len(K) == 127
    assert L == set(f['L_states']) and len(L) == 109
    assert all(x == 1023 or any(not (x >> i & 1) for i in (0, 1, 5)) for x in K)
    assert {i for i in range(10) if 1023 ^ (1 << i) in K} == {0, 1, 5}
    assert {i for i in range(9) if 1 << i in L} == {3, 4, 5, 7, 8}
    assert len(f['prefix']) == 14 and len(f['after']) == 3
    k_assignments = check_witnesses(f, f['after'], f['K_witnesses'], 0, 10)
    case_assignments = 0
    for c, case in enumerate(f['cases']):
        image = images[c]
        assert image == set(case['states']) and len(image) == (68, 67, 68)[c]
        assert {32, 64, 128, 160, 253, 254, case['two_one_test']} <= image
        assert case['two_one_test'] == (40, 48, 40)[c]
        assert case['two_one_test'] & 128 == 0 and case['two_one_test'].bit_count() == 2
        after = f['after'] + f['pure_minimum'] + [(a+1, b+1) for a, b in case['maximum_prefix']]
        case_assignments += check_witnesses(f, after, case['witnesses'], 1, 9)
        assert {(w['x'], w['y']): w['cap'] for w in case['witnesses']} == {(128, 254): 2, (160, 254): 3}
    closure = check_closure(cert)
    bad = dict(cert)
    removed = [6, 6, 1, 192, 72, 0, 1]
    assert removed in cert['states']
    bad['states'] = [s for s in cert['states'] if s != removed]
    try:
        check_closure(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Incomplete closure accepted')
    bad['states'] = cert['states'] + [[7, 7, 0, 192, 192, 2, 3]]
    try:
        check_closure(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Accepting state accepted')
    result = dict(agent='six-sorting-2', role='researcher', status='VERIFIED',
                  K_states=len(K), L_states=len(L), minimum_kernels=43,
                  minimum_cover_states=minimum_states, pure_maximum_words=3,
                  case_states=list(map(len, images)), original_K_L_inputs=2048,
                  original_case_inputs=6144, positive_bubble_control_inputs=6144,
                  K_marker_assignments=k_assignments, case_marker_assignments=case_assignments,
                  closure=closure, negative_certificate_controls=2, sharp_controls=sharp_controls(),
                  certificate_sha256=hashlib.sha256((HERE / 'closure.json').read_bytes()).hexdigest())
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
