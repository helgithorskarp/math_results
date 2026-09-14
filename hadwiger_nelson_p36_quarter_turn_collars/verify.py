#!/usr/bin/env python3
"""Independent exact verifier for the P36 quarter-turn collar theorem.

The verifier imports no producer code.  It reconstructs physical point sets
and every unit edge directly from coordinates, checks the elementary residue
colouring where it applies, and otherwise checks a stored positive word.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
Vec = tuple[int, int, int, int]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def plus(u: Vec, v: Vec) -> Vec:
    return tuple(a + b for a, b in zip(u, v))  # type: ignore[return-value]


def minus(u: Vec, v: Vec) -> Vec:
    return tuple(a - b for a, b in zip(u, v))  # type: ignore[return-value]


def quarter(u: Vec) -> Vec:
    a, b, c, d = u
    return (-c, -d, a, b)


def quarter_power(u: Vec, exponent: int) -> Vec:
    for _ in range(exponent % 4):
        u = quarter(u)
    return u


def divided_by_two(u: Vec) -> Vec:
    require(all(value % 2 == 0 for value in u), "half-integral center")
    return tuple(value // 2 for value in u)  # type: ignore[return-value]


def sixth_turn(u: Vec) -> Vec:
    a, b, c, d = u
    return divided_by_two((a - 3 * d, b - c, 3 * b + c, a + d))


def mirror(u: Vec) -> Vec:
    a, b, c, d = u
    return (a, b, -c, -d)


def canonical(u: Vec) -> Vec:
    images = []
    for initial in (u, mirror(u)):
        current = initial
        for _ in range(6):
            images.append(current)
            current = sixth_turn(current)
        require(current == initial, "sixth-turn orbit did not close")
    return min(images)


def squared_norm(u: Vec) -> tuple[int, int]:
    """Coefficients of 16|u|^2 in the basis (1,sqrt(3))."""
    a, b, c, d = u
    return (a * a + 3 * b * b + c * c + 3 * d * d,
            2 * (a * b + c * d))


def exact_unit_vectors() -> tuple[Vec, ...]:
    # The rational coefficient of 16|u|^2 is a sum of nonnegative terms.
    # Hence these bounds contain every integral-coefficient unit vector.
    vectors = []
    for a in range(-4, 5):
        for b in range(-2, 3):
            for c in range(-4, 5):
                for d in range(-2, 3):
                    u = (a, b, c, d)
                    if squared_norm(u) == (16, 0):
                        vectors.append(u)
    return tuple(sorted(vectors))


def make_patch() -> tuple[list[tuple[int, int]], list[Vec]]:
    rows = []
    for a in range(-14, 15):
        for b in range(-14, 15):
            if a * a + a * b + b * b <= 36:
                rows.append(((4 * a + 2 * b, 0, 0, 2 * b), (a, b)))
    rows.sort()
    return [label for _, label in rows], [point for point, _ in rows]


def center(p: Vec, q: Vec) -> Vec:
    translation = minus(p, quarter(q))
    return divided_by_two(plus(translation, quarter(translation)))


def physical_graph(c: Vec, patch_points: list[Vec], units: tuple[Vec, ...]):
    occurrences: dict[Vec, list[tuple[int, int]]] = defaultdict(list)
    layers = []
    for layer in range(4):
        image = []
        for index, point in enumerate(patch_points):
            mapped = plus(c, quarter_power(minus(point, c), layer))
            image.append(mapped)
            occurrences[mapped].append((layer, index))
        layers.append(image)
    points = sorted(occurrences)
    index = {point: number for number, point in enumerate(points)}
    edges = set()
    for first, point in enumerate(points):
        for displacement in units:
            second = index.get(plus(point, displacement))
            if second is not None and first < second:
                edges.add((first, second))
    masks = []
    for point in points:
        mask = 0
        for layer, _ in occurrences[point]:
            mask |= 1 << layer
        masks.append(mask)
    return points, edges, occurrences, masks, layers


def check_word(text: str, vertices: int, edges: set[tuple[int, int]]) -> None:
    require(len(text) == vertices, "colour-word length mismatch")
    require(set(text) <= set("0123"), "invalid colour name")
    require(all(text[x] != text[y] for x, y in edges),
            "positive word has a monochromatic unit edge")


def residue_word(points: list[Vec], edges: set[tuple[int, int]],
                 occurrences: dict[Vec, list[tuple[int, int]]],
                 labels: list[tuple[int, int]]) -> str | None:
    residues = [(a - b) % 3 for a, b in labels]
    signs = [int(value == 2) for value in residues]
    sign_equations = []
    zero_equations = []
    impossible = False

    def equation(left: tuple[int, int], right: tuple[int, int], equal: bool) -> None:
        nonlocal impossible
        layer1, index1 = left
        layer2, index2 = right
        zero1 = residues[index1] == 0
        zero2 = residues[index2] == 0
        if equal:
            if zero1 != zero2:
                impossible = True
            elif zero1:
                zero_equations.append((layer1, layer2, 0))
            else:
                sign_equations.append(
                    (layer1, layer2, signs[index1] ^ signs[index2]))
        elif zero1 == zero2:
            if zero1:
                zero_equations.append((layer1, layer2, 1))
            else:
                sign_equations.append(
                    (layer1, layer2, 1 ^ signs[index1] ^ signs[index2]))

    for point in points:
        row = occurrences[point]
        for other in row[1:]:
            equation(row[0], other, True)
    for x, y in edges:
        equation(occurrences[points[x]][0], occurrences[points[y]][0], False)
    if impossible:
        return None

    def solve(rows: list[tuple[int, int, int]]) -> int | None:
        for mask in range(16):
            if all(((mask >> x) ^ (mask >> y)) & 1 == value
                   for x, y, value in rows):
                return mask
        return None

    sign_mask = solve(sign_equations)
    zero_mask = solve(zero_equations)
    if sign_mask is None or zero_mask is None:
        return None
    word = []
    for point in points:
        layer, index = occurrences[point][0]
        if residues[index] == 0:
            word.append(str((zero_mask >> layer) & 1))
        else:
            word.append(str(2 + (((sign_mask >> layer) & 1) ^ signs[index])))
    answer = "".join(word)
    check_word(answer, len(points), edges)
    return answer


def histogram_rows(counter: Counter) -> list[list[object]]:
    return [[*key, value] if isinstance(key, tuple) else [key, value]
            for key, value in sorted(counter.items())]


def verify(certificate_path: Path) -> dict[str, object]:
    labels, patch_points = make_patch()
    require(len(patch_points) == 127, "P36 order changed")
    require(len(set(patch_points)) == 127, "duplicate P36 point")
    units = exact_unit_vectors()
    require(len(units) == 12, "unit-vector census changed")
    point_set = set(patch_points)
    require({sixth_turn(point) for point in patch_points} == point_set,
            "P36 is not sixth-turn invariant")
    require({mirror(point) for point in patch_points} == point_set,
            "P36 is not reflection invariant")
    patch_index = {point: number for number, point in enumerate(patch_points)}
    patch_edges = {
        (i, j) for i, point in enumerate(patch_points)
        for displacement in units
        if (j := patch_index.get(plus(point, displacement))) is not None and i < j
    }
    require(len(patch_edges) == 342, "P36 edge count changed")

    raw_centers = [center(p, q) for p in patch_points for q in patch_points]
    require(len(raw_centers) == 16129, "anchor-pair count changed")
    require(len(set(raw_centers)) == len(raw_centers),
            "two ordered anchor pairs produce the same center")
    center_set = set(raw_centers)
    require(all(canonical(c) in center_set for c in raw_centers),
            "symmetry leaves the center family")
    diagonal = {center(p, p) for p in patch_points}
    require(diagonal == point_set, "diagonal anchors do not give patch centers")

    orbit_members: dict[Vec, list[Vec]] = defaultdict(list)
    for c in raw_centers:
        orbit_members[canonical(c)].append(c)
    require(sum(map(len, orbit_members.values())) == 16129,
            "orbit partition is incomplete")

    payload_bytes = certificate_path.read_bytes()
    payload = json.loads(payload_bytes)
    require(payload.get("schema") ==
            "p36-quarter-turn-collar-positive-colourings-v1",
            "certificate schema mismatch")
    rows = payload.get("certificates")
    require(isinstance(rows, list), "missing certificate list")
    certificates = {}
    for row in rows:
        require(set(row) == {"center", "vertices", "edges", "word"},
                "unexpected certificate field")
        c = tuple(row["center"])
        require(len(c) == 4 and all(isinstance(x, int) for x in c),
                "invalid certificate center")
        require(c == canonical(c) and c in orbit_members,
                "certificate center is not a family representative")
        require(c not in certificates, "duplicate certificate center")
        certificates[c] = row

    support_hist = Counter()
    edge_hist = Counter()
    ansatz_hist = Counter()
    orbit_ansatz_hist = Counter()
    orbit_size_hist = Counter()
    common_points_hist = Counter()
    graph_hash = hashlib.sha256()
    colour_hash = hashlib.sha256()
    center_hash = hashlib.sha256()
    used_certificates = set()
    empty_extra_contact_placements = 0
    empty_extra_contact_orbits = 0

    for representative in sorted(orbit_members):
        multiplicity = len(orbit_members[representative])
        orbit_size_hist[multiplicity] += 1
        center_hash.update(json.dumps(
            [list(representative), multiplicity], separators=(",", ":")).encode())
        center_hash.update(b"\n")
        points, edges, occurrences, masks, _ = physical_graph(
            representative, patch_points, units)
        common_points = sum(mask == 15 for mask in masks)
        scope = "empty" if common_points == 0 else "common"
        common_points_hist[(scope, common_points)] += multiplicity
        support_hist[(scope, len(points))] += multiplicity
        edge_hist[(scope, len(edges))] += multiplicity
        if scope == "empty" and len(edges) > 4 * len(patch_edges):
            empty_extra_contact_placements += multiplicity
            empty_extra_contact_orbits += 1

        candidate = residue_word(points, edges, occurrences, labels)
        if candidate is None:
            require(representative in certificates,
                    "missing positive word for a residue-conflict orbit")
            row = certificates[representative]
            require(row["vertices"] == len(points) and row["edges"] == len(edges),
                    "certificate graph counts mismatch")
            candidate = row["word"]
            check_word(candidate, len(points), edges)
            used_certificates.add(representative)
            route = "certificate"
        else:
            require(representative not in certificates,
                    "redundant certificate for a residue-colourable orbit")
            route = "residue"
        ansatz_hist[(scope, route)] += multiplicity
        orbit_ansatz_hist[(scope, route)] += 1

        graph_hash.update(json.dumps(
            [list(representative), [list(point) for point in points],
             [list(edge) for edge in sorted(edges)]],
            separators=(",", ":")).encode())
        graph_hash.update(b"\n")
        colour_hash.update(json.dumps(
            [list(representative), candidate], separators=(",", ":")).encode())
        colour_hash.update(b"\n")

    require(used_certificates == set(certificates),
            "unused positive certificate")
    require(sum(value for (scope, _), value in support_hist.items()
                if scope == "empty") == 16002,
            "empty-intersection count changed")
    require(sum(value for (scope, _), value in support_hist.items()
                if scope == "common") == 127,
            "common-intersection count changed")
    require(all(size == 504 for (scope, size), value in support_hist.items()
                if scope == "empty" and value),
            "an empty-intersection collar does not have 504 points")

    return {
        "status": "ALL_QUARTER_TURN_COLLARS_FOUR_COLOURABLE",
        "coordinate_model": "((a+b*sqrt(3))/4,(c+d*sqrt(3))/4)",
        "patch_vertices": len(patch_points),
        "patch_edges": len(patch_edges),
        "unit_vectors": len(units),
        "ordered_anchor_pairs": len(raw_centers),
        "distinct_centers": len(center_set),
        "dihedral_center_orbits": len(orbit_members),
        "orbit_size_histogram": histogram_rows(orbit_size_hist),
        "support_histogram": histogram_rows(support_hist),
        "edge_histogram": histogram_rows(edge_hist),
        "common_point_histogram": histogram_rows(common_points_hist),
        "colour_route_histogram": histogram_rows(ansatz_hist),
        "orbit_colour_route_histogram": histogram_rows(orbit_ansatz_hist),
        "positive_certificate_words": len(certificates),
        "empty_extra_contact_placements": empty_extra_contact_placements,
        "empty_extra_contact_orbits": empty_extra_contact_orbits,
        "minimum_empty_edges": min(edges for (scope, edges), value in edge_hist.items()
                                   if scope == "empty" and value),
        "maximum_empty_edges": max(edges for (scope, edges), value in edge_hist.items()
                                   if scope == "empty" and value),
        "center_orbit_sha256": center_hash.hexdigest(),
        "graph_stream_sha256": graph_hash.hexdigest(),
        "colour_cover_sha256": colour_hash.hexdigest(),
        "certificate_sha256": hashlib.sha256(payload_bytes).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path,
                        default=HERE / "colourings.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify(args.certificate)
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(result == expected, "result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
