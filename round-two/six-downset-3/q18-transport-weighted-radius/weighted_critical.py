"""Fresh original-column certificate excluding sharp equality at rho.

Openly shares the NEW local census defining-DATA decoder. Ordinary
equality, PSD-kernel and all-real bridges belong in WEIGHTED-CRITICAL.md.
No ancestor EXPECTED, factor or mathematical program is imported.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import gcd, isqrt, lcm
from pathlib import Path
import hashlib
import importlib.util
import json


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def multiply(p, q):
    return [p[0]*q[0], p[0]*q[1]+p[1]*q[0], p[1]*q[1]]


def check():
    root = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location('critical_weighted_census', root/'census.py')
    decoder = importlib.util.module_from_spec(spec); spec.loader.exec_module(decoder)
    S, B, label, A, nums, P, N, D = decoder.original(); X = sorted(label)
    abc = S.index(7); J = [i for i in P if i != abc]
    triples = [j for j, bad in enumerate(B) if label[bad] == (6, 0, 1)]
    raw = (root.parent/'q18-schur-weight-radius/COMPARISON.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            '6770d9db69983e4cbd75480a9f784dd4c9c9d254cf7f455bbd0d4a62633b2ca2',
            'whole original comparison DATA')
    comp = json.loads(raw)
    keys = sorted({tuple(sorted((label[u], label[v]))) for i, u in enumerate(X) for v in X[i+1:]
                   if u != 1 and v != 1 and not u & v})
    require(len(keys) == 143 and comp['comparison_free_denominator'] == 16384 and
            len(comp['comparison_free_numerators']) == 143, 'entire comparison coefficient domain')
    table = {key: F(value, 16384) for key, value in zip(keys, comp['comparison_free_numerators'])}
    old = [[F(57) if u == v else F(-1) if u & v else
            table[tuple(sorted((label[u], label[v])))] for v in B] for u in B]
    a = [F(nums[abc], D), F(-15840)]
    b = [F(sum(nums[i] for i in P)-nums[abc], D), F(-269280)]
    R = F(186731, 4096); lam = [(b[0]-19*R)/580, b[1]/580]
    T = [a[i]+b[i] for i in range(2)]
    x = [a[i]-9*lam[i] for i in range(2)]
    y = [(b[i]+351*lam[i])/19 for i in range(2)]
    z = [-(T[i]+342*lam[i])/38 for i in range(2)]
    base_energy = [multiply(a, a)[i]+multiply(b, b)[i]/19+multiply(T, T)[i]/38 for i in range(3)]
    Baffine = [b[0]-19*R, b[1]]
    f = [base_energy[i]/58-(F(4998177, 1024) if i == 0 else 0)+
         F(9, 11020)*multiply(Baffine, Baffine)[i] for i in range(3)]
    common = lcm(*(value.denominator for value in f)); primitive = [int(value*common) for value in f]
    div = gcd(gcd(abs(primitive[0]), abs(primitive[1])), abs(primitive[2]))
    primitive = [value//div for value in primitive]
    require(primitive == [10134638482936670690842619, -3933215268387039896854855680,
                          234665871787304147493480038400], 'exact original weighted root polynomial')
    disc = primitive[1]**2-4*primitive[0]*primitive[2]
    require(disc > 0 and isqrt(disc)**2 != disc, 'weighted root irrational')
    groups = defaultdict(list)
    for j, bad in enumerate(B):
        pure = j not in triples
        row_sum = sum(old[j]); triple_sum = sum(old[j][k] for k in triples)
        ac = [F(A[abc][j], D), F(-220*int(pure and not S[abc] & bad))]
        jc = [F(sum(A[i][j] for i in J), D),
              F(-220*sum(not S[i] & bad for i in J)) if pure else F(0)]
        # ONLY disjoint P/pure entries are forced to the radius lower bound.
        # The nine triple J column sums remain39, not39-18*220e.
        require((ac[1], jc[1]) == ((F(-220), F(-3740)) if pure else (F(0), F(0))),
                'whole81 original column licence; fixed triple sums not decremented')
        rhs1 = multiply([x[i]-z[i] for i in range(2)], ac)
        rhs2 = multiply([y[i]-z[i] for i in range(2)], jc)
        residual = [(row_sum if i == 0 else 0)+(triple_sum*lam[i] if i < 2 else 0)-
                    (rhs1[i]+rhs2[i])/58 for i in range(3)]
        reduced = [residual[i]-residual[2]*f[i]/f[2] for i in range(2)]
        if pure:
            require(reduced[1] != 0 and reduced[0] != 0, 'each72 pure critical equation has nonzero affine remainder')
            forced = -reduced[0]/reduced[1]
            require(forced > F(1, 150) > F(1, 314), 'each72 exact forced critical radius outside proved cage')
        else:
            forced = None
            require(residual == [0, 0, 0] and reduced == [0, 0],
                    'each9 triple critical equation exactly satisfied by chosen lambda')
        groups[label[bad]].append({'original_bad_mask': bad, 'old_row_sum': str(row_sum),
                                  'old_triple_sum': str(triple_sum),
                                  'forced_original_abc_affine': [str(v) for v in ac],
                                  'forced_original_J_sum_affine': [str(v) for v in jc],
                                  'critical_residual_polynomial': [str(v) for v in residual],
                                  'exact_affine_remainder_mod_F': [str(v) for v in reduced],
                                  'forced_radius_if_critical_equation': str(forced) if forced else None})
    classes = []
    for typ, rows in sorted(groups.items()):
        profile = {k: v for k, v in rows[0].items() if k != 'original_bad_mask'}
        require(all({k: v for k, v in row.items() if k != 'original_bad_mask'} == profile for row in rows),
                'whole original class uniformity checked individually')
        classes.append({'original_type': list(typ), 'all_original_masks': [row['original_bad_mask'] for row in rows],
                        'original_count': len(rows), **profile})
    require(sorted(len(rows) for rows in groups.values()) == [9, 36, 36], 'complete81 original column classification')
    pure_classes = [row for row in classes if row['original_count'] == 36]
    require([F(v) for v in pure_classes[0]['exact_affine_remainder_mod_F']] ==
            [-F(v) for v in pure_classes[1]['exact_affine_remainder_mod_F']],
            'opposite pure-class remainders explain unresolved weighted direction')
    return {'actual_agent': 'six-downset-3', 'role': 'researcher',
            'status': 'PRIVATE original-column critical equality finite certificate; ordinary bridge separate',
            'original_bad_columns_checked': 81, 'original_comparison_entries_checked': 6561,
            'all72_pure_critical_equalities_excluded': True,
            'all9_triple_equalities_identically_satisfied': True,
            'primitive_F_polynomial_low_to_high': primitive, 'full_original_column_classification': classes,
            'stronger_original_sharp_distance_theorem': 'd>rho for ALL tau in[0,1/256]; proof separate',
            'uniform_separation_above_rho': 'existential only, ordinary compactness proof separate',
            'exact_best_distance_or_original_realization_or_general_H_I_claimed': False,
            'formal_proof': False, 'independent_review': False,
            'source_commit': None, 'graph_ref': None, 'new_graph_packet': None}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
