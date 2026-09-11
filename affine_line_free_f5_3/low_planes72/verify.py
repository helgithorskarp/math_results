"""Replay exhaustive planar counts and check all certificates with integers."""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import time
from model import CASES, PROFILES, incidence_system, projection_system


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=Path('build/low_planes72'))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent
    start = time.monotonic()
    executable = (args.out/'enumerate_spectra').resolve()
    subprocess.run(['g++', '-O3', '-std=c++20', '-Wall', '-Wextra', '-Wconversion',
                    str(source/'enumerate_spectra.cpp'), '-o', str(executable)], check=True)
    raw = subprocess.check_output([str(executable)])
    assert raw == (source/'spectra_expected.txt').read_bytes()
    spectra = [list(map(int, line.split())) for line in raw.decode().splitlines()]
    assert len(spectra) == 70
    for m, *tail in spectra:
        counts, multiplicity = tail[:5], tail[5]
        assert sum(counts) == 30 and multiplicity > 0
        assert sum(k*counts[k] for k in range(5)) == 6*m
        assert sum(k*(k-1)//2*counts[k] for k in range(5)) == m*(m-1)//2

    columns, names, matrix, rhs = incidence_system(spectra)
    assert len(columns) == 463 and len(matrix) == 61
    incidence_results = []
    certs = json.loads((source/'incidence_certificates.json').read_text())
    assert [c['cutoff'] for c in certs] == [9, 10, 11]
    for cert in certs:
        d, z = cert['denominator'], cert['multipliers']
        assert d > 0 and len(z) == len(matrix)
        assert all(type(v) is int for v in z)
        objective = [int(t == 's' and x[0] <= cert['cutoff']) for t, x in columns]
        slacks = [d*objective[j]-sum(z[i]*matrix[i][j] for i in range(len(z)))
                  for j in range(len(columns))]
        bound = sum(z[i]*rhs[i] for i in range(len(z)))
        assert min(slacks) == cert['minimum_slack'] >= 0
        assert bound == cert['bound_numerator']
        incidence_results.append({'cutoff': cert['cutoff'],
            'rational_lower_bound': str(Fraction(bound, d)),
            'integer_lower_bound': (bound+d-1)//d})
    assert [c['integer_lower_bound'] for c in incidence_results] == [5, 7, 9]
    # An exact integral control shows that the aggregate system alone is
    # insufficient for the 72-point decision. It is not a point-set witness.
    control = json.loads((source/'incidence_integer_control.json').read_text())
    vector = [0]*len(columns)
    seen = set()
    for j, value in control['nonzero_entries']:
        assert type(j) is int and 0 <= j < len(columns) and j not in seen
        assert type(value) is int and value > 0
        seen.add(j)
        vector[j] = value
    assert [sum(a*v for a, v in zip(row, vector)) for row in matrix] == rhs

    projections = json.loads((source/'projection_certificates.json').read_text())
    expected = {(0, 0)+b for b in product(range(5), repeat=3)}
    assert len(projections) == 125
    assert {tuple(c['offsets']) for c in projections} == expected
    maximum = Fraction(0)
    for cert in projections:
        lines, bounds = projection_system(cert['offsets'])
        d, z = cert['denominator'], cert['multipliers']
        assert d > 0 and len(z) == 55 and all(type(v) is int and v >= 0 for v in z)
        for i in range(25):
            assert sum(z[j]*lines[j][i] for j in range(30))+z[30+i] >= d
        value = sum(z[j]*bounds[j] for j in range(30))+4*sum(z[30:])
        assert value == cert['upper_numerator'] < 72*d
        maximum = max(maximum, Fraction(value, d))
    assert maximum == Fraction(1499, 21)

    # Validate the independent affine incidence counts used to interpret rows.
    points = list(product(range(5), repeat=3))
    directions = [v for v in points if any(v) and next(x for x in v if x) == 1]
    planes = [frozenset(i for i, p in enumerate(points)
                        if sum(x*y for x, y in zip(p, normal)) % 5 == b)
              for normal in directions for b in range(5)]
    affine_lines = {frozenset(points.index(tuple((x+t*y) % 5 for x, y in zip(p, v)))
                             for t in range(5)) for p in points for v in directions}
    assert len(planes) == 155 and len(affine_lines) == 775
    intersections = {h & g for h, g in combinations(planes, 2) if h & g}
    assert intersections == affine_lines
    assert set(Counter(i for h in planes for i in h).values()) == {31}
    assert set(Counter(pair for h in planes for pair in combinations(sorted(h), 2)).values()) == {6}
    for line in affine_lines:
        pencil = [h for h in planes if line <= h]
        assert len(pencil) == 6
        counts = Counter(i for h in pencil for i in h)
        assert all(counts[i] == (6 if i in line else 1) for i in range(125))
    # Affine scalings normalize the unique 15-plane of profile B to label 1.
    assert all(any((a*b) % 5 == 1 for a in range(1, 5)) for b in range(1, 5))
    assert len(CASES) == 4 and all(sum(p) == 72 for p in PROFILES)
    result = {'status': 'GLOBAL_72_LOW_PLANE_REDUCTION_VERIFIED',
        'spectra': 70, 'incidence_variables': 463, 'incidence_equations': 61,
        'incidence_bounds': incidence_results, 'projection_certificates': 125,
        'projection_upper_bound': str(maximum), 'coordinate_cases': CASES,
        'numeric_bounds': [70, 72], '72_point_decision': 'OPEN',
        'aggregate_integer_feasibility_control_verified': True,
        'optimizer_required_for_replay': False}
    (args.out/'verified.json').write_text(json.dumps(result, indent=2)+'\n')
    (args.out/'metadata.json').write_text(json.dumps({'seconds': time.monotonic()-start}, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
