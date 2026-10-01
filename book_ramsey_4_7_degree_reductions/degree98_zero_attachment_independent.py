"""Separate binary-word/cofactor/full-Gram and literal-page audit.
six-books-1, researcher. Two author implementations, not peer review.
Python 3.11+, standard library only. No import from the primary checker.
"""
from itertools import combinations, permutations, product
from fractions import Fraction
from pathlib import Path
import argparse
import copy
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def decode_certificate(c):
    require(type(c) is dict and c.get('schema') == 1, 'schema')
    pool = c['negative_vectors']
    require(type(pool) is list and pool, 'negative pool')
    require(all(type(q) is list and len(q) == 10 and any(q)
                and all(type(x) is int for x in q) for q in pool), 'integer negative-vector words')
    reps = c['cubic_representatives']
    require(type(reps) is list and len(reps) == 4, 'four graph words')
    for row in reps:
        require(type(row) is list and len(row) == 10, 'ten graph words')
        require(all(type(w) is int and 0 <= w < 1024 for w in row), 'graph word range')
        require(all(row[i].bit_count() == 3 and not (row[i] >> i & 1) for i in range(10)), 'simple cubic')
        require(all((row[i] >> k & 1) == (row[k] >> i & 1) for i in range(10) for k in range(10)), 'symmetry')
    return pool, reps


def matrix(words):
    n = len(words)
    return [[int(words[i] >> k & 1) for k in range(n)] for i in range(n)]


def capacity(words):
    # Direct local codegrees, with a common red root outside these ten.
    return [[5 if i == k else ((2 if words[i] >> k & 1 else 3)
                               - (words[i] & words[k]).bit_count())
             for k in range(10)] for i in range(10)]


def all_profiles():
    profiles = set()
    for inside in range(8):
        residual = [2] * 3
        for bit, (i, k) in enumerate(combinations(range(3), 2)):
            if inside >> bit & 1:
                residual[i] -= 1
                residual[k] -= 1
        # Independent labeled neighbor-subset domain, then sort columns.
        choices = [list(combinations(range(6), d)) for d in residual]
        for selected in product(*choices):
            cols = tuple(sorted(sum((x in selected[i]) << i for i in range(3)) for x in range(6)))
            profiles.add((inside, cols))
    return sorted(profiles)


def binary_tails(profiles):
    required = {tuple(3 - w.bit_count() for w in cols) for inside, cols in profiles}
    buckets = {d: [] for d in required}
    edges = list(combinations(range(6), 2))
    for word in range(1 << 15):
        rows = [0] * 6
        for bit, (i, k) in enumerate(edges):
            if word >> bit & 1:
                rows[i] |= 1 << k
                rows[k] |= 1 << i
        degrees = tuple(w.bit_count() for w in rows)
        if degrees in buckets:
            buckets[degrees].append(tuple(rows))
    return {d: sorted(rows) for d, rows in buckets.items()}


def join_profile(inside, cols, tail):
    rows = [0] * 10
    def connect(i, k):
        rows[i] |= 1 << k
        rows[k] |= 1 << i
    for i in (1, 2, 3):
        connect(0, i)
    for bit, (i, k) in enumerate(combinations((1, 2, 3), 2)):
        if inside >> bit & 1:
            connect(i, k)
    for x, w in enumerate(cols):
        for i in range(3):
            if w >> i & 1:
                connect(i + 1, x + 4)
    for i, k in combinations(range(6), 2):
        if tail[i] >> k & 1:
            connect(i + 4, k + 4)
    require(all(w.bit_count() == 3 for w in rows), 'joined cubic')
    return rows


def rooted_map(rows, representative):
    # All images of root and its three neighbors; only tail permutations
    # within equal incidence classes remain. Covers every possible map.
    for root in range(10):
        ns = [i for i in range(10) if representative[root] >> i & 1]
        other = [i for i in range(10) if i != root and i not in ns]
        for order in permutations(ns):
            images = [root, *order] + [-1] * 6
            if any((rows[i] >> k & 1) != (representative[images[i]] >> images[k] & 1)
                   for i in range(4) for k in range(4)):
                continue
            groups_left, groups_right = {}, {}
            for x in range(4, 10):
                w = sum((rows[x] >> (i + 1) & 1) << i for i in range(3))
                groups_left.setdefault(w, []).append(x)
            for x in other:
                w = sum((representative[x] >> order[i] & 1) << i for i in range(3))
                groups_right.setdefault(w, []).append(x)
            if {w: len(v) for w, v in groups_left.items()} != {w: len(v) for w, v in groups_right.items()}:
                continue
            keys = sorted(groups_left)
            for choices in product(*(permutations(groups_right[w]) for w in keys)):
                for w, selected in zip(keys, choices):
                    for x, t in zip(groups_left[w], selected):
                        images[x] = t
                if all((rows[i] >> k & 1) == (representative[images[i]] >> images[k] & 1)
                       for i in range(10) for k in range(10)):
                    return images
    return None


def census(certificate, private_matrices):
    pool, reps = decode_certificate(certificate)
    profiles = all_profiles()
    tails = binary_tails(profiles)
    output_profiles = []
    counts = [0] * 4
    rejects = 0
    graph_hash, matrix_hash = hashlib.sha256(), hashlib.sha256()
    entry = 0
    for inside, cols in profiles:
        residual = tuple(3 - w.bit_count() for w in cols)
        output_profiles.append({'mask': inside, 'columns': list(cols), 'count': len(tails[residual])})
        for tail in tails[residual]:
            rows = join_profile(inside, cols, tail)
            j, s = matrix(rows), capacity(rows)
            word = ''.join(str(j[i][k]) for i, k in combinations(range(10), 2))
            graph_hash.update((word + '\n').encode())
            matrix_hash.update((json.dumps(s, separators=(',', ':')) + '\n').encode())
            negative = any(sum(q[i] * s[i][k] * q[k] for i in range(10) for k in range(10)) < 0 for q in pool)
            if negative:
                rejects += 1
                cid = None
            else:
                found = [i for i, r in enumerate(reps) if rooted_map(rows, r) is not None]
                require(len(found) == 1, 'unique remaining class')
                cid = found[0]
                counts[cid] += 1
            if private_matrices is not None:
                require(entry < len(private_matrices), 'full matrices missing entry')
                r = private_matrices[entry]
                require(r['profile'] == len(output_profiles) - 1 and r['tail'] == list(tail), 'complete ordered domain')
                require(r['J'] == j and r['S0'] == s and r['class'] == cid, 'every literal J/S0 entry')
            entry += 1
    if private_matrices is not None:
        require(entry == len(private_matrices), 'no extra full matrices')
    return {'profiles': output_profiles, 'graphs': entry, 'negative_forms': rejects,
            'class_copies': counts, 'graph_sha256': graph_hash.hexdigest(),
            'matrix_sha256': matrix_hash.hexdigest()}


def determinant(a):
    # Fraction-free Bareiss, separate from the primary Gauss-Jordan inverse.
    b = [r[:] for r in a]
    n, sign, denominator = len(b), 1, 1
    for k in range(n - 1):
        p = next((i for i in range(k, n) if b[i][k]), None)
        if p is None:
            return 0
        if p != k:
            b[k], b[p] = b[p], b[k]
            sign = -sign
        value = b[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = value * b[i][j] - b[i][k] * b[k][j]
                require(numerator % denominator == 0, 'exact Bareiss division')
                b[i][j] = numerator // denominator
        for i in range(k + 1, n):
            b[i][k] = 0
        denominator = value
    return sign * b[-1][-1]


def adjugate(a):
    d = determinant(a)
    require(d != 0, 'invertible representative')
    adj = [[(-1) ** (i + j) * determinant([[a[r][s] for s in range(10) if s != i]
                                         for r in range(10) if r != j])
            for j in range(10)] for i in range(10)]
    require(all(sum(a[i][k] * adj[k][j] for k in range(10)) == d * (i == j)
                for i in range(10) for j in range(10)), 'all adjugate entries')
    return d, adj


def literal_stars(jwords, rows, exceptional):
    aset = set(range(5)) - set(exceptional)
    # Full red neighborhoods of all ten N points, fixed independently of W.
    rn = [{0} | {y + 1 for y in range(10) if jwords[x] >> y & 1}
          | {v + 11 for v in range(11) if rows[v] >> x & 1} for x in range(10)]
    bn = [set(range(22)) - {x + 1} - rn[x] for x in range(10)]
    result = []
    for v in sorted(aset):
        required = sum(1 << u for u in aset if u != v)
        allowed = []
        for word in range(2048):
            if word.bit_count() != 4 or word >> v & 1 or word & required != required:
                continue
            rv = {x + 1 for x in range(10) if rows[v] >> x & 1}
            rv |= {u + 11 for u in range(11) if word >> u & 1}
            require(len(rv) == 8, 'literal A degree')
            bv = set(range(22)) - {v + 11} - rv
            if all((len(rv & rn[x]) <= 3 if rows[v] >> x & 1 else len(bv & bn[x]) <= 6)
                   for x in range(10)):
                allowed.append(word)
        result.append({'vertex': v, 'stars': allowed})
    require(any(not r['stars'] for r in result), 'literal A obstruction')
    return result


def rows_audit(jwords):
    s = capacity(jwords)
    det, adj = adjugate(s)
    def numerator(a, b):
        return sum(adj[i][k] for i in range(10) if a >> i & 1
                   for k in range(10) if b >> k & 1)
    four = [w for w in range(1024) if w.bit_count() == 4 and 23 * numerator(w, w) == 20 * det]
    pairs = {(i, k) for i, k in combinations(range(len(four)), 2)
             if 23 * numerator(four[i], four[k]) == -3 * det}
    disjoint = [list(pair) for pair in sorted(pairs) if not four[pair[0]] & four[pair[1]]]
    # A literal combination census is separate from the primary clique search.
    all_h = ([h for h in combinations(range(len(four)), 5)
              if all(pair in pairs for pair in combinations(h, 2))] if disjoint else None)
    eligible = ([] if all_h is None else
                [h for h in all_h if any(i in h and k in h for i, k in disjoint)
                 and all(sum(four[i] >> x & 1 for i in h) == 2 for x in range(10))])
    five = [w for w in range(1024) if w.bit_count() == 5 and 69 * numerator(w, w) == 65 * det]
    completions, stars = [], []
    for h in eligible:
        hrows = tuple(four[i] for i in h)
        candidates = [w for w in five if all(23 * numerator(w, r) == 2 * det for r in hrows)]
        solutions = []
        # No inverse-Gram clique condition is used for these six rows:
        # directly test every six-subset's columns and full 100-entry Gram.
        for selected in combinations(candidates, 6):
            rows = hrows + selected
            if any(sum(w >> x & 1 for w in rows) != 5 for x in range(10)):
                continue
            g = [[sum((w >> x & 1) * (w >> y & 1) for w in rows) for y in range(10)] for x in range(10)]
            if g != s:
                continue
            solutions.append(list(rows))
            for pair in combinations(range(5), 2):
                if not rows[pair[0]] & rows[pair[1]]:
                    stars.append({'rows': list(rows), 'exceptional': list(pair),
                                  'A_star_domains': literal_stars(jwords, rows, pair)})
        completions.append({'H': list(hrows), 'five_candidates': candidates, 'solutions': sorted(solutions)})
    inverse = [[Fraction(x, det) for x in row] for row in adj]
    return {'S0': s, 'inverse': [[[x.numerator, x.denominator] for x in row] for row in inverse],
            'four_candidates': four, 'four_compatible_pairs': len(pairs),
            'compatible_disjoint_pairs': disjoint,
            'H_cliques': None if all_h is None else len(all_h), 'eligible_H': len(eligible),
            'five_candidates': five, 'completions': completions, 'stars': stars}


def rejection_controls(certificate, regenerated, private_matrices):
    rejected = 0
    for change in ('short_vector', 'boolean_vector', 'zero_vector', 'empty_pool',
                   'loop', 'degree', 'asymmetry', 'missing_class'):
        c = copy.deepcopy(certificate)
        if change == 'short_vector':
            c['negative_vectors'][0].pop()
        elif change == 'boolean_vector':
            c['negative_vectors'][0][0] = True
        elif change == 'zero_vector':
            c['negative_vectors'][0] = [0] * 10
        elif change == 'empty_pool':
            c['negative_vectors'] = []
        elif change == 'loop':
            c['cubic_representatives'][0][0] |= 1
        elif change == 'degree':
            c['cubic_representatives'][0][0] = 0
        elif change == 'asymmetry':
            c['cubic_representatives'][0][0] ^= (1 << 1) | (1 << 4)
        else:
            c['cubic_representatives'].pop()
        try:
            decode_certificate(c)
        except (ValueError, KeyError, TypeError):
            rejected += 1
        else:
            raise ValueError('malformed certificate accepted: ' + change)
    for change in ('capacity', 'Gram_row', 'star', 'domain_hash'):
        wrong = copy.deepcopy(regenerated)
        if change == 'capacity':
            wrong['row_domains'][0]['S0'][0][0] += 1
        elif change == 'Gram_row':
            wrong['row_domains'][0]['completions'][0]['solutions'][0][0] ^= 1
        elif change == 'star':
            wrong['row_domains'][0]['stars'][0]['A_star_domains'][0]['stars'].append(0)
        else:
            wrong['cubic_census']['graph_sha256'] = '0' * 64
        require(wrong != regenerated, 'actual corruption')
        try:
            require(wrong == regenerated, 'regenerated entry comparison')
        except ValueError:
            rejected += 1
    if private_matrices is not None:
        wrong = copy.deepcopy(private_matrices[0])
        wrong['S0'][0][1] += 1
        try:
            require(wrong['S0'] == capacity([sum(x << k for k, x in enumerate(row))
                                            for row in wrong['J']]), 'literal full matrix')
        except ValueError:
            rejected += 1
        else:
            raise ValueError('altered full matrix accepted')
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--matrices', type=Path)
    args = parser.parse_args()
    c = json.loads(Path(__file__).with_name('degree98_zero_attachment_expected.json').read_text())
    private = None
    if args.matrices:
        private = json.loads(args.matrices.read_text())['cubic_matrices']
    ci = census(c, private)
    rs = [rows_audit(j) for j in c['cubic_representatives']]
    regenerated = {'cubic_census': ci, 'row_domains': rs}
    require(ci == c['results']['cubic_census'] and rs == c['results']['row_domains'], 'complete entry agreement')
    corruptions = rejection_controls(c, regenerated, private)
    print(json.dumps({'agent': 'six-books-1', 'role': 'researcher', 'complete': True,
                      'binary_six_words': 32768, 'profiles': len(ci['profiles']), 'graphs': ci['graphs'],
                      'negative_forms': ci['negative_forms'], 'class_copies': ci['class_copies'],
                      'binary_Gram_matrices': sum(len(r['solutions']) for x in rs for r in x['completions']),
                      'exceptional_pair_placements': sum(len(x['stars']) for x in rs),
                      'A_star_survivors': 0, 'corruptions_rejected': corruptions,
                      'full_J_entries_compared': 100 * ci['graphs'] if private is not None else 0,
                      'full_S0_entries_compared': 100 * ci['graphs'] if private is not None else 0}, sort_keys=True))


if __name__ == '__main__':
    main()
