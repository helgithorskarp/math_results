"""new 81-weight dual, no original candidate PSD replay.

The new weight-space matrix is E-H, where H=A_NS^T A_NS/58-C_old,BB.
Only public compact DATA and this contribution's fresh aggregation run.
New physical action and rational factors certify this distinct matrix.
All ordinary reduction/completeness bridges are proved in PROOF.md,
unformalized and independently unreviewed.
"""
from fractions import Fraction as F
import json
from aggregate import aggregate, require


def factor(A):
    n = len(A)
    lower = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    pivots = []
    for j in range(n):
        pivot = A[j][j] - sum(lower[j][k]**2*pivots[k] for k in range(j))
        require(pivot > 0, 'NEW dual positive exact pivot')
        pivots.append(pivot)
        for i in range(j+1, n):
            lower[i][j] = (A[i][j] - sum(lower[i][k]*lower[j][k]*pivots[k]
                                         for k in range(j))) / pivot
    for i in range(n):
        for j in range(n):
            require(A[i][j] == sum(lower[i][k]*pivots[k]*lower[j][k] for k in range(n)),
                    'ALL new dual factor identity positions')
    return [str(p) for p in pivots]


def check(aggregated=None):
    if aggregated is None:
        aggregated = aggregate(include_individual_data=True)
    literal = aggregated.pop('_new_individual_data')
    masks = literal['bad_masks'];types = literal['bad_type_index'];n = len(masks)
    require(n == 81, 'whole weight-space dimension')
    K = [[F(x) for x in row] for row in aggregated['Schur_minus_comparison_K']]
    # Ordered edge multiplicities are 756,756,324,252 for these four types.
    edge_coefficients = {
        (0, 0): (K[0][0]+K[0][1]-K[2][2]/2)/756,
        (1, 1): (K[1][1]+K[0][1]-K[2][2]/2)/756,
        (0, 2): (K[0][2]+K[2][2]/2)/324,
        (1, 2): (K[1][2]+K[2][2]/2)/252,
    }
    require(all(v > 0 for v in edge_coefficients.values()), 'ALL four positive actual edge prices')
    original_NS = literal['star_by_bad_candidate_numerators']
    old_BB = literal['old_bad_by_bad_numerators']
    denominator = aggregated['candidate_vector_denominator']
    old_denominator = literal['old_denominator']
    H = [[F(sum(original_NS[s][i]*original_NS[s][j] for s in range(58)),
              58*denominator**2) - F(old_BB[i][j], old_denominator)
          for j in range(n)] for i in range(n)]
    E = [[edge_coefficients.get(tuple(sorted((types[i], types[j]))), F(0))
          if not (masks[i] & masks[j]) else F(0)
          for j in range(n)] for i in range(n)]
    R = [[E[i][j]-H[i][j] for j in range(n)] for i in range(n)]
    require(all(sum(row) == 0 for row in R), 'ALL 81 exact dual kernel rows')
    maximum_twice = sum(x for row in K for x in row)
    require(sum(x for row in E for x in row) == maximum_twice,
            'whole new edge budget equals all-one gap')
    require(all(sum(H[i][j] for i in range(n) if types[i] == a
                    for j in range(n) if types[j] == b) == K[a][b]
                for a in range(3) for b in range(3)), 'ALL nine original-to-aggregate dual positions')
    # The constants use physical orbit indicators. Standards use point differences.
    constant = [[int(t == a) for t in types] for a in range(3)]
    zstd = [[int(t == 0)*(int(bool(m & 8))-int(bool(m & 16)))
             for m, t in zip(masks, types)]]
    wstd = [[int(t == a)*(int(bool(m & (1 << 12)))-int(bool(m & (1 << 13))))
             for m, t in zip(masks, types)] for a in (1, 2)]
    def pair_seed(offset, type_index):
        pairs = {(0, 1): 1, (2, 3): 1, (0, 2): -1, (1, 3): -1}
        return [pairs.get(tuple(p for p in range(9) if m & (1 << (offset+p))), 0)
                if t == type_index else 0 for m, t in zip(masks, types)]
    sectors = {'constant': constant, 'Z_standard': zstd, 'W_standard': wstd,
               'ZZ_zero_incidence': [pair_seed(3, 0)],
               'WW_zero_incidence': [pair_seed(12, 1)]}
    actions = 0;grams = {};pivots = {};factor_positions = 0
    for name, seeds in sectors.items():
        norms = [sum(x*x for x in v) for v in seeds]
        require(all(sum(x*y for x, y in zip(v, w)) == norms[i]*int(i == j)
                    for i, v in enumerate(seeds) for j, w in enumerate(seeds)),
                'ALL new weight-space seed metric positions')
        images = [[sum(R[i][j]*v[j] for j in range(n)) for i in range(n)] for v in seeds]
        gram = [[sum(v[i]*images[j][i] for i in range(n))
                 for j in range(len(seeds))] for v in seeds]
        for j, image in enumerate(images):
            for i in range(n):
                require(image[i] == sum(seeds[k][i]*gram[k][j]/norms[k]
                                        for k in range(len(seeds))),
                        'EVERY new exact physical dual action coordinate')
                actions += 1
        grams[name] = [[str(x) for x in row] for row in gram]
        if name == 'constant':
            # (1_ZZ-4*1_bcW,1_WW-4*1_bcW) span constants perpendicular to 1_B.
            T = [[1, 0, -4], [0, 1, -4]]
            restricted = [[sum(T[a][i]*gram[i][j]*T[b][j]
                               for i in range(3) for j in range(3))
                           for b in range(2)] for a in range(2)]
        else:
            restricted = gram
        pivots[name] = factor(restricted)
        factor_positions += len(restricted)**2
    require(actions == 81*8 and factor_positions == 11,
            'ALL new eight seeds and five full factors accounted for')
    return {
        'actual_agent': 'six-downset-3', 'role': 'researcher',
        'status': 'complete ordinary author dual proof; unformalized and independently unreviewed',
        'witness_source_commit': aggregated['published_witness_source_commit'],
        'dimension': n, 'strict_positive_edge_prices': {
            str(k): str(v) for k, v in edge_coefficients.items()},
        'edge_price_ZZ_WW': '0', 'kernel': 'span of the all-one 81-vector',
        'whole_original_dual_kernel_rows': 81, 'whole_original_H_aggregate_positions': 9,
        'new_complete_physical_actions': actions, 'new_complete_factor_positions': factor_positions,
        'physical_sector_dimensions': [3, 8, 16, 27, 27],
        'new_seed_physical_Gram_R': grams, 'all_new_exact_factor_pivots': pivots,
        'sum_all_ordered_edge_prices': str(maximum_twice),
        'full_individual_weight_maximum': str(maximum_twice/2),
        'full_individual_weight_domain': 'all real u_i>=0 on the 81 bad vertices; alpha>0 for quotient',
        'unique_maximizers': 'all 81 individual weights equal to the same positive constant',
        'alpha_zero_implies_nonpositive_gap': True,
        'ancestor_executable_or_PSD_factor_replayed': False,
        'independent_review_claimed': False,
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
