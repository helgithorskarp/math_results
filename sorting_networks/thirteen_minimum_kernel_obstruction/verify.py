"""Independent Boolean-list, distinct-rank and minimum-grammar checker.

Imports neither generator nor encoding. Author: six-sorting-1 (researcher).
These different algorithms are not a claim of external peer review.
"""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOWER = [0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39, 44]


def evaluate(values, word):
    values = values.copy()
    for a, b in word:
        assert 0 <= a < b < len(values)
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def mask(values):
    return sum(v << i for i, v in enumerate(values))


def extreme_witness(original, word, high):
    marked = [i for i in range(13) if bool(original >> i & 1) == high]
    other = [i for i in range(13) if i not in marked]
    order = other + marked if high else marked + other
    ranks = [None] * 13
    for rank, i in enumerate(order):
        ranks[i] = rank
    extreme = set(range(13 - len(marked), 13)) if high else set(range(len(marked)))
    count = 0
    for a, b in word:
        count += ranks[a] in extreme or ranks[b] in extreme
        if ranks[a] > ranks[b]:
            ranks[a], ranks[b] = ranks[b], ranks[a]
    flags = [int(v in extreme if high else v not in extreme) for v in ranks]
    return mask(flags[2:10]), count, len(marked)


def kernel_grammar():
    words = []
    visited = 0
    caps = (1, 2, 3)

    def visit(support, counts, word):
        nonlocal visited
        visited += 1
        if list(support) == [0] and support[0] == 7:
            words.append(word)
            return
        if len(word) == 3:
            return
        for a, b in itertools.combinations(range(8), 2):
            if (a == 0 and b != 1) or (b == 7 and a != 6):
                continue
            union = support.get(a, 0) | support.get(b, 0)
            if not union:
                continue
            new_counts = tuple(counts[i] + bool(union >> i & 1) for i in range(3))
            if any(new_counts[i] > caps[i] for i in range(3)):
                continue
            new = support.copy()
            new[a] = union
            new.pop(b, None)
            visit(new, new_counts, word + [[a, b]])

    visit({0: 1, 1: 2, 2: 4}, (0, 0, 0), [])
    return words, visited


def verify(f, c):
    assert f['known_lower_bounds'] == LOWER
    assert c['fixture_sha256'] == hashlib.sha256((HERE / 'fixture.json').read_bytes()).hexdigest()
    inputs = rank_bounds = mixed_bounds = 0
    sets = {}
    for case in c['cases']:
        p32 = f['prefix21'] + f['tournaments'][str(case['case'])] + f['minimum_front']
        p32 += [[a + 1, b + 1] for a, b in f['minimum7_on_V']]
        p34 = p32 + [[a + 2, b + 2] for a, b in f['maximum3_on_U']]
        assert p32 == case['prefix32'] and p34 == case['prefix34']
        U, F = set(), set()
        for x in range(8192):
            bits = [x >> i & 1 for i in range(13)]
            sorted_bits = sorted(bits)
            out32, out34 = evaluate(bits, p32), evaluate(bits, p34)
            assert out32[:2] == sorted_bits[:2] and out32[-2:] == sorted_bits[-2:]
            assert out34[:2] == sorted_bits[:2] and out34[-3:] == sorted_bits[-3:]
            U.add(mask(out32[2:11])); F.add(mask(out34[2:10]))
            assert evaluate(bits, p32 + [[a + 2, b + 2] for a, b in f['known_U13']]) == sorted_bits
            assert evaluate(bits, p34 + [[a + 2, b + 2] for a, b in f['known_F11']]) == sorted_bits
            inputs += 1
        assert U == set(case['U_states']) and len(U) == 53
        assert F == set(case['F_states']) and len(F) == 41
        for n, S in ((9, U), (8, F)):
            assert all(((1 << n) - 1 ^ ((1 << n) - 1 >> w)) in S for w in range(n + 1))
        assert [i for i in range(9) if 1 << i in U] == [4, 7, 8]
        assert [i for i in range(9) if 511 ^ (1 << i) in U] == [0, 1, 2]
        assert all(x == 0 or any(x >> i & 1 for i in (4, 7, 8)) for x in U)
        assert [i for i in range(8) if 255 ^ (1 << i) in F] == [0, 1, 2]
        assert 64 in F and 128 in F
        assert all(x == 255 or any(not (x >> i & 1) for i in (0, 1, 2)) for x in F)
        sets[case['case']] = U
    assert c['cases'][0]['F_states'] == c['cases'][1]['F_states']
    for r in c['F_single_threshold_bounds']:
        for high, direction in ((True, 'high'), (False, 'low')):
            output, count, marked = extreme_witness(r[direction + '_witness'], c['cases'][1]['prefix34'], high)
            assert output == r['state'] and count == r[direction + '_deleted']
            assert r[direction + '_cap'] == 44 - LOWER[13 - marked] - count
            rank_bounds += 1
    expected_pairs = {(4, 0): 3, (7, 0): 3, (8, 0): 2, (8, 1): 3}
    for case_id in (1, 2):
        rows = [r for r in f['mixed_witnesses'] if r['case'] == case_id]
        assert {(r['high_leaf'], r['low_leaf']): r['union_cap'] for r in rows} == expected_pairs
        for r in rows:
            code = r['witness_base3']; colors = []
            for _ in range(13):
                colors.append(code % 3); code //= 3
            assert code == 0
            low, middle = colors.count(0), colors.count(1)
            pools = [iter(range(low)), iter(range(low, low + middle)), iter(range(low + middle, 13))]
            ranks = [next(pools[v]) for v in colors]; deleted = 0
            for a, b in c['cases'][case_id - 1]['prefix32']:
                deleted += ranks[a] < low or ranks[b] < low or ranks[a] >= low + middle or ranks[b] >= low + middle
                if ranks[a] > ranks[b]:
                    ranks[a], ranks[b] = ranks[b], ranks[a]
            h = mask([int(v >= low + middle) for v in ranks[2:11]])
            n = mask([int(v >= low) for v in ranks[2:11]])
            assert h == 1 << r['high_leaf'] and n == 511 ^ (1 << r['low_leaf'])
            assert middle == r['middle_wires'] == 7
            assert r['union_cap'] == 44 - LOWER[middle] - deleted
            assert all((x >> r['low_leaf'] & 1) <= (x >> r['high_leaf'] & 1) for x in sets[case_id])
            mixed_bounds += 1
            if case_id == 2 and r['high_leaf'] == 8:
                # After the extra maximum tree, all marked maxima have
                # left F. These witnesses directly bound its minimum
                # routes by1 and2, without a disjoint-route inference.
                for a, b in [[6, 9], [9, 10]]:
                    deleted += ranks[a] < low or ranks[b] < low or ranks[a] >= low + middle or ranks[b] >= low + middle
                    if ranks[a] > ranks[b]:
                        ranks[a], ranks[b] = ranks[b], ranks[a]
                hF = mask([int(v >= low + middle) for v in ranks[2:10]])
                nF = mask([int(v >= low) for v in ranks[2:10]])
                assert hF == 0 and nF == 255 ^ (1 << r['low_leaf'])
                assert 44 - LOWER[middle] - deleted == r['union_cap'] - 1
                mixed_bounds += 1
    words, histories = kernel_grammar()
    assert sorted(words) == sorted(c['F_minimum_kernels']) and len(words) == 5
    for r in c['subsumed_Y2_cases']:
        S = {mask(evaluate([x >> i & 1 for i in range(13)], r['prefix32'])[2:11]) for x in range(8192)}
        assert S == set(r['states'])
        p = r['source_to_target_permutation']
        assert sorted(p) == list(range(9))
        mapped = {sum((x >> i & 1) << p[i] for i in range(9)) for x in sets[2]}
        assert mapped <= S
        inputs += 8192
    return {'agent': 'six-sorting-1', 'role': 'researcher', 'Boolean_input_checks': inputs,
            'rank_threshold_bounds': rank_bounds, 'mixed_rank_witnesses': mixed_bounds,
            'minimum_grammar_partial_histories': histories, 'minimum_kernels': len(words),
            'subsumed_Y2_cases': len(c['subsumed_Y2_cases'])}


def main():
    f = json.loads((HERE / 'fixture.json').read_text())
    c = json.loads((HERE / 'certificate.json').read_text())
    result = verify(f, c)
    corrupt = json.loads(json.dumps(c))
    corrupt['F_single_threshold_bounds'][0]['high_deleted'] += 1
    try:
        verify(f, corrupt)
    except AssertionError:
        result['wrong_deletion_count_rejected'] = True
    else:
        raise AssertionError('Corrupted bound accepted')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
