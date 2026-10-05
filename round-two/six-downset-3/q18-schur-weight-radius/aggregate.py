"""exact three-weight deduction from published q18 witness DATA.

Only the 58-by-81 S/B entries and old 81-by-81 B/B entries are evaluated.
The canonical mask/orbit definition is openly credited to the published
q18-ns-fiber-obstruction source. No ancestor executable or PSD factor runs.
This is an author computation, not an independent review or PSD recertification.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def data_file(root, name, digest):
    raw = (root / name).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest, 'whole public DATA: ' + name)
    return json.loads(raw)


def aggregate(include_individual_data=False):
    root = Path(__file__).resolve().parent
    witness = data_file(root, 'CANDIDATE.json',
                        'fae303f40a542478e22083289ea982cd1814b58323f4e13d237d7269583ab16e')
    comparison = data_file(root, 'COMPARISON.json',
                           '6770d9db69983e4cbd75480a9f784dd4c9c9d254cf7f455bbd0d4a62633b2ca2')
    published = data_file(root, 'QUARTER-REFERENCE.json',
                          'd50efb0d24ef3f1f10a205e9e317058f7b4ac4cebb9427ab3faacce1691979b0')
    denominator = witness['denominator']
    old_denominator = comparison['comparison_free_denominator']
    require(denominator == 2**32 and old_denominator == 16384, 'exact normalizations')
    masks = []
    for size in range(1, 4):
        for support in combinations(range(21), size):
            m = sum(1 << p for p in support)
            if size == 3 and ((m & 7).bit_count() < 2 or
                              ((m & 7) == 6 and (m & (((1 << 9) - 1) << 3)))):
                continue
            masks.append(m)
    masks.sort()
    label = {m: (m & 7, ((m >> 3) & 511).bit_count(), (m >> 12).bit_count())
             for m in masks}
    star = [m for m in masks if m & 1]
    types = [(0, 2, 0), (0, 0, 2), (6, 0, 1)]
    bad = [[m for m in masks if label[m] == o] for o in types]
    require(len(masks) == 277 and len(star) == 58 and list(map(len, bad)) == [36, 36, 9],
            'same original carrier and three actual bad types')
    keys = sorted({tuple(sorted((label[m], label[n])))
                   for i, m in enumerate(masks) for n in masks[i+1:]
                   if m != 1 and n != 1 and not (m & n)})
    require(len(keys) == 143 and len(set(keys)) == 143, 'whole canonical free order')
    require(len(witness['free_numerators']) == len(keys) ==
            len(comparison['comparison_free_numerators']), 'all attributed coefficient ownership')
    table = dict(zip(keys, witness['free_numerators']))
    old_table = dict(zip(keys, comparison['comparison_free_numerators']))

    def entry(m, n, coefficient, d):
        if m == n:
            return 57 * d
        if m & n:
            return -d
        if m == 1:
            return -sum(entry(s, n, coefficient, d) for s in star if s != 1)
        if n == 1:
            return entry(n, m, coefficient, d)
        return coefficient[tuple(sorted((label[m], label[n])))]

    # Three integer columns, with literal original star coordinates retained.
    columns = [[sum(entry(s, m, table, denominator) for m in block) for s in star]
               for block in bad]
    require(all(sum(v) == 0 for v in columns), 'three whole original star-kernel vectors')
    old_cap = [[F(sum(entry(m, n, old_table, old_denominator)
                     for m in left for n in right), old_denominator)
                for right in bad] for left in bad]
    gram = [[F(sum(x*y for x, y in zip(left, right)), 58*denominator**2)
             for right in columns] for left in columns]
    K = [[gram[i][j] - old_cap[i][j] for j in range(3)] for i in range(3)]
    require(all(K[i][j] == K[j][i] for i in range(3) for j in range(3)),
            'whole symmetric quadratic')
    edge_counts = [[sum(not (m & n) for m in left for n in right)
                    for right in bad] for left in bad]
    require(edge_counts == [[756, 1296, 324], [1296, 756, 252], [324, 252, 0]],
            'every original unordered type-pair edge exists except bcW/bcW')
    require(old_cap[2][2] == 441, 'literal shared-core old cap')
    qweights = [F(1, 4), F(1, 4), F(1)]
    def value(A, u):
        return sum(u[i]*A[i][j]*u[j] for i in range(3) for j in range(3))
    require(value(gram, qweights) == F(published['Q']) and
            value(old_cap, qweights) == F(published['old_BB_cap']),
            'fresh aggregate exactly decodes published quarter-weight DATA')
    quarter_vector = [sum(qweights[i]*columns[i][s] for i in range(3))
                      for s in range(len(star))]
    require([4*x for x in quarter_vector] == published['v_S_complete58_numerators'] and
            published['v_S_complete58_denominator'] == 4*denominator,
            'ALL 58 fresh quarter-weight original vector coordinates')
    A = K[0][0] + 2*K[0][1] + K[1][1]
    B = 2*(K[0][2] + K[1][2])
    C = K[2][2]
    result = {
        'actual_agent': 'six-downset-3', 'role': 'researcher',
        'status': 'exact aggregation; real optimization bridge separately required',
        'published_witness_source_commit': '782bc9042896c0f3887b1807dbd991f75fa13c9b',
        'bad_type_order': ['ZZ', 'WW', 'bcW'], 'bad_sizes': [36, 36, 9],
        'original_star_masks': star, 'candidate_vector_denominator': denominator,
        'candidate_three_whole58_vector_numerators': columns,
        'Q_Gram': [[str(x) for x in row] for row in gram],
        'old_BB_cap': [[str(x) for x in row] for row in old_cap],
        'Schur_minus_comparison_K': [[str(x) for x in row] for row in K],
        'ordered_original_BB_disjoint_type_counts': edge_counts,
        'balanced_gap_coefficients_t2_t_1': [str(A), str(B), str(C)],
        'balanced_normalized_bound_at_quarter': str(2*value(K, qweights)),
        'balanced_low_chart_derivative_twice_at_quarter': str(A-16*C),
        'parent_executable_or_PSD_factor_replayed': False,
        'independent_review_claimed': False,
    }
    if include_individual_data:
        flat_bad = [m for block in bad for m in block]
        result['_new_individual_data'] = {
            'bad_masks': flat_bad,
            'bad_type_index': [i for i, block in enumerate(bad) for m in block],
            'star_by_bad_candidate_numerators': [
                [entry(s, m, table, denominator) for m in flat_bad] for s in star],
            'old_bad_by_bad_numerators': [
                [entry(m, n, old_table, old_denominator) for n in flat_bad] for m in flat_bad],
            'old_denominator': old_denominator,
        }
    return result


if __name__ == '__main__':
    print(json.dumps(aggregate(), indent=2))
