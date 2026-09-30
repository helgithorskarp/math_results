"""Own Python point-partition reference, attributed reuse from source d408e72d803d58e8d07b3f42e6b138fd68f0afbe.
"""
import time
from collections import Counter
from exact import insist, bits, mask, pairs

def point_first_covers(required, columns, cap=200000, seconds=10):
    """Partition one point's neighbors first; memoize complete residual pair-cover suffixes."""
    required = tuple(sorted(required))
    insist(len(required) == len(set(required)), 'duplicate required pair')
    insist(len(columns) == len(set(columns)) and all(w.bit_count() == 4 for w in columns), 'column domain')
    required_set = set(required)
    insist(all(pairs(w) <= required_set for w in columns), 'column outside pair universe')
    if not required:
        return [()], {'point': None, 'partition_states': 0, 'residual_states': 0, 'memo_hits': 0, 'complete_point_partitions': 1}
    index = {p: i for i, p in enumerate(required)}
    row_words = [sum(1 << index[p] for p in pairs(w)) for w in columns]
    row_columns = [0] * len(required)
    for i, word in enumerate(row_words):
        for row in bits(word):
            row_columns[row] |= 1 << i
    conflicts = [0] * len(columns)
    for i, word in enumerate(row_words):
        for row in bits(word):
            conflicts[i] |= row_columns[row]
    vertices = sorted({z for p in required for z in p})
    neighbors = {z: mask(y if x == z else x for x, y in required if z in (x, y)) for z in vertices}
    point = min(vertices, key=lambda z: (neighbors[z].bit_count(), sum(w >> z & 1 for w in columns), z))
    if neighbors[point].bit_count() % 3:
        return [], {'point': point, 'partition_states': 0, 'residual_states': 0,
                    'memo_hits': 0, 'complete_point_partitions': 0}
    tails = [(w ^ 1 << point, i) for i, w in enumerate(columns) if w >> point & 1]
    tail_at = {z: [(tail, i) for tail, i in tails if tail >> z & 1] for z in bits(neighbors[point])}
    started = time.monotonic()
    counts = {'point': point, 'partition_states': 0, 'residual_states': 0, 'memo_hits': 0, 'complete_point_partitions': 0}
    cache, answers = {}, []

    def guard():
        if counts['partition_states'] + counts['residual_states'] > cap or time.monotonic() - started > seconds:
            raise RuntimeError('INCOMPLETE: point-first cover guard')

    def suffix(rows, active):
        counts['residual_states'] += 1
        guard()
        if not rows:
            return ((),)
        if rows in cache:
            counts['memo_hits'] += 1
            return cache[rows]
        best = None
        for row in bits(rows):
            choices = row_columns[row] & active
            if not choices:
                cache[rows] = ()
                return ()
            candidate = (choices.bit_count(), -row, choices)
            if best is None or candidate < best:
                best = candidate
        choices = best[2]
        out = []
        for i in bits(choices):
            insist(row_words[i] & rows == row_words[i], 'used pair in active column')
            for rest in suffix(rows ^ row_words[i], active & ~conflicts[i]):
                out.append(tuple(sorted((i,) + rest)))
        cache[rows] = tuple(out)
        return cache[rows]

    def partition(remaining, chosen, rows, active):
        counts['partition_states'] += 1
        guard()
        if not remaining:
            counts['complete_point_partitions'] += 1
            for rest in suffix(rows, active):
                answers.append(tuple(sorted(chosen + rest)))
            return
        z = (remaining & -remaining).bit_length() - 1
        for tail, i in tail_at[z]:
            if tail & remaining == tail:
                insist(active >> i & 1, 'disjoint tails have conflicting pair sets')
                partition(remaining ^ tail, chosen + (i,), rows ^ row_words[i], active & ~conflicts[i])

    partition(neighbors[point], (), (1 << len(required)) - 1, (1 << len(columns)) - 1)
    insist(len(answers) == len(set(answers)), 'duplicated complete cover')
    result = []
    for ids in answers:
        covered = Counter(p for i in ids for p in pairs(columns[i]))
        insist(set(covered) == required_set and set(covered.values()) == {1}, 'false complete cover')
        result.append(tuple(sorted(tuple(bits(columns[i])) for i in ids)))
    return sorted(result), counts
