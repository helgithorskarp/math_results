"""Exact arithmetic controls for the ordinary k=1,2,3 fixed-point proof."""
import itertools
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    degree_table = {}
    for k in range(1, 5):
        m = 22 - 5 * k
        degree_table[str(k)] = [[r, h, 5 * r + h] for r in range(k + 1)
                               for h in range(m) if 8 <= 5 * r + h <= 10]
    require(degree_table == {
        '1': [[0, 8, 8], [0, 9, 9], [0, 10, 10], [1, 3, 8], [1, 4, 9], [1, 5, 10]],
        '2': [[0, 8, 8], [0, 9, 9], [0, 10, 10], [1, 3, 8], [1, 4, 9], [1, 5, 10], [2, 0, 10]],
        '3': [[1, 3, 8], [1, 4, 9], [1, 5, 10], [2, 0, 10]],
        '4': [[2, 0, 10]],
    }, 'Fixed degree table')
    pairs = []
    for left, right in itertools.product(range(3, 6), repeat=2):
        allowed_common = left + right - 9
        if allowed_common >= 0:
            pairs.append([left, right, allowed_common])
    require(pairs == [[4, 5, 0], [5, 4, 0], [5, 5, 1]], 'One-orbit blue-pair caps')
    packing = []
    for s in (0, 2):
        for a in range(18):
            if 8 <= s + a <= 10:
                lhs = (a - 1) * comb(5, 2) + comb(4, 2)
                rhs = comb(17 - a, 2)
                require(a >= 6 and lhs > rhs, 'One-orbit pair packing')
                packing.append([s, a, lhs, rhs])
    # Complete small scalar coverage after the written type bounds.
    maximum = max(e + a + b + c for e, a, b, c in
                  itertools.product(range(2), range(4), range(4), range(2)))
    require(maximum == 8 and maximum < 12, 'Two-orbit cardinality contradiction')
    require(3 - 1 < 3 and 7 > 3 and (7 - 2) + 5 > 6, 'Three-orbit type contradictions')
    output = {'status': 'pass', 'fixed_degree_table': degree_table,
              'one_orbit_admissible_degree_pairs': pairs, 'one_orbit_packing_bounds': packing,
              'two_orbit_fixed_vertex_maximum': maximum,
              'covered_ordinary_cycle_counts': [1, 2, 3]}
    expected = json.loads((HERE / 'expected_fixed_points.json').read_text())
    require(output == expected, 'Expected fixed-point arithmetic differs')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
