"""Targeted new-line semantic defects and small exact hand controls."""
import argparse
import copy
from fractions import Fraction as F
import json
from pathlib import Path
from original import audit, build, canonical, member_type, require
from sparse import point_at
from check_original import audit_new, endpoint_form
from read_lower import check_proof
from read_tree import check_tree
from face import controls, slack_identity
from positive_elimination import divide_content, eliminate


def rejects(name, action):
    try:
        action()
    except ValueError as error:
        return {'name': name, 'rejected': True, 'reason': str(error)}
    raise ValueError('semantic defect accepted: '+name)


def reconstruct(C):
    sums = [sum(row) for row in C]
    L = [[1+sum(sums)]+[1-x for x in sums]]+[
        [1-sums[i]]+[1+x for x in row] for i, row in enumerate(C)]
    return [row[1:] for row in C[1:]], L


def run():
    data = json.loads(Path(__file__).with_name('COEFFICIENTS.json').read_bytes())
    base = build(data); audit(base); proper = base['members'][1:]
    _, T, L = point_at(base, F(0), return_matrices=True); audit_new(base, F(0), T, L)
    C = [[L[i+1][j+1]-1 for j in range(254)] for i in range(254)]
    records = []; a = proper.index((0,)); abc = proper.index((0, 1, 2))
    xs = [i for i, v in enumerate(proper) if member_type(v) == (0, 1, 0)]

    def remove_trade(v, amount):
        bad = copy.deepcopy(C)
        for x in xs:
            bad[v][x] -= amount/8; bad[x][v] -= amount/8
            bad[a][x] += amount/8; bad[x][a] += amount/8
        t, l = reconstruct(bad); audit_new(base, F(0), t, l)

    records.append(rejects('missing_new_aY_trade', lambda: remove_trade(
        proper.index((0, 11)), F(-19013, 32768))))
    records.append(rejects('missing_abc_trade', lambda: remove_trade(abc, F(14121, 32768))))

    def edge_change(type_pair, amount):
        bad = copy.deepcopy(C)
        matches = [(i, j) for i, v in enumerate(proper) for j, w in enumerate(proper)
                   if i < j and set(v).isdisjoint(w) and
                   (member_type(v), member_type(w)) == type_pair]
        require(bool(matches), 'literal defect edge exists')
        i, j = matches[0]; bad[i][j] += amount; bad[j][i] += amount
        t, l = reconstruct(bad); audit_new(base, F(0), t, l)

    records.append(rejects('wrong_YY_bad_row_degree', lambda: edge_change(
        ((0, 0, 2), (0, 0, 2)), F(1, 100))))
    records.append(rejects('extra_unpaid_positive_NN_mass', lambda: edge_change(
        ((0, 2, 0), (0, 2, 0)), F(1, 100))))

    def damaged(name, mutate):
        t = copy.deepcopy(T); l = copy.deepcopy(L); mutate(t, l)
        records.append(rejects(name, lambda: audit_new(base, F(0), t, l)))

    damaged('omitted_original_empty_vertex', lambda t, l: l.pop(0))
    damaged('incorrect_original_empty_loop_factor', lambda t, l: l[0].__setitem__(0, l[0][0]+F(1)))
    damaged('missing_full_residual_coordinate', lambda t, l: t.pop())
    damaged('wrong_residual_binding', lambda t, l: t[0].__setitem__(0, t[0][0]+F(1)))
    damaged('wrong_maximum_star_anchor', lambda t, l: l[1].__setitem__(2, l[1][2]+F(1)))
    damaged('float_original_entry', lambda t, l: l[0].__setitem__(0, 55.0))
    damaged('wrong_original_C_to_M_units', lambda t, l: l[0].__setitem__(0, l[0][0]*200))
    bad_data = copy.deepcopy(data); bad_data['free_pair_values'].pop()
    records.append(rejects('missing_defining_pair_type', lambda: build(bad_data)))
    records.append(rejects('wrong_parameter_units', lambda: point_at(base, F(1, 64))))
    records.append(rejects('float_parameter', lambda: point_at(base, 0.0)))
    records.append(rejects('negative_content_scale', lambda: divide_content([[2]], -2)))
    records.append(rejects('inexact_content_division', lambda: divide_content([[3]], 2)))
    records.append(rejects('necessary_22_types_not_whole_253_proof', lambda: check_proof(
        {'status': 'positive_definite', 'dimension': 22})))
    records.append(rejects('incomplete_original_pivot_proof', lambda: check_proof(
        {'status': 'positive_definite', 'dimension': 253, 'original_leading_minors': ['1']})))
    _, _, last = point_at(base, F(1, 128), return_matrices=True)
    matrices = [L, last]; hub = base['members'].index((3,))
    edges = [{'child': v, 'parent': 0 if L[0][v] > 0 else hub,
              'endpoint_weights': [str(m[0 if L[0][v] > 0 else hub][v]/200) for m in matrices]}
             for v in range(1, 255)]
    check_tree(base, matrices, edges)
    records.append(rejects('missing_tree_vertex', lambda: check_tree(base, matrices, edges[:-1])))
    bad = copy.deepcopy(edges); bad[0]['endpoint_weights'][0] = '1'
    records.append(rejects('tree_weight_not_bound_to_original_M', lambda: check_tree(base, matrices, bad)))
    bad2 = copy.deepcopy(edges); bad2[0]['parent'] = bad2[0]['child']
    records.append(rejects('tree_cycle', lambda: check_tree(base, matrices, bad2)))
    records.append(rejects('float_dual_change', lambda: slack_identity(
        [F(-1), F(1)], F(0), {(0, 1): .5})))
    positives = []
    for matrix, minors in [([[2, 1], [1, 2]], [2, 3]),
                           ([[4, 2], [2, 4]], [4, 12]),
                           ([[4, 2, 0], [2, 5, 1], [0, 1, 6]], [4, 16, 92])]:
        proof = eliminate(matrix)
        require(proof['status'] == 'positive_definite' and
                list(map(int, proof['original_leading_minors'])) == minors,
                'hand-computed small determinant controls')
        positives.append(minors)
    require(len(records) == 22, 'new-line semantic rejection census')
    return {'agent': 'six-downset-2', 'role': 'researcher', 'semantic_rejections': records,
            'small_hand_computed_positive_minors': positives, 'mass_identity_controls': controls(),
            'normal_O_agreement_is_same_author_not_independent_review': True}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--record', required=True)
    result = run(); Path(p.parse_args().record).write_bytes(canonical(result)+b'\n')
    print(json.dumps(result))
