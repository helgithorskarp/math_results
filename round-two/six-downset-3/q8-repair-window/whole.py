"""Rational whole-matrix decoder and original support/rank controls."""
from fractions import Fraction as F
from itertools import combinations
import json
import inputs
from literal import require, core_data, action, quadratic
from exact import digest, lift, schur_psd
from claims import POLY


def matrices(kappa, t):
    require(isinstance(kappa, (int, F)) and isinstance(t, (int, F)),
            'this finite evaluator takes exact rational parameters')
    X, N, s, C0, delta, R, U0 = core_data(8, 3)
    C = [[C0[i][j]+kappa*delta[i][j]+t*R[i][j] for j in range(N-1)]
         for i in range(N-1)]
    L = lift(C)
    M = [[(L[i][j]-s*int(i == j))/F(N-s) for j in range(N)] for i in range(N)]
    return X, C, L, M


def original(X, L, M, kappa=F(0)):
    N, s = 89, 28
    require(len(X) == len(L) == len(M) == N and X[0] == 0,
            'whole domain includes actual empty set')
    require(all(len(row) == N for row in L+M), 'whole matrix dimensions')
    require(all(type(x) is int or isinstance(x, F) for row in L+M for x in row),
            'exact original entries')
    require(all(L[i][j] == L[j][i] and M[i][j] == M[j][i]
                for i in range(N) for j in range(N)), 'whole original symmetry')
    require(all(sum(row) == N for row in L) and all(sum(row) == 1 for row in M),
            'every original row equation')
    require(L[0][0] == 76+F(1065, 29)*kappa
            and M[0][0] == (48+F(1065, 29)*kappa)/61, 'actual empty-set diagonal')
    require(all(M[i][j] == 0 for i, a in enumerate(X) for j, b in enumerate(X)
                if a & b), 'all original intersecting support zeroes')
    require(all(M[i][j] == (L[i][j]-s*int(i == j))/F(N-s)
                for i in range(N) for j in range(N)), 'whole H normalization')
    star = [F(bool(a&1))-F(s, N) for a in X]
    require(not any(action(L, star)), 'whole centered maximum-star kernel')
    require(sum(star) == 0, 'whole lower kernel perpendicular to ones')
    return True


def controls():
    records = []
    for kappa, t in ((F(0), F(3, 8)), (F(0), F(1, 2)),
                     (F(0), F(6)), (F(1, 4096), F(1, 2))):
        X, C, L, M = matrices(kappa, t)
        original(X, L, M, kappa)
        U = [[F(89*int(i == j)-1)-C[i][j] for j in range(88)] for i in range(88)]
        cap = [[F(89*int(i == j))-L[i][j] for j in range(89)] for i in range(89)]
        lower_rank, upper_rank = schur_psd(C), schur_psd(U)
        require(schur_psd(L) == lower_rank+1 and schur_psd(cap) == upper_rank,
                'whole PSD congruence and both original ranks')
        require((lower_rank+1, upper_rank) == ((87, 88) if kappa == 0 else (88, 88)),
                'interior and prior positive-kappa rank controls')
        require(sum(sum(row) for row in C) == 75+F(1065, 29)*kappa,
                'closed empty formula independent of the repair parameter')
        records.append({'kappa': str(kappa), 't': str(t), 'N': 89,
                        'L_rank': lower_rank+1, 'cap_rank': upper_rank,
                        'entries': 89*89, 'whole_M_digest': digest([[str(x) for x in row] for row in M]),
                        'M_empty_empty': str(M[0][0])})
    # Every three-deletion subset of the eight outside points is transported
    # by a complete permutation, rather than by testing a sample of its entries.
    X = core_data(8, 3)[0]
    all_points = tuple(range(3, 11))
    for chosen in combinations(all_points, 3):
        target = chosen+tuple(i for i in all_points if i not in chosen)
        move = {i: i for i in range(3)} | dict(zip(all_points, target))
        moved = sorted(sum(1 << move[i] for i in range(11) if mask & (1 << i)) for mask in X)
        expected = [mask for mask in range(1 << 11)
                    if (mask.bit_count() <= 2 or mask.bit_count() == 3 and (mask&7).bit_count() >= 2)
                    and mask not in {6+(1 << i) for i in chosen}]
        require(moved == expected, 'every canonical three-deletion outside transport')
    rec = {'agent': 'six-downset-3', 'role': 'researcher', 'rational_whole_controls': records,
           'outside_three_deletion_transports': 56, 'all_original_entry_count': 4*89*89,
           'exact_evaluator_scope': 'rational inputs; real algebraic endpoints decoded in the ordinary proof'}
    rec['record_sha256'] = digest(rec)
    return rec


if __name__ == '__main__':
    print(json.dumps(controls(), sort_keys=True, indent=2))
