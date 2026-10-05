"""Literal rational bad-block row certificate for the new critical obstruction.

The sharp-dual/Schur equality and compactness bridges are ordinary proof
premises in CRITICAL-EXTENSION.md. Only whole-pinned defining DATA are
read, with explicitly credited same-author original coefficient order.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check():
    root = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location('critical_original_decoder', root/'census.py')
    decoder = importlib.util.module_from_spec(spec); spec.loader.exec_module(decoder)
    S, B, label, A, nums, P, N, D = decoder.original()
    raw = (root.parent/'q18-schur-weight-radius/COMPARISON.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            '6770d9db69983e4cbd75480a9f784dd4c9c9d254cf7f455bbd0d4a62633b2ca2',
            'attributed whole original comparison DATA')
    comparison = json.loads(raw); X = sorted(label)
    keys = sorted({tuple(sorted((label[u], label[v])))
                   for i, u in enumerate(X) for v in X[i+1:]
                   if u != 1 and v != 1 and not u & v})
    require(len(keys) == 143 and comparison['comparison_free_denominator'] == 16384
            and len(comparison['comparison_free_numerators']) == 143,
            'complete rational original comparison coefficient domain')
    table = {key: F(value, 16384) for key, value in
             zip(keys, comparison['comparison_free_numerators'])}
    old = [[F(57) if u == v else F(-1) if u & v else
            table[tuple(sorted((label[u], label[v])))] for v in B] for u in B]
    require(sum(map(sum, old)) == F(4998177, 1024), 'whole6561 original BB cap baseline')
    disjoint = [(i, j) for i, u in enumerate(B) for j, v in enumerate(B)
                if i < j and not u & v]
    require(len(disjoint) == 2628 and all(old[i][j] == old[j][i] for i in range(81) for j in range(81)),
            'all2628 unordered bad edges and6561 original symmetric entries')
    abc = S.index(7); J = [i for i in P if i != abc]
    bc = [j for j, bad in enumerate(B) if label[bad] == (6, 0, 1)]
    require(len(bc) == 9 and all(A[i][j] == -D for i in N+[abc] for j in bc) and
            all(sum(A[i][j] for i in J) == 39*D for j in bc),
            'whole9 actual bcW fixed-complement and J column equations')
    V = F(sum(nums[i] for i in P), D); alpha = F(nums[abc], D)
    rows = []
    for j in bc:
        row_sum = sum(old[j]); forced = (V-alpha-19*row_sum)/269280
        require(row_sum == F(186731, 4096) and forced == F(41666495813, 6571299962880),
                'EACH9 exact original comparison row and forced critical radius')
        require(forced > F(1, 160) > F(1, 362),
                'exact rational incompatible critical radius cage')
        rows.append({'original_bad_mask': B[j], 'old_BB_row_sum': str(row_sum),
                     'forced_radius_if_sharp_critical_completion': str(forced)})
    # For q constant on J,N and the actual bcW column constraints,
    # A_col dot q = 39*(b/19)-a+T = 58*b/19, for ALL real a,b.
    require(F(39, 19)+1 == F(58, 19), 'symbolic whole bcW critical inner-product coefficient')
    return {'actual_agent': 'six-downset-3', 'role': 'researcher',
            'status': 'PRIVATE exact critical-row finite certificate; ordinary equality/compactness proof separate',
            'all_original_BB_positions': 6561, 'all_unordered_disjoint_BB_edges': 2628,
            'all9_actual_bcW_rows': rows, 'exact_BB_cap': '4998177/1024',
            'critical_scalar_equation': '(V-alpha-269280*r_*)/19=C_old_BB_row_sum',
            'proven_root_upper_from_separate_subsets_theorem': '1/362',
            'strict_original_sharp_distance_and_uniform_positive_gap_claimed_by_code_alone': False,
            'original_global_matrix_realization_or_exact_best_distance_claimed': False,
            'ancestor_program_PSD_factor_or_peer_input_imported': False,
            'source_commit': None, 'graph_ref': None, 'independent_review': False}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
