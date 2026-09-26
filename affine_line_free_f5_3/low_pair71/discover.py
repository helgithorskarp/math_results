"""Optional floating-point discovery; exact certificates are checked before output.

This program is not part of the theorem's trust boundary. The verifier uses
only Python integers and the separately rerun complete planar census.
"""
from fractions import Fraction
import argparse
import json
from pathlib import Path

from scipy.optimize import linprog

from model import FORMS, case_rhs, incidence_system

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    spectra = [tuple(map(int, line.split()[:6]))
               for line in (HERE / 'spectra_expected.txt').read_text().splitlines()]
    columns, names, matrix, base, objective = incidence_system(spectra)
    cases = []
    for form in FORMS:
        for bit in (0, 1):
            rhs = case_rhs(base, form, bit)
            result = linprog(objective, A_eq=matrix, b_eq=rhs,
                             bounds=(0, None), method='highs')
            if not result.success:
                raise RuntimeError((form, bit, result.message))
            denominator = 100_000_000
            z = [int(round(denominator*v)) for v in result.eqlin.marginals]
            # Rounding may violate columns. Each block has a constant-one row,
            # so decreasing that row's multiplier repairs every column exactly.
            for kind, row_name in (('s', 'planes'), ('p', 'parallel_classes'),
                                   ('l', 'lines')):
                excess = max([0] + [sum(z[i]*matrix[i][j] for i in range(len(z)))
                                     - denominator*objective[j]
                                     for j, column in enumerate(columns)
                                     if column[0] == kind])
                z[names.index(row_name)] -= excess
            lhs = [sum(z[i]*matrix[i][j] for i in range(len(z)))
                   for j in range(len(columns))]
            if any(a > denominator*c for a, c in zip(lhs, objective)):
                raise RuntimeError('internal integer inequality failure')
            numerator = sum(v*w for v, w in zip(z, rhs))
            lower = Fraction(numerator, denominator)
            bound = -(-numerator // denominator)
            if bound < 2:
                raise RuntimeError('certificate does not prove two low planes')
            cases.append(dict(form=form, mu_in_set=bit, denominator=denominator,
                              multipliers=z, numerator=numerator, lower_bound=bound))
            print(form, bit, str(lower), '=>', bound, flush=True)
    output = dict(schema=1, row_names=names, cases=cases)
    args.out.write_text(json.dumps(output, sort_keys=True, indent=2) + '\n')


if __name__ == '__main__':
    main()
