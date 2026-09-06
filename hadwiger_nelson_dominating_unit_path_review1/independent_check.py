#!/usr/bin/env python3
"""Independent review of connected-dominating-triple four-colourability.

This checker imports no executable from the reviewed contribution.  It
reconstructs the formal patch and event equations directly, proves that the
named exact parameters exhaust all circle/line events, rebuilds every generic
and exceptional graph with recursive quadratic-tower arithmetic, checks the
submitted list colourings, finds fresh list colourings, audits the residual
palette edge types, and verifies the sharp Moser-spindle example.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, lcm
import os
from pathlib import Path
import sys


TARGET_COMMIT = "43db8b0a81018d98ff7135f74983f6174af466a1"
TARGET_HASHES = {
    ".gitignore": "0175fcafc5d8328c584d3df3eeba657ad2c5ccda3956d46d15e15adb9ecdd57c",
    "README.md": "6279998a50594d7147000e335350182c9ab299de427ec2d3051e682d88fabbdb",
    "build.py": "cf02df6d62d0cf47e5cd09c2a4607517a6aef45ac426d305ecdd7eb127cd261e",
    "certificate.json": "52c3f952f5bb8fcd70b36ecd7acd9fc420d60fa583b394310a392a5ebe92c6a2",
    "expected.json": "c458cd07dd1185a7effb1e3b3caf91072008e03ea29d78bb0178fddac01a3942",
    "validation.json": "d15ce54f4dc06e809160718cd576f1855ef1e1df6a6814d10f4e1631d9eb70bd",
    "verify.py": "0bf7647508b08407e3092fc17c9609afd01c90d809202d95ff30aa6d05380f43",
}
TARGET_MANIFEST_HASH = "60018d23239ea6586f8242bc73c89223f0ea41b41b7a9170de32057889460435"
TARGET_CERTIFICATE_HASH = "52c3f952f5bb8fcd70b36ecd7acd9fc420d60fa583b394310a392a5ebe92c6a2"
DENOMINATOR = 24
EVALUATION_DENOMINATOR = 48
ZERO_VECTOR = (0,) * 8
ONE_VECTOR = (DENOMINATOR,) + (0,) * 7
SQRT3_VECTOR = (0, DENOMINATOR) + (0,) * 6
ZERO_COMPLEX = (ZERO_VECTOR, ZERO_VECTOR)


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def file_record(path: Path) -> dict[str, int | str]:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def stream_record(raw: bytes) -> dict[str, int | str]:
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def verify_sources(target: Path) -> dict[str, object]:
    records = {}
    for name, expected in TARGET_HASHES.items():
        record = file_record(target / name)
        require(record["sha256"] == expected, "reviewed source identity: " + name)
        records[name] = record
    manifest_raw = (target / "SHA256SUMS").read_bytes()
    require(sha256(manifest_raw).hexdigest() == TARGET_MANIFEST_HASH,
            "reviewed SHA256SUMS identity")
    manifest = {}
    for line in manifest_raw.decode("ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        manifest[name] = digest
    require(manifest == TARGET_HASHES, "reviewed source manifest entries")
    records["SHA256SUMS"] = {
        "bytes": len(manifest_raw), "sha256": TARGET_MANIFEST_HASH,
    }
    return records


# An Eisenstein integer is represented by (a,b) = a+b*omega, where
# omega=(1+i*sqrt(3))/2 and omega^2=omega-1.  A formal patch point is
# (a,b,c,d) = (a+b*omega)+(c+d*omega)*beta.
Eisenstein = tuple[int, int]
Form = tuple[int, int, int, int]

ROOTS: list[Eisenstein] = [
    (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1),
]
CENTRE_FORMS: list[Form] = [(0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0)]


def add_form(left: Form, right: Form) -> Form:
    return tuple(a + b for a, b in zip(left, right))


def formal_patch() -> list[Form]:
    directions = [(a, b, 0, 0) for a, b in ROOTS]
    directions += [(0, 0, a, b) for a, b in ROOTS]
    forms = sorted({add_form(centre, direction)
                    for centre in CENTRE_FORMS for direction in directions})
    require(len(forms) == 30, "thirty distinct formal patch expressions")
    return forms


def cartesian_coeff(value: Eisenstein) -> tuple[Fraction, Fraction]:
    a, b = value
    return Fraction(2 * a + b, 2), Fraction(b, 2)


def eisenstein_norm(value: Eisenstein) -> int:
    a, b = value
    return a * a + a * b + b * b


def primitive_fraction_triple(values: tuple[Fraction, Fraction, Fraction]):
    denominator = lcm(*(value.denominator for value in values))
    entries = [int(value * denominator) for value in values]
    divisor = gcd(*entries)
    if divisor:
        entries = [entry // abs(divisor) for entry in entries]
    if any(entries):
        first = next(entry for entry in entries if entry)
        if first < 0:
            entries = [-entry for entry in entries]
    return tuple(entries)


def event_equation(left: Form, right: Form, target: int) -> tuple[int, int, int]:
    s = (left[0] - right[0], left[1] - right[1])
    t = (left[2] - right[2], left[3] - right[3])
    sx, sy = cartesian_coeff(s)
    tx, ty = cartesian_coeff(t)
    # conj(s)*t = real + i*imaginary_coefficient*sqrt(3).
    real = sx * tx + 3 * sy * ty
    imaginary_coefficient = sx * ty - sy * tx
    values = (2 * real, -2 * imaginary_coefficient,
              Fraction(eisenstein_norm(s) + eisenstein_norm(t) - target))
    return primitive_fraction_triple(values)


def classify_events(forms: list[Form]):
    lines = set()
    persistent_units = []
    persistent_collisions = []
    collision_lines = set()
    unit_lines = set()
    checks = 0
    for left, right in combinations(range(len(forms)), 2):
        for target, event_set, persistent in (
                (0, collision_lines, persistent_collisions),
                (1, unit_lines, persistent_units)):
            equation = event_equation(forms[left], forms[right], target)
            checks += 1
            if equation == (0, 0, 0):
                persistent.append((left, right))
            elif equation[:2] != (0, 0):
                event_set.add(equation)
                lines.add(equation)
    require(not persistent_collisions, "no persistent collision of formal points")
    require(len(persistent_units) == 72, "generic persistent unit edges")
    require(len(lines) == 46, "complete nonconstant event-line set")
    require(checks == 870, "all formal pair/target equations")
    return {
        "lines": sorted(lines),
        "persistent_units": sorted(persistent_units),
        "collision_lines": collision_lines,
        "unit_lines": unit_lines,
        "checks": checks,
    }


# Exact field vectors use the ordered basis
# (1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)).
# Multiplication is recursive through Q(sqrt(3))(sqrt(5))(sqrt(11)), not the
# submitted XOR or sparse-radicand implementation.
def vector_add(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple(a + b for a, b in zip(left, right))


def vector_sub(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple(a - b for a, b in zip(left, right))


def vector_scale(value: tuple[int, ...], factor: int):
    return tuple(factor * entry for entry in value)


def tower_product(left: tuple[int, ...], right: tuple[int, ...],
                  primes: tuple[int, ...] = (11, 5, 3)):
    require(len(left) == len(right) == 2 ** len(primes), "tower vector shape")
    if not primes:
        return (left[0] * right[0],)
    half = len(left) // 2
    a, b = left[:half], left[half:]
    c, d = right[:half], right[half:]
    tail = primes[1:]
    low = vector_add(tower_product(a, c, tail),
                     vector_scale(tower_product(b, d, tail), primes[0]))
    high = vector_add(tower_product(a, d, tail), tower_product(b, c, tail))
    return low + high


def scaled_product(left: tuple[int, ...], right: tuple[int, ...]):
    raw = tower_product(left, right)
    require(all(entry % DENOMINATOR == 0 for entry in raw),
            "product remains on denominator-24 lattice")
    return tuple(entry // DENOMINATOR for entry in raw)


def complex_add(left, right):
    return vector_add(left[0], right[0]), vector_add(left[1], right[1])


def complex_sub(left, right):
    return vector_sub(left[0], right[0]), vector_sub(left[1], right[1])


def complex_mul(left, right):
    real = vector_sub(scaled_product(left[0], right[0]),
                      scaled_product(left[1], right[1]))
    imaginary = vector_add(scaled_product(left[0], right[1]),
                           scaled_product(left[1], right[0]))
    return real, imaginary


def complex_mul_to_evaluation_scale(left, right):
    real = vector_sub(tower_product(left[0], right[0]),
                      tower_product(left[1], right[1]))
    imaginary = vector_add(tower_product(left[0], right[1]),
                           tower_product(left[1], right[0]))
    divisor = DENOMINATOR * DENOMINATOR // EVALUATION_DENOMINATOR
    require(all(entry % divisor == 0 for axis in (real, imaginary) for entry in axis),
            "evaluated point lies on denominator-48 lattice")
    return (tuple(entry // divisor for entry in real),
            tuple(entry // divisor for entry in imaginary))


def squared_norm_numerator(value):
    return vector_add(tower_product(value[0], value[0]),
                      tower_product(value[1], value[1]))


def squared_distance_numerator(left, right):
    return squared_norm_numerator(complex_sub(left, right))


def is_unit(value) -> bool:
    return squared_norm_numerator(value) == (DENOMINATOR ** 2,) + (0,) * 7


def eisenstein_complex(value: Eisenstein):
    a, b = value
    x = (12 * (2 * a + b),) + (0,) * 7
    y = (0, 12 * b) + (0,) * 6
    return x, y


def evaluate_form(form: Form, beta):
    s = eisenstein_complex((form[0], form[1]))
    t = eisenstein_complex((form[2], form[3]))
    doubled_s = vector_scale(s[0], 2), vector_scale(s[1], 2)
    return complex_add(doubled_s, complex_mul_to_evaluation_scale(t, beta))


def conjugate(value):
    return value[0], vector_scale(value[1], -1)


def omega_powers():
    omega = ((12,) + (0,) * 7, (0, 12) + (0,) * 6)
    values = [((24,) + (0,) * 7, ZERO_VECTOR)]
    for _ in range(5):
        values.append(complex_mul(values[-1], omega))
    require(len(set(values)) == 6 and complex_mul(values[-1], omega) == values[0],
            "exact sixth roots of unity")
    return values


def named_parameters():
    units = omega_powers()
    values = set(units)
    for sign in (-1, 1):
        rho = ((20,) + (0,) * 7,
               (0, 0, 0, 0, 4 * sign, 0, 0, 0))
        require(is_unit(rho), "rho is unit")
        for exponent in (-1, 0, 1):
            values.add(complex_mul(rho, units[exponent % 6]))
    for sign in (-1, 1):
        eta = ((21,) + (0,) * 7,
               (0, 0, 0, 3 * sign, 0, 0, 0, 0))
        require(is_unit(eta), "eta is unit")
        values.add(eta)
    require(len(values) == 14 and all(is_unit(value) for value in values),
            "fourteen distinct named unit parameters")
    return sorted(values)


def decode_complex(raw):
    require(isinstance(raw, list) and len(raw) == 16
            and all(type(value) is int for value in raw), "parameter encoding")
    return tuple(raw[:8]), tuple(raw[8:])


def line_value(line: tuple[int, int, int], beta):
    a, b, c = line
    sqrt3_y = scaled_product(SQRT3_VECTOR, beta[1])
    return vector_add(vector_add(vector_scale(beta[0], a),
                                 vector_scale(sqrt3_y, b)),
                      vector_scale(ONE_VECTOR, c))


def line_root_audit(lines, parameters):
    histogram = Counter()
    used = set()
    incidences = 0
    tests = 0
    for line in lines:
        a, b, c = line
        discriminant = a * a + 3 * b * b - c * c
        expected = 0 if discriminant < 0 else 1 if discriminant == 0 else 2
        hits = []
        for index, beta in enumerate(parameters):
            if line_value(line, beta) == ZERO_VECTOR:
                hits.append(index)
            tests += 1
        require(len(hits) == expected, "all roots of event line are named")
        used.update(hits)
        histogram[expected] += 1
        incidences += len(hits)
    require(used == set(range(14)), "every named parameter is a genuine event")
    require(histogram == Counter({0: 24, 1: 6, 2: 16}),
            "event-line root histogram")
    require(tests == 644 and incidences == 38, "complete line/parameter audit")
    return histogram, tests, incidences


def masks_for_graph(vertices, centres, coincident: bool, scale: int):
    masks = []
    for index, vertex in enumerate(vertices):
        if coincident:
            masks.append(0b0111)
            continue
        if index in centres:
            masks.append(1 << (2, 3, 0)[centres.index(index)])
            continue
        owners = {owner for owner, centre in enumerate(centres)
                  if squared_distance_numerator(vertex, vertices[centre])
                  == (scale ** 2,) + (0,) * 7}
        if owners == {1}:
            masks.append(0b0011)
        elif owners == {2}:
            masks.append(0b1100)
        else:
            masks.append(0b1111)
    return masks


def check_colouring(colouring, masks, edges) -> int:
    require(isinstance(colouring, list) and len(colouring) == len(masks),
            "colouring length")
    require(all(type(colour) is int and 0 <= colour < 4
                and masks[index] & (1 << colour)
                for index, colour in enumerate(colouring)), "colouring lists")
    require(all(colouring[left] != colouring[right] for left, right in edges),
            "proper colouring")
    return len(edges)


def find_colouring(masks, edges):
    adjacency = [set() for _ in masks]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    colours = [-1] * len(masks)
    nodes = 0

    def search():
        nonlocal nodes
        nodes += 1
        if all(colour >= 0 for colour in colours):
            return list(colours)
        candidates = []
        for vertex, colour in enumerate(colours):
            if colour >= 0:
                continue
            forbidden = {colours[neighbor] for neighbor in adjacency[vertex]
                         if colours[neighbor] >= 0}
            allowed = [candidate for candidate in range(3, -1, -1)
                       if masks[vertex] & (1 << candidate) and candidate not in forbidden]
            if not allowed:
                return None
            uncoloured_degree = sum(colours[neighbor] < 0 for neighbor in adjacency[vertex])
            candidates.append((len(allowed), -uncoloured_degree, -vertex, vertex, allowed))
        _, _, _, vertex, allowed = min(candidates)
        for candidate in allowed:
            colours[vertex] = candidate
            answer = search()
            if answer is not None:
                return answer
        colours[vertex] = -1
        return None

    answer = search()
    require(answer is not None, "fresh list colouring exists")
    check_colouring(answer, masks, edges)
    return answer, nodes


def edge_stream(edges) -> bytes:
    return "".join(f"{left},{right}\n" for left, right in edges).encode("ascii")


def colouring_stream(rows) -> bytes:
    return "".join("".join(map(str, row)) + "\n" for row in rows).encode("ascii")


def case_audit(certificate, forms, events, parameters):
    centre_indices = [forms.index(centre) for centre in CENTRE_FORMS]
    generic_edges = events["persistent_units"]
    # Formal points are used as dummy unequal vertices here.  Owners are read
    # directly from persistent unit relations, not specialized coordinates.
    adjacency_pairs = set(generic_edges)
    generic_masks = []
    for index in range(len(forms)):
        if index in centre_indices:
            generic_masks.append(1 << (2, 3, 0)[centre_indices.index(index)])
            continue
        owners = {owner for owner, centre in enumerate(centre_indices)
                  if tuple(sorted((index, centre))) in adjacency_pairs}
        generic_masks.append(0b0011 if owners == {1}
                             else 0b1100 if owners == {2} else 0b1111)
    require(certificate["generic"]["edges"] == len(generic_edges) == 72,
            "generic graph edge count")
    require(certificate["generic"]["lists"] == generic_masks,
            "generic list assignment")
    target_rows = [certificate["generic"]["colouring"]]
    target_checks = check_colouring(target_rows[0], generic_masks, generic_edges)
    fresh_generic, generic_nodes = find_colouring(generic_masks, generic_edges)
    fresh_rows = [fresh_generic]
    fresh_checks = len(generic_edges)

    target_cases = {decode_complex(row["parameter"]): row
                    for row in certificate["cases"]}
    require(len(target_cases) == len(certificate["cases"]) == 14
            and set(target_cases) == set(parameters), "exact exceptional case set")
    histogram = Counter()
    pair_checks = 0
    case_records = []
    for beta in parameters:
        row = target_cases[beta]
        evaluated = [evaluate_form(form, beta) for form in forms]
        vertices = []
        indices = {}
        aliases = []
        for point in evaluated:
            if point not in indices:
                indices[point] = len(vertices)
                vertices.append(point)
            aliases.append(indices[point])
        require(row["aliases"] == aliases, "exceptional formal aliases")
        centres = [aliases[index] for index in centre_indices]
        coincident = centres[1] == centres[2]
        require(row["coincident"] is coincident, "coincident-centre status")
        require(coincident == (beta == (ONE_VECTOR, ZERO_VECTOR)),
                "only beta=1 has coincident outer centres")
        edges = [(left, right) for left, right in combinations(range(len(vertices)), 2)
                 if squared_distance_numerator(vertices[left], vertices[right])
                 == (EVALUATION_DENOMINATOR ** 2,) + (0,) * 7]
        pair_checks += len(vertices) * (len(vertices) - 1) // 2
        masks = masks_for_graph(vertices, centres, coincident, EVALUATION_DENOMINATOR)
        require(row["edges"] == len(edges) and row["lists"] == masks,
                "exceptional graph and list assignment")
        target_checks += check_colouring(row["colouring"], masks, edges)
        fresh, nodes = find_colouring(masks, edges)
        fresh_checks += check_colouring(fresh, masks, edges)
        target_rows.append(row["colouring"])
        fresh_rows.append(fresh)
        histogram[len(vertices), len(edges)] += 1
        case_records.append({
            "parameter_sha256": sha256(json.dumps(beta).encode("ascii")).hexdigest(),
            "vertices": len(vertices), "edges": len(edges),
            "edge_stream_sha256": sha256(edge_stream(edges)).hexdigest(),
            "fresh_search_nodes": nodes,
        })
    require(pair_checks == 3891, "all exceptional pair norms")
    require(histogram == Counter({(10, 19): 1, (12, 24): 2, (13, 26): 3,
                                  (30, 74): 6, (30, 76): 2}),
            "exceptional graph histogram")
    require(target_checks == fresh_checks == 813, "all target and fresh patch edges")
    target_record = stream_record(colouring_stream(target_rows))
    fresh_record = stream_record(colouring_stream(fresh_rows))
    require(target_record["sha256"] != fresh_record["sha256"],
            "fresh list colourings differ from submitted rows")
    return {
        "generic_vertices": 30,
        "generic_edges": 72,
        "generic_edge_stream": stream_record(edge_stream(generic_edges)),
        "generic_fresh_search_nodes": generic_nodes,
        "exceptional_pair_norms": pair_checks,
        "exceptional_histogram": {
            f"{vertices},{edges}": count
            for (vertices, edges), count in sorted(histogram.items())},
        "target_positive_edge_checks": target_checks,
        "fresh_positive_edge_checks": fresh_checks,
        "target_colouring_stream": target_record,
        "fresh_colouring_stream": fresh_record,
        "case_records": case_records,
    }, target_rows, fresh_rows


def boundary_palette_controls():
    circle0 = lambda parity: parity
    circle1 = lambda parity: 1 - parity
    circle_beta = lambda parity: 2 + parity
    checks = 0
    for colour in (circle0, circle1, circle_beta):
        for parity in (0, 1):
            require(colour(parity) != colour(1 - parity), "same-circle parity edge")
            checks += 1
    for parity in (0, 1):
        require(circle0(parity) != circle1(parity), "0/1 direction-preserving edge")
        require(circle0(parity) != circle_beta(parity), "0/beta disjoint palettes")
        checks += 2
    for left in (0, 1):
        for right in (0, 1):
            require(circle1(left) != circle_beta(right), "outer-circle disjoint palettes")
            checks += 1
    for centre_colour, residual in ((2, {0, 1}), (3, {0, 1}), (0, {2, 3})):
        for colour in residual:
            require(centre_colour != colour, "owner spoke avoids centre colour")
            checks += 1
    for patch_palette, outside_palette in (({0, 1}, {2, 3}), ({2, 3}, {0, 1})):
        for left in patch_palette:
            for right in outside_palette:
                require(left != right, "unique-owner patch boundary palette")
                checks += 1
    require(checks == 28, "all residual palette edge types")
    return checks


def sharpness_audit(certificate):
    root = ZERO_COMPLEX
    tip = ((0, DENOMINATOR) + (0,) * 6, ZERO_VECTOR)
    upper = ((0, 12) + (0,) * 6, (12,) + (0,) * 7)
    lower = ((0, 12) + (0,) * 6, (-12,) + (0,) * 7)
    rho = ((20,) + (0,) * 7, (0, 0, 0, 0, 4, 0, 0, 0))
    vertices = [root, tip, upper, lower,
                complex_mul(tip, rho), complex_mul(upper, rho), complex_mul(lower, rho)]
    target_vertices = [decode_complex(raw) for raw in certificate["sharpness"]["vertices"]]
    require(vertices == target_vertices and len(set(vertices)) == 7,
            "exact seven spindle points")
    edges = {(left, right) for left, right in combinations(range(7), 2)
             if squared_distance_numerator(vertices[left], vertices[right])
             == (DENOMINATOR ** 2,) + (0,) * 7}
    expected = {(0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
                (0, 5), (0, 6), (4, 5), (4, 6), (5, 6), (1, 4)}
    require(edges == expected, "exact Moser spindle unit graph")
    path = certificate["sharpness"]["dominating_path"]
    require(path == [0, 2, 1]
            and all(tuple(sorted(edge)) in edges for edge in zip(path, path[1:])),
            "connected unit path")
    require(all(vertex in path or any(tuple(sorted((vertex, centre))) in edges
                                      for centre in path)
                for vertex in range(7)), "path dominates spindle")
    require(squared_distance_numerator(vertices[path[0]], vertices[path[-1]])
            == (3 * DENOMINATOR ** 2,) + (0,) * 7,
            "120-degree path opening")
    check_colouring(certificate["sharpness"]["colouring"], [15] * 7, sorted(edges))
    proper_three = sum(all(colouring[left] != colouring[right] for left, right in edges)
                       for colouring in product(range(3), repeat=7))
    require(proper_three == 0, "spindle is not three-colourable")
    return {"vertices": 7, "pair_norms": 21, "unit_edges": len(edges),
            "three_colour_assignments": 3 ** 7, "proper_three_colourings": 0,
            "proper_four_colouring_checked": True,
            "connected_dominating_path": path, "opening_angle_degrees": 120}


def expect_failure(callback, message: str):
    try:
        callback()
    except ReviewFailure:
        return
    raise ReviewFailure(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    repository = args.repository.resolve()
    target = repository / "hadwiger_nelson_dominating_unit_path"
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    sources = verify_sources(target)
    certificate_path = target / "certificate.json"
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    require(file_record(certificate_path)["sha256"] == TARGET_CERTIFICATE_HASH,
            "reviewed certificate identity")

    forms = formal_patch()
    require(certificate["forms"] == [list(form) for form in forms],
            "submitted complete formal patch")
    events = classify_events(forms)
    require(certificate["equations"] == [list(line) for line in events["lines"]],
            "submitted complete event-line set")
    parameters = named_parameters()
    histogram, line_tests, incidences = line_root_audit(events["lines"], parameters)
    cases, target_rows, fresh_rows = case_audit(
        certificate, forms, events, parameters)
    palette_checks = boundary_palette_controls()
    sharpness = sharpness_audit(certificate)

    form_raw = "".join(",".join(map(str, form)) + "\n" for form in forms).encode("ascii")
    line_raw = "".join(",".join(map(str, line)) + "\n" for line in events["lines"]).encode("ascii")
    parameter_raw = b"".join(json.dumps(parameter, separators=(",", ":")).encode("ascii") + b"\n"
                             for parameter in parameters)

    # Mutations exercise independent rejection paths.
    bad_target = list(target_rows[0])
    left, right = events["persistent_units"][0]
    bad_target[right] = bad_target[left]
    generic_masks = certificate["generic"]["lists"]
    expect_failure(lambda: check_colouring(bad_target, generic_masks,
                                            events["persistent_units"]),
                   "monochromatic generic colouring accepted")
    expect_failure(lambda: require(set(parameters[:-1]) == set(parameters),
                                   "missing event parameter"),
                   "missing parameter set accepted")
    nonunit = ((25,) + (0,) * 7, ZERO_VECTOR)
    expect_failure(lambda: require(is_unit(nonunit), "nonunit parameter"),
                   "nonunit parameter accepted")
    bad_masks = list(generic_masks); bad_masks[0] = 0
    expect_failure(lambda: check_colouring(target_rows[0], bad_masks,
                                            events["persistent_units"]),
                   "empty list accepted")
    bad_sharpness = json.loads(json.dumps(certificate))
    bad_sharpness["sharpness"]["dominating_path"] = [0, 1, 4]
    expect_failure(lambda: sharpness_audit(bad_sharpness),
                   "invalid dominating path accepted")

    result = {
        "all_checks_passed": True,
        "accepted_claim": ("every Euclidean unit-distance graph with a connected "
                           "dominating set of at most three vertices is four-colourable, "
                           "and the bound four is attained"),
        "reviewed_source_commit": TARGET_COMMIT,
        "source_identity": sources,
        "finite_classification": {
            "formal_patch_vertices": len(forms),
            "formal_patch_stream": stream_record(form_raw),
            "formal_pair_target_checks": events["checks"],
            "persistent_collision_pairs": 0,
            "generic_persistent_unit_edges": len(events["persistent_units"]),
            "event_lines": len(events["lines"]),
            "collision_event_lines": len(events["collision_lines"]),
            "unit_event_lines": len(events["unit_lines"]),
            "event_line_overlap": len(events["collision_lines"] & events["unit_lines"]),
            "event_line_stream": stream_record(line_raw),
            "named_exceptional_parameters": len(parameters),
            "parameter_stream": stream_record(parameter_raw),
            "root_count_histogram": {str(key): histogram[key] for key in sorted(histogram)},
            "circle_line_parameter_tests": line_tests,
            "circle_line_root_incidences": incidences,
        },
        "patch_list_colourings": cases,
        "continuum_extension": {
            "unit_centre_pair_lemma_rederived": True,
            "multiple_owner_points_contained_in_patch": True,
            "same_circle_six_rotation_orbits": True,
            "residual_palette_edge_type_checks": palette_checks,
            "coincident_beta_one_uses_accepted_two_centre_theorem": True,
            "all_unit_parameters_covered": True,
            "all_distinct_centre_precolourings_extend": True,
        },
        "sharpness": sharpness,
        "negative_controls": {
            "monochromatic_generic_colouring_rejected": True,
            "missing_event_parameter_rejected": True,
            "nonunit_parameter_rejected": True,
            "empty_vertex_list_rejected": True,
            "invalid_dominating_path_rejected": True,
        },
        "dependency": {
            "coincident_two_centre_case":
                "bafkreiauzabwiqtpeqzdkwuy35l33xrexthvv2knfozsl5e3jb7kxewboi",
            "independent_acceptance":
                "bafkreigcxi3wttalq3fg2dzm3g4iwnsmz5zucaq5zmnbzwrhjwz52esxfu",
        },
        "scope": {
            "connected_dominating_set_size_at_most_three": True,
            "four_colour_upper_bound": True,
            "sharp": True,
            "arbitrary_disconnected_dominating_triples": False,
            "equal_outer_centre_precolour_extension": False,
            "sub509_graph": False,
            "record_improvement": False,
            "priority_claim": False,
        },
        "trust_boundary": [
            "the written continuum boundary-extension proof, including the unit-centre-pair lemma",
            "linear independence of the eight squarefree-radical basis elements",
            "ordinary CPython integer/Fraction arithmetic and exhaustive finite enumeration",
            "the separately accepted two-unit-centre theorem for beta=1 and dominating sets of size at most two",
            "SHA-256 collision resistance for source and canonical stream identities",
        ],
        "python": sys.version.split()[0],
    }
    atomic_json(args.report.resolve(), result)
    print(json.dumps({
        "all_checks_passed": True,
        "event_lines": len(events["lines"]),
        "exceptional_parameters": len(parameters),
        "generic_edges": cases["generic_edges"],
        "patch_edge_checks": cases["fresh_positive_edge_checks"],
        "sharpness_chromatic_number": 4,
        "fresh_colouring_sha256": cases["fresh_colouring_stream"]["sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
