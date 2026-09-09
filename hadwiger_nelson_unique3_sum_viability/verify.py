#!/usr/bin/env python3
"""Exact checker for the unique-three-colour rotational-sum interface."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class VerificationError(Exception):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def parse_edges(n: int, raw: object, name: str) -> set[tuple[int, int]]:
    need(type(n) is int and n >= 1, f"{name}: bad order")
    need(type(raw) is list, f"{name}: edges are not a list")
    edges: set[tuple[int, int]] = set()
    for item in raw:
        need(
            type(item) is list
            and len(item) == 2
            and all(type(x) is int for x in item),
            f"{name}: malformed edge",
        )
        a, b = item
        need(0 <= a < n and 0 <= b < n and a != b, f"{name}: bad edge endpoint")
        edge = tuple(sorted((a, b)))
        need(edge not in edges, f"{name}: duplicate edge")
        edges.add(edge)
    return edges


def adjacency(n: int, edges: set[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def connected(n: int, edges: set[tuple[int, int]]) -> bool:
    adj = adjacency(n, edges)
    seen = {0}
    queue = [0]
    for v in queue:
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                queue.append(w)
    return len(seen) == n


def enumerate_colourings(
    n: int,
    edges: set[tuple[int, int]],
    colours: int,
    fixed: dict[int, int] | None = None,
    limit: int | None = None,
) -> tuple[list[tuple[int, ...]], int]:
    adj = adjacency(n, edges)
    word = [-1] * n
    fixed = {} if fixed is None else dict(fixed)
    for v, colour in fixed.items():
        need(type(v) is int and 0 <= v < n, "bad fixed vertex")
        need(type(colour) is int and 0 <= colour < colours, "bad fixed colour")
        word[v] = colour
    for a, b in edges:
        need(word[a] < 0 or word[b] < 0 or word[a] != word[b], "improper fixed colours")

    answers: list[tuple[int, ...]] = []
    nodes = 0

    def visit() -> None:
        nonlocal nodes
        if limit is not None and len(answers) >= limit:
            return
        nodes += 1
        unassigned = [v for v in range(n) if word[v] < 0]
        if not unassigned:
            answers.append(tuple(word))
            return
        vertex = max(
            unassigned,
            key=lambda v: (
                len({word[w] for w in adj[v] if word[w] >= 0}),
                len(adj[v]),
                -v,
            ),
        )
        forbidden = {word[w] for w in adj[vertex] if word[w] >= 0}
        for colour in range(colours):
            if colour not in forbidden:
                word[vertex] = colour
                visit()
                word[vertex] = -1

    visit()
    return answers, nodes


def verify_factor(raw: object, name: str) -> dict[str, object]:
    need(type(raw) is dict, f"{name}: factor is not an object")
    n = raw.get("vertices")
    need(type(n) is int, f"{name}: bad order")
    edges = parse_edges(n, raw.get("edges"), name)
    need(connected(n, edges), f"{name}: factor is disconnected")
    colour = raw.get("colouring")
    need(
        type(colour) is list
        and len(colour) == n
        and all(type(x) is int and 0 <= x < 3 for x in colour),
        f"{name}: bad named colouring",
    )
    need(set(colour) == {0, 1, 2}, f"{name}: named colouring is not surjective")
    need(all(colour[a] != colour[b] for a, b in edges), f"{name}: improper named colouring")
    triangle = raw.get("palette_triangle")
    need(
        type(triangle) is list
        and len(triangle) == 3
        and len(set(triangle)) == 3
        and all(type(v) is int and 0 <= v < n for v in triangle),
        f"{name}: bad palette triangle",
    )
    need(
        all(tuple(sorted(edge)) in edges for edge in itertools.combinations(triangle, 2)),
        f"{name}: palette anchor is not a triangle",
    )
    need({colour[v] for v in triangle} == {0, 1, 2}, f"{name}: triangle palette")
    fixed = {v: colour[v] for v in triangle}
    anchored, nodes = enumerate_colourings(n, edges, 3, fixed, limit=2)
    need(anchored == [tuple(colour)], f"{name}: factor is not uniquely 3-colourable")
    return {
        "name": raw.get("name", name),
        "n": n,
        "edges": edges,
        "colour": tuple(colour),
        "triangle": tuple(triangle),
        "uniqueness_nodes": nodes,
    }


def product_edges(left: dict[str, object], right: dict[str, object]) -> set[tuple[int, int]]:
    n = int(left["n"])
    m = int(right["n"])
    result: set[tuple[int, int]] = set()
    for a, b in left["edges"]:  # type: ignore[union-attr]
        for y in range(m):
            result.add(tuple(sorted((a * m + y, b * m + y))))
    for c, d in right["edges"]:  # type: ignore[union-attr]
        for x in range(n):
            result.add(tuple(sorted((x * m + c, x * m + d))))
    return result


def pattern_word(
    left: dict[str, object], right: dict[str, object], sign: int
) -> tuple[int, ...]:
    need(sign in (-1, 1), "bad sign")
    return tuple(
        (a + sign * b) % 3
        for a in left["colour"]  # type: ignore[union-attr]
        for b in right["colour"]  # type: ignore[union-attr]
    )


def normalize_quotient(raw: object, labels: int, name: str) -> tuple[int, ...]:
    need(
        type(raw) is list
        and len(raw) == labels
        and all(type(x) is int and x >= 0 for x in raw),
        f"{name}: malformed quotient",
    )
    used = sorted(set(raw))
    need(used == list(range(len(used))), f"{name}: quotient labels are not canonical")
    return tuple(raw)


def quotient_graph(
    product: set[tuple[int, int]], quotient: tuple[int, ...], extras: object, name: str
) -> tuple[int, set[tuple[int, int]]]:
    order = max(quotient) + 1
    edges: set[tuple[int, int]] = set()
    for a, b in product:
        qa, qb = quotient[a], quotient[b]
        need(qa != qb, f"{name}: a product edge collapses")
        edges.add(tuple(sorted((qa, qb))))
    extra_edges = parse_edges(order, extras, f"{name}: extra")
    edges.update(extra_edges)
    return order, edges


def test_pattern(
    word: tuple[int, ...], quotient: tuple[int, ...], edges: set[tuple[int, int]]
) -> dict[str, object]:
    classes: dict[int, list[int]] = {}
    for label, vertex in enumerate(quotient):
        classes.setdefault(vertex, []).append(label)
    class_colour: dict[int, int] = {}
    for vertex in sorted(classes):
        labels = classes[vertex]
        first = labels[0]
        for other in labels[1:]:
            if word[other] != word[first]:
                return {"valid": False, "witness": ["collision", first, other]}
        class_colour[vertex] = word[first]
    representatives = {vertex: labels[0] for vertex, labels in classes.items()}
    for a, b in sorted(edges):
        if class_colour[a] == class_colour[b]:
            return {
                "valid": False,
                "witness": ["edge", representatives[a], representatives[b]],
            }
    return {"valid": True, "witness": None, "class_word": [class_colour[i] for i in range(len(classes))]}


def chromatic_number(n: int, edges: set[tuple[int, int]], upper: int = 4) -> tuple[int, int]:
    total_nodes = 0
    for colours in range(1, upper + 1):
        answers, nodes = enumerate_colourings(n, edges, colours, {0: 0}, limit=1)
        total_nodes += nodes
        if answers:
            return colours, total_nodes
    raise VerificationError("fixture chromatic number exceeds control bound")


def verify_instance(
    raw: object, left: dict[str, object], right: dict[str, object], check_claims: bool
) -> dict[str, object]:
    need(type(raw) is dict, "instance is not an object")
    name = raw.get("name")
    need(type(name) is str and name, "instance name")
    labels = int(left["n"]) * int(right["n"])
    quotient = normalize_quotient(raw.get("quotient"), labels, name)
    product = product_edges(left, right)
    order, edges = quotient_graph(product, quotient, raw.get("extra_edges"), name)
    tests = {str(sign): test_pattern(pattern_word(left, right, sign), quotient, edges) for sign in (-1, 1)}
    valid_signs = [sign for sign in (-1, 1) if tests[str(sign)]["valid"]]

    y0 = 0
    anchor_labels = [v * int(right["n"]) + y0 for v in left["triangle"]]  # type: ignore[union-attr]
    anchor_vertices = [quotient[label] for label in anchor_labels]
    need(len(set(anchor_vertices)) == 3, f"{name}: anchor triangle collapsed")
    fixed = {
        quotient[label]: left["colour"][v]  # type: ignore[index]
        for label, v in zip(anchor_labels, left["triangle"])  # type: ignore[union-attr]
    }
    direct, direct_nodes = enumerate_colourings(order, edges, 3, fixed, limit=3)
    expected_words = []
    for sign in valid_signs:
        result = tests[str(sign)]
        word = result["class_word"]
        shift = sign * right["colour"][y0]  # type: ignore[index]
        expected_words.append(tuple((value - shift) % 3 for value in word))  # type: ignore[union-attr]
    need(sorted(direct) == sorted(expected_words), f"{name}: direct colourings disagree with interface")
    chi, chromatic_nodes = chromatic_number(order, edges)
    need((chi == 3) == bool(valid_signs), f"{name}: viability equivalence failed")
    if check_claims:
        need(raw.get("expected_valid_signs") == valid_signs, f"{name}: expected signs")
        need(raw.get("expected_chromatic_number") == chi, f"{name}: expected chromatic number")
    return {
        "name": name,
        "physical_vertices": order,
        "product_labels": labels,
        "edges": len(edges),
        "valid_signs": valid_signs,
        "pattern_tests": tests,
        "direct_anchored_three_colourings": len(direct),
        "direct_three_colour_nodes": direct_nodes,
        "chromatic_number": chi,
        "chromatic_search_nodes": chromatic_nodes,
    }


def bit_edges(n: int, mask: int) -> set[tuple[int, int]]:
    return {edge for i, edge in enumerate(itertools.combinations(range(n), 2)) if (mask >> i) & 1}


def edge_mask(n: int, edges: set[tuple[int, int]]) -> int:
    positions = {edge: i for i, edge in enumerate(itertools.combinations(range(n), 2))}
    return sum(1 << positions[edge] for edge in edges)


def canonical_mask(n: int, edges: set[tuple[int, int]]) -> int:
    values = []
    for permutation in itertools.permutations(range(n)):
        image = {tuple(sorted((permutation[a], permutation[b]))) for a, b in edges}
        values.append(edge_mask(n, image))
    return min(values)


def first_triangle(n: int, edges: set[tuple[int, int]]) -> tuple[int, int, int] | None:
    for triple in itertools.combinations(range(n), 3):
        if all(tuple(sorted(edge)) in edges for edge in itertools.combinations(triple, 2)):
            return triple
    return None


def small_unique_graphs() -> list[dict[str, object]]:
    result = []
    for n in range(3, 6):
        for mask in range(1 << (n * (n - 1) // 2)):
            edges = bit_edges(n, mask)
            if not connected(n, edges) or canonical_mask(n, edges) != mask:
                continue
            triangle = first_triangle(n, edges)
            if triangle is None:
                continue
            fixed = {triangle[i]: i for i in range(3)}
            words, nodes = enumerate_colourings(n, edges, 3, fixed, limit=2)
            if len(words) == 1:
                result.append(
                    {
                        "name": f"g{n}_{mask}",
                        "n": n,
                        "edges": edges,
                        "colour": words[0],
                        "triangle": triangle,
                        "uniqueness_nodes": nodes,
                    }
                )
    return result


def exhaustive_product_census() -> dict[str, object]:
    factors = small_unique_graphs()
    rows = []
    total_nodes = 0
    total_colourings = 0
    for left in factors:
        for right in factors:
            edges = product_edges(left, right)
            m = int(right["n"])
            y0 = 0
            anchor = {v * m + y0: left["colour"][v] for v in left["triangle"]}  # type: ignore[index,union-attr]
            words, nodes = enumerate_colourings(int(left["n"]) * m, edges, 3, anchor, limit=3)
            expected = []
            for sign in (-1, 1):
                shift = sign * right["colour"][y0]  # type: ignore[index]
                expected.append(tuple((x - shift) % 3 for x in pattern_word(left, right, sign)))
            need(sorted(words) == sorted(expected), "small-product census mismatch")
            rows.append(
                {
                    "left": left["name"],
                    "right": right["name"],
                    "vertices": int(left["n"]) * m,
                    "edges": len(edges),
                    "anchored_colourings": len(words),
                    "nodes": nodes,
                }
            )
            total_nodes += nodes
            total_colourings += len(words)
    order_histogram: dict[str, int] = {}
    for factor in factors:
        key = str(factor["n"])
        order_histogram[key] = order_histogram.get(key, 0) + 1
    return {
        "factor_isomorphism_classes": len(factors),
        "factor_order_histogram": order_histogram,
        "ordered_factor_pairs": len(rows),
        "product_vertex_range": [min(row["vertices"] for row in rows), max(row["vertices"] for row in rows)],
        "anchored_product_colourings": total_colourings,
        "backtracking_nodes": total_nodes,
        "pair_receipts_sha256": canonical_hash(rows),
    }


def run(data: object, check_claims: bool = True) -> dict[str, object]:
    need(type(data) is dict, "root is not an object")
    left = verify_factor(data.get("left"), "left")
    right = verify_factor(data.get("right"), "right")
    instances_raw = data.get("instances")
    need(type(instances_raw) is list and instances_raw, "missing instances")
    instances = [verify_instance(raw, left, right, check_claims) for raw in instances_raw]
    core = {
        "status": "VERIFIED_UNIQUE3_ROTATIONAL_SUM_VIABILITY_INTERFACE",
        "factor_uniqueness_nodes": [left["uniqueness_nodes"], right["uniqueness_nodes"]],
        "instances": instances,
        "small_graph_census": exhaustive_product_census(),
        "trust_boundary": "written combinatorial proof plus CPython exact finite enumeration; no SAT, floating point, or external package",
    }
    core["receipt_sha256"] = canonical_hash(core)
    return core


def run_controls(data: object) -> list[str]:
    need(type(data) is dict, "control root")
    controls = []

    def reject(name: str, mutated: object) -> None:
        try:
            run(mutated, check_claims=True)
        except VerificationError:
            controls.append(name)
            return
        raise VerificationError(f"control survived: {name}")

    bad = copy.deepcopy(data)
    bad["left"]["colouring"] = [0, 0, 2]  # type: ignore[index]
    reject("improper_factor_colouring", bad)

    bad = copy.deepcopy(data)
    bad["left"]["palette_triangle"] = [0, 1, 1]  # type: ignore[index]
    reject("malformed_palette_triangle", bad)

    bad = copy.deepcopy(data)
    bad["instances"][0]["quotient"] = [0, 0, 1, 2, 3, 4, 5, 6, 7]  # type: ignore[index]
    reject("collapsed_product_edge", bad)

    bad = copy.deepcopy(data)
    bad["left"] = {  # type: ignore[index]
        "name": "nonunique-triangle-with-leaf",
        "vertices": 4,
        "edges": [[0, 1], [0, 2], [1, 2], [0, 3]],
        "colouring": [0, 1, 2, 1],
        "palette_triangle": [0, 1, 2],
    }
    reject("nonunique_factor", bad)

    bad = copy.deepcopy(data)
    bad["instances"][0]["extra_edges"] = [[0, 0]]  # type: ignore[index]
    reject("loop_extra_edge", bad)

    bad = copy.deepcopy(data)
    bad["instances"][2]["expected_valid_signs"] = [1]  # type: ignore[index]
    reject("false_pattern_claim", bad)

    bad = copy.deepcopy(data)
    bad["instances"][2]["expected_chromatic_number"] = 3  # type: ignore[index]
    reject("false_chromatic_claim", bad)
    return controls


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", type=Path, default=ROOT / "fixtures.json")
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.instance.read_text())
    receipt = run(data, check_claims=True)
    if args.check_expected:
        expected = json.loads((ROOT / "EXPECTED.json").read_text())
        need(receipt == expected, "receipt differs from EXPECTED.json")
    if args.controls:
        receipt["rejected_controls"] = run_controls(data)
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
