#!/usr/bin/env python3
"""Cross-basis and exhaustive small-colouring controls."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name):
    spec = spec_from_file_location(name, HERE / f"{name}.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


V = load("verify")
A = load("audit")


def need(ok, message):
    if not ok:
        raise ValueError(message)


def convert_scaled(value, denominator=7):
    t = A.mul(A.ZPOW[6], A.W)
    answer = A.ZERO
    power = A.ONE
    for coefficient in value:
        scaled = coefficient * denominator
        need(scaled.denominator == 1, "conversion denominator")
        answer = A.add(answer, A.scale(power, scaled.numerator))
        power = A.mul(power, t)
    return answer


def brute_extension(order, edges, terminals, pattern):
    for word in product(range(4), repeat=order):
        if tuple(word[v] for v in terminals) != tuple(pattern):
            continue
        if all(word[i] != word[j] for i, j in edges):
            return word
    return None


def main():
    primary_seed, primary_classes, _, primary_edges, _, _ = V.build_graph()
    audit_seed, audit_classes, _, audit_edges, _, _ = A.build_graph()
    primary_moved = tuple(
        V.add(primary_seed[0], V.mul(V.POWERS[-6 % 42], V.sub(point, primary_seed[0])))
        for point in primary_seed
    )
    audit_moved = tuple(
        A.add(audit_seed[0], A.mul(A.ZPOW[6], A.sub(point, audit_seed[0])))
        for point in audit_seed
    )
    need(tuple(convert_scaled(point) for point in primary_seed + primary_moved)
         == audit_seed + audit_moved, "formal-coordinate basis conversion")
    need(primary_classes == audit_classes, "collision classes disagree")
    need(primary_edges == audit_edges, "edge lists disagree")

    solver_cases = 0
    for order in range(1, 5):
        pairs = tuple(combinations(range(order), 2))
        for mask in range(1 << len(pairs)):
            edges = tuple(pair for index, pair in enumerate(pairs) if mask >> index & 1)
            graph = V.adjacency(order, edges)
            audit_graph = A.adjacency(order, edges)
            terminal_choices = [()] + [(i,) for i in range(order)]
            if order >= 2:
                terminal_choices += list(combinations(range(order), 2))
            for terminals in terminal_choices:
                for pattern in product(range(4), repeat=len(terminals)):
                    expected = brute_extension(order, edges, terminals, pattern)
                    observed = V.extend(order, edges, graph, terminals, pattern)
                    alternate = A.extend_label_order(
                        order, edges, audit_graph, terminals, pattern
                    )
                    need((expected is None) == (observed is None), "primary solver control")
                    need((expected is None) == (alternate is None), "audit solver control")
                    solver_cases += 1

    # The collision and closing contacts are not generic consequences of taking
    # two copies: the identity map collapses every corresponding address.
    seed = V.seed()
    identity_classes = {}
    for address, point in enumerate(seed + seed):
        identity_classes.setdefault(point, []).append(address)
    need(len(identity_classes) == 21, "identity negative control")
    need(sum(len(group) == 2 for group in identity_classes.values()) == 21,
         "identity collision control")
    print(f"CONTROLS PASSED: 42 coordinate conversions and {solver_cases} solver cases")


if __name__ == "__main__":
    main()
