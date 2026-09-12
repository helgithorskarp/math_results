"""Exhaustive six-vertex control of the implementation, not an R55 result.

Direct forbidden-five masks supply a separate check from the normalization's
common-neighborhood triangle search. Includes a nontrivial hand-checkable map.
"""

if not __debug__:
    raise RuntimeError('Run this research program without -O or -OO; its exact checks require assertions.')
from itertools import combinations
import json
from normalize import normalize


def main():
    n = 6
    pairs = list(combinations(range(n), 2))
    index = {e: k for k, e in enumerate(pairs)}
    masks = [sum(1 << index[e] for e in combinations(S, 2)) for S in combinations(range(n), 5)]
    selected = [(0, 1), (0, 5)]
    mutable_mask = sum(1 << index[e] for e in selected)

    def good(bits):
        return all(0 < bits & mask < mask for mask in masks)

    def verify(before, after, record):
        assert good(before) and good(after)
        assert (before ^ after) & ~mutable_mask == 0
        assert after & ~before == 0
        kept = {tuple(row['edge']): tuple(row['witness']) for row in record['kept']}
        assert len(kept) == len(record['kept'])
        for e in selected:
            if after >> index[e] & 1:
                S = kept[e]
                assert len(set(S)) == 3 and not set(S) & set(e)
                assert all(not (after >> index[p] & 1) for p in combinations(sorted(e + S), 2) if p != e)
                assert not good(after & ~(1 << index[e]))
        current = before
        for e in record['deleted']:
            assert e in selected and current >> index[e] & 1
            current &= ~(1 << index[e])
            assert good(current)
        assert current == after

    valid = changed = deletions = retained_red = 0
    for bits in range(1 << len(pairs)):
        if not good(bits):
            continue
        a = [[0] * n for _ in range(n)]
        for k, (u, v) in enumerate(pairs):
            a[u][v] = a[v][u] = bits >> k & 1
        b, record = normalize(a, selected)
        output = sum(b[u][v] << k for k, (u, v) in enumerate(pairs))
        verify(bits, output, record)
        valid += 1
        changed += int(output != bits)
        deletions += len(record['deleted'])
        retained_red += len(record['kept'])

    # Blue K5 minus 01 on 0..4; all edges to vertex 5 red. The map keeps
    # 01, with witness 234, and deletes 05. Its frame outside E is unchanged.
    start = sum(1 << index[e] for e in pairs if 5 in e or e == (0, 1))
    a = [[0] * n for _ in range(n)]
    for k, (u, v) in enumerate(pairs):
        a[u][v] = a[v][u] = start >> k & 1
    b, record = normalize(a, selected)
    output = sum(b[u][v] << k for k, (u, v) in enumerate(pairs))
    assert record == {'deleted': [(0, 5)], 'kept': [{'edge': (0, 1), 'witness': (2, 3, 4)}]}
    verify(start, output, record)
    rejected = 0
    for damaged_output, damaged_record in [
        (output & ~(1 << index[(0, 1)]), record),
        (output, {'deleted': [(0, 5)], 'kept': []}),
        (output, {'deleted': [(0, 5)], 'kept': [{'edge': (0, 1), 'witness': (2, 3, 5)}]}),
    ]:
        try:
            verify(start, damaged_output, damaged_record)
        except (AssertionError, KeyError):
            rejected += 1
    assert rejected == 3
    result = {'status': 'VERIFIED_NORMALIZATION_IMPLEMENTATION_CONTROLS', 'all_six_vertex_colorings': 1 << len(pairs), 'good_six_vertex_colorings': valid, 'changed': changed, 'red_deletions': deletions, 'kept_critical_red_edges': retained_red, 'negative_controls_rejected': rejected, 'fixture': {'before_red_bits': start, 'after_red_bits': output, 'record': record}, 'original_43_decisions': 0, 'scope': 'Implementation control only; universal same-ID completeness uses PROOF.md.'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
