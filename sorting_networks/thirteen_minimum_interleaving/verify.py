"""Independent rank audit of the minimum-kernel preparation obstruction.

No generator, SAT package, or packed Boolean execution is imported.
Kernel coverage follows the closed classification explained in the report.
Author: six-sorting-1, researcher.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent


def classification():
    answer = [(('pure', 0), [(0, 5), (0, 1)])]
    empty = (2, 3, 4, 6, 7, 8, 9, 10)
    for p in empty:
        answer.append((('unary0', p), [(0, p), (0, 5), (0, 1)]))
        m = min(p, 5)
        answer.append((('unary5', p), [tuple(sorted((p, 5))), (0, m), (0, 1)]))
    for p in range(2, 11):
        answer.append((('joint', p), [(0, 5), (0, p), (0, 1)]))
    for p, q in itertools.product(empty, repeat=2):
        answer.append((('both0first', p, q),
                       [(0, p), tuple(sorted((q, 5))), (0, min(q, 5)), (0, 1)]))
    for q in empty:
        m = min(q, 5)
        for p in range(2, 11):
            if p == m:
                continue
            answer.append((('both5first', p, q),
                           [tuple(sorted((q, 5))), (0, p), (0, m), (0, 1)]))
    assert len(answer) == 154 and len({tuple(w) for _, w in answer}) == 154
    assert Counter(len(w) for _, w in answer) == {2: 1, 3: 25, 4: 128}
    return answer


def simulate(values, word, count_low=False, low_count=2):
    v = list(values)
    hits = 0
    for a, b in word:
        if count_low:
            hits += v[a] < low_count or v[b] < low_count
        if v[a] > v[b]:
            v[a], v[b] = v[b], v[a]
    return v, hits


def rank_bases(p24):
    result = []
    for a, b in itertools.combinations(range(13), 2):
        others = [i for i in range(13) if i not in (a, b)]
        order = [a, b] + others
        ranks = [0] * 13
        for rank, wire in enumerate(order):
            ranks[wire] = rank
        out, deleted = simulate(ranks, p24, True)
        result.append((out, deleted, (a, b)))
    assert len(result) == 78
    return result


def check_rank_profile(base, word, budget=44, require_obstruction=True):
    caps = {}
    for values, previous, _ in base:
        out, deleted = simulate(values, word, True)
        assert out[0] == 0 and out[11:] == [11, 12]
        leaf = out.index(1) - 1
        assert 0 <= leaf < 10
        cap = budget - 35 - previous - deleted
        caps[leaf] = min(cap, caps.get(leaf, cap))
    assert caps and min(caps.values()) >= 0
    exponent = max(caps.values())
    numerator = sum(2 ** (exponent - cap) for cap in caps.values())
    if require_obstruction:
        assert numerator > 2 ** exponent, (word, caps)
    return numerator, 2 ** exponent, tuple(sorted(caps.items()))


def placements(word):
    # Individual zero trajectories supply occupancy, unlike the generator's
    # support-mask recurrence. Each inserted gate must be nonkernel.
    positions = [0, 1, 5]
    for slot, (a, b) in enumerate(word):
        for c, d in itertools.combinations(range(11), 2):
            if c not in positions and d not in positions:
                yield word[:slot] + [(c, d)] + word[slot:]
        positions = [a if p in (a, b) else p for p in positions]
    assert positions == [0, 0, 0]


def main():
    start = time.monotonic()
    raw = (HERE / 'fixture.json').read_bytes()
    f = json.loads(raw)
    certificate = json.loads((HERE / 'certificate.json').read_text())
    assert certificate['fixture_sha256'] == hashlib.sha256(raw).hexdigest()
    assert f['full_budget'] == 44 and f['Y_budget'] == 20
    assert f['known_sizes'] == {'11': 35, '12': 39}
    assert f['conditional_minimum1_passages'] == 1
    words = sorted(classification(), key=lambda r: r[1])
    assert [word for _, word in words] == [[tuple(pair) for pair in word]
                                         for word in certificate['kernels']]
    full_inputs = rank_assignments = prefix_count = front_count = 0
    single_minimum_checks = positive_inputs = negative_controls = 0
    bounds = Counter()
    fingerprints = hashlib.sha256()
    for case in (1, 2):
        p24 = f['prefix21'] + f['tournaments'][str(case)]
        assert len(p24) == 24 and all(0 <= a < b < 13 for a, b in p24)
        image = set()
        for x in range(8192):
            values = [int(bool(x & (1 << i))) for i in range(13)]
            out, _ = simulate(values, p24)
            assert out[11:] == sorted(values)[-2:]
            image.add(sum(out[i] << i for i in range(11)))
            full_inputs += 1
        assert image == set(f['Y_states'][str(case)])
        assert all(x == 2047 or any(not (x >> i & 1) for i in (0, 1, 5)) for x in image)
        assert {i for i in range(11) if 2047 ^ (1 << i) in image} == {0, 1, 5}
        for leaf in (0, 1, 5):
            mask = f['single_minimum_witnesses'][str(leaf)]
            marked = [i for i in range(13) if not (mask >> i & 1)]
            assert len(marked) == 1
            order = marked + [i for i in range(13) if i not in marked]
            ranks = [0] * 13
            for rank, position in enumerate(order):
                ranks[position] = rank
            out, D = simulate(ranks, p24, True, 1)
            assert out.index(0) == leaf
            assert 44 - 39 - D == (2 if leaf == 1 else 3)
            single_minimum_checks += 1
        # Duplicate the first comparator of the known21 suffix and commute
        # its (0,1) forward. This valid22 suffix has an early unary kernel,
        # showing why the stated budget20 hypothesis is essential.
        known = [tuple(g) for g in f['known21_suffix']]
        assert known[:4] == [(0, 5), (3, 8), (4, 7), (0, 1)]
        controls = [known, [(0, 5), (0, 5), (0, 1), (3, 8), (4, 7)] + known[4:]]
        for control in controls:
            for x in range(8192):
                values = [int(bool(x & (1 << i))) for i in range(13)]
                out, _ = simulate(values, p24 + control)
                assert out == sorted(values)
                positive_inputs += 1
        base = rank_bases(p24)
        early = [(0, 5), (0, 5), (0, 1)]
        n, d, _ = check_rank_profile(base, early, budget=46, require_obstruction=False)
        assert n <= d
        try:
            check_rank_profile(base, early, budget=46)
        except AssertionError:
            negative_controls += 1
        else:
            raise AssertionError('Weakened pruning bound was accepted as an obstruction')
        for kind, word in words:
            # Three independent one-zero executions verify caps and the
            # final root; monotonicity extends it to all proper Y rows.
            for i, cap in ((0, 3), (1, 1), (5, 3)):
                row = [1] * 11
                row[i] = 0
                hits = 0
                for a, b in word:
                    hits += row[a] == 0 or row[b] == 0
                    if row[a] > row[b]:
                        row[a], row[b] = row[b], row[a]
                assert row == [0] + [1] * 10 and hits <= cap
            if kind[0] == 'pure':
                continue
            for prefix in itertools.chain((word,), placements(word)):
                n, d, caps = check_rank_profile(base, prefix)
                bounds[n, d] += 1
                front_count += prefix == word
                prefix_count += 1
                rank_assignments += 78
                fingerprints.update(json.dumps([case, prefix, caps], separators=(',', ':')).encode())
    assert front_count == 306 and prefix_count - front_count == 35464
    histogram = {f'{n}/{d}': v for (n, d), v in sorted(bounds.items())}
    assert histogram == certificate['Kraft_histogram']
    assert fingerprints.hexdigest() == certificate['profile_digest_sha256']
    assert rank_assignments == certificate['rank_assignments_for_independent_check']
    assert all(n * 4 >= 5 * d for (n, d) in bounds)
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'fixture_sha256': hashlib.sha256(raw).hexdigest(),
              'kernels_per_case': 154, 'unary_kernels_per_case': 153,
              'front_unary_prefixes': front_count,
              'one_nonkernel_prefixes': prefix_count - front_count,
              'distinct_rank_assignments_checked': rank_assignments,
              'original_boolean_inputs_checked': full_inputs,
              'positive_control_original_inputs_checked': positive_inputs,
              'single_minimum_rank_checks': single_minimum_checks,
              'weakened_bound_negative_controls_rejected': negative_controls,
              'profile_digest_sha256': fingerprints.hexdigest(),
              'Kraft_histogram': histogram,
              'elapsed_seconds': time.monotonic() - start,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'status': 'Independent scalar/rank obstruction passed; written classification and S11=35 remain separate mathematical dependencies.'}
    print(json.dumps(result))


if __name__ == '__main__':
    main()
