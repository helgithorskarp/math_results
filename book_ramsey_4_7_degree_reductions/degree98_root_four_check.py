"""Exact root-defect-four exclusion at histogram (4,16,2), CPython 3.11.

All generated records belong outside the source directory. No solver, floating
point, host catalogue, or omitted certificate is used. Checks survive -O.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


PAIRS = list(it.combinations(range(6), 2))
COORDS = [(i, i) for i in range(6)] + PAIRS
POS = {p: i for i, p in enumerate(COORDS)}
BITS = [tuple((w >> i) & 1 for i in range(6)) for w in range(64)]
DELTA = [sum(x[:4]) - sum(x[4:]) for x in BITS]
TYPES = {d: [w for w in range(64) if DELTA[w] == d] for d in range(5)}
PACKED = [sum((x[i] * x[j]) << (5 * t) for t, (i, j) in enumerate(COORDS)) for x in BITS]
SENTINEL = sum(16 << (5 * t) for t in range(21))
PROFILES = [
    [(0, 3), (1, 3), (2, 3), (4, 5)],
    [(0, 3), (1, 3), (2, 3), (3, 5), (4, 5)],
    [(0, 3), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5)],
    [(0, 3), (1, 2)],
    [(0, 3), (1, 2), (2, 3), (4, 5)],
    [(0, 3), (1, 2), (2, 3), (3, 5), (4, 5)],
    [(0, 3), (1, 2), (2, 3), (2, 5), (3, 5), (4, 5)],
    [(0, 3), (1, 2), (2, 3), (2, 5), (3, 4), (4, 5)],
]


def matrix(edges, n=6):
    R = [[0] * n for _ in range(n)]
    for i, j in edges:
        R[i][j] = R[j][i] = 1
    return R


def root_f(R):
    return [2 * (sum(R[i][:4]) - sum(R[i][4:]) + (-1 if i < 4 else 1)) for i in range(6)]


def root_orbits():
    families = []
    for edges in PROFILES:
        words = set()
        for a in it.permutations(range(4)):
            for c in ((4, 5), (5, 4)):
                perm = a + c
                image = {tuple(sorted((perm[i], perm[j]))) for i, j in edges}
                words.add(tuple(int(p in image) for p in PAIRS))
        families.append(sorted(words))
    flat = [x for family in families for x in family]
    require(len(set(flat)) == len(flat) == 127, 'root-orbit overlap')
    require(list(map(len, families)) == [4, 8, 4, 3, 12, 48, 24, 24], 'root labeling counts')
    for word in flat:
        f = root_f(matrix([p for p, x in zip(PAIRS, word) if x]))
        require(min(f) >= 0 and sum(f) == 4, 'invalid analytic root profile')
    return families


def specification(profile, weight=0):
    R = matrix(PROFILES[profile - 1])
    f = root_f(R)
    active = [i for i, x in enumerate(f) if x]
    d = [8] * 4 + [10] * 2
    s = [d[i] - sum(R[i]) for i in range(6)]
    G = [[s[i] if i == j else d[i] + d[j] - 14 + (17 - d[i] - d[j]) * R[i][j]
          - sum(R[i][k] * R[k][j] for k in range(6))
          - (weight if len(active) == 2 and {i, j} == set(active) else 0)
          for j in range(6)] for i in range(6)]
    ell = [3] * 4 + [5] * 2
    Z = [[s[i] * ell[j] - sum(G[i][k] * (R[k][j] + (2 if k == j and j >= 4 else 0))
                              for k in range(6)) for j in range(6)] for i in range(6)]
    saturated = [i for i in range(6) if i not in active]
    correlations = [[Z[i][a] - Z[a][i] for i in saturated] for a in active]
    return {'profile': profile, 'weight': weight, 'R': R, 'f': f, 'active': active,
            'saturated': saturated, 'G': G, 'Z': Z, 'correlations': correlations}


def moment_profiles(G):
    q = [1] * 4 + [-1] * 2
    second = sum(q[i] * G[i][j] * q[j] for i in range(6) for j in range(6))
    return [list(c) for c in it.product(range(9), repeat=4)
            if sum((i + 1) * c[i] for i in range(4)) == 8
            and sum((i + 1) ** 2 * c[i] for i in range(4)) == second]


def incidence(spec):
    G = spec['G']
    require(all(0 <= G[i][j] <= 10 for i, j in COORDS), 'packing bound')
    target = sum(G[i][j] << (5 * t) for t, (i, j) in enumerate(COORDS))
    survivors = []
    tested = 0
    moments = moment_profiles(G)
    expected = 0
    import math
    for counts in moments:
        expected += math.prod(math.comb(len(TYPES[i + 1]) + counts[i] - 1, counts[i]) for i in range(4))
        pools = [it.combinations_with_replacement(TYPES[i + 1], counts[i]) for i in range(4)]
        for groups in it.product(*pools):
            positive = sum(groups, ())
            require(len(positive) <= 8, 'packing subtraction bound')
            tested += 1
            value = target + SENTINEL - sum(PACKED[w] for w in positive)
            if value & SENTINEL != SENTINEL:
                continue
            residual = [((value >> (5 * j)) & 31) - 16 for j in range(21)]
            mult = {}
            for i, j in it.combinations(range(4), 2):
                mult[(1 << i) | (1 << j) | 48] = residual[POS[(i, j)]]
            for i in range(4):
                mass = sum(residual[POS[tuple(sorted((i, j)))]] for j in range(4) if i != j)
                for c in (4, 5):
                    mult[(1 << i) | (1 << c)] = residual[POS[(i, c)]] - mass
            mult[0] = 16 - len(positive) - sum(mult.values())
            if min(mult.values()) < 0 or sum(mult[w] * PACKED[w] for w in mult) != value - SENTINEL:
                continue
            full = [0] * 64
            for w in positive:
                full[w] += 1
            for w, c in mult.items():
                full[w] += c
            require(sum(full) == 16 and all(full[w] == 0 for w in range(64) if DELTA[w] < 0), 'row domain')
            require([[sum(full[w] * BITS[w][i] * BITS[w][j] for w in range(64))
                      for j in range(6)] for i in range(6)] == G, 'decoded full Gram')
            survivors.append(full)
    require(tested == expected, 'incomplete moment domain')
    require(len({tuple(x) for x in survivors}) == len(survivors), 'duplicate incidence')
    return moments, tested, sorted(survivors)


def assignments(spec, rows):
    active, sat, f, R, Z, w = (spec[k] for k in ('active', 'saturated', 'f', 'R', 'Z', 'weight'))
    options = []
    for a, required in zip(active, spec['correlations']):
        total = f[a] - (w if len(active) == 2 else 0)
        vectors = []
        for selected in it.combinations_with_replacement(range(16), total):
            g = [selected.count(i) for i in range(16)]
            if [sum(g[i] * rows[i][j] for i in range(16)) for j in sat] != required:
                continue
            if any(g[i] > (3 if rows[i][a] else 6) for i in range(16)):
                continue
            root_red = w * R[a][next(b for b in active if b != a)] if len(active) == 2 else 0
            if (root_red + sum(g[i] * rows[i][a] for i in range(16))) % 2:
                continue
            vectors.append(g)
        options.append(vectors)
    out = []
    for columns in it.product(*options):
        if len(active) == 2:
            a, b = active
            if sum(rows[i][a] * columns[1][i] - rows[i][b] * columns[0][i] for i in range(16)) != Z[a][b] - Z[b][a]:
                continue
        if any(sum(g[i] for g in columns) > 1 + 2 * (sum(rows[i][:4]) - sum(rows[i][4:])) for i in range(16)):
            continue
        out.append([list(g) for g in columns])
    return sorted(out)


def local_stars(spec, full):
    words = [w for w, c in enumerate(full) for _ in range(c)]
    rows = [BITS[w] for w in words]
    defect_options = assignments(spec, rows)
    domains = []
    if defect_options:
        R, active, sat = (spec[k] for k in ('R', 'active', 'saturated'))
        cmask = [sum(x[j] << i for i, x in enumerate(rows)) for j in range(6)]
        for word in sorted(set(words)):
            i = words.index(word)
            x = rows[i]
            degree = 9 - sum(x)
            base = [(3 if j < 4 else 5 - 2 * x[j]) - sum(x[k] * R[k][j] for k in range(6)) for j in range(6)]
            required = sorted({tuple(g[k] for g in columns) for columns in defect_options
                               for k, v in enumerate(words) if v == word})
            stars = {key: [] for key in required}
            for selected in it.combinations([j for j in range(16) if j != i], degree):
                mask = sum(1 << j for j in selected)
                cc = [(mask & cmask[j]).bit_count() for j in range(6)]
                if any(cc[j] != base[j] for j in sat):
                    continue
                key = tuple(base[a] - cc[a] for a in active)
                if key in stars:
                    stars[key].append(mask)
            domains.append({'word': word, 'representative': i,
                            'stars': [{'g': list(key), 'masks': sorted(stars[key])} for key in required]})
    lookup = {d['word']: {tuple(s['g']): s['masks'] for s in d['stars']} for d in domains}
    survivors = [columns for columns in defect_options
                 if all(lookup[word].get(tuple(g[i] for g in columns), []) for i, word in enumerate(words))]
    record = {'counts': full, 'defect_assignments': defect_options, 'local_domains': domains,
              'local_surviving_assignments': survivors}
    record['symmetry_exclusions'] = []
    for columns in survivors:
        choices = []
        for i, word in enumerate(words):
            rep = words.index(word)
            row = lookup[word][tuple(g[i] for g in columns)]
            if rep != i:
                row = [mask ^ ((1 << rep) | (1 << i))
                       if bool(mask & (1 << rep)) != bool(mask & (1 << i)) else mask for mask in row]
            choices.append(sorted(row))
        trace = symmetry_trace(choices)
        require(trace['empty_row'] is not None, 'mutual-spine consistency survives; no exclusion proved')
        record['symmetry_exclusions'].append(trace)
    return record


def set_indices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def symmetry_trace(domains):
    """Delete only candidates lacking a reciprocal edge choice in another row.

    This is elementary forced-edge propagation. It never branches and uses no
    B--B book-page inequality. Every deletion is recorded for literal replay.
    """
    n = len(domains)
    require(all(row and len(set(row)) == len(row) for row in domains), 'empty or repeated starting row')
    support = [[[sum(1 << a for a, mask in enumerate(domains[i]) if (mask >> j) & 1 == value)
                 for value in (0, 1)] for j in range(n)] for i in range(n)]
    state = [(1 << len(row)) - 1 for row in domains]
    queue = [(i, j) for i in range(n) for j in range(n) if i != j]
    steps = []
    while queue:
        i, j = queue.pop()
        keep = (support[i][j][0] if state[j] & support[j][i][0] else 0)
        keep |= support[i][j][1] if state[j] & support[j][i][1] else 0
        removed = state[i] & ~keep
        if not removed:
            continue
        state[i] ^= removed
        steps.append([i, j, removed])
        if not state[i]:
            return {'domains': domains, 'steps': steps, 'final_state': state, 'empty_row': i}
        queue.extend((k, i) for k in range(n) if k != i and k != j)
    return {'domains': domains, 'steps': steps, 'final_state': state, 'empty_row': None}


def signed_controls():
    """32 deterministic Havel--Hakimi/two-edge-switch controls, validation only."""
    degrees = [8] * 4 + [9] * 16 + [10] * 2
    todo, adj = degrees[:], [set() for _ in range(22)]
    while max(todo):
        v = max(range(22), key=lambda i: (todo[i], -i))
        candidates = sorted((i for i in range(22) if i != v and todo[i]), key=lambda i: (-todo[i], i))[:todo[v]]
        require(len(candidates) == todo[v], 'non-graphical control degrees')
        todo[v] = 0
        for i in candidates:
            require(i not in adj[v], 'repeated control edge')
            adj[v].add(i)
            adj[i].add(v)
            todo[i] -= 1
    state, records = 104733, []
    perm = list(range(4)) + [20, 21] + list(range(4, 20))
    d = [8] * 4 + [10] * 2 + [9] * 16
    for sample in range(32):
        changed = 0
        for trial in range(20000):
            edges = [(i, j) for i in range(22) for j in sorted(adj[i]) if i < j]
            state = (1664525 * state + 1013904223) % (1 << 32)
            a, z = edges[state % len(edges)]
            state = (1664525 * state + 1013904223) % (1 << 32)
            x, y = edges[state % len(edges)]
            if len({a, z, x, y}) != 4 or x in adj[a] or y in adj[z]:
                continue
            for i, j in ((a, z), (x, y)):
                adj[i].remove(j); adj[j].remove(i)
            for i, j in ((a, x), (z, y)):
                adj[i].add(j); adj[j].add(i)
            changed += 1
            if changed == 16:
                break
        require(changed == 16, 'unfinished control construction')
        R = [[int(perm[j] in adj[perm[i]]) for j in range(22)] for i in range(22)]
        require(list(map(sum, R)) == d, 'control degree mismatch')
        F = [[0 if i == j else d[i] + d[j] - 14 + (17 - d[i] - d[j]) * R[i][j]
              - sum(R[i][k] * R[k][j] for k in range(22)) for j in range(22)] for i in range(22)]
        M = [row[:6] for row in R[6:]]
        G = [[sum(x[i] * x[j] for x in M) for j in range(6)] for i in range(6)]
        root = [row[:6] for row in R[:6]]
        for i in range(16):
            for j in range(6):
                rhs = (3 if j < 4 else 5 - 2 * M[i][j]) - sum(M[i][k] * root[k][j] for k in range(6)) - F[i + 6][j]
                require(sum(R[i + 6][k + 6] * M[k][j] for k in range(16)) == rhs, 'signed spine identity')
        f = [sum(row) for row in F]
        require(f[:6] == root_f(root), 'signed root incidence')
        require(f[6:] == [1 + 2 * (sum(x[:4]) - sum(x[4:])) for x in M], 'signed B incidence')
        require(sum(f[:6]) == -4 + 4 * (sum(root[i][j] for i, j in it.combinations(range(4), 2)) - root[4][5]), 'root budget identity')
        records.append({'R': R, 'F': F, 'G': G})
    return records


def run():
    families = root_orbits()
    two_active = [4, 5, 6, 8]
    closed_weight_two = []
    for profile in two_active:
        spec = specification(profile, 2)
        require(all(spec['f'][a] == 2 for a in spec['active']), 'two active roots')
        require(any(x for vector in spec['correlations'] for x in vector), 'weight-two obstruction missing')
        closed_weight_two.append({'profile': profile, 'correlations': spec['correlations']})
    cases = []
    for profile, weight in [(4, 0), (4, 1), (8, 0), (8, 1), (6, 0), (6, 1), (7, 0), (5, 0), (5, 1)]:
        spec = specification(profile, weight)
        moments, tested, full = incidence(spec)
        records = [local_stars(spec, c) for c in full]
        summary = {'profile': profile, 'weight': weight, 'moments': moments, 'positive_multisets': tested,
                   'binary_forms': len(full), 'incidence_sha256': fingerprint(full),
                   'defect_assignments': sum(len(r['defect_assignments']) for r in records),
                   'forms_with_defect_assignment': sum(bool(r['defect_assignments']) for r in records),
                   'local_star_masks': sum(len(s['masks']) for r in records for d in r['local_domains'] for s in d['stars']),
                   'local_surviving_assignments': sum(len(r['local_surviving_assignments']) for r in records),
                   'forms_with_local_survivor': sum(bool(r['local_surviving_assignments']) for r in records),
                   'symmetry_exclusions': sum(len(r['symmetry_exclusions']) for r in records),
                   'symmetry_deletion_steps': sum(len(t['steps']) for r in records for t in r['symmetry_exclusions']),
                   'symmetry_deleted_candidates': sum(step[2].bit_count() for r in records for t in r['symmetry_exclusions'] for step in t['steps']),
                   'unexcluded_assignments': 0,
                   'full_records_sha256': fingerprint(records)}
        cases.append({'spec': spec, 'summary': summary, 'records': records})
        print(json.dumps(summary, sort_keys=True), flush=True)
    controls = signed_controls()
    propagation_controls = [symmetry_trace(d) for d in ([[2], [1]], [[2], [0]], [[0, 2], [1]])]
    require([t['empty_row'] is not None for t in propagation_controls] == [False, True, False], 'positive/negative symmetry controls')
    summary = {'agent': 'six-books-1', 'role': 'researcher', 'complete': True,
               'histogram': [4, 16, 2], 'root_defect_four_excluded': True, 'root_defect_lower_bound': 8,
               'analytic_root_profiles': 8, 'labeled_root_profiles': 127,
               'profile_copy_counts': list(map(len, families)),
               'root_families_sha256': fingerprint(families), 'weight_two_obstructions': closed_weight_two,
               'cases': [c['summary'] for c in cases], 'signed_controls': 32,
               'signed_controls_sha256': fingerprint(controls), 'controls_are_validation_only': True,
               'propagation_controls_sha256': fingerprint(propagation_controls),
               'B_pair_page_constraints_used': False, 'branching_used': False}
    return summary, {'cases': cases, 'root_families': families, 'controls': controls,
                     'propagation_controls': propagation_controls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', type=Path, help='Optional private runtime records for the separate checker')
    parser.add_argument('--write-expected', type=Path, help='Explicit development output; otherwise compare committed expectation')
    args = parser.parse_args()
    summary, records = run()
    if args.records:
        args.records.write_text(json.dumps(records, separators=(',', ':')) + '\n')
    if args.write_expected:
        args.write_expected.write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    else:
        expected = json.loads(Path(__file__).with_name('degree98_root_four_expected.json').read_text())
        require(summary == expected, 'compact expected result mismatch')
    print(json.dumps({'agent': 'six-books-1', 'role': 'researcher', 'complete': True,
                      'root_defect_four_excluded': True, 'root_defect_lower_bound': 8,
                      'binary_forms': sum(c['binary_forms'] for c in summary['cases']),
                      'defect_assignments': sum(c['defect_assignments'] for c in summary['cases'])}, sort_keys=True))


if __name__ == '__main__':
    main()
