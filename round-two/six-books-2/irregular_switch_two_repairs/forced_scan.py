"""Exact switch-and-repair scan using forced spines and successive repairs.

This program does not import cover_scan.py or verify.py. See PROOF.md for
the coverage argument. Only a full scan has status 'complete'.
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
INDEX = [[-1] * N for _ in range(N)]
for edge, (i, j) in enumerate(PAIRS):
    INDEX[i][j] = INDEX[j][i] = edge
UNIVERSE = (1 << len(PAIRS)) - 1
SEED_PATH = Path(__file__).with_name('seed.txt')
SEED_BYTES = SEED_PATH.read_bytes()
text_rows = SEED_BYTES.decode('ascii').splitlines()
if len(text_rows) != N or any(len(row) != N or set(row) - {'0', '1'} for row in text_rows):
    raise ValueError('Seed must have exactly 21 binary rows of length 21')
BASE = [int(row[::-1], 2) for row in text_rows]
for i in range(N):
    if BASE[i] >> i & 1:
        raise ValueError('Nonzero seed diagonal')
    for j in range(i):
        if (BASE[i] >> j & 1) != (BASE[j] >> i & 1):
            raise ValueError('Asymmetric seed')


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


def switched_rows(cut):
    return [BASE[i] ^ cut ^ (WHOLE if cut >> i & 1 else 0) for i in range(N)]


def toggle(rows, edge):
    i, j = PAIRS[edge]
    result = rows.copy()
    result[i] ^= 1 << j
    result[j] ^= 1 << i
    return result


def spine(rows, i, j):
    red = rows[i] >> j & 1
    pages = (rows[i] & rows[j]) if red else (
        WHOLE & ~(rows[i] | rows[j]) & ~((1 << i) | (1 << j)))
    return red, pages


def valid(rows):
    for i, j in PAIRS:
        red, pages = spine(rows, i, j)
        if pages.bit_count() > (3 if red else 6):
            return False
    return True


def book_edges(i, j, pages, red):
    witness = 1 << INDEX[i][j]
    for k in itertools.islice(bits(pages), 4 if red else 7):
        witness |= (1 << INDEX[i][k]) | (1 << INDEX[j][k])
    return witness


def single_candidates(rows):
    """Edges meeting every current forbidden book; final validity is separate."""
    allowed = UNIVERSE
    for i, j in PAIRS:
        red, pages = spine(rows, i, j)
        cap = 3 if red else 6
        count = pages.bit_count()
        if count <= cap:
            continue
        witness = ((1 << INDEX[i][j]) if count > cap + 1
                   else book_edges(i, j, pages, red))
        allowed &= witness
        if not allowed:
            break
    return allowed


def screen(rows, budget):
    forced = first = 0
    for i, j in PAIRS:
        red, pages = spine(rows, i, j)
        cap = 3 if red else 6
        count = pages.bit_count()
        if count <= cap:
            continue
        if not first:
            first = book_edges(i, j, pages, red)
        if count > cap + budget:
            forced |= 1 << INDEX[i][j]
            if forced.bit_count() > budget:
                return None, first
    return forced, first


def repairs(rows, counters):
    forced, witness = screen(rows, 2)
    if forced is None:
        counters['forced_reject'] += 1
        return []
    results = set()
    if forced.bit_count() == 2:
        counters['two_forced'] += 1
        edits = list(bits(forced))
        if valid(toggle(toggle(rows, edits[0]), edits[1])):
            results.add(tuple(edits))
        return sorted(results)
    if not witness:
        results.add(())
    first = forced or witness or UNIVERSE
    counters['branchable_cuts'] += 1
    for edge in bits(first):
        counters['first_repairs'] += 1
        changed = toggle(rows, edge)
        options = single_candidates(changed) & ~(1 << edge)
        if options == UNIVERSE & ~(1 << edge):
            results.add((edge,))
        for other in bits(options):
            counters['second_tests'] += 1
            if valid(toggle(changed, other)):
                results.add(tuple(sorted((edge, other))))
    return sorted(results)


def exhaustive(rows):
    """Literal control over all 22,156 edit sets of size at most two."""
    results = []
    if valid(rows):
        results.append(())
    for edge in range(len(PAIRS)):
        changed = toggle(rows, edge)
        if valid(changed):
            results.append((edge,))
        for other in range(edge):
            if valid(toggle(changed, other)):
                results.append((other, edge))
    return sorted(results)


def controls():
    # Different normalized cuts, including an initially valid graph.
    for cut in (0, 2, 38):
        rows = switched_rows(cut)
        actual = repairs(rows, collections.Counter())
        reference = exhaustive(rows)
        if actual != reference:
            raise RuntimeError(('Exhaustive radius-two control mismatch', cut))
        print('All 22,156 edit sets matched at cut', cut, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=CUTS)
    parser.add_argument('--output', type=Path, default=Path('forced_results.json'))
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.limit <= CUTS:
        parser.error('--limit must be between 1 and 1048576')
    if args.controls:
        controls()
        return
    start = time.perf_counter()
    records, counters = [], collections.Counter()
    for assignment in range(args.limit):
        cut = assignment << 1  # Vertex zero is outside every switch.
        for edits in repairs(switched_rows(cut), counters):
            records.append([cut, list(edits)])
        if (assignment + 1) % 65536 == 0:
            print('Cuts', assignment + 1, 'seconds', round(time.perf_counter() - start, 2), flush=True)
    result = {
        'method': 'forced-spines', 'traversal': 'binary', 'radius': 2,
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
