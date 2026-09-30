"""Complete sharing-graph census for the classical S(3,5,17)."""
from itertools import combinations
from collections import Counter
from pathlib import Path
import json
from steiner import classical_design, orbit_summary
from hashlib import sha256
from math import comb
import argparse

if not __debug__:
    raise RuntimeError('run the verifier with assertions enabled, without -O')


def reproduce():
    design = classical_design()
    index = {tuple(t): i for i, c in enumerate(design)
             for t in combinations([p for p in range(17) if c >> p & 1], 3)}
    q = []
    blockers = []
    contained = 0
    for points in combinations(range(17), 4):
        targets = {index[t] for t in combinations(points, 3)}
        if len(targets) == 1:
            contained += 1
            continue
        assert len(targets) == 4
        q.append(sum(1 << p for p in points))
        blockers.append(sum(1 << i for i in targets))
    adjacency = [0] * len(q)
    pair_histogram = Counter()
    for i, j in combinations(range(len(q)), 2):
        if (q[i] & q[j]).bit_count() > 1:
            continue
        shared = (blockers[i] & blockers[j]).bit_count()
        assert shared <= 1
        pair_histogram[shared] += 1
        if shared:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    counts = Counter()
    first = {}
    small_examples = {}
    common_point_histogram = Counter()
    linear_five_extensions_with9_shared_blocks = 0
    all_bits = (1 << len(q)) - 1

    def build_example(ids):
        removed = 0
        for i in ids:
            removed |= blockers[i]
        words = [c for i, c in enumerate(design) if not (removed >> i & 1)]
        words += [(1 << 17) | q[i] for i in ids]
        assert all((a & b).bit_count() <= 2 for a, b in combinations(words, 2))
        return {'old_4subsets': [q[i] for i in ids], 'deleted_blocks': removed.bit_count(),
                'resulting_code_size': len(words)}

    def extend(ids, candidates):
        nonlocal linear_five_extensions_with9_shared_blocks
        depth = len(ids)
        if depth >= 2:
            counts[depth] += 1
            first.setdefault(depth, ids)
        assert depth < 5, 'a five-clique contradicts the stated census'
        if depth == 4:
            common = q[ids[0]]
            for i in ids[1:]:
                common &= q[i]
            common_point_histogram[common.bit_count()] += 1
            # Count K5 minus one edge, with all old four-subsets mutually linear.
            for subset in combinations(ids, 3):
                available = all_bits
                for i in subset:
                    available &= adjacency[i]
                while available:
                    bit = available & -available
                    available ^= bit
                    extra = bit.bit_length() - 1
                    if extra in ids or any((q[extra] & q[i]).bit_count() > 1 for i in ids):
                        continue
                    example = build_example(ids + (extra,))
                    if example['deleted_blocks'] == 11:
                        linear_five_extensions_with9_shared_blocks += 1
            if 5 not in small_examples:
                for subset in combinations(ids, 2):
                    available = adjacency[subset[0]] & adjacency[subset[1]]
                    while available:
                        bit = available & -available
                        available ^= bit
                        extra = bit.bit_length() - 1
                        if extra in ids or any((q[extra] & q[i]).bit_count() > 1 for i in ids):
                            continue
                        example = build_example(ids + (extra,))
                        if example['deleted_blocks'] == 12:
                            small_examples[5] = example
                            break
                    if 5 in small_examples:
                        break
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            i = bit.bit_length() - 1
            extend(ids + (i,), candidates & adjacency[i])

    extend((), all_bits)
    for depth, ids in first.items():
        small_examples[depth] = build_example(ids)
    small_examples[1] = build_example((0,))
    result = {'contained_4subsets': contained, 'noncontained_4subsets': len(q),
              'compatible_pair_shared_block_histogram': dict(pair_histogram),
              'sharing_graph_degree_histogram': dict(Counter(x.bit_count() for x in adjacency)),
              'sharing_cliques_by_size': {i: counts[i] for i in range(2, 6)},
              'small_t_examples': small_examples,
              'four_clique_common_point_histogram': dict(common_point_histogram),
              'linear_five_extensions_with9_shared_blocks': linear_five_extensions_with9_shared_blocks,
              'steiner_design_blocks': len(design),
              'covered_old_triples': len(index),
              'design_sha256': sha256(','.join(map(str, design)).encode()).hexdigest(),
              'C5_model': orbit_summary(design)}
    # Integer check of the algebraic identity; the unbounded proof is in PROOF.md.
    for k in range(5, 101):
        for m in range(3, k-1):
            assert comb(k-2,3)+1-comb(m,3)-comb(k-m+1,3) == (k-1)*(m-3)*(k-2-m)//2
    assert counts[4] == 4080 and linear_five_extensions_with9_shared_blocks == 0
    return json.loads(json.dumps(result))


def check_candidate(path):
    design = set(classical_design())
    lines = Path(path).read_text().splitlines()
    if not lines or any(len(s) != 18 or set(s) - {'0', '1'} or s.count('1') != 5 for s in lines):
        raise ValueError('expected nonempty file of weight-five 18-bit strings')
    words = [sum(1 << i for i, x in enumerate(s) if x == '1') for s in lines]
    if len(set(words)) != len(words):
        raise ValueError('duplicate words')
    if any((a & b).bit_count() > 2 for a, b in combinations(words, 2)):
        raise ValueError('minimum distance less than six')
    R = len(design - set(words))
    s = sum(not (b >> 17 & 1) and b not in design for b in words)
    a = t = 0
    for b in words:
        if b >> 17 & 1:
            q = b ^ (1 << 17)
            contained = any(q & c == q for c in design)
            a += contained
            t += not contained
    local_bound = max(2*t, 4*t-t*(t-1)//2)
    if t == 5:
        local_bound = 12
    assert R >= a + local_bound
    assert len(words) <= 68+s+t-local_bound
    return {'words': len(words), 'R': R, 's': s, 'a': a, 't': t,
            'conditional_upper_bound': 68+s+t-local_bound}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='print exact report without comparing expected.json')
    parser.add_argument('--check-code', help='independently validate a file of 18-bit words and count trade parameters')
    args = parser.parse_args()
    report = reproduce()
    if not args.emit:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        if report != expected:
            raise ValueError('reproduction disagrees with expected.json')
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.check_code:
        print(json.dumps(check_candidate(args.check_code), sort_keys=True))


if __name__ == '__main__':
    main()
