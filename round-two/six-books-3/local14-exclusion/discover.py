"""Optional floating LP discovery; all output cuts are verified with integers.

HiGHS 1.15.1 / NumPy 2.2.6. These packages are unnecessary for the proof.
Actual author six-books-3, researcher. One solver thread; no MILP verdict.
"""
import argparse
from fractions import Fraction
import json
from math import gcd, lcm
from pathlib import Path

import highspy
import numpy as np
import generate


def integer_vector(values):
    rational = [Fraction(float(x)).limit_denominator(10000) for x in values]
    scale = lcm(*(x.denominator for x in rational))
    integer = [int(scale * x) for x in rational]
    common = gcd(*integer)
    generate.need(common > 0, 'Zero suggested certificate')
    return [x // common for x in integer]


def discover():
    generate.need(highspy.Highs().version() == '1.15.1', 'HiGHS version differs')
    generate.need(np.__version__ == '2.2.6', 'NumPy version differs')
    output = {'schema': 1, 'agent': 'six-books-3', 'role': 'researcher',
              'source_core_claim': 'bafkreihrw6fz7nozp5m5g2s5hnmeqkyte6taxfejvjk6gowwkepulvc4z4',
              'cuts': []}
    for mask in generate.CORE_MASKS:
        graph = generate.local_graph(mask)
        upper = generate.capacities(graph)
        rows = list(generate.row_words(graph, upper))
        features = [[z >> i & 1 for i in range(10)]
                    + [int(bool(z >> i & 1 and z >> j & 1)) for i, j in generate.PAIRS]
                    + [1] for z in rows]
        rhs = [upper[i][i] for i in range(10)] + [upper[i][j] for i, j in generate.PAIRS] + [11]
        matrix = np.array(features, dtype=float).T
        starts, indices, values = [0], [], []
        for row in matrix:
            nonzero = np.nonzero(row)[0]
            indices.extend(nonzero)
            values.extend(row[nonzero])
            starts.append(len(indices))
        solver = highspy.Highs()
        for key, value in [('output_flag', False), ('threads', 1), ('parallel', 'off'),
                           ('presolve', 'off'), ('solver', 'simplex'), ('time_limit', 10.0)]:
            generate.need(solver.setOptionValue(key, value) == highspy.HighsStatus.kOk,
                          'Solver option was rejected')
        lower = rhs.copy()
        lower[10:55] = [-highspy.kHighsInf] * 45
        solver.addVars(len(rows), np.zeros(len(rows)), np.full(len(rows), highspy.kHighsInf))
        solver.addRows(56, np.array(lower, dtype=float), np.array(rhs, dtype=float), len(indices),
                       np.array(starts, dtype=np.int32), np.array(indices, dtype=np.int32),
                       np.array(values, dtype=float))
        solver.run()
        status = solver.getModelStatus()
        if status == highspy.HighsModelStatus.kInfeasible:
            _, exists, ray = solver.getDualRay()
            generate.need(exists, 'No suggested infeasibility ray')
            vector = integer_vector([-x for x in ray])
        elif status == highspy.HighsModelStatus.kOptimal:
            support = set()
            while True:
                costs = np.array([0 if z in support else -1 for z in rows], dtype=float)
                solver.changeColsCost(len(rows), np.arange(len(rows), dtype=np.int32), costs)
                solver.run()
                generate.need(solver.getModelStatus() == highspy.HighsModelStatus.kOptimal,
                              'Incomplete support discovery')
                solution = solver.getSolution()
                if solver.getObjectiveValue() > -1e-7:
                    vector = integer_vector([-x for x in solution.row_dual])
                    break
                new = {z for z, value in zip(rows, solution.col_value) if value > 1e-7}
                generate.need(bool(new - support), 'Support discovery made no progress')
                support.update(new)
        else:
            raise RuntimeError('No decisive LP result: ' + solver.modelStatusToString(status))
        cut = {'F_mask': mask, 'alpha': vector[:10],
               'beta': [[i, j, q] for (i, j), q in zip(generate.PAIRS, vector[10:55]) if q],
               'gamma': vector[55], 'rhs': sum(a * b for a, b in zip(vector, rhs))}
        generate.check_cut(cut, graph, upper, rows)
        output['cuts'].append(cut)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='Separate candidate certificate path')
    args = parser.parse_args()
    generate.need(args.output.resolve() != (generate.HERE / 'cuts.json').resolve(),
                  'Discovery must not overwrite the published certificate')
    output = discover()
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'cuts_discovered': len(output['cuts']), 'integer_verified': True,
                      'solver_threads': 1}, sort_keys=True))


if __name__ == '__main__':
    main()
