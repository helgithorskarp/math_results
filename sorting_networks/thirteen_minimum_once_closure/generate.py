"""Exact finite unary-minimum closures; one CPU, standard library only.
Author: six-sorting-1, researcher. No horizon on nonkernel events.
"""
import argparse
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
PAIRS = tuple(itertools.combinations(range(11), 2))
CAPS = {0: 3, 1: 1, 5: 3}

def kernels():
    result = []

    def visit(occupied, depths, word):
        if len(occupied) == 3:
            remaining = {0: 2, 1: 1, 5: 2}
        else:
            remaining = {i: len(occupied) - 1 for i in CAPS}
        if any(depths[i] + remaining[i] > CAPS[i] for i in CAPS):
            return
        if len(occupied) == 1:
            assert list(occupied) == [0]
            result.append(word)
            return
        assert len(word) <= 3
        for a, b in PAIRS:
            support = occupied.get(a, 0) | occupied.get(b, 0)
            if not support:
                continue
            new_depths = {i: depths[i] + bool(support >> i & 1) for i in CAPS}
            if any(new_depths[i] > CAPS[i] for i in CAPS):
                continue
            new = dict(occupied)
            new[a] = support
            new.pop(b, None)
            visit(new, new_depths, word + [list((a, b))])

    visit({i: 1 << i for i in CAPS}, {i: 0 for i in CAPS}, [])
    return result

def canonical(rows):
    strongest = {}
    for mask, deleted in rows:
        if deleted > 9:
            return None
        strongest[mask] = max(deleted, strongest.get(mask, deleted))
    # A comparator has fibers of size at most2 on two-marker rows. Every
    # member of a two-row fiber touches a marker, hence pays one deletion.
    # Thus sum(2**D) cannot decrease: 2**(max(D1,D2)+1)
    # >=2**D1+2**D2. A sorted two-marker image has one row andD<=9
    # by S11=35 at fullbudget44, so its weight is at most512.
    if sum(1 << deleted for deleted in strongest.values()) > 512:
        return None
    return tuple(sorted((mask << 4) | deleted for mask, deleted in strongest.items()))

def step(state, gate):
    a, b = gate
    A, B = 1 << a, 1 << b
    rows = []
    for entry in state:
        mask, deleted = entry >> 4, entry & 15
        deleted += bool(mask & (A | B))
        if mask & B and not mask & A:
            mask ^= A | B
        rows.append((mask, deleted))
    return canonical(rows)


def initial_profiles(fixture):
    result = {}
    for case in (1, 2):
        rows = []
        prefix = fixture['prefix21'] + fixture['tournaments'][str(case)]
        for a, b in itertools.combinations(range(13), 2):
            mask = 8191 ^ (1 << a) ^ (1 << b)
            deleted = 0
            for i, j in prefix:
                A, B = mask >> i & 1, mask >> j & 1
                deleted += not (A and B)
                if A > B:
                    mask ^= (1 << i) | (1 << j)
            rows.append((8191 ^ mask, deleted))
        result[case] = canonical(rows)
    assert result[1] == result[2]
    assert result[1] == canonical(fixture['initial_two_minimum_profile'])
    return result[1]


def close(index, word, initial):
    start = time.monotonic()
    positions = [0, 1, 5]
    allowed = []
    for gate in word:
        allowed.append(tuple(pair for pair in PAIRS if not set(pair).intersection(positions)))
        positions = [gate[0] if position in gate else position for position in positions]
    assert positions == [0, 0, 0]
    known = [set() for depth in range(len(word) + 1)]
    known[0].add(initial)
    queue = deque([(0, initial)])
    unique = 1
    edges = rejected = 0
    while queue:
        assert unique <= 50000 and time.monotonic() - start <= 45, 'Operational budget reached; closure is incomplete'
        depth, state = queue.popleft()
        assert depth < len(word), 'A terminal survived; the exclusion is false'
        events = [(depth + 1, tuple(word[depth]))] + [(depth, gate) for gate in allowed[depth]]
        for child, gate in events:
            edges += 1
            new = step(state, gate)
            if new is None:
                rejected += 1
            elif new not in known[child]:
                known[child].add(new)
                queue.append((child, new))
                unique += 1
    digest = hashlib.sha256()
    for depth, states in enumerate(known):
        for state in sorted(states):
            digest.update(json.dumps([depth, state], separators=(',', ':')).encode())
    return {'index': index, 'word': word, 'states': unique, 'edges': edges,
            'rejected': rejected, 'depth_counts': {str(depth): len(rows) for depth, rows in enumerate(known) if rows},
            'state_sha256': digest.hexdigest()}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    p.add_argument('--index', type=int, help='Check a single original kernel index')
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    start = time.monotonic()
    raw = (HERE / 'fixture.json').read_bytes()
    fixture = json.loads(raw)
    certificate = json.loads((HERE / 'certificate.json').read_text()) if args.check else None
    if certificate:
        assert certificate['fixture_sha256'] == hashlib.sha256(raw).hexdigest()
    initial = initial_profiles(fixture)
    words = kernels()
    assert len(words) == 154 and sum(len(word) == 2 for word in words) == 1
    expected = {record['index']: record for record in certificate['closures']} if certificate else {}
    records = []
    for index, word in enumerate(words):
        if len(word) == 2 or args.index is not None and index != args.index:
            continue
        record = close(index, word, initial)
        if certificate:
            assert record == expected[index], (index, record, expected[index])
        records.append(record)
        if len(records) % 25 == 0:
            print(json.dumps({'kernels_complete': len(records)}), flush=True)
    assert records
    if args.index is None:
        assert len(records) == 153
    summary = {'agent': 'six-sorting-1', 'role': 'researcher',
               'fixture_sha256': hashlib.sha256(raw).hexdigest(), 'closures': records,
               'total_states': sum(record['states'] for record in records),
               'total_edges': sum(record['edges'] for record in records),
               'elapsed_seconds': time.monotonic() - start,
               'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'status': 'All selected exact closures exhausted with no surviving terminal.'}
    if args.out:
        args.out.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({key: value for key, value in summary.items() if key != 'closures'}))


if __name__ == '__main__':
    main()
