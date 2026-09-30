"""Packed two-minimum markers and minimum-support kernel enumeration.

Author: six-sorting-1, researcher. Standard library, one process/thread.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAIRS = tuple(itertools.combinations(range(11), 2))
CAPS = {0: 3, 1: 1, 5: 3}


def kernels():
    answer = []

    def visit(occupied, depth, word):
        remaining = ({0: 2, 1: 1, 5: 2} if len(occupied) == 3 else
                     {i: len(occupied) - 1 for i in CAPS})
        if any(depth[i] + remaining[i] > CAPS[i] for i in CAPS):
            return
        if len(occupied) == 1:
            assert list(occupied) == [0]
            answer.append(word)
            return
        for a, b in PAIRS:
            support = occupied.get(a, 0) | occupied.get(b, 0)
            if not support:
                continue
            next_depth = {i: depth[i] + bool(support >> i & 1) for i in CAPS}
            if any(next_depth[i] > CAPS[i] for i in CAPS):
                continue
            next_support = dict(occupied)
            next_support[a] = support
            next_support.pop(b, None)
            visit(next_support, next_depth, word + [(a, b)])

    visit({i: 1 << i for i in CAPS}, {i: 0 for i in CAPS}, [])
    return sorted(answer)


def prefixes(word):
    yield word
    occupied = {i: 1 << i for i in CAPS}
    for slot, (a, b) in enumerate(word):
        for gate in PAIRS:
            if set(gate).isdisjoint(occupied):
                yield word[:slot] + [gate] + word[slot:]
        occupied[a] = occupied.get(a, 0) | occupied.get(b, 0)
        occupied.pop(b, None)


def execute(x, word):
    deleted = 0
    for a, b in word:
        A, B = x >> a & 1, x >> b & 1
        deleted += not (A and B)
        if A > B:
            x ^= (1 << a) | (1 << b)
    return x, deleted


def data():
    raw = (HERE / 'fixture.json').read_bytes()
    f = json.loads(raw)
    words = kernels()
    assert len(words) == 154
    histogram = Counter()
    digest = hashlib.sha256()
    front = one_preparation = 0
    for case in (1, 2):
        p24 = f['prefix21'] + f['tournaments'][str(case)]
        base = [execute(8191 ^ (1 << a) ^ (1 << b), p24)
                for a, b in itertools.combinations(range(13), 2)]
        for word in words:
            if len(word) == 2:
                continue
            for prefix in prefixes(word):
                caps = {}
                for x, D in base:
                    y, d = execute(x, prefix)
                    assert not (y & 1)
                    other = (8191 ^ y) ^ 1
                    assert other.bit_count() == 1
                    leaf = other.bit_length() - 2
                    assert 0 <= leaf < 10
                    cap = f['full_budget'] - f['known_sizes']['11'] - D - d
                    caps[leaf] = min(cap, caps.get(leaf, cap))
                assert min(caps.values()) >= 0
                power = max(caps.values())
                n, denominator = sum(1 << (power - c) for c in caps.values()), 1 << power
                assert n > denominator
                histogram[n, denominator] += 1
                front += prefix == word
                one_preparation += prefix != word
                digest.update(json.dumps([case, prefix, sorted(caps.items())],
                                         separators=(',', ':')).encode())
    assert front == 306 and one_preparation == 35464
    return {'schema': 1, 'agent': 'six-sorting-1', 'role': 'researcher',
            'fixture_sha256': hashlib.sha256(raw).hexdigest(),
            'kernels': words, 'kernel_lengths': {str(k): v for k, v in sorted(Counter(map(len, words)).items())},
            'front_unary_prefixes': front, 'one_nonkernel_prefixes': one_preparation,
            'rank_assignments_for_independent_check': 78 * (front + one_preparation),
            'profile_digest_sha256': digest.hexdigest(),
            'Kraft_histogram': {f'{n}/{d}': v for (n, d), v in sorted(histogram.items())},
            'minimum_Kraft_ratio': [5, 4],
            'claim': 'In a Y1/Y2 twenty-comparator completion with minimum1 passage count1, a unary-containing minimum kernel requires at least two nonkernel gates before its final merge. No complete Y20 or global44 exclusion.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    raw = (json.dumps(data(), indent=2) + '\n').encode()
    if args.check:
        assert (HERE / 'certificate.json').read_bytes() == raw
    else:
        (HERE / 'certificate.json').write_bytes(raw)
    print(json.dumps({'certificate_bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}))


if __name__ == '__main__':
    main()
