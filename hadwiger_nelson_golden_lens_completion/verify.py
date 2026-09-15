#!/usr/bin/env python3
"""Independent checker in Q(sqrt(5), i*sqrt(10+2sqrt(5)))."""

from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
QZERO = (F(0), F(0))
QONE = (F(1), F(0))
H2 = (F(10), F(2))


def qadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def qneg(a):
    return (-a[0], -a[1])


def qsub(a, b):
    return qadd(a, qneg(b))


def qmul(a, b):
    return (a[0] * b[0] + 5 * a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def qinverse(a):
    denominator = a[0] * a[0] - 5 * a[1] * a[1]
    assert denominator
    return (a[0] / denominator, -a[1] / denominator)


def qscale(value, a):
    return (value * a[0], value * a[1])


def cadd(a, b):
    return (qadd(a[0], b[0]), qadd(a[1], b[1]))


def cneg(a):
    return (qneg(a[0]), qneg(a[1]))


def csub(a, b):
    return cadd(a, cneg(b))


def cmul(a, b):
    return (
        qsub(qmul(a[0], b[0]), qmul(H2, qmul(a[1], b[1]))),
        qadd(qmul(a[0], b[1]), qmul(a[1], b[0])),
    )


def cconjugate(a):
    return (a[0], qneg(a[1]))


def cnorm(a):
    result = cmul(a, cconjugate(a))
    assert result[1] == QZERO
    return result[0]


def cscale(value, a):
    return (qscale(value, a[0]), qscale(value, a[1]))


def cpow(a, exponent):
    result = (QONE, QZERO)
    while exponent:
        if exponent & 1:
            result = cmul(result, a)
        a = cmul(a, a)
        exponent //= 2
    return result


ZETA = ((F(-1, 4), F(1, 4)), (F(1, 4), F(0)))
POWERS = tuple(cpow(ZETA, exponent) for exponent in range(5))
PHI = ((F(1, 2), F(1, 2)), QZERO)
INVERSE_PHI = ((F(-1, 2), F(1, 2)), QZERO)
UNIT_NORM = (F(5, 2), F(-1, 2))
GOLDEN_NORM = (F(5, 2), F(1, 2))

SOURCE_ROWS = (
    (0, 0, 0, 0, 5), (1, 0, 0, 0, 4),
    (0, 0, 0, 1, 4), (1, 0, 0, 1, 3),
    (0, 1, 0, 0, 4), (0, 0, 1, 0, 4),
    (1, 0, 1, 0, 3), (0, 1, 0, 1, 3),
    (1, 1, 0, 0, 3), (0, 0, 1, 1, 3),
    (1, 1, 0, 1, 2), (1, 0, 1, 1, 2),
    (0, 1, 1, 0, 3), (1, 1, 1, 0, 2),
    (0, 1, 1, 1, 2), (1, 1, 1, 1, 1),
)


def linear_combination(row):
    result = (QZERO, QZERO)
    for coefficient, value in zip(row, POWERS):
        result = cadd(result, cscale(F(coefficient), value))
    return result


def source_points():
    return tuple(linear_combination(row) for row in SOURCE_ROWS)


def distance_edges(points, target):
    return tuple(
        (left, right)
        for left, right in combinations(range(len(points)), 2)
        if cnorm(csub(points[right], points[left])) == target
    )


def digest_rows(rows):
    digest = sha256()
    for row in rows:
        digest.update((" ".join(map(str, row)) + "\n").encode())
    return digest.hexdigest()


def reconstruct():
    source = source_points()
    unit = distance_edges(source, UNIT_NORM)
    golden = distance_edges(source, GOLDEN_NORM)
    assert len(unit) == len(golden) == 28
    multipliers = (
        ("plus", cmul(INVERSE_PHI, cneg(cpow(ZETA, 3)))),
        ("minus", cmul(INVERSE_PHI, cneg(cpow(ZETA, 2)))),
    )
    points = []
    index = {}
    addresses = defaultdict(list)

    def insert(point, address):
        if point not in index:
            index[point] = len(points)
            points.append(point)
        addresses[index[point]].append(address)
        return index[point]

    for i, point in enumerate(source):
        insert(point, f"source:{i}")
    prescribed = set(unit)
    for left, right in golden:
        difference = csub(source[right], source[left])
        for sign, multiplier in multipliers:
            point = cadd(source[left], cmul(multiplier, difference))
            lens = insert(point, f"lens:{left}:{right}:{sign}")
            assert cnorm(csub(point, source[left])) == UNIT_NORM
            assert cnorm(csub(point, source[right])) == UNIT_NORM
            prescribed.add(tuple(sorted((left, lens))))
            prescribed.add(tuple(sorted((right, lens))))
    edges = distance_edges(points, UNIT_NORM)
    return source, tuple(points), unit, golden, edges, tuple(sorted(prescribed)), tuple(
        tuple(addresses[i]) for i in range(len(points))
    )


def main():
    data = json.loads((HERE / "certificate.json").read_text())
    source, points, source_unit, source_golden, edges, prescribed, addresses = reconstruct()
    need = lambda condition, message: condition or (_ for _ in ()).throw(
        AssertionError(message))
    need(len(source) == 16, "source order")
    need(len(points) == data["distinct_points"] == 40, "physical point count")
    need(len(edges) == data["complete_unit_edges"] == 92, "complete edge count")
    need([list(edge) for edge in edges] == data["unit_edges"], "edge list")
    need([list(edge) for edge in source_unit] == data["source_unit_edges"],
         "source unit incidences")
    need([list(edge) for edge in source_golden] == data["source_golden_edges"],
         "source golden incidences")
    need([list(row) for row in addresses] == data["addresses"], "collision addresses")
    need(len(prescribed) == data["prescribed_distinct_edges"] == 76,
         "prescribed edge count")
    need(len(set(edges) - set(prescribed)) == data["incidental_unit_edges"] == 16,
         "incidental edge count")

    # Convert the producer's independent power-basis coordinates into this
    # nested-quadratic model and compare them point by point.
    converted = tuple(linear_combination(row)
                      for row in data["coordinates_power_basis"])
    need(converted == points, "coordinate list")
    basis_rows = tuple(tuple(row) for row in data["coordinates_power_basis"])
    need(digest_rows(basis_rows) == data["point_sha256"], "point digest")
    need(digest_rows(edges) == data["edge_sha256"], "edge digest")

    colouring = data["three_colouring"]
    need(len(colouring) == len(points), "colouring length")
    need(set(colouring) == {0, 1, 2}, "three colours used")
    need(all(colouring[left] != colouring[right] for left, right in edges),
         "three-colouring edge check")
    edge_set = set(edges)
    odd_cycle = data["odd_cycle"]
    need(len(odd_cycle) == 6 and odd_cycle[0] == odd_cycle[-1], "5-cycle shape")
    need(len(set(odd_cycle[:-1])) == 5, "5-cycle distinctness")
    need(all(tuple(sorted(pair)) in edge_set
             for pair in zip(odd_cycle, odd_cycle[1:])), "5-cycle edges")
    need(data["chromatic_number"] == 3, "chromatic claim")
    need(data["candidate_status"] is False and data["record_progress"] is False,
         "scope guard")

    triangle_count = sum(
        {(a, b), (a, c), (b, c)} <= edge_set
        for a, b, c in combinations(range(len(points)), 3)
    )
    need(triangle_count == data["triangle_count"] == 0, "triangle census")
    multiplicities = Counter(map(len, addresses))
    need({str(key): value for key, value in sorted(multiplicities.items())}
         == data["address_multiplicity_histogram"], "collision multiplicities")

    print(json.dumps({
        "verified": True,
        "claim_scope": data["claim_scope"],
        "raw_addresses": data["raw_addresses"],
        "distinct_points": len(points),
        "complete_unit_edges": len(edges),
        "incidental_unit_edges": data["incidental_unit_edges"],
        "chromatic_number": 3,
        "lower_bound_witness": odd_cycle,
        "upper_bound_witness_checked_edges": len(edges),
        "candidate_status": False,
        "record_progress": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
