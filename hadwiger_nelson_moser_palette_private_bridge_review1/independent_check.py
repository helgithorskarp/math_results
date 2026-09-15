#!/usr/bin/env python3
"""Independent exact review of the 19-point Moser/palette bridge.

This program imports no code from the reviewed package.  Geometry is rebuilt
from the displayed radical formulas in SymPy's algebraic-number field.  The
terminal relation is obtained by enumerating canonical proper colourings of
the whole inherited-edge graph, recording which of the four physical cross
contacts each colouring satisfies, and then evaluating every contact subset.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from sympy import QQ, Rational, sqrt


HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE.parent / "hadwiger_nelson_moser_palette_private_bridge"
CONTACTS = ((0, 11), (1, 16), (2, 15), (3, 12))
CONTACT_NAMES = ("M0-P1", "M1-Y1", "M2-X1", "M3-P2")
TERMINALS = (7, 8, 9, 10, 13, 14, 15, 16, 17, 18)


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def json_digest(value) -> str:
    raw = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(word) -> tuple[int, ...]:
    names = {}
    return tuple(names.setdefault(colour, len(names)) for colour in word)


def rgs_words(length: int, colours: int = 4):
    """Restricted-growth strings: one representative of each colour orbit."""

    word = [0] * length

    def rec(pos: int, high: int):
        if pos == length:
            yield tuple(word)
            return
        for colour in range(min(high + 1, colours - 1) + 1):
            word[pos] = colour
            yield from rec(pos + 1, max(high, colour))

    yield from rec(0, -1)


def orbit_weight(word: tuple[int, ...], colours: int = 4) -> int:
    used = max(word, default=-1) + 1
    return math.factorial(colours) // math.factorial(colours - used)


def point_add(p, q):
    return p[0] + q[0], p[1] + q[1]


def point_sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def point_scale(p, q):
    return p[0] * q, p[1] * q


def complex_mul(p, q):
    return p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0]


def squared_norm(p):
    return p[0] * p[0] + p[1] * p[1]


def exact_geometry(certificate: dict) -> tuple[list, list[tuple[int, int]], list[tuple[int, int]]]:
    """Reconstruct formulas and compare the certificate only afterwards."""

    field = QQ.algebraic_field(sqrt(3), sqrt(11), sqrt((4 - sqrt(3)) / 2))
    need(field.ext.minpoly.degree() == 8, "the displayed field is not degree eight")
    zero = field.zero
    one = field.one
    s = field.from_sympy(sqrt(3))
    t = field.from_sympy(sqrt(11))
    y = field.from_sympy(sqrt((4 - sqrt(3)) / 2))
    two = field.convert(2)
    six = field.convert(6)
    need(s * s == field.convert(3), "sqrt(3) relation")
    need(t * t == field.convert(11), "sqrt(11) relation")
    need(y * y == (field.convert(4) - s) / two, "y relation")

    rho = ((one + zero) / two, s / two)
    tau = (field.convert(5) / six, t / six)
    z = (zero, zero)
    one_point = (one, zero)
    moser = [
        z,
        one_point,
        rho,
        point_add(one_point, rho),
        tau,
        complex_mul(tau, rho),
        complex_mul(tau, point_add(one_point, rho)),
        (rho[0], -rho[1]),
        point_scale(rho, two),
        point_scale(tau, two),
        complex_mul(tau, (rho[0] - one, rho[1])),
    ]

    p0 = z
    p1 = ((one + s) / two, y)
    p2 = ((one - s) / two, y)
    p3 = one_point
    caps = (p0, p1, p2, p3)
    palette = [p1, p2]
    for left, right in zip(caps, caps[1:]):
        delta = point_sub(right, left)
        midpoint = point_scale(point_add(left, right), one / two)
        # 1/(2 sqrt(3)) = sqrt(3)/6.
        offset = (-delta[1] * s / six, delta[0] * s / six)
        palette.extend((point_add(midpoint, offset), point_sub(midpoint, offset)))

    multiplier = (-s / two, -one / two)
    translation = (zero, one)
    moved = [point_add(translation, complex_mul(multiplier, point_sub(p, p1))) for p in palette]
    points = moser + moved

    rows = certificate["coordinates"]
    need(len(rows) == len(points) == 19, "coordinate count")
    basis = (one, s, t, s * t, y, s * y, t * y, s * t * y)
    parsed = []
    for row in rows:
        need(len(row) == 2 and all(len(axis) == 8 for axis in row), "coordinate row shape")
        axes = []
        for axis in row:
            value = zero
            for coefficient, basis_element in zip(axis, basis):
                value += field.from_sympy(Rational(coefficient)) * basis_element
            axes.append(value)
        parsed.append(tuple(axes))
    need(parsed == points, "certificate coordinates do not equal the displayed formulas")
    need(all(points[a] != points[b] for a, b in combinations(range(19), 2)), "point collision")

    distances = {}
    edges = []
    for a, b in combinations(range(19), 2):
        distance = squared_norm(point_sub(points[a], points[b]))
        distances[(a, b)] = distance
        if distance == one:
            edges.append((a, b))
    inherited = [edge for edge in edges if (edge[0] < 11) == (edge[1] < 11)]
    cross = [edge for edge in edges if edge not in inherited]
    need(len(distances) == 171, "all-pairs count")
    need(edges == [tuple(edge) for edge in certificate["edges"]], "complete edge-list mismatch")
    need(inherited == [tuple(edge) for edge in certificate["inherited_edges"]], "inherited edge-list mismatch")
    need(cross == list(CONTACTS), "cross-contact mismatch")
    need(len(edges) == 34 and len(inherited) == 30, "edge counts")
    need(len([edge for edge in inherited if edge[1] < 11]) == 19, "Moser edge count")
    need(len([edge for edge in inherited if edge[0] >= 11]) == 11, "palette edge count")
    return points, edges, inherited


def enumerate_canonical_colourings(
    vertex_count: int,
    edges: list[tuple[int, int]],
    colours: int,
    on_word,
) -> int:
    """Enumerate proper set partitions in vertex order, without a SAT solver."""

    earlier = [[] for _ in range(vertex_count)]
    for a, b in edges:
        need(a < b, "edges must be sorted")
        earlier[b].append(a)
    word = [-1] * vertex_count
    count = 0

    def rec(vertex: int, high: int) -> None:
        nonlocal count
        if vertex == vertex_count:
            count += 1
            on_word(word)
            return
        limit = min(high + 1, colours - 1)
        for colour in range(limit + 1):
            if all(word[neighbour] != colour for neighbour in earlier[vertex]):
                word[vertex] = colour
                rec(vertex + 1, max(high, colour))
        word[vertex] = -1

    rec(0, -1)
    return count


def contact_profile(inherited: list[tuple[int, int]]):
    pattern_masks: dict[tuple[int, ...], int] = defaultdict(int)

    def record(word) -> None:
        terminal_word = canonical(tuple(word[v] for v in TERMINALS))
        satisfied = 0
        for bit, (a, b) in enumerate(CONTACTS):
            if word[a] != word[b]:
                satisfied |= 1 << bit
        pattern_masks[terminal_word] |= 1 << satisfied

    canonical_full_colourings = enumerate_canonical_colourings(19, inherited, 4, record)
    supersets = [
        sum(1 << mask for mask in range(16) if mask & required == required)
        for required in range(16)
    ]
    relations = {
        required: {
            word for word, available in pattern_masks.items() if available & supersets[required]
        }
        for required in range(16)
    }
    rows = []
    baseline = relations[0]
    for required in range(16):
        relation = relations[required]
        named = sum(orbit_weight(word) for word in relation)
        rows.append(
            {
                "mask": required,
                "contacts": [CONTACT_NAMES[i] for i in range(4) if required & (1 << i)],
                "canonical": len(relation),
                "named": named,
                "gain_from_baseline_canonical": len(baseline) - len(relation),
                "gain_from_baseline_named": sum(orbit_weight(word) for word in baseline) - named,
            }
        )
    return canonical_full_colourings, relations, rows


def direct_relation(edges: list[tuple[int, int]], colours: int = 4):
    relation = set()

    def record(word) -> None:
        relation.add(canonical(tuple(word[v] for v in TERMINALS)))

    count = enumerate_canonical_colourings(19, edges, colours, record)
    return count, relation


def formula_baseline(all_patterns: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    result = set()
    for word in all_patterns:
        moser_ok = word[0] != word[1] or word[2] != word[3]
        edge_palettes = tuple(frozenset(word[i : i + 2]) for i in (4, 6, 8))
        palette_ok = all(len(palette) == 2 for palette in edge_palettes)
        palette_ok &= bool(edge_palettes[0] & edge_palettes[1])
        palette_ok &= bool(edge_palettes[1] & edge_palettes[2])
        if moser_ok and palette_ok:
            result.add(word)
    return result


def find_named_extension(edges: list[tuple[int, int]], pins: dict[int, int]):
    adjacency = [set() for _ in range(19)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    word = [-1] * 19
    for vertex, colour in pins.items():
        word[vertex] = colour
    if any(word[a] >= 0 and word[a] == word[b] for a, b in edges):
        return None

    def rec() -> tuple[int, ...] | None:
        free = [v for v in range(19) if word[v] < 0]
        if not free:
            return tuple(word)
        domains = {
            v: tuple(c for c in range(4) if all(word[u] != c for u in adjacency[v]))
            for v in free
        }
        vertex = min(free, key=lambda v: (len(domains[v]), -len(adjacency[v]), v))
        for colour in domains[vertex]:
            word[vertex] = colour
            answer = rec()
            if answer is not None:
                return answer
        word[vertex] = -1
        return None

    return rec()


def check_colour_word(word, colours: int, edges: list[tuple[int, int]]) -> None:
    need(len(word) == 19, "colour-word length")
    need(all(type(c) is int and 0 <= c < colours for c in word), "colour-word range")
    need(all(word[a] != word[b] for a, b in edges), "improper colour word")


def review(source_dir: Path) -> dict:
    certificate_path = source_dir / "certificate.json"
    certificate = json.loads(certificate_path.read_text())
    need(certificate["schema"] == "moser-palette-private-bridge-v1", "certificate schema")
    points, edges, inherited = exact_geometry(certificate)
    need(tuple(certificate["terminals"]) == TERMINALS, "terminal order")

    baseline_colourings, relations, subset_rows = contact_profile(inherited)
    all_patterns = list(rgs_words(10, 4))
    need(len(all_patterns) == 43947, "ten-terminal partition count")
    need(relations[0] == formula_baseline(all_patterns), "isolated-source formula mismatch")
    full_colourings, direct_full = direct_relation(edges, 4)
    need(direct_full == relations[15], "direct full-graph relation disagrees with contact profile")
    three_colourings, _ = direct_relation(edges, 3)
    need(three_colourings == 0, "unexpected three-colouring")

    baseline = relations[0]
    full = relations[15]
    baseline_named = sum(orbit_weight(word) for word in baseline)
    full_named = sum(orbit_weight(word) for word in full)
    gains = sorted("".join(map(str, word)) for word in baseline - full)
    stream = hashlib.sha256()
    for word in all_patterns:
        text = "".join(map(str, word))
        stream.update(f"{text}:{int(word in baseline)}{int(word in full)}\n".encode())
    moser_projection = {canonical(word[:4]) for word in full}
    palette_projection = {canonical(word[4:]) for word in full}

    relation_result = {
        "all_canonical_patterns": len(all_patterns),
        "baseline_canonical": len(baseline),
        "baseline_named": baseline_named,
        "full_canonical": len(full),
        "full_named": full_named,
        "gain_canonical": len(baseline) - len(full),
        "gain_named": baseline_named - full_named,
        "full_moser_projection_canonical": len(moser_projection),
        "full_palette_projection_canonical": len(palette_projection),
        "canonical_truth_stream_sha256": stream.hexdigest(),
        "gain_words_sha256": json_digest(gains),
    }
    need(relation_result == certificate["relation"], "certificate relation mismatch")

    expected_word = (0, 0, 1, 2, 2, 3, 0, 2, 0, 1)
    need(tuple(certificate["newly_forbidden_terminal_word"]) == expected_word, "forbidden word")
    pins = dict(zip(TERMINALS, expected_word))
    baseline_extension = find_named_extension(inherited, pins)
    full_extension = find_named_extension(edges, pins)
    need(baseline_extension is not None and full_extension is None, "pinned gain witness")
    check_colour_word(certificate["isolated_extension"], 4, inherited)
    need(tuple(certificate["isolated_extension"][v] for v in TERMINALS) == expected_word, "submitted baseline pins")
    check_colour_word(certificate["four_colouring"], 4, edges)
    check_colour_word(certificate["five_colouring"], 5, edges)
    need(set(certificate["five_colouring"]) == set(range(5)), "five-colour witness does not use all colours")

    # Structural audit of the two-contact contradiction.
    diamond = {(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)}
    diamond_words = [
        word
        for word in rgs_words(4, 3)
        if all(word[a] != word[b] for a, b in diamond)
    ]
    need(diamond_words and all(word[0] == word[3] for word in diamond_words), "diamond equality")
    need(set(range(4)) - set(expected_word[4:8]) == {1}, "P1 forced colour")
    need(set(range(4)) - set(expected_word[6:10]) == {3}, "P2 forced colour")

    # Every actual cross contact should make an individually detectable
    # contribution after the other three are imposed.
    relation_without = {}
    for bit, name in enumerate(CONTACT_NAMES):
        relation_without[name] = {
            "canonical_restored": len(relations[15 ^ (1 << bit)]) - len(full),
            "named_restored": sum(orbit_weight(w) for w in relations[15 ^ (1 << bit)]) - full_named,
        }
    need(all(row["canonical_restored"] > 0 for row in relation_without.values()), "redundant cross contact")

    prescribed_gain = baseline - relations[9]  # M0--P1 and M3--P2.
    incidental_gain = baseline - relations[6]  # M1--Y1 and M2--X1.
    need(not (prescribed_gain & incidental_gain), "pair gains unexpectedly overlap")
    need(prescribed_gain | incidental_gain == baseline - full, "pair gains do not decompose full gain")
    pair_decomposition = {
        "prescribed_pair": {
            "mask": 9,
            "gain_canonical": len(prescribed_gain),
            "gain_named": sum(orbit_weight(word) for word in prescribed_gain),
        },
        "incidental_pair": {
            "mask": 6,
            "gain_canonical": len(incidental_gain),
            "gain_named": sum(orbit_weight(word) for word in incidental_gain),
        },
        "gain_sets_disjoint_and_exhaust_full_gain": True,
    }

    source_expected = json.loads((source_dir / "expected.json").read_text())
    need(source_expected["relation"] == relation_result, "source expected relation mismatch")
    return {
        "status": "ACCEPTED_INDEPENDENTLY",
        "reviewed_source_commit": "2e26eadaa928d089c86462f567e3e29dfa9f0511",
        "source_certificate_sha256": file_digest(certificate_path),
        "geometry": {
            "field_degree": 8,
            "points": len(points),
            "all_pairs_checked": 171,
            "strict_unit_edges": len(edges),
            "inherited_edges": len(inherited),
            "cross_edges": [list(edge) for edge in CONTACTS],
            "coordinate_sha256": json_digest(certificate["coordinates"]),
            "edge_sha256": json_digest(certificate["edges"]),
        },
        "colouring": {
            "chromatic_number": 4,
            "canonical_baseline_full_colourings": baseline_colourings,
            "canonical_complete_full_colourings": full_colourings,
            "canonical_three_colourings": three_colourings,
            "proper_four_witness_checked": True,
            "proper_all_five_witness_checked": True,
        },
        "relation": relation_result,
        "contact_subset_census": subset_rows,
        "leave_one_contact_out": relation_without,
        "contact_pair_decomposition": pair_decomposition,
        "explicit_gain_witness": {
            "terminal_word": list(expected_word),
            "independent_baseline_extension": list(baseline_extension),
            "complete_extension_exists": False,
            "two_contact_structural_contradiction_checked": True,
        },
        "scope": {
            "ordinary_nonfour_signal": False,
            "record_candidate": False,
            "marginal_source_relations_unchanged": True,
            "single_frozen_frame_only": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = review(args.source_dir.resolve())
    if args.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "review expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
