"""Entrywise comparison: subset inequalities, independent matrix DP, and flow.

The DP enumerates row-degree orbits while retaining exact labeled-matrix
multiplicities. It neither calls the inequality oracle nor uses network flow.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools as it
import json
from math import comb, factorial, prod
from pathlib import Path
from flow import obstruction, lift, need


def matrix_dp(columns):
    states = {(0,0,0,0): 1}
    for degree in columns:
        next_states = defaultdict(int)
        for rows, count in states.items():
            for chosen in it.combinations(range(4), degree):
                updated = tuple(sorted(rows[i] + (i in chosen) for i in range(4)))
                next_states[updated] += count
        states = next_states
    return dict(states)


def check_certificate(rows, columns, certificate):
    """Check the returned literal obstruction without calling the producer."""
    kind = certificate['kind']
    if kind == 'bound':
        side = certificate['side']
        need(side in ('row','column'), 'bound side')
        values, upper = (rows,len(columns)) if side == 'row' else (columns,len(rows))
        i = certificate['index']
        need(0 <= i < len(values), 'bound index')
        need(certificate['value'] == values[i] and certificate['upper'] == upper, 'bound values')
        need(values[i] < 0 or values[i] > upper, 'violated bound')
    elif kind == 'balance':
        need(certificate['row_total'] == sum(rows) and certificate['column_total'] == sum(columns), 'totals')
        need(sum(rows) != sum(columns), 'violated balance')
    elif kind == 'subset':
        S = certificate['rows']
        need(S and len(set(S)) == len(S) and all(0 <= i < len(rows) for i in S), 'subset')
        lhs = sum(rows[i] for i in S)
        rhs = sum(min(c,len(S)) for c in columns)
        need(certificate['lhs'] == lhs and certificate['rhs'] == rhs and lhs > rhs, 'violated subset')
    else:
        raise ValueError('unknown certificate kind')


def check_matrix(matrix, rows, columns):
    need(len(matrix) == len(rows) and all(len(row) == len(columns) for row in matrix), 'matrix shape')
    need(all(type(x) is int and x in (0,1) for row in matrix for x in row), 'binary matrix')
    need([sum(row) for row in matrix] == list(rows), 'rows')
    need([sum(row[j] for row in matrix) for j in range(len(columns))] == list(columns), 'columns')


def small_literal():
    reports = []
    for n in range(1,5):
        literal = defaultdict(Counter)
        for bits in range(1 << (4*n)):
            rows = [0]*4; columns = [0]*n
            for i in range(4):
                for j in range(n):
                    x = (bits >> (i*n+j)) & 1
                    rows[i] += x; columns[j] += x
            # Only canonical column vectors are compared with a single DP run.
            # Row labels are intentionally forgotten, not divided out.
            if columns == sorted(columns):
                literal[tuple(columns)][tuple(sorted(rows))] += 1
        for columns in it.combinations_with_replacement(range(5),n):
            need(dict(literal[columns]) == matrix_dp(columns), 'literal matrix census versus DP')
        reports.append({'columns': n, 'literal_matrices': 1 << (4*n),
                        'canonical_column_vectors': comb(n+4,4)})
    return reports


def audit(n):
    row_vectors = list(it.combinations_with_replacement(range(n+1),4))
    checked = balanced = feasible = permuted = 0
    labeled_census = 0
    digest = hashlib.sha256()
    for columns in it.combinations_with_replacement(range(5),n):
        dp = matrix_dp(columns)
        need(sum(dp.values()) == prod(comb(4,c) for c in columns), 'column product census')
        multiplicity = factorial(n)//prod(factorial(v) for v in Counter(columns).values())
        labeled_census += multiplicity * sum(dp.values())
        for rows in row_vectors:
            checked += 1
            certificate = obstruction(rows,columns)
            exists = rows in dp
            need((certificate is None) == exists, 'entrywise DP versus subset inequalities')
            if certificate is not None:
                check_certificate(rows,columns,certificate)
            if sum(rows) == sum(columns):
                balanced += 1
                matrix = lift(rows,columns)
                need((matrix is not None) == exists, 'entrywise DP versus integral flow')
                if matrix is not None:
                    check_matrix(matrix,rows,columns)
            if exists:
                feasible += 1
                digest.update((json.dumps([rows,columns,dp[rows]],separators=(',',':'))+'\n').encode())
                if feasible % 101 == 1:
                    # Non-sorted labels exercise labeled cuts and row/column lifting.
                    r = rows[1:]+rows[:1]; c = tuple(reversed(columns))
                    need(obstruction(r,c) is None, 'permuted inequality test')
                    check_matrix(lift(r,c),r,c)
                    permuted += 1
    need(labeled_census == 1 << (4*n), 'all labeled binary matrices counted')
    return {'columns':n, 'canonical_row_vectors':len(row_vectors),
            'canonical_column_vectors':comb(n+4,4), 'margin_pairs_checked':checked,
            'balanced_pairs_flow_checked':balanced, 'feasible_margin_pairs':feasible,
            'additional_permuted_flow_checks':permuted,
            'labeled_matrix_census':labeled_census, 'feasible_margin_count_stream_sha256':digest.hexdigest()}


def negative_controls():
    cases = [([-1,0,0,0],[0]*8), ([9,0,0,0],[0]*8),
             ([0]*4,[5]+[0]*7), ([1,0,0,0],[0]*8),
             ([4,4,0,0],[3,3,1,1]+[0]*4)]
    for rows,columns in cases:
        certificate = obstruction(rows,columns)
        check_certificate(rows,columns,certificate)
        need(lift(rows,columns) is None, 'negative flow case')
    for rows,columns in [([True,0,0,0],[0]*8), ([0.0,0,0,0],[0]*8)]:
        for function in (obstruction,lift):
            try:
                function(rows,columns)
            except ValueError:
                pass
            else:
                raise ValueError('noninteger accepted')
    rows,columns = cases[-1]
    need(all(r <= sum(min(c,1) for c in columns) for r in rows), 'singleton cuts pass example')
    certificate = obstruction(rows,columns)
    corrupt = dict(certificate); corrupt['rhs'] = corrupt['lhs']
    try:
        check_certificate(rows,columns,corrupt)
    except ValueError:
        pass
    else:
        raise ValueError('corrupted subset certificate accepted')
    return {'infeasible_examples_checked':len(cases), 'noninteger_rejections':4,
            'corrupted_certificate_rejections':1,
            'singleton_insufficiency_example':{'rows':rows,'columns':columns,'certificate':certificate}}


def main():
    p = argparse.ArgumentParser(); p.add_argument('--report',type=Path,required=True)
    a = p.parse_args()
    report = {'method':'independent matrix-orbit DP versus every canonical margin pair',
              'small_literal_censuses':small_literal(), 'negative_controls':negative_controls(),
              'block_censuses':[audit(n) for n in (8,9)],
              'scope':'binary degree blocks only; not a Ramsey graph census or SAT verdict'}
    with a.report.open('x') as f:
        json.dump(report,f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps(report,sort_keys=True),flush=True)


if __name__ == '__main__':
    main()
