"""Independent audit of the reduced Parts-509 near-injective realization theorem.

This checker does not import the claimed verifier or generator.  In particular,
it ignores the certificate's compressed orientation prefix cover and enumerates
all 2^12 complete orientation words.  It also recomputes the exceptional
one-pair quotients from adjacency and checks all ranks modulo an independent
prime with a different (left-pivot) elimination convention.
"""

from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CLAIM = ROOT / "hadwiger_nelson_parts509_plane_realizations"
EDGE_PATH = ROOT / "hadwiger_nelson_parts509_edge_criticality" / "reduced_edges.json"
POINT_PATH = ROOT / "hadwiger_nelson_parts509_degree_pool_minimum" / "certificate_D7.json"
CERT_PATH = CLAIM / "certificate.json"

EXPECTED = {
    EDGE_PATH: "99b8ca39503a33c692bed66e45afcc7e8b67bec0870253c53b097836fbbbe3b2",
    POINT_PATH: "41a47be8d0568be7e1497f16a45c17d433e31e01fb62877856189fbf1ad53729",
    CERT_PATH: "675a5c65e67f9080cdf82649c1ce2f1ca9371e83536c536b0394b04f1c6cef74",
}
RADICALS = (1, 3, 5, 15, 11, 33, 55, 165)
USED_FLAT_COORDINATES = (0, 2, 5, 7, 9, 11, 12, 14)
ALT_PRIME = 998244353  # prime, 2 modulo 3, so Q[t]/(t^2+3) remains a field


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def qadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def qneg(x):
    return -x[0], -x[1]


def qsub(x, y):
    return x[0] - y[0], x[1] - y[1]


def qmul(x, y, square):
    return x[0] * y[0] + square * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def qinv(x, square):
    denominator = x[0] * x[0] - square * x[1] * x[1]
    require(denominator != 0, "quadratic-field division by zero")
    return x[0] / denominator, -x[1] / denominator


def qdiv(x, y, square):
    return qmul(x, qinv(y, square), square)


QZERO = (F(0), F(0))
QONE = (F(1), F(0))


def exact_rref(rows, width, square=-3):
    """Gauss-Jordan RREF over Q(sqrt(square)), pivoting left to right."""
    matrix = [list(row) for row in rows]
    pivot_row = 0
    pivots = []
    for column in range(width):
        selected = next((r for r in range(pivot_row, len(matrix)) if matrix[r][column] != QZERO), None)
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        inverse = qinv(matrix[pivot_row][column], square)
        matrix[pivot_row] = [qmul(value, inverse, square) for value in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r == pivot_row:
                continue
            factor = matrix[r][column]
            if factor != QZERO:
                matrix[r] = [qsub(a, qmul(factor, b, square)) for a, b in zip(matrix[r], matrix[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivots, matrix[:pivot_row]


def exact_reduce(row, pivots, rref, square=-3):
    row = list(row)
    for pivot, basis_row in zip(pivots, rref):
        factor = row[pivot]
        if factor != QZERO:
            row = [qsub(a, qmul(factor, b, square)) for a, b in zip(row, basis_row)]
    return tuple(row)


def madd(x, y, p=ALT_PRIME):
    return (x[0] + y[0]) % p, (x[1] + y[1]) % p


def msub(x, y, p=ALT_PRIME):
    return (x[0] - y[0]) % p, (x[1] - y[1]) % p


def mmul(x, y, p=ALT_PRIME):
    return (x[0] * y[0] - 3 * x[1] * y[1]) % p, (x[0] * y[1] + x[1] * y[0]) % p


def minv(x, p=ALT_PRIME):
    denominator = (x[0] * x[0] + 3 * x[1] * x[1]) % p
    require(denominator, "finite-field division by zero")
    inverse = pow(denominator, -1, p)
    return x[0] * inverse % p, -x[1] * inverse % p


MZERO = (0, 0)


def modular_rref(rows, width, p=ALT_PRIME):
    matrix = [list(row) for row in rows]
    pivot_row = 0
    pivots = []
    for column in range(width):
        selected = next((r for r in range(pivot_row, len(matrix)) if matrix[r][column] != MZERO), None)
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        inverse = minv(matrix[pivot_row][column], p)
        matrix[pivot_row] = [mmul(value, inverse, p) for value in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r == pivot_row:
                continue
            factor = matrix[r][column]
            if factor != MZERO:
                matrix[r] = [msub(a, mmul(factor, b, p), p) for a, b in zip(matrix[r], matrix[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivots, matrix[:pivot_row]


def modular_reduce(row, pivots, rref, p=ALT_PRIME):
    row = list(row)
    for pivot, basis_row in zip(pivots, rref):
        factor = row[pivot]
        if factor != MZERO:
            row = [msub(a, mmul(factor, b, p), p) for a, b in zip(row, basis_row)]
    return tuple(row)


def rational_mod(value, p=ALT_PRIME):
    value = F(value)
    return value.numerator * pow(value.denominator, -1, p) % p


def sparse_rank(rows, p=ALT_PRIME):
    """Left-pivot sparse elimination over F_p."""
    basis = {}
    for original in rows:
        row = {i: value % p for i, value in original.items() if value % p}
        while row:
            pivot = min(row)
            if pivot not in basis:
                inverse = pow(row[pivot], -1, p)
                basis[pivot] = {i: value * inverse % p for i, value in row.items()}
                break
            factor = row[pivot]
            for i, value in basis[pivot].items():
                new = (row.get(i, 0) - factor * value) % p
                if new:
                    row[i] = new
                else:
                    row.pop(i, None)
    return len(basis)


def dense_rank(rows, p=ALT_PRIME):
    sparse = []
    for row in rows:
        sparse.append({i: rational_mod(value, p) for i, value in enumerate(row) if value})
    return sparse_rank(sparse, p)


def load_inputs():
    for path, digest in EXPECTED.items():
        require(file_sha(path) == digest, "unexpected input hash: " + str(path))
    raw_edges = json.loads(EDGE_PATH.read_text())["edges"]
    edges = [tuple(pair) for pair in raw_edges]
    require(len(edges) == 2259 and edges == sorted(set(edges)), "edge census/canonical order")
    require(all(0 <= u < v < 509 for u, v in edges), "edge endpoint range")

    raw_points = json.loads(POINT_PATH.read_text())["coordinates"]
    points = []
    coefficient_rows = []
    for vertex in range(509):
        point = raw_points[str(vertex)]
        require(len(point) == 2 and all(len(axis) == 8 for axis in point), "coordinate shape")
        parsed = tuple(tuple(F(value) for value in axis) for axis in point)
        flat = parsed[0] + parsed[1]
        require(all(flat[i] == 0 for i in range(16) if i not in USED_FLAT_COORDINATES), "coordinate support")
        points.append(parsed)
        coefficient_rows.append(tuple(flat[i] for i in USED_FLAT_COORDINATES))
    require(len(set(points)) == 509, "source coordinates are not injective")
    require(points[0] == ((F(0),) * 8, (F(0),) * 8), "source origin")
    return edges, points, coefficient_rows, json.loads(CERT_PATH.read_text())


def enumerate_rhombi(edges):
    adjacency = [set() for _ in range(509)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    rhombi = []
    maximum_common = 0
    for a, b in combinations(range(509), 2):
        common = sorted(adjacency[a] & adjacency[b])
        maximum_common = max(maximum_common, len(common))
        if len(common) == 2 and (a, b) < tuple(common):
            rhombi.append((a, b, common[0], common[1]))
    require(maximum_common == 2, "source common-neighbour maximum")
    return adjacency, rhombi


def quotient_k23(edges, first, second):
    """Return a K2,3 witness after identifying second with first, if present."""
    def image(v):
        return first if v == second else v

    quotient_edges = set()
    for u, v in edges:
        a, b = sorted((image(u), image(v)))
        if a != b:
            quotient_edges.add((a, b))
    adjacency = {v: set() for v in range(509) if v != second}
    for u, v in quotient_edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    vertices = sorted(adjacency)
    for i, u in enumerate(vertices):
        for v in vertices[i + 1:]:
            common = sorted(adjacency[u] & adjacency[v])
            if len(common) >= 3:
                return (u, v, common[0], common[1], common[2])
    return None


def check_rigidity(edges, coefficients, cert):
    adjacency, rhombi = enumerate_rhombi(edges)
    require(len(rhombi) == 2726, "rhombus census")
    for a, b, c, d in rhombi:
        require(
            all(coefficients[a][j] + coefficients[b][j] == coefficients[c][j] + coefficients[d][j]
                for j in range(8)),
            "coordinate coefficient outside rhombus kernel",
        )

    augmented = [(F(1),) + row for row in coefficients]
    require(dense_rank(augmented) == 9, "constant-plus-coordinate rank")

    bases = cert["bases"]
    require(len(bases) == 6, "basis count")
    for indices in bases:
        require(len(indices) == 500 and len(set(indices)) == 500, "basis size/duplicates")
        require(all(type(index) is int and 0 <= index < len(rhombi) for index in indices), "basis index")
        rows = []
        for index in indices:
            a, b, c, d = rhombi[index]
            rows.append({a: 1, b: 1, c: -1, d: -1})
        require(sparse_rank(rows) == 500, "alternate-prime rhombus rank")

    common_indices = set.intersection(*(set(indices) for indices in bases))
    require(len(common_indices) == 5, "common basis intersection")
    edge_set = set(edges)
    edge_obstructions = 0
    k23_obstructions = 0
    derived_k23 = []
    for index in sorted(common_indices):
        a, b, c, d = rhombi[index]
        for u, v in ((a, b), (c, d)):
            if tuple(sorted((u, v))) in edge_set:
                edge_obstructions += 1
            else:
                witness = quotient_k23(edges, u, v)
                require(witness is not None, "unresolved exceptional quotient")
                derived_k23.append((u, v, witness))
                k23_obstructions += 1
    require((edge_obstructions, k23_obstructions) == (4, 6), "exception type census")
    return rhombi, {
        "alternate_prime": ALT_PRIME,
        "constant_plus_coordinate_rank": 9,
        "rhombi": len(rhombi),
        "rhombus_basis_count": 6,
        "rhombus_basis_rank": 500,
        "common_basis_rows": len(common_indices),
        "edge_collapse_obstructions": edge_obstructions,
        "derived_K23_obstructions": k23_obstructions,
        "derived_K23_witnesses": derived_k23,
    }


def normalized_direction(coefficients, u, v):
    direction = tuple(b - a for a, b in zip(coefficients[u], coefficients[v]))
    first = next((value for value in direction if value), None)
    require(first is not None, "zero direction")
    if first < 0:
        direction = tuple(-value for value in direction)
    return direction


def get_directions(edges, coefficients, cert):
    edge_set = set(edges)
    all_directions = {normalized_direction(coefficients, u, v) for u, v in edges}
    directions = []
    for witness in cert["direction_edges"]:
        pair = tuple(witness)
        require(pair in edge_set, "direction witness is not an edge")
        directions.append(normalized_direction(coefficients, *pair))
    require(len(directions) == len(set(directions)) == 36, "direction witness census")
    require(set(directions) == all_directions, "direction witness completeness")

    triads = [tuple(row) for row in cert["triads"]]
    require(len(triads) == 12, "triad census")
    used = []
    for i, j, k, s, r in triads:
        require(len({i, j, k}) == 3 and all(0 <= x < 36 for x in (i, j, k)), "triad indices")
        require(s in (-1, 1) and r in (-1, 1), "triad signs")
        require(all(directions[i][q] + s * directions[j][q] == r * directions[k][q] for q in range(8)),
                "false direction triad")
        used.extend((i, j, k))
    require(sorted(used) == list(range(36)), "triads do not partition directions")
    return directions, triads


def orientation_rows(word, directions, triads, modular=False):
    rows = []
    for epsilon, (i, j, _k, s, _r) in zip(word, triads):
        # U_j/U_i = (-s + epsilon*t)/2, t^2=-3.
        if modular:
            half = pow(2, -1, ALT_PRIME)
            factor = ((-s * half) % ALT_PRIME, (epsilon * half) % ALT_PRIME)
            row = []
            for a, b in zip(directions[i], directions[j]):
                aa = (rational_mod(a), 0)
                bb = (rational_mod(b), 0)
                row.append(msub(bb, mmul(factor, aa)))
        else:
            factor = (F(-s, 2), F(epsilon, 2))
            row = []
            for a, b in zip(directions[i], directions[j]):
                row.append(qsub((b, F(0)), qmul(factor, (a, F(0)), -3)))
        rows.append(row)
    return rows


def equality_candidates(groups):
    for vertices in groups.values():
        if len(vertices) > 1:
            yield from combinations(vertices, 2)


def relation_row(left, right, factor):
    row = [QZERO] * 8
    row[left] = QONE
    row[right] = qneg(factor)
    return row


def check_all_orientations(coefficients, directions, triads):
    rank_histogram = Counter()
    modular_class_histogram = Counter()
    rejected = 0
    survivors = []
    survivor_sigmas = []

    modular_coefficients = [tuple((rational_mod(value), 0) for value in row) for row in coefficients]
    for word in product((-1, 1), repeat=12):
        exact_pivots, exact_basis = exact_rref(orientation_rows(word, directions, triads), 8)
        mod_pivots, mod_basis = modular_rref(orientation_rows(word, directions, triads, modular=True), 8)
        require(exact_pivots == mod_pivots, "exact/modular pivot mismatch")
        rank_histogram[len(exact_pivots)] += 1

        groups = defaultdict(list)
        for vertex, row in enumerate(modular_coefficients):
            groups[modular_reduce(row, mod_pivots, mod_basis)].append(vertex)
        modular_classes = len(groups)
        modular_class_histogram[modular_classes] += 1

        forced_pairs = []
        for u, v in equality_candidates(groups):
            difference = tuple((a - b, F(0)) for a, b in zip(coefficients[u], coefficients[v]))
            if exact_reduce(difference, exact_pivots, exact_basis) == (QZERO,) * 8:
                forced_pairs.append((u, v))
                if len(forced_pairs) == 2:
                    break
        if len(forced_pairs) >= 2:
            rejected += 1
            continue

        # A modular image cannot split an exact equality, so a word with fewer
        # than 509 modular classes but fewer than two confirmed pairs signals a
        # bad-prime collision or an implementation error, not a survivor.
        require(modular_classes == 509 and not forced_pairs, "unresolved modular coincidence")
        require(len(exact_pivots) == 4, "surviving orientation rank")
        matching_sigmas = []
        for sigma in (-1, 1):
            t = (F(0), F(sigma))
            relations = [
                relation_row(4, 0, t),
                relation_row(5, 1, t),
                relation_row(6, 2, (F(0), F(sigma, 3))),
                relation_row(7, 3, (F(0), F(sigma, 3))),
            ]
            if all(exact_reduce(row, exact_pivots, exact_basis) == (QZERO,) * 8 for row in relations):
                matching_sigmas.append(sigma)
        require(len(matching_sigmas) == 1, "survivor frame relation")
        survivors.append(word)
        survivor_sigmas.extend(matching_sigmas)

    require(rejected == 4094, "rejected orientation count")
    require(len(survivors) == 2 and sorted(survivor_sigmas) == [-1, 1], "surviving orientations")
    return {
        "complete_orientation_words": 4096,
        "orientation_words_rejected_by_two_exact_equalities": rejected,
        "orientation_survivors": [list(word) for word in survivors],
        "survivor_frame_signs": survivor_sigmas,
        "orientation_rank_histogram": dict(sorted(rank_histogram.items())),
        "modular_image_class_histogram": dict(sorted(modular_class_histogram.items())),
        "compressed_orientation_cover_used": False,
    }


def padd(poly, exponent, coefficient):
    if coefficient == QZERO:
        return
    value = qadd(poly.get(exponent, QZERO), coefficient)
    if value == QZERO:
        poly.pop(exponent, None)
    else:
        poly[exponent] = value


def pmul(left, right):
    answer = {}
    for a, x in left.items():
        for b, y in right.items():
            padd(answer, tuple(u + v for u, v in zip(a, b)), qmul(x, y, 33))
    return answer


def pscale(poly, scalar):
    answer = {}
    for exponent, coefficient in poly.items():
        padd(answer, exponent, qmul(coefficient, scalar, 33))
    return answer


def psum(polynomials):
    answer = {}
    for poly in polynomials:
        for exponent, coefficient in poly.items():
            padd(answer, exponent, coefficient)
    return answer


def constant(value):
    return {(0, 0, 0, 0): value} if value != QZERO else {}


def variable(index):
    exponent = tuple(int(i == index) for i in range(4))
    return {exponent: QONE}


def check_final_algebra(directions, cert):
    """Expand the survivor's unit equations in b,y,d,z over Q(sqrt(33))."""
    one = constant(QONE)
    zero = {}
    c = (F(0), F(1))
    b, y, d, z = (variable(i) for i in range(4))
    # Each parameter is represented as real_part + t*t_part, t^2=-3.
    parameters = [
        (one, zero),
        (b, y),
        (constant(c), zero),
        (d, z),
        (zero, one),
        (pscale(y, (F(-3), F(0))), b),
        (zero, constant((F(0), F(1, 3)))),
        (pscale(z, (F(-1), F(0))), pscale(d, (F(1, 3), F(0)))),
    ]

    equations = []
    for direction in directions:
        real_parts = []
        t_parts = []
        for coefficient, (real, tpart) in zip(direction, parameters):
            scalar = (coefficient, F(0))
            real_parts.append(pscale(real, scalar))
            t_parts.append(pscale(tpart, scalar))
        real = psum(real_parts)
        tpart = psum(t_parts)
        norm = psum((pmul(real, real), pscale(pmul(tpart, tpart), (F(3), F(0)))))
        padd(norm, (0, 0, 0, 0), (F(-1), F(0)))
        equations.append(norm)

    targets = {
        "norm_B_minus_5": {
            (2, 0, 0, 0): QONE,
            (0, 2, 0, 0): (F(3), F(0)),
            (0, 0, 0, 0): (F(-5), F(0)),
        },
        "y": {(0, 1, 0, 0): QONE},
        "z": {(0, 0, 0, 1): QONE},
        "d_minus_c_b": {(0, 0, 1, 0): QONE, (1, 0, 0, 0): qneg(c)},
    }
    combinations_data = cert["polynomial_combinations"]
    require(set(combinations_data) == set(targets), "polynomial target names")
    nonzero_weights = 0
    for name, terms in combinations_data.items():
        pieces = []
        used = set()
        for index, rational, radical in terms:
            require(index not in used and 0 <= index < 36, "polynomial equation index")
            used.add(index)
            weight = (F(rational), F(radical))
            require(weight != QZERO, "zero polynomial weight")
            pieces.append(pscale(equations[index], weight))
            nonzero_weights += 1
        require(psum(pieces) == targets[name], "failed polynomial consequence: " + name)

    # The normalization directions separately give |A|=1, C real, C^2=33.
    normalization_directions = {
        (F(1), F(0), F(0), F(0), F(0), F(0), F(0), F(0)),
        (F(0), F(0), F(1, 6), F(0), F(1, 6), F(0), F(0), F(0)),
        (F(0), F(0), F(1, 6), F(0), F(-1, 6), F(0), F(0), F(0)),
    }
    require(normalization_directions <= set(directions), "missing normalization directions")
    return {
        "normalization_unit_directions": 3,
        "exact_polynomial_consequences": sorted(targets),
        "polynomial_combination_terms": nonzero_weights,
    }


def multiply_radicals(r, s):
    factor = gcd(r, s)
    return factor, r * s // (factor * factor)


def squared_distance(point, other):
    expansion = defaultdict(F)
    for axis in range(2):
        difference = [a - b for a, b in zip(point[axis], other[axis])]
        for i, left in enumerate(difference):
            if not left:
                continue
            for j, right in enumerate(difference):
                if right:
                    factor, radical = multiply_radicals(RADICALS[i], RADICALS[j])
                    expansion[radical] += left * right * factor
    return {radical: value for radical, value in expansion.items() if value}


def check_four_realizations(points, edges):
    hashes = []
    for sign5, sign11 in product((-1, 1), repeat=2):
        image = []
        for point in points:
            conjugate = []
            for axis in point:
                conjugate.append(tuple(
                    coefficient * (sign5 if radical % 5 == 0 else 1) * (sign11 if radical % 11 == 0 else 1)
                    for coefficient, radical in zip(axis, RADICALS)
                ))
            image.append(tuple(conjugate))
        require(len(set(image)) == 509, "noninjective conjugate realization")
        require(all(squared_distance(image[u], image[v]) == {1: F(1)} for u, v in edges),
                "non-unit edge in conjugate realization")
        raw = (json.dumps(image, separators=(",", ":"), default=str) + "\n").encode()
        hashes.append(sha256(raw).hexdigest())
    return {
        "normalized_realizations": 4,
        "vertices_per_realization": 509,
        "exact_unit_edge_checks": 4 * len(edges),
        "independent_realization_hashes": hashes,
    }


def main():
    require(ALT_PRIME % 3 == 2, "alternate prime congruence")
    require(all(ALT_PRIME % divisor for divisor in range(2, isqrt(ALT_PRIME) + 1)), "alternate prime primality")
    edges, points, coefficients, cert = load_inputs()
    result = {
        "checker": "independent direct-orientation audit",
        "claimed_verifier_imported": False,
        "source_vertices": len(points),
        "source_edges": len(edges),
    }
    _rhombi, rigidity = check_rigidity(edges, coefficients, cert)
    result.update(rigidity)
    directions, triads = get_directions(edges, coefficients, cert)
    result["unit_directions"] = len(directions)
    result["disjoint_direction_triads"] = len(triads)
    result.update(check_all_orientations(coefficients, directions, triads))
    result.update(check_final_algebra(directions, cert))
    result.update(check_four_realizations(points, edges))
    result.update({
        "all_checks_passed": True,
        "no_realization_with_exactly_508_images": True,
        "all_injective_realizations_classified": True,
        "images_at_most_507_classified": False,
        "record_improvement": False,
    })
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
