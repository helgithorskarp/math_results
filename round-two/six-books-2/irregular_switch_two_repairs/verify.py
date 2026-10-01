"""Literal certificate checker and entrywise comparison of two full reports.

No scan implementation is imported. This checker cannot establish coverage
from a hand-written summary: rerun both scanners as documented in README.md.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 21
PAIRS = list(itertools.combinations(range(N), 2))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_seed(expected):
    raw = (HERE / 'seed.txt').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == expected['seed_sha256'], 'Seed digest differs')
    lines = raw.decode('ascii').splitlines()
    require(len(lines) == N and all(len(line) == N and not set(line) - {'0', '1'}
                                 for line in lines), 'Malformed seed')
    rows = [{j for j, bit in enumerate(line) if bit == '1'} for line in lines]
    require(all(i not in rows[i] for i in range(N)), 'Seed diagonal')
    require(all((j in rows[i]) == (i in rows[j]) for i, j in PAIRS), 'Seed symmetry')
    return rows


def actual_pages(rows, i, j):
    color = int(j in rows[i])
    pages = (rows[i] & rows[j] if color else set(range(N)) - {i, j} - rows[i] - rows[j])
    return color, pages


def reconstruct(base, cut, edits):
    require(type(cut) is int and 0 <= cut < 1 << N and cut & 1 == 0, 'Invalid normalized cut')
    require(len(edits) <= 2 and edits == sorted(set(edits))
            and all(type(edge) is int and 0 <= edge < len(PAIRS) for edge in edits), 'Invalid edits')
    rows = [set() for _ in range(N)]
    for edge, (i, j) in enumerate(PAIRS):
        if int(j in base[i]) ^ (cut >> i & 1) ^ (cut >> j & 1) ^ (edge in edits):
            rows[i].add(j)
            rows[j].add(i)
    return rows


def literal_valid(rows):
    for i, j in PAIRS:
        color, pages = actual_pages(rows, i, j)
        if len(pages) > (3 if color else 6):
            return False
    return True


def check_baseline(base, expected):
    degrees = collections.Counter(map(len, base))
    histograms = {0: collections.Counter(), 1: collections.Counter()}
    for i, j in PAIRS:
        color, pages = actual_pages(base, i, j)
        histograms[color][len(pages)] += 1
    encode = lambda histogram: {str(k): v for k, v in sorted(histogram.items())}
    require(sum(map(len, base)) // 2 == expected['red_edges'], 'Baseline edges')
    require(encode(degrees) == expected['red_degree_histogram'], 'Baseline degrees')
    require(encode(histograms[1]) == expected['red_page_histogram'], 'Baseline red pages')
    require(encode(histograms[0]) == expected['blue_page_histogram'], 'Baseline blue pages')


def check_paths(base, expected):
    certificates = json.loads((HERE / 'attachment_paths.json').read_text())['hosts']
    require([host['edits'] for host in certificates] == [record[1] for record in expected['records']],
            'Attachment certificates do not cover exactly the three hosts')
    steps = 0
    for host in certificates:
        rows = reconstruct(base, 0, host['edits'])
        require(literal_valid(rows), 'A certificate host is invalid')
        for key, endpoints in [('zero_to_one', (0, 1)), ('one_to_zero', (1, 0))]:
            path = host[key]
            require(len(path) >= 2 and (path[0], path[-1]) == endpoints, 'Wrong contradiction endpoints')
            require(all(type(node) is int and 0 <= node < 2 * N for node in path), 'Invalid literal')
            for source, target in zip(path, path[1:]):
                i, assumed_color = divmod(source, 2)
                j, forced_color = divmod(target, 2)
                require(i != j and forced_color == 1 - assumed_color, 'Invalid implication colors')
                color, pages = actual_pages(rows, i, j)
                require(color == assumed_color and len(pages) == (3 if color else 6),
                        'Implication does not come from a saturated spine')
                steps += 1
    print('Three attachment contradictions verified;', steps, 'literal implication steps')


def formula_controls():
    # Literal intersections of all forbidden books at a synthetic spine.
    for cap in (3, 6):
        for count in range(cap + 1, cap + 5):
            spine = (0, 1)
            intersection = None
            for chosen in itertools.combinations(range(2, count + 2), cap + 1):
                edges = {spine} | {(i, k) for i in (0, 1) for k in chosen}
                intersection = edges if intersection is None else intersection & edges
            predicted = ({spine} | {(i, k) for i in (0, 1) for k in range(2, count + 2)}
                         if count == cap + 1 else {spine})
            require(intersection == predicted, 'Book-intersection control')
    print('Eight literal book-intersection controls passed')


def check_report(path, method, traversal, counter_key, expected, base):
    report = json.loads(path.read_text())
    require(report.get('status') == 'complete', 'Incomplete scan')
    require(report.get('cuts_scanned') == expected['normalized_cuts'], 'Incomplete cut domain')
    require(report.get('method') == method and report.get('traversal') == traversal, 'Wrong scan method')
    require(report.get('radius') == 2 and report.get('normalized_vertex') == 0, 'Wrong radius or gauge')
    require(report.get('seed_sha256') == expected['seed_sha256'], 'Wrong input graph')
    records = report.get('records')
    require(records == expected['records'], 'Entrywise record mismatch')
    require(report.get('counters') == expected[counter_key], 'Coverage counters differ')
    digest = hashlib.sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest()
    require(digest == report.get('sha256') == expected['records_sha256'], 'Record digest differs')
    for cut, edits in records:
        require(literal_valid(reconstruct(base, cut, edits)), 'Invalid surviving graph')
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--forced', type=Path)
    parser.add_argument('--cover', type=Path)
    parser.add_argument('--primary', type=Path, help='Optional raw primary witness with off-diagonal zero = red')
    parser.add_argument('--certificates-only', action='store_true')
    args = parser.parse_args()
    if not args.certificates_only and (args.forced is None or args.cover is None):
        parser.error('Supply both --forced and --cover, or --certificates-only')
    expected = json.loads((HERE / 'expected.json').read_text())
    base = read_seed(expected)
    check_baseline(base, expected)
    formula_controls()
    check_paths(base, expected)
    if args.primary:
        raw = args.primary.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == expected['primary_raw_sha256'], 'Raw primary digest differs')
        # The original file appends search metadata after the JSON matrix.
        original, _ = json.JSONDecoder().raw_decode(raw.decode('ascii').lstrip())
        require(len(original) == N and all(len(row) == N for row in original)
                and all(type(bit) is int and bit in (0, 1) for row in original for bit in row),
                'Malformed primary witness')
        require(all((j in base[i]) == (i != j and original[i][j] == 0)
                    for i in range(N) for j in range(N)), 'Primary color convention mismatch')
        print('Primary raw input and off-diagonal complementation verified')
    if args.certificates_only:
        print('Certificate checks passed; no cut-domain completeness claimed by this mode')
        return
    forced = check_report(args.forced, 'forced-spines', 'binary', 'forced_counters', expected, base)
    cover = check_report(args.cover, 'original-book-covers', 'gray', 'cover_counters', expected, base)
    require(forced == cover, 'Independent reports disagree entrywise')
    f, c = expected['forced_counters'], expected['cover_counters']
    require(f['branchable_cuts'] + f['two_forced'] + f['forced_reject'] == 1 << 20,
            'First scan category coverage')
    require(c['initially_valid'] + c['old_book_cover_reject'] == 1 << 20,
            'Second scan category coverage')
    print('Both full cut domains agree entrywise: exactly three records')
    print('Canonical record SHA256:', expected['records_sha256'])


if __name__ == '__main__':
    main()
