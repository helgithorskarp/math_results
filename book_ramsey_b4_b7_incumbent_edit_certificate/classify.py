"""Complete exact edit-ball enumeration by repairing a current forbidden book.

No solver or symmetry quotient is used. See README.md for the coverage proof.
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


def load(path):
    data = json.loads(Path(path).read_text())
    n = data['n']
    assert n == 21
    red = [tuple(e) for e in data['red_edges']]
    assert len(set(red)) == len(red)
    assert all(0 <= u < v < n for u, v in red)
    return n, set(red)


def run(path, radius):
    n, red = load(path)
    edges = list(itertools.combinations(range(n), 2))
    index = {e: i for i, e in enumerate(edges)}
    rows = [0] * n
    for u, v in red:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    full = (1 << n) - 1
    counts = collections.Counter()
    valid = set()

    def flip(i):
        u, v = edges[i]
        rows[u] ^= 1 << v
        rows[v] ^= 1 << u

    def forbidden_book():
        for u, v in edges:
            color = (rows[u] >> v) & 1
            common = rows[u] & rows[v] if color else (
                full & ~(rows[u] | rows[v] | (1 << u) | (1 << v)))
            size = 4 if color else 7
            if common.bit_count() >= size:
                pages = []
                for w in range(n):
                    if (common >> w) & 1:
                        pages.append(w)
                    if len(pages) == size:
                        break
                return sorted([index[(u, v)]] + [
                    index[tuple(sorted((x, w)))]
                    for x in (u, v) for w in pages])
        return None

    def visit(chosen, excluded):
        counts['nodes'] += 1
        book = forbidden_book()
        if book is None:
            key = tuple(sorted(chosen))
            assert key not in valid, 'Duplicate search coverage'
            valid.add(key)
            counts[f'valid{len(chosen)}'] += 1
            if len(chosen) == radius:
                return
            options = [i for i in range(len(edges))
                       if i not in chosen and not (excluded >> i) & 1]
        else:
            if len(chosen) == radius:
                counts['book_at_budget'] += 1
                return
            options = [i for i in book
                       if i not in chosen and not (excluded >> i) & 1]
            if not options:
                counts['book_no_repair'] += 1
                return
        # Child j contains option j and excludes every earlier option.
        # The children therefore partition the admissible strict supersets.
        for i in options:
            flip(i)
            visit(chosen + (i,), excluded)
            flip(i)
            excluded |= 1 << i

    visit((), 0)
    ordered = [list(k) for k in sorted(valid, key=lambda k: (len(k), k))]
    digest = hashlib.sha256(json.dumps(ordered, separators=(',', ':')).encode()).hexdigest()
    return {'complete': True, 'radius': radius, 'counts': dict(counts),
            'valid_edge_index_sets': ordered, 'valid_sets_sha256': digest}


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
