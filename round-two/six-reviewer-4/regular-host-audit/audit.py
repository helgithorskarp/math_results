"""six-reviewer-4, independent reviewer: Petersen/Book22 audit.

Exact standard-library set arithmetic; imports no author program.
The 22-point locally Petersen exclusion has an ordinary written proof.
This checker independently covers all 1024 common-neighbor sets, 906 high
row choices and 21 necessary incidence multisets, and checks every cut.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
POINTS = tuple(range(5))
PAIRS = tuple(combinations(POINTS, 2))
VERTICES = frozenset(range(10))
GROUND = tuple(frozenset(p) for p in PAIRS)
NEIGHBORS = tuple(frozenset(j for j, y in enumerate(GROUND) if x.isdisjoint(y))
                  for x in GROUND)
STARS = tuple(frozenset(i for i, x in enumerate(GROUND) if a in x) for a in POINTS)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def word(subset):
    return sum(1 << i for i in subset)


def decode(value):
    need(type(value) is int and 0 <= value < 1024, 'binary ten-column word')
    return frozenset(i for i in range(10) if value & (1 << i))


def stream_hash(values):
    return hashlib.sha256(b''.join(json.dumps(x, separators=(',', ':')).encode()
                                  + b'\n' for x in values)).hexdigest()


def matching_pairs(center):
    others = sorted(set(POINTS) - {center})
    first = others[0]
    result = []
    for partner in others[1:]:
        rest = sorted(set(others) - {first, partner})
        result.append(frozenset((PAIRS.index(tuple(sorted((first, partner)))),
                                 PAIRS.index(tuple(rest)))))
    return tuple(sorted(result, key=word))


def row_domain():
    """Every common-red set has its induced Petersen graph one-regular."""
    rows = []
    for mask in range(1024):
        common = decode(mask)
        if all(len(NEIGHBORS[i] & common) == 1 for i in common):
            rows.append(VERTICES - common)
    parameter_rows = {VERTICES}
    for a in POINTS:
        parameter_rows.add(STARS[a])
        for matching in matching_pairs(a):
            parameter_rows.add(STARS[a] | matching)
            parameter_rows.add(VERTICES - matching)
    need(set(rows) == parameter_rows, 'complete common-neighbor row classification')
    need(len(rows) == len(set(rows)), 'unique row domain')
    return tuple(sorted(rows, key=word))


def capacities(rows):
    need(len(rows) == 11, 'eleven outside rows')
    need(all(sum(i in z for z in rows) == 5 for i in range(10)), 'literal column counts five')
    for i, j in combinations(range(10), 2):
        upper = 1 if j in NEIGHBORS[i] else 3
        need(sum(i in z and j in z for z in rows) <= upper, 'literal pair capacities')


def normalized(rows):
    return tuple(sorted((word(z) for z in rows)))


def reconstruct(rows):
    """Exhaust high-row multisets, solve star multiplicities from three columns."""
    groups = {k: tuple(z for z in rows if len(z) == k) for k in (4, 6, 8, 10)}
    need(set(groups[4]) == set(STARS), 'five size-four stars')
    families = [((6, 6, 6), combinations_with_replacement(groups[6], 3)),
                ((8, 6), product(groups[8], groups[6])),
                ((10,), ((z,) for z in groups[10]))]
    matrices, raw, integral = [], Counter(), Counter()
    for pattern, choices in families:
        for high in choices:
            raw[pattern] += 1
            residual = {p: 5 - sum(i in z for z in high) for i, p in enumerate(PAIRS)}
            twice = residual[0, 1] + residual[0, 2] - residual[1, 2]
            if twice % 2:
                continue
            counts = [twice // 2]
            counts.extend(residual[0, j] - counts[0] for j in range(1, 5))
            if min(counts) < 0 or sum(counts) != 11 - len(high):
                continue
            if any(counts[i] + counts[j] != residual[i, j] for i, j in PAIRS):
                continue
            integral[pattern] += 1
            full = list(high) + [z for z, count in zip(STARS, counts) for _ in range(count)]
            capacities(full)
            matrices.append(normalized(full))
    need(len(matrices) == len(set(matrices)), 'unique complete incidence domain')
    return sorted(matrices), {'raw_high_choices': [[list(p), n] for p, n in sorted(raw.items())],
                              'integral_column_completions': [[list(p), n] for p, n in sorted(integral.items())]}


def algebraic_cases():
    """Literal models supplied by the ordinary ground-degree argument."""
    cases = [normalized([VERTICES] + [z for z in STARS for _ in range(2)])]
    for a in POINTS:
        matches = matching_pairs(a)
        cases.append(normalized([STARS[a] | m for m in matches]
                                + [STARS[i] for i in POINTS if i != a for _ in range(2)]))
        for m in matches:
            cases.append(normalized([VERTICES - m, STARS[a] | m, STARS[a]]
                                    + [STARS[i] for i in POINTS if i != a for _ in range(2)]))
    need(len(cases) == len(set(cases)), 'distinct algebraic cases')
    return sorted(cases)


def demand(z):
    k = len(z)
    return tuple(k - len(NEIGHBORS[i] & z) - 3 * (i in z) for i in range(10))


def pair_cut(rows, b, pair):
    required = sum(demand(rows[b])[i] for i in pair)
    supply = sum(sorted((len(z & pair) for c, z in enumerate(rows) if c != b),
                        reverse=True)[:len(rows[b])])
    return required, supply


def make_certificates(matrices):
    records = []
    for words in matrices:
        rows = [decode(x) for x in words]
        maximum = max(map(len, rows))
        b = next(i for i, z in enumerate(rows) if len(z) == maximum)
        if maximum == 10:
            records.append({'rows': list(words), 'kind': 'FULL_MISS_RED_PAIR', 'row': b})
            continue
        common = VERTICES - rows[b]
        pair = next(frozenset((i, j)) for i, j in combinations(sorted(common), 2)
                    if j in NEIGHBORS[i])
        records.append({'rows': list(words), 'kind': 'PAIR_RANK_SUM', 'row': b,
                        'pair': sorted(pair)})
    return {'schema': 1, 'actual_author': 'six-reviewer-4', 'role': 'independent reviewer',
            'incidences_sha256': stream_hash(matrices), 'records': records}


def verify_certificates(cert, matrices):
    need(cert['schema'] == 1 and cert['incidences_sha256'] == stream_hash(matrices),
         'certificate matrix-stream binding')
    need([item['rows'] for item in cert['records']] == [list(x) for x in matrices],
         'complete 21-case certificate coverage')
    margins, kinds = Counter(), Counter()
    for item, words in zip(cert['records'], matrices):
        rows = [decode(x) for x in words]
        b = item['row']
        need(type(b) is int and 0 <= b < 11, 'outside row index')
        if item['kind'] == 'PAIR_RANK_SUM':
            pair = item['pair']
            need(isinstance(pair, list) and len(pair) == 2 and all(type(i) is int for i in pair)
                 and 0 <= pair[0] < pair[1] < 10, 'pair cut indices')
            required, supply = pair_cut(rows, b, frozenset(pair))
            need(required > supply, 'strict pair rank-sum contradiction')
            margins[required - supply] += 1
        elif item['kind'] == 'FULL_MISS_RED_PAIR':
            need(rows[b] == VERTICES and all(len(z) == 4 for c, z in enumerate(rows) if c != b),
                 'full-miss structural case')
            other = [VERTICES - z for c, z in enumerate(rows) if c != b]
            lower = [1 + len(x & y) for x, y in combinations(other, 2)]
            need(min(lower) > 3, 'every remaining red pair violates red page cap')
            need(all(len(z) - 1 == 3 for c, z in enumerate(rows) if c != b),
                 'positive required degree after universal red neighbor')
        else:
            raise ValueError('unknown obstruction kind')
        kinds[item['kind']] += 1
    return {'kinds': dict(sorted(kinds.items())), 'pair_cut_margins': dict(sorted(margins.items()))}


def literal_star_checks(matrices):
    """Check the 20 non-full cases using full 22-point hypothetical stars."""
    stars = spines = 0
    for words in matrices:
        rows = [decode(x) for x in words]
        maximum = max(map(len, rows))
        if maximum == 10:
            continue
        b = next(i for i, z in enumerate(rows) if len(z) == maximum)
        actual_b = 11 + b
        for chosen in combinations([c for c in range(11) if c != b], maximum):
            red_b = {1 + i for i in VERTICES - rows[b]} | {11 + c for c in chosen}
            failed = False
            for i in range(10):
                red_i = {0} | {1 + j for j in NEIGHBORS[i]} | {
                    11 + c for c, z in enumerate(rows) if i not in z}
                coverage = sum(i in rows[c] for c in chosen)
                if i in rows[b]:
                    blue_i = set(range(22)) - red_i - {1 + i}
                    blue_b = set(range(22)) - red_b - {actual_b}
                    pages, cap = len(blue_i & blue_b), 6
                else:
                    pages, cap = len(red_i & red_b), 3
                need(pages - cap == demand(rows[b])[i] - coverage,
                     'literal 22-point page/demand bridge')
                failed |= pages > cap
                spines += 1
            need(failed, 'no non-full outside star extends')
            stars += 1
    return {'outside_stars': stars, 'literal_spine_identities': spines}


def packing_check():
    """Independent count-vector coverage of 11 integer occupancies of four columns."""
    cost_counts = Counter()
    for counts in product(range(12), repeat=4):
        if sum(counts) > 11:
            continue
        all_counts = (11 - sum(counts),) + counts
        if sum(i * n for i, n in enumerate(all_counts)) == 20:
            cost_counts[sum((i * (i - 1) // 2) * n for i, n in enumerate(all_counts))] += 1
    need(min(cost_counts) == 9, 'exact four-column packing minimum')
    need(all((t - 1) * (t - 2) >= 0 for t in range(5)), 'integer occupancy inequality')
    return {'minimum': min(cost_counts), 'occupancy_histograms': sum(cost_counts.values())}


def boundary_control():
    """KG(7,2) is a genuine 21-point locally Petersen graph, not a Book22 witness."""
    pairs = tuple(combinations(range(7), 2))
    sets = tuple(frozenset(x) for x in pairs)
    adj = tuple(frozenset(j for j, y in enumerate(sets) if x.isdisjoint(y)) for x in sets)
    for v in range(21):
        need(len(adj[v]) == 10, '21-point control degree')
        for u in adj[v]:
            need(len(adj[u] & adj[v]) == 3, '21-point local cubicity')
        for i, j in combinations(sorted(adj[v]), 2):
            need(len(adj[v] & adj[i] & adj[j]) == (0 if j in adj[i] else 1),
                 '21-point local Petersen common-neighbor identity')
    root = 0
    a = sorted(adj[root])
    outside = sorted(set(range(21)) - adj[root] - {root})
    need(all(sum(i not in adj[b] for b in outside) == 4 for i in a),
         '21-point columns have four misses, not five')
    return {'vertices': 21, 'red_edges': sum(map(len, adj)) // 2,
            'miss_rows': len(outside), 'miss_column_size': 4}


def build(cert_path=None):
    need(all(len(x) == 3 for x in NEIGHBORS), 'Petersen degree three')
    need(all(len(NEIGHBORS[i] & NEIGHBORS[j]) == (0 if j in NEIGHBORS[i] else 1)
             for i, j in combinations(range(10), 2)), 'Petersen common-neighbor parameters')
    rows = row_domain()
    matrices, reconstruction = reconstruct(rows)
    need(matrices == algebraic_cases(), 'all independent/algebraic incidence matrices entrywise')
    need(len(matrices) == 21, 'complete case count')
    cert = make_certificates(matrices) if cert_path is None else json.loads(cert_path.read_text())
    summary = verify_certificates(cert, matrices)
    record = {'actual_author': 'six-reviewer-4', 'role': 'independent reviewer', 'status': 'PASS',
              'row_types': dict(sorted(Counter(map(len, rows)).items())),
              'row_words_sha256': stream_hash([word(z) for z in rows]),
              'reconstruction': reconstruction, 'incidence_matrices': len(matrices),
              'incidences_sha256': stream_hash(matrices),
              'patterns': [[list(p), n] for p, n in sorted(Counter(tuple(sorted(
                  (len(decode(x)) for x in words if len(decode(x)) > 4), reverse=True))
                  for words in matrices).items())], 'obstructions': summary,
              'literal_stars': literal_star_checks(matrices), 'packing': packing_check(),
              'boundary_control': boundary_control()}
    return record, cert


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=HERE / 'expected.json')
    parser.add_argument('--certificates', type=Path, default=HERE / 'certificates.json')
    parser.add_argument('--emit', action='store_true')
    parser.add_argument('--emit-certificates', action='store_true')
    args = parser.parse_args()
    record, cert = build(None if args.emit or args.emit_certificates else args.certificates)
    if args.emit or args.emit_certificates:
        print(json.dumps(cert if args.emit_certificates else record, indent=2, sort_keys=True))
        return
    need(json.loads(args.expected.read_text()) == json.loads(json.dumps(record)), 'complete expected record')
    print(json.dumps({'status': 'PASS', 'incidence_matrices': record['incidence_matrices'],
                      'obstructions': record['obstructions'], 'literal_stars': record['literal_stars']},
                     sort_keys=True))


if __name__ == '__main__':
    main()
