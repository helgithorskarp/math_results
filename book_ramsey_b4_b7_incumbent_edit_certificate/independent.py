"""Independent edit-ball enumeration from fixed baseline near-book clauses.

Uses sets of edges to check graphs, rather than bit-intersection codegrees.
Only books with exactly one wrong baseline edge are used to prune the tree.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import resource
import sys
import time

if not __debug__:
    raise SystemExit('Run with Python assertions enabled, without -O')


def run(path, radius):
    data = json.loads(Path(path).read_text())
    n = data['n']
    assert n == 21
    base = set(map(tuple, data['red_edges']))
    assert len(base) == len(data['red_edges'])
    assert all(0 <= u < v < n for u, v in base)
    edges = list(itertools.combinations(range(n), 2))
    index = {e: i for i, e in enumerate(edges)}
    clauses = [set() for _ in edges]

    def edge(u, v):
        return tuple(sorted((u, v)))

    def install(spine, pages, color):
        pairs = [spine] + [edge(x, w) for x in spine for w in pages]
        wrong = [e for e in pairs if int(e in base) != color]
        assert len(wrong) == 1
        support = sum(1 << index[e] for e in pairs if e != wrong[0])
        clauses[index[wrong[0]]].add(support)

    for u, v in edges:
        for color, size in [(1, 4), (0, 7)]:
            common = [w for w in range(n) if w not in (u, v)
                      and int(edge(u, w) in base) == color
                      and int(edge(v, w) in base) == color]
            if int((u, v) in base) != color:
                for pages in itertools.combinations(common, size):
                    install((u, v), pages, color)
            elif len(common) == size - 1:
                for w in range(n):
                    if w not in (u, v) and sum(
                            int(edge(x, w) in base) == color for x in (u, v)) == 1:
                        install((u, v), common + [w], color)
    clauses = [sorted(s) for s in clauses]
    counts = collections.Counter()
    valid = set()

    def is_valid(mask):
        red = base.symmetric_difference({edges[i] for i in range(len(edges))
                                         if (mask >> i) & 1})
        for u, v in edges:
            color = int((u, v) in red)
            count = sum(int(edge(u, w) in red) == color
                        and int(edge(v, w) in red) == color
                        for w in range(n) if w not in (u, v))
            if count > (3 if color else 6):
                return False
        return True

    assert is_valid(0), 'The baseline must avoid the two books'

    def visit(chosen, mask, excluded):
        counts['nodes'] += 1
        options = None
        for i in chosen:
            for support in clauses[i]:
                if not (mask & support):
                    available = support & ~excluded
                    if options is None or available.bit_count() < options.bit_count():
                        options = available
        if options is None:
            if is_valid(mask):
                key = tuple(sorted(chosen))
                assert key not in valid, 'Duplicate search coverage'
                valid.add(key)
                counts[f'valid{len(chosen)}'] += 1
            else:
                counts['full_check_invalid'] += 1
            if len(chosen) == radius:
                return
            options = ((1 << len(edges)) - 1) & ~(excluded | mask)
        elif len(chosen) == radius:
            counts['nearbook_at_budget'] += 1
            return
        elif options == 0:
            counts['nearbook_no_repair'] += 1
            return
        while options:
            bit = options & -options
            options ^= bit
            i = bit.bit_length() - 1
            visit(chosen + (i,), mask | bit, excluded)
            excluded |= bit

    visit((), 0, 0)
    ordered = [list(k) for k in sorted(valid, key=lambda k: (len(k), k))]
    digest = hashlib.sha256(json.dumps(ordered, separators=(',', ':')).encode()).hexdigest()
    return {'complete': True, 'radius': radius,
            'nearbook_clauses': sum(map(len, clauses)),
            'counts': dict(counts), 'valid_edge_index_sets': ordered,
            'valid_sets_sha256': digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('h21.json'))
    parser.add_argument('--radius', type=int, default=7)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not 0 <= args.radius <= 7:
        parser.error('This bounded artifact supports radii 0 through 7')
    started = time.perf_counter()
    result = run(args.input, args.radius)
    result.update(seconds=time.perf_counter() - started,
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  python=sys.version)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
