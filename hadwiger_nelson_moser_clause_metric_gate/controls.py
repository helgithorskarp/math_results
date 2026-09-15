"""Fault controls for the finite relation/metric certificate."""
import copy
import itertools
import json
from pathlib import Path
import verify


def main():
    cert = json.loads(Path(__file__).with_name('certificate.json').read_text())
    verify.verify(cert)
    faults = []
    for key, value in [('raw_points', 440), ('five_colour_terminal_word', [0]*7),
                       ('declared_gram_determinant', [0, 1]),
                       ('physical_realization_exists', True)]:
        bad = copy.deepcopy(cert)
        bad[key] = value
        faults.append(bad)
    bad = copy.deepcopy(cert)
    bad['metric_witness'] = bad['metric_witness'][:-1]
    faults.append(bad)
    bad = copy.deepcopy(cert)
    bad['clauses'][0] = [[0, 0], [2, 3]]
    faults.append(bad)
    for bad in faults:
        try:
            verify.verify(bad)
        except ValueError:
            continue
        raise ValueError('damaged certificate accepted')
    # A realizable unit equilateral triangle has the expected rank-two Gram
    # matrix. It must not trigger the four-point rank-three contradiction.
    from fractions import Fraction as F
    if verify.determinant([[1, F(1, 2)], [F(1, 2), 1]]) != F(3, 4):
        raise ValueError('triangle Gram control')
    if verify.determinant([[1, 0, 1], [0, 1, 1], [1, 1, 2]]) != 0:
        raise ValueError('planar three-vector Gram control')
    print(json.dumps({'status': 'PASS', 'rejected_faults': len(faults),
                      'realizable_Gram_controls': 2}, sort_keys=True))


if __name__ == '__main__':
    main()
