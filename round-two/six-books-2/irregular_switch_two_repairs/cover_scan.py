"""Independent exact scan by triangle parity and covers of original books.

This program does not import forced_scan.py or verify.py. Gray traversal
and reverse spine order differ from the first scan. See PROOF.md.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import time

N = 21
WHOLE = (1 << N) - 1
CUTS = 1 << (N - 1)
PAIRS = list(itertools.combinations(range(N), 2))
PAIR_INDEX = {pair: edge for edge, pair in enumerate(PAIRS)}
SEED_BYTES = Path(__file__).with_name('seed.txt').read_bytes()
LINES = SEED_BYTES.decode('ascii').splitlines()
if len(LINES) != N or any(len(line) != N or set(line) - {'0', '1'} for line in LINES):
    raise ValueError('Invalid 21 by 21 binary seed')
A = [[int(bit) for bit in line] for line in LINES]
if any(A[i][i] or A[i][j] != A[j][i] for i in range(N) for j in range(N)):
    raise ValueError('Seed is not a simple symmetric graph')
BASE_ROWS = [sum(1 << k for k in range(N) if A[i][k]) for i in range(N)]
PARITIES = []
for i, j in PAIRS:
    masks = [0, 0]
    for k in range(N):
        if k != i and k != j:
            masks[A[i][j] ^ A[i][k] ^ A[j][k]] |= 1 << k
    PARITIES.append(masks)
ALL_PAIRS = (1 << len(PAIRS)) - 1
NO_SECOND_EDIT = 1 << len(PAIRS)


def bit_indices(mask):
    while mask:
        bit = mask & -mask
        mask -= bit
        yield bit.bit_length() - 1


def page_mask(cut, edge):
    """Compute pages from invariant original triangle parity, not row intersections."""
    i, j = PAIRS[edge]
    zi = cut >> i & 1
    color = A[i][j] ^ zi ^ (cut >> j & 1)
    phase = cut ^ BASE_ROWS[i]
    pages = PARITIES[edge][color] & (phase if zi ^ color else WHOLE ^ phase)
    return color, pages


def book(i, j, pages, color):
    witness = 1 << PAIR_INDEX[tuple(sorted((i, j)))]
    for k in itertools.islice(bit_indices(pages), 4 if color else 7):
        witness |= 1 << PAIR_INDEX[tuple(sorted((i, k)))]
        witness |= 1 << PAIR_INDEX[tuple(sorted((j, k)))]
    return witness


def literal_valid(cut, edits):
    # Reconstruct actual red-neighbor sets; no parity/cover identity is used.
    red_neighbors = [set() for _ in range(N)]
    for edge, (i, j) in enumerate(PAIRS):
        color = A[i][j] ^ (cut >> i & 1) ^ (cut >> j & 1) ^ (edge in edits)
        if color:
            red_neighbors[i].add(j)
            red_neighbors[j].add(i)
    vertices = set(range(N))
    for i, j in reversed(PAIRS):
        if j in red_neighbors[i]:
            pages, cap = red_neighbors[i] & red_neighbors[j], 3
        else:
            pages, cap = vertices - {i, j} - red_neighbors[i] - red_neighbors[j], 6
        if len(pages) > cap:
            return False
    return True


def cover(cut, counters):
    first = None
    for edge in range(len(PAIRS) - 1, -1, -1):
        color, pages = page_mask(cut, edge)
        if pages.bit_count() > (3 if color else 6):
            first = edge
            break
    if first is None:
        counters['initially_valid'] += 1
        # No original book constrains edits, so examine every edit set literally.
        answer = [[]]
        for edge in range(len(PAIRS)):
            if literal_valid(cut, {edge}):
                answer.append([edge])
            for other in range(edge):
                if literal_valid(cut, {edge, other}):
                    answer.append([other, edge])
        return sorted(answer)
    i, j = PAIRS[first]
    color, pages = page_mask(cut, first)
    witness = book(i, j, pages, color)
    # Every repair must contain an edge of this fixed original book.
    options = {edge: (ALL_PAIRS & ~(1 << edge)) | NO_SECOND_EDIT
               for edge in bit_indices(witness)}
    for spine in range(len(PAIRS) - 1, -1, -1):
        color, pages = page_mask(cut, spine)
        cap = 3 if color else 6
        if pages.bit_count() <= cap:
            continue
        i, j = PAIRS[spine]
        for edge in list(options):
            if edge == spine:
                continue  # This edge meets every book at the current spine.
            a, b = PAIRS[edge]
            remaining = pages
            if a == i or a == j:
                remaining &= ~(1 << b)
            elif b == i or b == j:
                remaining &= ~(1 << a)
            # Removing an unrelated vertex has no effect on the page mask.
            count = remaining.bit_count()
            if count <= cap:
                continue
            allowed = ((1 << spine) if count > cap + 1
                       else book(i, j, remaining, color))
            options[edge] &= allowed
            if not options[edge]:
                del options[edge]
        if not options:
            counters['old_book_cover_reject'] += 1
            return []
    counters['cover_survivor_cuts'] += 1
    answer = set()
    for edge, mask in options.items():
        for other in bit_indices(mask):
            edits = ((edge,) if other == len(PAIRS)
                     else tuple(sorted((edge, other))))
            counters['literal_repair_tests'] += 1
            if literal_valid(cut, set(edits)):
                answer.add(edits)
    return [list(edits) for edits in sorted(answer)]


def controls():
    for cut in (0, 2, 625662, 1471282, 1633142, 1675894):
        for edge, (i, j) in enumerate(PAIRS):
            color, pages = page_mask(cut, edge)
            actual = {k for k in range(N) if k != i and k != j
                      and (A[i][k] ^ (cut >> i & 1) ^ (cut >> k & 1)) == color
                      and (A[j][k] ^ (cut >> j & 1) ^ (cut >> k & 1)) == color}
            if set(bit_indices(pages)) != actual:
                raise RuntimeError(('Triangle parity page mismatch', cut, edge))
    print('1260 literal triangle-parity page controls passed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=CUTS)
    parser.add_argument('--output', type=Path, default=Path('cover_results.json'))
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.limit <= CUTS:
        parser.error('--limit must be between 1 and 1048576')
    if args.controls:
        controls()
        return
    start = time.perf_counter()
    records, counters = [], collections.Counter()
    for rank in range(args.limit):
        cut = (rank ^ (rank >> 1)) << 1
        for edits in cover(cut, counters):
            records.append([cut, edits])
        if (rank + 1) % 65536 == 0:
            print('Gray ranks', rank + 1, 'seconds', round(time.perf_counter() - start, 2), flush=True)
    records.sort()
    result = {
        'method': 'original-book-covers', 'traversal': 'gray', 'radius': 2,
        'normalized_vertex': 0,
        'seed_sha256': hashlib.sha256(SEED_BYTES).hexdigest(),
        'status': 'complete' if args.limit == CUTS else 'partial',
        'cuts_scanned': args.limit, 'records': records,
        'counters': dict(counters), 'seconds': round(time.perf_counter() - start, 3),
        'sha256': hashlib.sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest(),
    }
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
