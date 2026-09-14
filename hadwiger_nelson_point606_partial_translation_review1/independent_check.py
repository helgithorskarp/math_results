#!/usr/bin/env python3
"""Clean-room exact audit of the point606 partial-translation theorem.

This checker imports no code from the reviewed package.  It reconstructs the
530 points from the original coordinate sources, computes every unit edge in
the nested tower Q(sqrt(3),sqrt(5),sqrt(11)), partitions edges by unoriented
displacement, and uses integer-bitset reachability after deleting up to two
direction classes.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
DENOMINATOR = 288
PINNED_HASHES = {
    "hadwiger_nelson_point606_partial_translation/.gitignore":
        "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "hadwiger_nelson_point606_partial_translation/EXPECTED.json":
        "76e2a1e208910249fde44d5ac5a3d599be4ca60c4a7600d983ee59092c110b2c",
    "hadwiger_nelson_point606_partial_translation/README.md":
        "0633c374540d95998765bd5aa0fae26f4dd28d3f93bfad213290b0755d44c4e5",
    "hadwiger_nelson_point606_partial_translation/SHA256SUMS":
        "0cd6c0c9dc9a2d12478fbe96af284f32d67c9ee9a07d3b7364f46bc9cdea6177",
    "hadwiger_nelson_point606_partial_translation/VALIDATION.json":
        "a9160c36a072a4dabc6a1a0241ed9b8350b5c3f735df51e8fa0d4f0b0f1e5282",
    "hadwiger_nelson_point606_partial_translation/audit.py":
        "4f0926f60756432dd52d373c6c1cad4ee965e8ff78d334218bb0dfb0d13b28bb",
    "hadwiger_nelson_point606_partial_translation/controls.py":
        "30b5f0b85f10b3f64e00aca6c5ce650c600e834826fde41b583f504b47c58da3",
    "hadwiger_nelson_point606_partial_translation/inputs.json":
        "8a2da217206b285baa23d525d34bb6f7b476c529c91acf394e6838f5c1750f91",
    "hadwiger_nelson_point606_partial_translation/verify.py":
        "d5a5dfc641eaa6b860626e80d7932a46b63dcb526c3f4cfdcd8a454fbfe92906",
    "hadwiger_nelson_point606_criticality_gate/certificate.json":
        "be652a44cb9e070c77a6404ee7cfc45a6956e94f600a0b486ec1d21ed6bfdb20",
    "hadwiger_nelson_parts509_completion_census_degree9/points.tsv":
        "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "hadwiger_nelson_parts509_swap_closure/completion_points.json":
        "b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    answer = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def multiply_biquadratic(left, right):
    """Multiply in basis 1,sqrt(3),sqrt(5),sqrt(15)."""
    x0, x3, x5, x15 = left
    y0, y3, y5, y15 = right
    return (
        x0*y0 + 3*x3*y3 + 5*x5*y5 + 15*x15*y15,
        x0*y3 + x3*y0 + 5*(x5*y15 + x15*y5),
        x0*y5 + x5*y0 + 3*(x3*y15 + x15*y3),
        x0*y15 + x15*y0 + x3*y5 + x5*y3,
    )


def add(left, right):
    return tuple(a+b for a, b in zip(left, right, strict=True))


def multiply_tower(left, right):
    """Multiply (a+b sqrt(11))(c+d sqrt(11)) as nested pairs."""
    a, b = left[:4], left[4:]
    c, d = right[:4], right[4:]
    low = add(multiply_biquadratic(a, c),
              tuple(11*x for x in multiply_biquadratic(b, d)))
    high = add(multiply_biquadratic(a, d), multiply_biquadratic(b, c))
    return low + high


def squared_distance(first, second):
    dx = tuple(a-b for a, b in zip(first[0], second[0], strict=True))
    dy = tuple(a-b for a, b in zip(first[1], second[1], strict=True))
    return add(multiply_tower(dx, dx), multiply_tower(dy, dy))


def read_points():
    for name, expected in PINNED_HASHES.items():
        require(digest(REPOSITORY / name) == expected, ("pinned hash", name))

    originals = []
    path = REPOSITORY / "hadwiger_nelson_parts509_completion_census_degree9/points.tsv"
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        require(len(row) == 16, ("original coordinate width", len(originals)))
        originals.append((row[:8], row[8:]))
    require(len(originals) == 509, ("original point count", len(originals)))

    raw = json.loads((REPOSITORY /
        "hadwiger_nelson_parts509_swap_closure/completion_points.json").read_text())
    completion = []
    common = 96
    for record in raw["points"]:
        point = (tuple(Fraction(value) for value in record["x"]),
                 tuple(Fraction(value) for value in record["y"]))
        require(len(point[0]) == len(point[1]) == 8, "completion coordinate width")
        for coefficient in point[0] + point[1]:
            common = lcm(common, coefficient.denominator)
        completion.append(point)
    require(len(completion) == 1158, ("completion point count", len(completion)))
    require(common == DENOMINATOR, ("common denominator", common))

    ambient = [
        (tuple((DENOMINATOR//96)*x for x in point[0]),
         tuple((DENOMINATOR//96)*y for y in point[1]))
        for point in originals
    ]
    ambient.extend(
        (tuple(int(DENOMINATOR*x) for x in point[0]),
         tuple(int(DENOMINATOR*y) for y in point[1]))
        for point in completion
    )
    host_labels = tuple(range(585)) + (606,)
    certificate = json.loads((REPOSITORY /
        "hadwiger_nelson_point606_criticality_gate/certificate.json").read_text())
    deleted = certificate["deleted_labels"]
    require(deleted == sorted(set(deleted)) and len(deleted) == 56,
            ("parent deleted labels", len(deleted)))
    core_labels = tuple(label for label in host_labels if label not in set(deleted))
    points = tuple(ambient[label] for label in core_labels)
    require(len(core_labels) == len(points) == len(set(points)) == 530,
            ("core points", len(points), len(set(points))))
    return core_labels, points


def canonical_unoriented(first, second):
    vector = tuple(b-a for axis_a, axis_b in zip(first, second, strict=True)
                   for a, b in zip(axis_a, axis_b, strict=True))
    require(any(vector), "zero displacement")
    first_nonzero = next(x for x in vector if x)
    return vector if first_nonzero > 0 else tuple(-x for x in vector)


def reconstruct_graph(points):
    target = (DENOMINATOR*DENOMINATOR,) + (0,)*7
    edges = []
    direction_edges = defaultdict(list)
    for first, second in combinations(range(len(points)), 2):
        if squared_distance(points[first], points[second]) != target:
            continue
        edge = (first, second)
        edges.append(edge)
        direction_edges[canonical_unoriented(points[first], points[second])].append(edge)
    directions = tuple(sorted(direction_edges))
    groups = tuple(tuple(direction_edges[direction]) for direction in directions)
    return tuple(edges), directions, groups


def reachable_count(order, edges):
    adjacency = [0]*order
    for first, second in edges:
        require(0 <= first < second < order, ("edge domain", first, second))
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    reached = frontier = 1
    while frontier:
        neighbours = 0
        todo = frontier
        while todo:
            bit = todo & -todo
            todo ^= bit
            neighbours |= adjacency[bit.bit_length()-1]
        frontier = neighbours & ~reached
        reached |= frontier
    return reached.bit_count()


def partition_digest(directions, groups):
    trace = sha256()
    for index, (direction, group) in enumerate(zip(directions, groups, strict=True)):
        trace.update(("D " + str(index) + " " + " ".join(map(str, direction)) + "\n").encode())
        for first, second in group:
            trace.update(f"E {first} {second}\n".encode())
    return trace.hexdigest()


def check_direction_robustness(order, groups):
    cases = [()] + [(i,) for i in range(len(groups))]
    cases.extend(combinations(range(len(groups)), 2))
    minimum_reached = order
    minimum_edges = sum(map(len, groups))
    maximum_pair_edges = 0
    pair_tests = 0
    trace = sha256()
    for removed in cases:
        removed_set = set(removed)
        retained = tuple(edge for index, group in enumerate(groups)
                         if index not in removed_set for edge in group)
        reached = reachable_count(order, retained)
        require(reached == order, ("disconnected direction deletion", removed, reached))
        minimum_reached = min(minimum_reached, reached)
        trace.update((" ".join(map(str, removed)) + f":{len(retained)}:{reached}\n").encode())
        if len(removed) == 2:
            pair_tests += 1
            minimum_edges = min(minimum_edges, len(retained))
            maximum_pair_edges = max(maximum_pair_edges, len(retained))
    return {
        "all_up_to_two_direction_deletions_connected": True,
        "zero_direction_deletion_tests": 1,
        "single_direction_deletion_tests": len(groups),
        "direction_pair_deletion_tests": pair_tests,
        "total_connectivity_tests": len(cases),
        "minimum_reachable_vertices": minimum_reached,
        "minimum_pair_retained_edges": minimum_edges,
        "maximum_pair_retained_edges": maximum_pair_edges,
        "connectivity_trace_sha256": trace.hexdigest(),
    }


def translate(point, vector, choice):
    return tuple(tuple(x + choice*y for x, y in zip(axis, delta, strict=True))
                 for axis, delta in zip(point, vector, strict=True))


def controls():
    radicands = (1, 3, 5, 15, 11, 33, 55, 165)
    field_products = 0
    for first in range(8):
        for second in range(8):
            left = tuple(int(i == first) for i in range(8))
            right = tuple(int(i == second) for i in range(8))
            common = gcd(radicands[first], radicands[second])
            radical = radicands[first]*radicands[second]//(common*common)
            expected = tuple(common if radicands[i] == radical else 0 for i in range(8))
            require(multiply_tower(left, right) == expected,
                    ("field basis product", first, second))
            field_products += 1
    zero = (0,)*8
    left = ((-1,)+(0,)*7, zero)
    right = ((1,)+(0,)*7, zero)
    top = (zero, (0, 1)+(0,)*6)
    bottom = (zero, (0, -1)+(0,)*6)
    diamond = (left, right, top, bottom)
    translation = (zero, (0, 2)+(0,)*6)
    unit = (4,) + (0,)*7
    edges = tuple((a, b) for a, b in combinations(range(4), 2)
                  if squared_distance(diamond[a], diamond[b]) == unit)
    require(len(edges) == 5, ("diamond edges", len(edges)))
    contractions = preserving = 0
    for choices in product((0, 1), repeat=4):
        image = tuple(translate(point, translation, choice)
                      for point, choice in zip(diamond, choices, strict=True))
        if all(squared_distance(image[a], image[b]) == unit for a, b in edges):
            preserving += 1
            contractions += len(set(image)) == 3
    require(contractions == 2, ("diamond contractions", contractions))
    require(reachable_count(4, ((0, 1), (2, 3))) == 2,
            "disconnected bitset control")
    try:
        canonical_unoriented(left, left)
    except RuntimeError:
        zero_rejected = True
    else:
        raise RuntimeError("zero direction accepted")
    return {
        "field_basis_products": field_products,
        "diamond_boolean_assignments": 16,
        "diamond_edge_preserving_assignments": preserving,
        "diamond_three_point_contractions": contractions,
        "disconnected_graph_rejected": True,
        "zero_direction_rejected": zero_rejected,
    }


def main():
    core_labels, points = read_points()
    edges, directions, groups = reconstruct_graph(points)
    require(len(edges) == 2648 and len(groups) == 36,
            ("graph dimensions", len(edges), len(groups)))
    edge_hash = sha256("".join(f"{a} {b}\n" for a, b in edges).encode()).hexdigest()
    require(edge_hash == "7116ca71d9b53598b931614a5c7f5406909f124555f0ecf231a4fc234b665faa",
            ("edge stream", edge_hash))
    robustness = check_direction_robustness(len(points), groups)
    result = {
        "status": "ACCEPTABLE EXACT FINITE CLAIM REPRODUCED",
        "reviewed_source_commit": "8b4a5d149d4d908530d9a3b0f8613446f627e36c",
        "imports_reviewed_code": False,
        "arithmetic_representation": "nested quadratic tower",
        "connectivity_representation": "integer bitsets",
        "source_vertices": len(points),
        "source_labels_sha256": sha256(json.dumps(core_labels, separators=(",", ":")).encode()).hexdigest(),
        "source_points_distinct": len(set(points)) == len(points),
        "complete_pair_checks": len(points)*(len(points)-1)//2,
        "complete_unit_edges": len(edges),
        "source_edge_sha256": edge_hash,
        "unoriented_unit_directions": len(groups),
        "direction_class_size_histogram": dict(sorted(Counter(map(len, groups)).items())),
        "direction_partition_sha256": partition_digest(directions, groups),
        **robustness,
        "criterion_consequence": "every edge-preserving Boolean partial translation is global",
        "minimum_image_order_in_declared_class": 530,
        "at_most_508_image_exists_in_declared_class": False,
        "chromatic_certificate_used": False,
        "record_candidate": False,
        "controls": controls(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
