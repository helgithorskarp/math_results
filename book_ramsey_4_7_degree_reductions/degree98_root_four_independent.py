"""Separate author audit; no imports from the primary checker.

Uses a weighted-moment join, generic exact rational elimination, grouped
neighbor multiplicities and literal ordinary-book page counts. This is an
independent algorithm by the same researcher, not independent peer review.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import hashlib
import itertools as it
import json
import math
from pathlib import Path


def check(test, reason):
    if not test:
        raise RuntimeError(reason)


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


EDGES = [
    [(0, 3), (1, 3), (2, 3), (4, 5)],
    [(0, 3), (1, 3), (2, 3), (3, 5), (4, 5)],
    [(0, 3), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5)],
    [(0, 3), (1, 2)],
    [(0, 3), (1, 2), (2, 3), (4, 5)],
    [(0, 3), (1, 2), (2, 3), (3, 5), (4, 5)],
    [(0, 3), (1, 2), (2, 3), (2, 5), (3, 5), (4, 5)],
    [(0, 3), (1, 2), (2, 3), (2, 5), (3, 4), (4, 5)],
]
COORD = [(i, i) for i in range(6)] + list(it.combinations(range(6), 2))
SUPPORT = [frozenset(i for i in range(6) if w & (1 << i)) for w in range(64)]
SURPLUS = [len(s & set(range(4))) - len(s & {4, 5}) for s in SUPPORT]
TYPES = {d: [w for w in range(64) if SURPLUS[w] == d] for d in range(5)}
FEATURES = [[1] + [int(i in s and j in s) for i, j in COORD] for s in SUPPORT]


def audit_roots(expected):
    pairs = list(it.combinations(range(6), 2))
    literal = set()
    for flags in it.product((0, 1), repeat=15):
        ns = [set() for _ in range(6)]
        for flag, (i, j) in zip(flags, pairs):
            if flag:
                ns[i].add(j); ns[j].add(i)
        f = [2 * (len(ns[i] & {0, 1, 2, 3}) - len(ns[i] & {4, 5}) - 1) for i in range(4)]
        f += [2 * (len(ns[i] & {0, 1, 2, 3}) - len(ns[i] & {4, 5}) + 1) for i in (4, 5)]
        if min(f) >= 0 and sum(f) == 4:
            literal.add(flags)
    got = set(tuple(x) for family in expected for x in family)
    check(literal == got and len(got) == 127, 'literal 32768-root-mask coverage')
    return 32768


def own_spec(profile, weight):
    ns = [set() for _ in range(6)]
    for i, j in EDGES[profile - 1]:
        ns[i].add(j); ns[j].add(i)
    R = [[int(j in ns[i]) for j in range(6)] for i in range(6)]
    d = [8] * 4 + [10] * 2
    f = [2 * (len(ns[i] & {0, 1, 2, 3}) - len(ns[i] & {4, 5}) + (-1 if i < 4 else 1)) for i in range(6)]
    active = [i for i in range(6) if f[i]]
    saturated = [i for i in range(6) if not f[i]]
    s = [d[i] - len(ns[i]) for i in range(6)]
    G = [[0] * 6 for _ in range(6)]
    for i in range(6):
        G[i][i] = s[i]
        for j in range(i + 1, 6):
            defect = weight if len(active) == 2 and set((i, j)) == set(active) else 0
            if j in ns[i]:
                x = 3 - defect - len(ns[i] & ns[j])
            else:
                blue_root = len(set(range(6)) - {i, j} - ns[i] - ns[j])
                x = 6 - defect - blue_root - 16 + s[i] + s[j]
            G[i][j] = G[j][i] = x
    Z = [[s[i] * (3 if j < 4 else 5) - sum(G[i][k] for k in ns[j])
          - (2 * G[i][j] if j >= 4 else 0) for j in range(6)] for i in range(6)]
    correlations = [[Z[i][a] - Z[a][i] for i in saturated] for a in active]
    return {'profile': profile, 'weight': weight, 'R': R, 'f': f, 'active': active,
            'saturated': saturated, 'G': G, 'Z': Z, 'correlations': correlations}


def zero_left_inverse():
    """Select independent feature equations and invert the 15-by-15 matrix."""
    zeros = TYPES[0]
    a = [[Q(FEATURES[w][j]) for j in range(22)] for w in zeros]
    pivot_columns = []
    row = 0
    for column in range(22):
        p = next((i for i in range(row, 15) if a[i][column]), None)
        if p is None:
            continue
        a[row], a[p] = a[p], a[row]
        z = a[row][column]
        a[row] = [x / z for x in a[row]]
        for i in range(15):
            if i != row and a[i][column]:
                z = a[i][column]
                a[i] = [x - z * y for x, y in zip(a[i], a[row])]
        pivot_columns.append(column)
        row += 1
        if row == 15:
            break
    check(row == 15, 'zero-surplus feature columns are not independent')
    square = [[Q(FEATURES[w][j]) for w in zeros] for j in pivot_columns]
    aug = [square[i] + [Q(int(i == j)) for j in range(15)] for i in range(15)]
    for j in range(15):
        p = next(i for i in range(j, 15) if aug[i][j])
        aug[j], aug[p] = aug[p], aug[j]
        t = aug[j][j]
        aug[j] = [x / t for x in aug[j]]
        for i in range(15):
            if i != j and aug[i][j]:
                t = aug[i][j]
                aug[i] = [x - t * y for x, y in zip(aug[i], aug[j])]
    inverse = [line[15:] for line in aug]
    check(all(sum(square[i][k] * inverse[k][j] for k in range(15)) == int(i == j)
              for i in range(15) for j in range(15)), 'literal inverse verification')
    return zeros, pivot_columns, inverse


def reconstruct(spec, left):
    """Group by M^T delta = G(1,1,1,1,-1,-1)^T before full Gram equations."""
    G = spec['G']
    q = [1] * 4 + [-1] * 2
    target = tuple(sum(G[i][j] * q[j] for j in range(6)) for i in range(6))
    second = sum(q[i] * target[i] for i in range(6))
    profiles = [c for c in it.product(range(9), repeat=4)
                if sum((i + 1) * c[i] for i in range(4)) == 8
                and sum((i + 1) ** 2 * c[i] for i in range(4)) == second]
    full = []
    join_candidates = 0
    domain_count = 0
    zeros, pivots, inverse = left
    feature_target = [16] + [G[i][j] for i, j in COORD]
    for counts in profiles:
        sizes = [math.comb(len(TYPES[i + 1]) + counts[i] - 1, counts[i]) for i in range(4)]
        domain_count += math.prod(sizes)
        grouped = max(range(4), key=lambda i: sizes[i])
        bucket = defaultdict(list)
        seen = 0
        for ws in it.combinations_with_replacement(TYPES[grouped + 1], counts[grouped]):
            signature = tuple((grouped + 1) * sum(int(i in SUPPORT[w]) for w in ws) for i in range(6))
            bucket[signature].append(ws)
            seen += 1
        check(seen == sizes[grouped], 'incomplete grouped moment domain')
        others = [i for i in range(4) if i != grouped]
        other_pools = [it.combinations_with_replacement(TYPES[i + 1], counts[i]) for i in others]
        other_seen = 0
        for groups in it.product(*other_pools):
            other_seen += 1
            want = tuple(target[j] - sum((i + 1) * sum(int(j in SUPPORT[w]) for w in ws)
                                         for i, ws in zip(others, groups)) for j in range(6))
            for ws in bucket.get(want, ()):
                positive = list(ws) + [w for group in groups for w in group]
                join_candidates += 1
                residual = [feature_target[j] - sum(FEATURES[w][j] for w in positive) for j in range(22)]
                if min(residual) < 0:
                    continue
                solved = [sum(inverse[i][j] * residual[pivots[j]] for j in range(15)) for i in range(15)]
                if any(x < 0 or x.denominator != 1 for x in solved):
                    continue
                mult = [int(x) for x in solved]
                if [sum(mult[i] * FEATURES[w][j] for i, w in enumerate(zeros)) for j in range(22)] != residual:
                    continue
                result = [0] * 64
                for w in positive:
                    result[w] += 1
                for w, c in zip(zeros, mult):
                    result[w] += c
                full.append(result)
        check(other_seen == math.prod(sizes[i] for i in others), 'incomplete other moment domain')
    check(len({tuple(v) for v in full}) == len(full), 'duplicate independent incidence')
    return sorted(full), domain_count, join_candidates


def weak_compositions(total, caps):
    def visit(i, left, prefix):
        if i == len(caps):
            if left == 0:
                yield prefix
            return
        for value in range(min(left, caps[i]) + 1):
            yield from visit(i + 1, left - value, prefix + [value])
    yield from visit(0, total, [])


def defect_columns(spec, words):
    active, sat = spec['active'], spec['saturated']
    options = []
    for a, wanted in zip(active, spec['correlations']):
        total = spec['f'][a] - (spec['weight'] if len(active) == 2 else 0)
        caps = [min(3 if a in SUPPORT[w] else 6, 1 + 2 * SURPLUS[w]) for w in words]
        good = []
        for g in weak_compositions(total, caps):
            if [sum(g[i] for i, w in enumerate(words) if j in SUPPORT[w]) for j in sat] != wanted:
                continue
            red_mass = sum(g[i] for i, w in enumerate(words) if a in SUPPORT[w])
            if len(active) == 2:
                b = next(x for x in active if x != a)
                red_mass += spec['weight'] * spec['R'][a][b]
            if red_mass % 2 == 0:
                good.append(g)
        options.append(good)
    accepted = []
    for columns in it.product(*options):
        if any(sum(g[i] for g in columns) > 1 + 2 * SURPLUS[w] for i, w in enumerate(words)):
            continue
        if len(active) == 2:
            a, b = active
            diff = sum(columns[1][i] * int(a in SUPPORT[w]) - columns[0][i] * int(b in SUPPORT[w])
                       for i, w in enumerate(words))
            if diff != spec['Z'][a][b] - spec['Z'][b][a]:
                continue
        accepted.append([list(g) for g in columns])
    return sorted(accepted)


def multiplicities(available, degree):
    suffix = [0] * (len(available) + 1)
    for i in range(len(available) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + available[i]
    def visit(i, left, chosen):
        if i == len(available):
            if left == 0:
                yield chosen
            return
        for c in range(max(0, left - suffix[i + 1]), min(left, available[i]) + 1):
            yield from visit(i + 1, left - c, chosen + [c])
    yield from visit(0, degree, [])


def literal_domains(spec, full, columns):
    words = [w for w, count in enumerate(full) for _ in range(count)]
    if not columns:
        return []
    universe = set(range(22))
    root_red = [{k for k in range(6) if spec['R'][j][k]} |
                {6 + i for i, w in enumerate(words) if j in SUPPORT[w]} for j in range(6)]
    root_blue = [universe - star - {j} for j, star in enumerate(root_red)]
    domains = []
    for word in sorted(set(words)):
        i = words.index(word)
        required = sorted({tuple(g[k] for g in cc) for cc in columns
                           for k, v in enumerate(words) if v == word})
        stars = {key: [] for key in required}
        groups = [[j for j, w in enumerate(words) if w == v and j != i] for v in sorted(set(words))]
        for counts in multiplicities(list(map(len, groups)), 9 - len(SUPPORT[word])):
            selected = [j for group, c in zip(groups, counts) for j in group[:c]]
            red = set(SUPPORT[word]) | {6 + j for j in selected}
            blue = universe - red - {6 + i}
            defects = [3 - len(red & root_red[j]) if j in SUPPORT[word]
                       else 6 - len(blue & root_blue[j]) for j in range(6)]
            if any(defects[j] != 0 for j in spec['saturated']):
                continue
            key = tuple(defects[j] for j in spec['active'])
            if key not in stars:
                continue
            for selections in it.product(*(it.combinations(group, c) for group, c in zip(groups, counts))):
                mask = sum(1 << j for selected_group in selections for j in selected_group)
                stars[key].append(mask)
        domains.append({'word': word, 'representative': i,
                        'stars': [{'g': list(key), 'masks': sorted(stars[key])} for key in required]})
    return domains


def signed_audit(controls):
    compared = 0
    for record in controls:
        R = record['R']
        red = [{j for j, x in enumerate(row) if x} for row in R]
        blue = [set(range(22)) - red[i] - {i} for i in range(22)]
        F = [[0 if i == j else 3 - len(red[i] & red[j]) if j in red[i]
              else 6 - len(blue[i] & blue[j]) for j in range(22)] for i in range(22)]
        check(F == record['F'], 'literal signed graph defects')
        compared += 484
        G = [[len(red[i] & red[j] & set(range(6, 22))) if i != j
              else len(red[i] & set(range(6, 22))) for j in range(6)] for i in range(6)]
        check(G == record['G'], 'literal signed incidence Gram')
        f = list(map(sum, F))
        for i in range(22):
            d = len(red[i])
            tri_red = sum(int(b in red[a]) for a, b in it.combinations(red[i], 2))
            tri_blue = sum(int(b in blue[a]) for a, b in it.combinations(blue[i], 2))
            check(f[i] == 3 * d + 6 * (21 - d) - 2 * (tri_red + tri_blue), 'triangle incident identity')
            check(sum(F[i][j] for j in red[i]) % 2 == d % 2, 'red defect parity')
            check(sum(F[i][j] for j in blue[i]) % 2 == 0, 'blue defect parity')
        for v in range(6, 22):
            for j in range(6):
                root_common = len(red[v] & red[j] & set(range(6)))
                outside_common = len(red[v] & red[j] & set(range(6, 22)))
                expected = (3 if j < 4 else 5 - 2 * int(j in red[v])) - root_common - F[v][j]
                check(outside_common == expected, 'literal signed root-to-B equation')
    return compared


def replay_symmetry(trace, own_domains):
    check(own_domains == trace['domains'], 'full starting symmetry domains')
    n = len(own_domains)
    alive = [set(range(len(row))) for row in own_domains]
    checks = deleted = 0
    for i, j, mask in trace['steps']:
        check(0 <= i < n and 0 <= j < n and i != j, 'malformed elimination pair')
        indices = {a for a in range(len(own_domains[i])) if mask & (1 << a)}
        check(indices and indices <= alive[i] and sum(1 << a for a in indices) == mask, 'invalid or repeated deletion')
        for a in indices:
            for b in alive[j]:
                left = j in {k for k in range(n) if own_domains[i][a] & (1 << k)}
                right = i in {k for k in range(n) if own_domains[j][b] & (1 << k)}
                check(left != right, 'deleted candidate has a reciprocal supporting edge')
                checks += 1
        alive[i] -= indices
        deleted += len(indices)
    final = [sum(1 << a for a in row) for row in alive]
    check(final == trace['final_state'], 'trace final state')
    empty = trace['empty_row']
    if empty is not None:
        check(0 <= empty < n and not alive[empty], 'missing empty-row contradiction')
    else:
        check(all(alive), 'positive control falsely excluded')
    return checks, deleted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', type=Path, required=True, help='Runtime records produced by the primary checker')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    primary = json.loads(args.records.read_text())
    expected = json.loads(Path(__file__).with_name('degree98_root_four_expected.json').read_text())
    root_masks = audit_roots(primary['root_families'])
    left = zero_left_inverse()
    check(len(primary['cases']) == len(expected['cases']) == 9, 'wrong finite case domain')
    compared_forms = compared_assignments = compared_stars = symmetry_pairs = symmetry_deleted = symmetry_traces = 0
    audits = []
    for case, wanted in zip(primary['cases'], expected['cases']):
        spec = own_spec(wanted['profile'], wanted['weight'])
        check(spec == case['spec'], 'full root Gram/correlation comparison')
        forms, domain, joined = reconstruct(spec, left)
        check(forms == [x['counts'] for x in case['records']], 'every incidence entry comparison')
        check(domain == wanted['positive_multisets'] and len(forms) == wanted['binary_forms'], 'complete incidence domain count')
        check(digest(forms) == wanted['incidence_sha256'], 'canonical incidence stream')
        own_records = []
        for full, original in zip(forms, case['records']):
            words = [w for w, c in enumerate(full) for _ in range(c)]
            columns = defect_columns(spec, words)
            check(columns == original['defect_assignments'], 'every defect assignment entry')
            local = literal_domains(spec, full, columns)
            check(local == original['local_domains'], 'all literal grouped neighbor subsets')
            lookup = {d['word']: {tuple(s['g']): s['masks'] for s in d['stars']} for d in local}
            surviving = [cc for cc in columns if all(lookup[w].get(tuple(g[i] for g in cc), [])
                                                     for i, w in enumerate(words))]
            check(surviving == original['local_surviving_assignments'], 'every locally surviving placement')
            check(len(original['symmetry_exclusions']) == len(surviving), 'uncovered local placement')
            for cc, trace in zip(surviving, original['symmetry_exclusions']):
                own_domains = []
                for i, word in enumerate(words):
                    rep = words.index(word)
                    choice = lookup[word][tuple(g[i] for g in cc)]
                    # Rebuild the transposition as a literal permutation of a set.
                    perm = list(range(16)); perm[i], perm[rep] = perm[rep], perm[i]
                    own_domains.append(sorted(sum(1 << perm[j] for j in range(16) if m & (1 << j)) for m in choice))
                pair_checks, deletions = replay_symmetry(trace, own_domains)
                check(trace['empty_row'] is not None, 'incomplete coupled exclusion')
                symmetry_pairs += pair_checks; symmetry_deleted += deletions; symmetry_traces += 1
            rebuilt = {'counts': full, 'defect_assignments': columns, 'local_domains': local,
                       'local_surviving_assignments': surviving,
                       'symmetry_exclusions': original['symmetry_exclusions']}
            check(rebuilt == original, 'complete finite record comparison')
            own_records.append(rebuilt)
            compared_forms += 1
            compared_assignments += len(columns)
            compared_stars += sum(len(s['masks']) for d in local for s in d['stars'])
        check(digest(own_records) == wanted['full_records_sha256'], 'full independent record digest')
        audits.append({'profile': spec['profile'], 'weight': spec['weight'], 'covered_positive_multisets': domain,
                       'weighted_moment_join_candidates': joined, 'binary_forms': len(forms)})
        print(json.dumps(audits[-1], sort_keys=True), flush=True)
    for profile in (4, 5, 6, 8):
        spec = own_spec(profile, 2)
        check(any(t != 0 for v in spec['correlations'] for t in v), 'independent weight-two root obstruction')
    control_entries = signed_audit(primary['controls'])
    check(digest(primary['controls']) == expected['signed_controls_sha256'], 'complete signed control comparison')
    check(len(primary['propagation_controls']) == 3, 'missing propagation controls')
    for t in primary['propagation_controls']:
        replay_symmetry(t, t['domains'])
    check(digest(primary['propagation_controls']) == expected['propagation_controls_sha256'], 'propagation controls digest')
    bad = {'domains': [[2], [1]], 'steps': [[0, 1, 1]], 'final_state': [0, 1], 'empty_row': 0}
    rejected = False
    try:
        replay_symmetry(bad, bad['domains'])
    except RuntimeError:
        rejected = True
    check(rejected, 'a supported deletion was accepted')
    report = {'agent': 'six-books-1', 'role': 'researcher', 'complete': True,
              'independent_peer_review': False, 'literal_root_masks': root_masks,
              'zero_surplus_feature_rank': 15, 'binary_count_vectors_compared': compared_forms,
              'binary_count_entries_compared': 64 * compared_forms,
              'defect_assignments_compared': compared_assignments,
              'permitted_local_star_masks_compared': compared_stars,
              'literal_signed_defect_entries_compared': control_entries, 'cases': audits,
              'symmetry_exclusion_traces_replayed': symmetry_traces,
              'symmetry_candidate_pairs_checked': symmetry_pairs,
              'symmetry_deleted_candidates_checked': symmetry_deleted,
              'supported_deletion_negative_control_rejected': True,
              'root_defect_four_excluded': True, 'root_defect_lower_bound': 8}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
