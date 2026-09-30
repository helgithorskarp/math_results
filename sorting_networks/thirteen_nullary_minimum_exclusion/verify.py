"""Independent scalar/rank and complete merge-history audit.

No generator, encoder, solver or proof checker is imported. Mathematical
Kraft, pruning, nonredundancy and commutation arguments are in PROOF.md.
"""
import collections
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent


def run(values, word):
    values = list(values)
    for a, b in word:
        assert 0 <= a < b < len(values)
        values[a], values[b] = min(values[a], values[b]), max(values[a], values[b])
    return values


def bits(x, n):
    return [x >> i & 1 for i in range(n)]


def mask(values):
    return sum(v << i for i, v in enumerate(values))


def one_rank(original, word, high, lower):
    chosen = [i for i in range(13) if bool(original >> i & 1) == high]
    other = [i for i in range(13) if i not in chosen]
    order = other + chosen if high else chosen + other
    values = [None] * 13
    for rank, i in enumerate(order):
        values[i] = rank
    marked = set(range(13 - len(chosen), 13)) if high else set(range(len(chosen)))
    removed = 0
    for a, b in word:
        removed += values[a] in marked or values[b] in marked
        values[a], values[b] = min(values[a], values[b]), max(values[a], values[b])
    flags = [int(v in marked if high else v not in marked) for v in values]
    return flags, 44 - lower[13 - len(chosen)] - removed


def two_rank(code, word, lower):
    colors = []
    for _ in range(13):
        colors.append(code % 3); code //= 3
    assert code == 0 and colors.count(0) == colors.count(2) == 3 and colors.count(1) == 7
    pools = [iter(range(3)), iter(range(3, 10)), iter(range(10, 13))]
    values = [next(pools[color]) for color in colors]
    removed = 0
    for a, b in word:
        removed += values[a] < 3 or values[b] < 3 or values[a] >= 10 or values[b] >= 10
        values[a], values[b] = min(values[a], values[b]), max(values[a], values[b])
    return values, [int(v >= 10) for v in values], [int(v >= 3) for v in values], 44 - lower[7] - removed


def signature(word):
    support = {i: 1 << i for i in (0, 1, 2, 3, 4, 6, 7)}
    depths = {i: 0 for i in support}; clades = []
    for a, b in word:
        assert a < b and a in support and b in support
        merged = support[a] | support[b]
        for i in depths:
            depths[i] += bool(merged >> i & 1)
        clades.append(merged); support[a] = merged; del support[b]
    assert list(support) == [0]
    return tuple(sorted(clades)), depths


def check_histories(words):
    representatives = {}
    for word in words:
        sig, depths = signature(word)
        assert depths == {i: 2 if i == 0 else 3 for i in depths}
        assert sig not in representatives
        representatives[sig] = list(map(tuple, word))
    histories = accepted = 0; seen = set()
    def visit(occupied, word):
        nonlocal histories, accepted
        if len(occupied) == 1:
            histories += 1
            sig, depths = signature(word)
            if all(depths[i] <= (2 if i == 0 else 3) for i in depths):
                accepted += 1; seen.add(sig)
                current = list(word)
                for t, desired in enumerate(representatives[sig]):
                    k = current.index(desired, t)
                    while k > t:
                        assert set(current[k]).isdisjoint(current[k - 1])
                        current[k - 1], current[k] = current[k], current[k - 1]; k -= 1
                assert current == representatives[sig]
            return
        for a, b in itertools.combinations(occupied, 2):
            visit([i for i in occupied if i != b], word + [(a, b)])
    visit([0, 1, 2, 3, 4, 6, 7], [])
    assert histories == 56700 and accepted == 900 and seen == set(representatives) and len(seen) == 45
    return histories, accepted


def main():
    start = time.monotonic()
    f = json.loads((HERE / 'fixture.json').read_text())
    raw = (HERE / 'certificate.json').read_bytes(); c = json.loads(raw)
    lower = f['known_lower_bounds']
    assert lower == [0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35, 39, 44]
    words = f['minimum_words_on_V']; counts = collections.Counter()
    counts['binary_merge_histories'], counts['feasible_merge_histories'] = check_histories(words)
    U, F, prefixes = {}, {}, {}
    for case in (1, 2):
        p26 = f['prefix21'] + f['tournaments'][case - 1] + f['minimum_front']
        assert len(p26) == 26
        V = {mask(run(bits(x, 13), p26)[1:11]) for x in range(8192)}
        counts['V_original_inputs'] += 8192
        leaves = [0, 1, 2, 3, 4, 6, 7]
        assert [i for i in range(10) if (1023 ^ (1 << i)) in V] == leaves
        assert all(x == 1023 or any(not (x >> i & 1) for i in leaves) for x in V)
        for leaf, original in f['V_single_minimum_witnesses'][case - 1]:
            flags, cap = one_rank(original, p26, False, lower)
            assert mask(flags[1:11]) == 1023 ^ (1 << leaf)
            assert cap == (2 if leaf == 0 else 3)
            counts['V_rank_witnesses'] += 1
        for index, word in enumerate(words):
            p32 = p26 + [[a + 1, b + 1] for a, b in word]
            p34 = p32 + [[a + 2, b + 2] for a, b in f['maximum_word_on_U']]
            us, fs = set(), set()
            for x in range(8192):
                original = bits(x, 13); a = run(original, p32); b = run(a, p34[-2:]); ordered = sorted(original)
                assert a[:2] == b[:2] == ordered[:2]
                assert a[-2:] == ordered[-2:] and b[-3:] == ordered[-3:]
                us.add(mask(a[2:11])); fs.add(mask(b[2:10])); counts['frontier_original_inputs'] += 1
            assert [i for i in range(9) if 1 << i in us] == [4, 7, 8]
            assert 510 in us and 509 in us
            assert all(x == 0 or x & ((1 << 4) | (1 << 7) | (1 << 8)) for x in us)
            assert sorted(fs) == c['F_states_by_tree'][index]
            assert all(255 ^ (255 >> k) in fs for k in range(9))
            U[case, index] = us; F[case, index] = fs; prefixes[case, index] = p32, p34
    assert len(f['U_witnesses']) == 90
    witness_keys = set()
    for w in f['U_witnesses']:
        key = w['case'], w['index']; assert key not in witness_keys; witness_keys.add(key)
        p32, p34 = prefixes[key]; us = U[key]
        reset = w['reset_row']; assert reset in us and reset.bit_count() == 2 and not (reset >> 8 & 1)
        for original, desired in zip(w['high_pair_original_masks'], (272, 384)):
            flags, cap = one_rank(original, p32, True, lower)
            assert mask(flags[2:11]) == desired and cap == 3; counts['U_high_pair_rank_witnesses'] += 1
        assert w['mixed_roots']
        for leaf, code in w['mixed_roots']:
            values, high, nonlow, cap = two_rank(code, p32, lower)
            assert values[:2] == [0, 1] and values[-2:] == [11, 12]
            assert mask(high[2:11]) == 256 and mask(nonlow[2:11]) == 511 ^ (1 << leaf) and cap == 2
            assert all((x >> leaf & 1) <= (x >> 8 & 1) for x in us)
            values, high, nonlow, cap = two_rank(code, p34, lower)
            assert values[:2] == [0, 1] and values[-3:] == [10, 11, 12]
            assert mask(high[2:10]) == 0 and mask(nonlow[2:10]) == 255 ^ (1 << leaf) and cap == 1
            counts['mixed_rank_witnesses'] += 1
    sources = {s['index']: s for s in c['sources']}
    assert len(sources) == 9
    for index, source in sources.items():
        p34 = prefixes[2, index][1]; fs = F[2, index]
        assert source['states'] == len(fs) and [r[0] for r in source['single_threshold_rows']] == sorted(fs)
        for z, hc, lc, hw, lw in source['single_threshold_rows']:
            for high, original, expected in ((True, hw, hc), (False, lw, lc)):
                flags, cap = one_rank(original, p34, high, lower)
                assert mask(flags[2:10]) == z and cap == expected; counts['F_single_rank_witnesses'] += 1
        w = next(w for w in f['U_witnesses'] if w['case'] == 2 and w['index'] == index)
        assert all(leaf == source['minimum_leaf_cap1'] for leaf, code in w['mixed_roots'])
    covered = set()
    for group in c['subsumption_cover']:
        index = group['source']; assert index in sources
        for hit in group['covered']:
            target, p = hit['target'], hit['permutation']; assert sorted(p) == list(range(8))
            image = {sum(1 << p[i] for i in range(8) if x >> i & 1) for x in F[2, index]}
            assert image <= F[2, target] and target not in covered; covered.add(target)
    assert covered == set(range(45))
    control = f['known_F38_11']; assert len(control) == 11 and len(F[2, 8]) == 38
    for case in (1, 2):
        full = prefixes[case, 8][1] + [[a + 2, b + 2] for a, b in control]
        assert len(full) == 45
        for x in range(8192):
            assert run(bits(x, 13), full) == sorted(bits(x, 13)); counts['positive_control_original_inputs'] += 1
    assert len(c['proofs']) == 9 and {p['index'] for p in c['proofs']} == set(sources)
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher', 'counts': dict(counts),
                      'certificate_sha256': hashlib.sha256(raw).hexdigest(),
                      'elapsed_seconds': time.monotonic() - start,
                      'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'status': 'Independent finite reduction audit passed; RUP exclusions are checked separately'}))


if __name__ == '__main__':
    main()
