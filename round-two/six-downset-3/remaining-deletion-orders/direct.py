"""independent original-domain check at the new dual exception.

Every representative is compared with every original member. Weighted
orbit invariance supplies full Gram sums; 10-million-pair enumeration
is NOT claimed. No binomial disjoint formula is used by this builder.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import orbits
from literal import member, table, typ, require
from dual import quadratic, congruence
from exact import digest
import three_vectors


def run():
    q, k = 74, 15
    X = sorted(sum(1 << j for j in points) for size in (1, 2, 3)
               for points in combinations(range(q+3), size)
               if member(q, k, sum(1 << j for j in points)))
    groups = {}
    for A in X:
        z = sum(bool(A & (1 << j)) for j in range(3, k+3))
        w = sum(bool(A & (1 << j)) for j in range(k+3, q+3))
        groups.setdefault((A & 7, z, w), []).append(A)
    keys = sorted(groups)
    sizes = [len(groups[key]) for key in keys]
    require(len(X) == 3211 and len(keys) == 23, 'independently generated original dual domain')
    tab = table(q)
    C, D, R = [], [], []
    original_positions = 0
    for i, key in enumerate(keys):
        A = groups[key][0]
        cr, dr, rr = [], [], []
        for other in keys:
            c, d, r = F(0), F(0), F(0)
            for B in groups[other]:
                if A == B:
                    a, b = F(3*q+3), F(0)
                elif A & B:
                    a, b = F(-1), F(0)
                else:
                    a, b = tab[tuple(sorted((typ(A), typ(B))))]
                    a -= 1
                repair = {(1, 2): 1, (1, 4): 1, (2, 5): -1, (3, 4): -1}.get(tuple(sorted((A, B))), 0)
                c += a; d += b; r += repair
                original_positions += 1
            cr.append(sizes[i]*c); dr.append(sizes[i]*d); rr.append(sizes[i]*r)
        C.append(cr); D.append(dr); R.append(rr)
    U = [[F(3212*sizes[i]*int(i == j)-sizes[i]*sizes[j])-C[i][j]
          for j in range(23)] for i in range(23)]
    counted = orbits.forms(q, k)
    require(keys == counted['keys'] and sizes == counted['sizes'] and
            [C, D, R, U] == [counted['C0'], counted['Delta'], counted['R'], counted['U0']],
            'ALL independently original weighted coefficient Gram entries')
    w, z, one, y, v = [], [], [], [], []
    for key in keys:
        candidate_values = set()
        for A in groups[key]:
            yy = int(A & 7 == 1 and (A >> 3).bit_count() == 1)
            vv = int(bool(A & 6) and A not in (3, 5))
            zz = 1-int(bool(A & 2))-int(bool(A & 4))+int((A & 7).bit_count() >= 2)
            candidate_values.add((255-3*yy+vv, zz, 1, yy, vv))
        require(len(candidate_values) == 1, 'EVERY original amplitude independently constant on orbit')
        ww, zz, oo, yy, vv = candidate_values.pop()
        for vector, value in zip((w, z, one, y, v), (ww, zz, oo, yy, vv)):
            vector.append(F(value))
    pairings = [quadratic(a, w) for a in (U, D, R)]
    require(pairings == [F(-1118484, 37), F(40973507610, 227), F(0)],
            'all three original compact exceptional dual pairings')
    require(all(sum(C[i][j]*z[j] for j in range(23)) == 0
                and sum(R[i][j]*z[j] for j in range(23)) == 0 for i in range(23)),
            'every original lower kernel and repair row')
    alpha = F(q*(q+1), 2)+F(3*(q+1), 3*q+5)
    require(quadratic(D, z) == alpha > 0, 'original lower kernel forces nonnegative kappa')
    expected = three_vectors.scalars(q, k)
    require(congruence(U, [one, y, v]) == [[expected['e'], expected['A'], expected['C']],
                                         [expected['A'], expected['T'], expected['B']],
                                         [expected['C'], expected['B'], expected['V']]],
            'new 3-by-3 formula from independent original positions')
    # Concrete bad candidates must fail the original necessary-dual checker.
    valid = lambda a: quadratic(U, a) < 0 and quadratic(D, a) >= 0 and quadratic(R, a) == 0
    require(valid(w), 'good original dual candidate accepted')
    wrong_repair = w[:]
    wrong_repair[keys.index((1, 0, 0))] += 1
    require(not valid(wrong_repair), 'broken R annihilation rejected against original repair')
    require(not valid([F(0)]*23), 'zero cap pairing rejected')
    original_data = dict(counted, C0=C, Delta=D, R=R, U0=U)
    three_vectors.check(original_data)
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'status': 'exact original dual calibration, ordinary symmetry bridge unformalized',
              'q': q, 'k': k, 'N': 3212, 'original_members': len(X),
              'original_representative_positions': original_positions,
              'whole_pair_enumeration_claimed': False, 'every_four_times_529_Gram_entry_matches': True,
              'every_original_vector_amplitude_matches': True, 'original_dual': [str(x) for x in w],
              'original_U0': str(pairings[0]), 'original_Delta': str(pairings[1]), 'original_R': str(pairings[2]),
              'original_lower_orientation': str(alpha), 'semantic_bad_duals_rejected': 2,
              'original_forms_digest': digest(orbits.encoded(original_data))}
    result['record_sha256'] = digest(result)
    return result


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('DIRECT.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True, indent=2))
