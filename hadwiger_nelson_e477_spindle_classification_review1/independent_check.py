"""Independent audit of the complete E477 marked-pair spindle classification.

The target verifier is not imported.  Base-field arithmetic here is indexed by
the actual square-free radicands 1, 3, 11, 33, rather than the target's bit
basis.  The sixteen isometries are reconstructed from the two circle
intersections and the two possible determinants, not from the target transform.
"""

from collections import defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PARENT = REPO / "hadwiger_nelson_overlapping_forcing_seed"
TARGET = REPO / "hadwiger_nelson_e477_spindle_classification"
PARENT_CERTIFICATE = PARENT / "certificate.json"
MANDATORY = PARENT / "mandatory_vertices.json"
SEPARATING = TARGET / "separating_basis.json"

EXPECTED_HASHES = {
    PARENT_CERTIFICATE: "3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237",
    MANDATORY: "f0cea2d38b8d43e22bf82cba23ee65fb971cd031918015c9061ee499485cac2d",
    SEPARATING: "dc6034eff3b3059c73b76373f8176e810cf3ffdf448b6ce98edb571dad67dc4d",
}

# Coefficient order in Q(sqrt(3),sqrt(11)) is the actual radicand order below.
RADICANDS = (1, 3, 11, 33)
RINDEX = {radicand: index for index, radicand in enumerate(RADICANDS)}
FZERO = (0, 0, 0, 0)
FONE = (1, 0, 0, 0)
SCALE = 36 * 128
UNIT_SQUARED = SCALE * SCALE


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def fadd(left, right):
    return tuple(a + b for a, b in zip(left, right))


def fneg(value):
    return tuple(-a for a in value)


def fsub(left, right):
    return tuple(a - b for a, b in zip(left, right))


def fscale(value, scalar):
    return tuple(scalar * a for a in value)


def fmul(left, right):
    """Multiply using sqrt(r)*sqrt(s)=gcd(r,s)*sqrt(rs/gcd(r,s)^2)."""
    output = [0, 0, 0, 0]
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            common = gcd(RADICANDS[i], RADICANDS[j])
            radicand = RADICANDS[i] * RADICANDS[j] // (common * common)
            output[RINDEX[radicand]] += common * a * b
    return tuple(output)


def fsum(values):
    result = FZERO
    for value in values:
        result = fadd(result, value)
    return result


def base_point(row):
    """Return physical point times 36 as two base-field coefficient tuples."""
    require(type(row) is list and len(row) == 4 and all(type(x) is int for x in row), "coordinate row")
    a, b, c, d = row
    return (0, a, b, 0), (c, 0, 0, d)


def point_sub(left, right):
    return fsub(left[0], right[0]), fsub(left[1], right[1])


def point_scale(point, scalar):
    return fscale(point[0], scalar), fscale(point[1], scalar)


def base_norm(point):
    return fadd(fmul(point[0], point[0]), fmul(point[1], point[1]))


def unit_difference(row, other):
    """Definition-level unit test in the four-radical input field."""
    difference = point_sub(base_point(row), base_point(other))
    return base_norm(difference) == (36 * 36, 0, 0, 0)


def source_edges(rows):
    return [(u, v) for u, v in combinations(range(len(rows)), 2) if unit_difference(rows[u], rows[v])]


def proper(word, edges, deleted=None):
    if type(word) is str:
        require(len(word) == 477 and all(char in "0123" for char in word), "colour word")
    else:
        require(type(word) is list and len(word) == 477
                and all(type(colour) is int and 0 <= colour < 4 for colour in word), "colour word")
    require(all(word[u] != word[v] for u, v in edges if deleted not in (u, v)), "monochromatic edge")


def check_positive_words(rows, edges, parent, separating, mandatory):
    parent_word = parent["colouring"]
    proper(parent_word, edges)
    require(parent_word[0] == parent_word[1], "parent colouring does not identify terminals")

    require(type(separating) is list and len(separating) == 18, "separating word count")
    for word in separating:
        proper(word, edges)
    signatures = defaultdict(list)
    for vertex in range(477):
        signatures[tuple(word[vertex] for word in separating)].append(vertex)
    nonsingletons = sorted(group for group in signatures.values() if len(group) > 1)
    require(nonsingletons == [[0, 1]], "unseparated-pair classification")

    require(type(mandatory) is list and len(mandatory) == 253, "deletion witness count")
    deleted = [entry["deleted"] for entry in mandatory]
    require(deleted == sorted(set(deleted)), "deletion labels not distinct/sorted")
    require(all(type(vertex) is int and 2 <= vertex < 477 for vertex in deleted), "deletion label")
    for entry in mandatory:
        word = entry["colouring"]
        proper(word, edges, deleted=entry["deleted"])
        require(word[0] != word[1], "deletion word fails to separate terminals")
    return {
        "proper_parent_four_colouring": True,
        "separating_words": len(separating),
        "only_unseparated_pair": [0, 1],
        "terminal_separating_deletion_words": len(mandatory),
        "mandatory_vertices_per_forcing_half": len(mandatory) + 2,
    }


def entry_add(left, right):
    """Entries are constant-part/sqrt(247)-part integer pairs."""
    return left[0] + right[0], left[1] + right[1]


def entry_neg(value):
    return -value[0], -value[1]


def entry_mul(left, right):
    return left[0] * right[0] + 247 * left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def apply_entry(entry, value):
    return fscale(value, entry[0]), fscale(value, entry[1])


def extension_add(left, right):
    return fadd(left[0], right[0]), fadd(left[1], right[1])


def matrix_point(matrix, point):
    """Apply a numerator-over-128 O(2) matrix to a point scaled by 36.

    The result is a point scaled by 36*128, with each coordinate represented
    as alpha+beta*sqrt(247), alpha,beta in Q(sqrt(3),sqrt(11)).
    """
    m11, m12, m21, m22 = matrix
    x, y = point
    out_x = extension_add(apply_entry(m11, x), apply_entry(m12, y))
    out_y = extension_add(apply_entry(m21, x), apply_entry(m22, y))
    return out_x, out_y


def frame_matrix(first_endpoint, second_endpoint, circle_sign, determinant):
    """Reconstruct an isometry from circle intersection and determinant.

    The first remaining terminal is at sign(first)*8/3 on the y-axis.  The
    other terminal is at (circle_sign*sqrt(247)/16,
    sign(first)*119/48).  The source terminal vector is vertical with sign
    determined by second_endpoint.  Entries returned are numerators / 128.
    """
    require(first_endpoint in (0, 1) and second_endpoint in (0, 1), "endpoint choice")
    require(circle_sign in (-1, 1) and determinant in (-1, 1), "frame signs")
    first_sign = 1 if first_endpoint == 0 else -1
    second_sign = 1 if second_endpoint == 0 else -1

    # The second column is the image of the positive y basis vector.
    column2_x = (0, second_sign * circle_sign * 3)
    column2_y = (second_sign * first_sign * 119, 0)
    if determinant == 1:
        column1_x = column2_y
        column1_y = entry_neg(column2_x)
    else:
        column1_x = entry_neg(column2_y)
        column1_y = column2_x
    require(119 * 119 + 9 * 247 == 128 * 128, "circle trigonometry")
    column1_norm = entry_add(entry_mul(column1_x, column1_x), entry_mul(column1_y, column1_y))
    column2_norm = entry_add(entry_mul(column2_x, column2_x), entry_mul(column2_y, column2_y))
    column_dot = entry_add(entry_mul(column1_x, column2_x), entry_mul(column1_y, column2_y))
    require(column1_norm == column2_norm == (128 * 128, 0) and column_dot == (0, 0),
            "matrix is not orthogonal")
    return column1_x, column2_x, column1_y, column2_y


def extension_point_key(point):
    return point[0][0], point[0][1], point[1][0], point[1][1]


def cross_distance(left, right):
    """Squared distance in F(sqrt(247)), at physical scale 36*128."""
    base_terms = []
    radical_terms = []
    for base_left, (base_right, radical_right) in zip(left, right):
        delta = fsub(base_left, base_right)
        base_terms.extend((fmul(delta, delta), fscale(fmul(radical_right, radical_right), 247)))
        radical_terms.append(fscale(fmul(delta, radical_right), -2))
    return fsum(base_terms), fsum(radical_terms)


def make_frame(rows, first_endpoint, second_endpoint, circle_sign, determinant):
    points = [base_point(row) for row in rows]
    left_origin = points[first_endpoint]
    second_origin = points[second_endpoint]
    left = [point_scale(point_sub(point, left_origin), 128) for point in points]
    matrix = frame_matrix(first_endpoint, second_endpoint, circle_sign, determinant)
    right = [matrix_point(matrix, point_sub(point, second_origin)) for point in points]

    zero_extension = ((FZERO, FZERO), (FZERO, FZERO))
    require(right[second_endpoint] == zero_extension, "second endpoint does not map to origin")
    expected_x = (FZERO, (circle_sign * 288, 0, 0, 0))
    first_sign = 1 if first_endpoint == 0 else -1
    expected_y = ((first_sign * 11424, 0, 0, 0), FZERO)
    require(right[1 - second_endpoint] == (expected_x, expected_y), "wrong circle intersection")

    left_keys = {(point[0], FZERO, point[1], FZERO) for point in left}
    right_keys = {extension_point_key(point) for point in right}
    require(len(left_keys) == len(right_keys) == 477, "noninjective copy")
    require(left_keys & right_keys == {(FZERO, FZERO, FZERO, FZERO)}, "unexpected overlap")

    contacts = []
    expected_distance = ((UNIT_SQUARED, 0, 0, 0), FZERO)
    for i, left_point in enumerate(left):
        if i == first_endpoint:
            continue
        for j, right_point in enumerate(right):
            if j == second_endpoint:
                continue
            if cross_distance(left_point, right_point) == expected_distance:
                contacts.append((i, j))
    require(contacts == [(1 - first_endpoint, 1 - second_endpoint)], "unexpected cross contacts")
    return {
        "first_endpoint": first_endpoint,
        "second_endpoint": second_endpoint,
        "circle_sign": circle_sign,
        "determinant": determinant,
        "vertices": 953,
        "cross_contacts": [list(contact) for contact in contacts],
    }


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def check_frames(rows, edges, parent_word):
    reports = []
    five_colour_edge_checks = 0
    for first, second, circle_sign, determinant in product((0, 1), (0, 1), (-1, 1), (-1, 1)):
        report = make_frame(rows, first, second, circle_sign, determinant)
        reports.append(report)

        # Explicit proper five-colouring: clone the checked four-colouring and
        # recolour the second copy's bridge endpoint with a fresh colour.
        left_colours = list(map(int, parent_word))
        right_colours = list(map(int, parent_word))
        require(left_colours[first] == right_colours[second], "common colour mismatch")
        right_colours[1 - second] = 4
        require(all(left_colours[u] != left_colours[v] for u, v in edges), "left five-colouring")
        require(all(right_colours[u] != right_colours[v] for u, v in edges), "right five-colouring")
        require(left_colours[1 - first] != right_colours[1 - second], "bridge five-colouring")
        five_colour_edge_checks += 2 * len(edges) + 1
    require(len(reports) == 16, "frame count")
    return {
        "normalized_frames": len(reports),
        "each_frame_vertices": 953,
        "each_frame_unit_edges": 2 * len(edges) + 1,
        "sole_overlap_each_frame": True,
        "sole_cross_edge_each_frame": True,
        "five_colour_edge_checks": five_colour_edge_checks,
        "independent_frame_sha256": digest(reports),
    }


def main():
    for path, expected in EXPECTED_HASHES.items():
        require(file_hash(path) == expected, "unexpected input hash: " + str(path))
    certificate = json.loads(PARENT_CERTIFICATE.read_text())
    parent = certificate["equal"]
    rows = parent["points"]
    require(parent["denominator"] == 1 and len(rows) == 477, "parent E477 input")
    require(rows[0] == [0, 0, 0, 0] and rows[1] == [0, 0, 96, 0], "terminal coordinates")
    require(len({base_point(row) for row in rows}) == 477, "repeated source point")
    edges = source_edges(rows)
    require(len(edges) == 2458, "source edge census")

    separating = json.loads(SEPARATING.read_text())
    mandatory = json.loads(MANDATORY.read_text())
    result = {
        "checker": "independent radicand/circle-intersection audit",
        "target_verifier_imported": False,
        "vertices": len(rows),
        "unit_edges": len(edges),
        "source_edge_sha256": digest([list(edge) for edge in edges]),
    }
    result.update(check_positive_words(rows, edges, parent, separating, mandatory))
    result.update(check_frames(rows, edges, parent["colouring"]))
    minimum = 2 * result["mandatory_vertices_per_forcing_half"] - 1
    require(minimum == 509, "spindle lower bound")
    result.update({
        "minimum_nonfour_order_lower_bound": minimum,
        "every_subgraph_through_508_four_colourable": True,
        "all_checks_passed": True,
        "record_improvement": False,
    })
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
