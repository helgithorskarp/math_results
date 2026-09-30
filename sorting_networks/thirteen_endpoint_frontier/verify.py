"""Independent scalar/rank checks and complete trajectory-kernel DFS.

No generator, solver, or prior checker is imported. Small-word controls check
the endpoint lemma, not an unrestricted network exclusion.
"""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOWER = [0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39, 44]


def values(word, row):
    row = list(row)
    for a, b in word:
        if row[a] > row[b]:
            row[a], row[b] = row[b], row[a]
    return row


def bits(n, mask):
    return [mask >> i & 1 for i in range(n)]


def mask(row):
    return sum(v << i for i, v in enumerate(row))


def rank_path(word, selected):
    threshold = 13 - len(selected)
    low = iter(range(threshold))
    high = iter(range(threshold, 13))
    row = [next(high) if i in selected else next(low) for i in range(13)]
    h = l = 0
    for a, b in word:
        h += row[a] >= threshold or row[b] >= threshold
        l += row[a] < threshold or row[b] < threshold
        row[a], row[b] = min(row[a], row[b]), max(row[a], row[b])
    return row, threshold, h, l


def kernel_words():
    # Select every labelled comparator touching at least one tracked zero.
    # Cap each trajectory; merges occur when positions coincide.
    result = set()
    caps = (2, 1, 3)
    pairs = [p for p in itertools.combinations(range(11), 2)
             if 10 not in p or p == (9, 10)]

    def visit(positions, counts, word):
        if positions == (0, 0, 0):
            result.add(tuple(word))
            return
        # With at least two unmerged groups, every group needs another touch
        # to merge. A group with an exhausted leaf budget cannot finish.
        if len(set(positions)) > 1 and any(c >= cap for c, cap in zip(counts, caps)):
            return
        for a, b in pairs:
            touch = tuple(i in (a, b) for i in positions)
            if not any(touch):
                continue
            updated = tuple(c + t for c, t in zip(counts, touch))
            if any(c > cap for c, cap in zip(updated, caps)):
                continue
            moved = tuple(a if i == b else i for i in positions)
            visit(moved, updated, word + [(a, b)])

    visit((0, 1, 5), (0, 0, 0), [])
    return sorted(result)


def check_endpoint_lemma():
    checked = active = 0
    for n, max_length in ((3, 6), (4, 5)):
        g = [(0, n - 1)]
        pairs = list(itertools.combinations(range(n), 2))
        good = [bits(n, x) for x in range(1 << n)
                if (x & 1) <= (x >> (n - 1) & 1)]
        bad = [bits(n, x) for x in range(1 << n)
               if (x & 1) > (x >> (n - 1) & 1)]
        for m in range(max_length + 1):
            for q in itertools.product(pairs, repeat=m):
                # All initially endpoint-ordered rows stay ordered.
                for row in good:
                    assert values(q + tuple(g), row) == values(tuple(g) + q, row)
                for row in bad:
                    checked += 1
                    out = values(q, row)
                    if out[0] <= out[-1]:
                        continue
                    active += 1
                    assert values(q + tuple(g), row) == values(tuple(g) + q, row)
    # Both hypotheses matter: a redundant terminal g need not commute.
    q, g = [(0, 1)], [(0, 2)]
    assert values(q + g, bits(3, 1)) != values(g + q, bits(3, 1))
    # Two initial inversions: g remains active on3, but fails to commute on1.
    assert values(q, bits(3, 3)) == bits(3, 3)
    assert {mask(values(q + g, bits(3, x))) for x in (1, 3)} != {
        mask(values(g + q, bits(3, x))) for x in (1, 3)}
    return checked, active


def verify(f, c):
    assert f['known_lower_bounds'] == LOWER and c['schema'] == 1
    p24 = f['prefix21'] + f['tournament']
    assert len(p24) == 24
    p25 = p24 + [[0, 10]]
    assert c['prefix25'] == p25 and c['target_budget'] == 19
    assert f['tournament'] == [[6, 11], [9, 10], [10, 11]]
    y, z = set(), set()
    for x in range(8192):
        row = bits(13, x)
        assert values(f['incumbent45'], row) == sorted(row)
        a = values(p24, row)
        b = values(p25, row)
        assert a[-2:] == b[-2:] == sorted(row)[-2:]
        y.add(mask(a[:11])); z.add(mask(b[:11]))
        assert values(f['known21'], b[:11]) + b[-2:] == sorted(row)
    assert sorted(y) == c['Y2_states'] and len(y) == 145
    assert sorted(z) == c['Z_states'] and len(z) == 144
    assert [x for x in sorted(y) if (x & 1) > (x >> 10 & 1)] == [65]
    assert c['unique_initial_inversion'] == 65
    assert mask(values([(0, 10)], bits(11, 65))) == c['replacement_state'] == 1088
    assert z == y - {65} and 1088 in y
    for k in range(12):
        assert ((1 << k) - 1) << (11 - k) in z
    maxima, minima = {}, {}
    for x in range(8192):
        selected = {i for i in range(13) if x >> i & 1}
        if len(selected) < 2:
            continue
        row, threshold, h, l = rank_path(p25, selected)
        assert row[-2:] == [11, 12]
        out = sum((v >= threshold) << i for i, v in enumerate(row[:11]))
        maxima[x] = out, h
        minima[x] = out, l
    assert [r['state'] for r in c['single_threshold_bounds']] == sorted(z)
    for r in c['single_threshold_bounds']:
        x = r['state']
        assert maxima[r['high_witness']] == (x, r['high_deleted'])
        assert minima[r['low_witness']] == (x, r['low_deleted'])
        assert r['high_cap'] == 44 - LOWER[11 - x.bit_count()] - r['high_deleted']
        assert r['low_cap'] == 44 - LOWER[x.bit_count() + 2] - r['low_deleted']
    one = {r['state']: r for r in c['single_threshold_bounds']}
    assert [one[1 << i]['high_cap'] for i in (6, 9, 10)] == [3, 3, 1]
    assert [one[2047 ^ (1 << i)]['low_cap'] for i in (0, 1, 5)] == [2, 2, 3]
    r = c['central_mixed_bound']
    rest = r['witness_base3']; labels = []
    for i in range(13):
        labels.append(rest % 3); rest //= 3
    assert rest == 0 and labels.count(0) == 1 and labels.count(2) == 3
    pools = [iter(range(1)), iter(range(1, 10)), iter(range(10, 13))]
    row = [next(pools[label]) for label in labels]
    deleted = 0
    for a, b in p25:
        deleted += row[a] == 0 or row[b] == 0 or row[a] >= 10 or row[b] >= 10
        row[a], row[b] = min(row[a], row[b]), max(row[a], row[b])
    assert deleted == r['prefix_deleted'] == 17
    assert sum((v >= 10) << i for i, v in enumerate(row[:11])) == r['high_mask'] == 1024
    assert sum((v >= 1) << i for i, v in enumerate(row[:11])) == r['nonlow_mask'] == 2045
    assert r['union_cap'] == 44 - LOWER[9] - deleted == 2
    assert all((x >> 1 & 1) <= (x >> 10 & 1) for x in z)
    assert c['minimum_candidates'] == [0, 1, 5] and c['minimum_caps'] == [2, 1, 3]
    # These minima cover every non-all-one input, so merging them finds min.
    assert all(x == 2047 or any(not (x >> i & 1) for i in (0, 1, 5)) for x in z)
    words = kernel_words()
    assert len(words) == 8
    assert [[list(p) for p in word] for word in words] == c['minimum_kernels']
    minimum = c['nullary_minimum_kernel']
    assert minimum == [[0, 5], [0, 1]]
    w = {mask(values(minimum, bits(11, x))[1:]) for x in z}
    assert sorted(w) == c['W_states'] and len(w) == 128
    for k in range(11):
        assert ((1 << k) - 1) << (10 - k) in w
    for x in z:
        after = values(minimum, bits(11, x))
        assert after[0] == min(bits(11, x))
    # Directly test the peeled construction on every original Boolean input.
    assert len(c['W_known19']) == 19
    for x in range(8192):
        row = values(p25 + minimum, bits(13, x))
        assert [row[0]] + values(c['W_known19'], row[1:11]) + row[11:] == sorted(bits(13, x))
    assert c['W_target_budget'] == 17
    return {'original_boolean_inputs': 8192, 'marked_rank_assignments': 8178,
            'Y2_states': 145, 'Z_states': 144, 'W_states': 128,
            'minimum_kernel_words': 8, 'known_sizes_Z_W': [21, 19]}


def main():
    raw = (HERE / 'certificate.json').read_bytes()
    c = json.loads(raw); fraw = (HERE / 'fixture.json').read_bytes()
    assert c['fixture_sha256'] == hashlib.sha256(fraw).hexdigest()
    result = verify(json.loads(fraw), c)
    result['endpoint_control_words'], result['active_endpoint_controls'] = check_endpoint_lemma()
    result['certificate_sha256'] = hashlib.sha256(raw).hexdigest()
    result['agent'] = 'six-sorting-1'; result['role'] = 'researcher'
    result['status'] = 'Conditional reductions checked; global gap remains open.'
    print(json.dumps(result))


if __name__ == '__main__':
    main()
