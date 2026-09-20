#!/usr/bin/env python3
"""Independent exact checks for the lattice-index four-dot theorem.

This checker imports no code or expected data from the reviewed package.  It
uses direct arithmetic-line membership for the negative witnesses, enumerates
the residual bipartite graphs relevant to every claimed size threshold, and
tests unimodular transport on all small periodic four-dot configurations.
"""

from __future__ import annotations

import hashlib
import json
from itertools import product
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return (x[0] + y[0], x[1] + y[1])


def sub(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return (x[0] - y[0], x[1] - y[1])


def scale(k: int, x: tuple[int, int]) -> tuple[int, int]:
    return (k * x[0], k * x[1])


def determinant(x: tuple[int, int], y: tuple[int, int]) -> int:
    return x[0] * y[1] - x[1] * y[0]


def lattice_coordinates(
    z: tuple[int, int], u: tuple[int, int], v: tuple[int, int]
) -> tuple[int, int] | None:
    """Return integral (u,v)-coordinates, or None outside their lattice."""
    delta = determinant(u, v)
    require(delta != 0, "dependent basis")
    first = determinant(z, v)
    second = determinant(u, z)
    if first % delta or second % delta:
        return None
    return (first // delta, second // delta)


def physical(
    ab: tuple[int, int], u: tuple[int, int], v: tuple[int, int]
) -> tuple[int, int]:
    return add(scale(ab[0], u), scale(ab[1], v))


def in_arithmetic_line(
    z: tuple[int, int], origin: tuple[int, int], direction: tuple[int, int]
) -> bool:
    """Exact membership in origin + Z direction, including nonprimitive data."""
    difference = sub(z, origin)
    if determinant(difference, direction) != 0:
        return False
    coordinate = 0 if direction[0] else 1
    require(direction[coordinate] != 0, "zero direction")
    return difference[coordinate] % direction[coordinate] == 0


def witness_value(
    z: tuple[int, int],
    u: tuple[int, int],
    v: tuple[int, int],
    t: tuple[int, int],
) -> int:
    return int(in_arithmetic_line(z, (0, 0), u)) ^ int(
        in_arithmetic_line(z, t, v)
    )


def outside_coset_representative(
    u: tuple[int, int], v: tuple[int, int]
) -> tuple[int, int]:
    q = abs(determinant(u, v))
    require(q > 1, "lattice is not proper")
    for z in product(range(-q, q + 1), repeat=2):
        if lattice_coordinates(z, u, v) is None:
            return z
    raise RuntimeError("failed to find a point outside the direction lattice")


def separator(
    w: tuple[int, int],
    u: tuple[int, int],
    v: tuple[int, int],
    t: tuple[int, int],
) -> tuple[int, int]:
    """Use the claimed two-point alternative, checked at definition level."""
    require(w != (0, 0), "the zero vector cannot be separated")
    candidates = ((0, 0), u) if determinant(u, w) else (t, add(t, v))
    for z in candidates:
        if witness_value(z, u, v, t) != witness_value(add(z, w), u, v, t):
            return z
    raise RuntimeError(f"unseparated proposed period {w}")


def incidence_language(window: list[tuple[int, int]]) -> set[int]:
    """The proposed zero/row/column masks, formed without lattice routines."""
    rows: dict[int, int] = {}
    columns: dict[int, int] = {}
    for index, (a, b) in enumerate(window):
        rows[b] = rows.get(b, 0) | (1 << index)
        columns[a] = columns.get(a, 0) | (1 << index)
    return {0, *rows.values(), *columns.values()}


def direct_sampled_language(
    window: list[tuple[int, int]],
    u: tuple[int, int],
    v: tuple[int, int],
    t: tuple[int, int],
    radius: int = 32,
) -> set[int]:
    """Evaluate the infinite arithmetic-line formula on a large physical box."""
    sites = [physical(ab, u, v) for ab in window]
    masks: set[int] = set()
    for shift in product(range(-radius, radius + 1), repeat=2):
        mask = 0
        for index, site in enumerate(sites):
            mask |= witness_value(add(shift, site), u, v, t) << index
        masks.add(mask)
    return masks


def formula_complexity(window: list[tuple[int, int]]) -> int:
    row_degrees: dict[int, int] = {}
    column_degrees: dict[int, int] = {}
    for a, b in window:
        row_degrees[b] = row_degrees.get(b, 0) + 1
        column_degrees[a] = column_degrees.get(a, 0) + 1
    isolated = sum(
        row_degrees[b] == 1 and column_degrees[a] == 1 for a, b in window
    )
    return 1 + len(row_degrees) + len(column_degrees) - isolated


def audit_negative_witnesses() -> dict[str, object]:
    fixtures = [
        ((1, 0), (1, 2)),
        ((2, 0), (0, 2)),
        ((2, 1), (1, 2)),
        ((-1, 2), (2, 1)),
        ((2, 0), (1, 3)),
        ((4, 2), (2, 3)),
        ((0, -3), (2, 1)),
    ]
    windows = {
        "singleton": [(0, 0)],
        "two_isolated": [(0, 0), (3, 4)],
        "square": list(product(range(2), repeat=2)),
        "k23": list(product(range(3), range(2))),
        "k24": list(product(range(4), range(2))),
        "k33_minus_edge": [
            z for z in product(range(3), repeat=2) if z != (2, 2)
        ],
        "k23_plus_isolated": list(product(range(3), range(2))) + [(7, -4)],
        "nonconsecutive": [(-4, -3), (-1, -3), (-4, 2), (5, 7)],
    }
    annihilator_checks = 0
    separator_checks = 0
    language_checks = 0
    records = []
    for u, v in fixtures:
        q = abs(determinant(u, v))
        t = outside_coset_representative(u, v)
        require(lattice_coordinates(t, u, v) is None, "bad coset representative")
        require(
            not ({scale(k, u) for k in range(-20, 21)} &
                 {add(t, scale(k, v)) for k in range(-20, 21)}),
            "sampled line intersection",
        )

        four_dot = ((0, 0), u, v, add(u, v))
        for z in product(range(-8, 9), repeat=2):
            total = sum(witness_value(sub(z, exponent), u, v, t)
                        for exponent in four_dot)
            require(total % 2 == 0, "four-dot annihilator failed")
            annihilator_checks += 1

        for w in product(range(-10, 11), repeat=2):
            if w == (0, 0):
                continue
            z = separator(w, u, v, t)
            require(witness_value(z, u, v, t) == 1, "separator is not a one")
            require(
                witness_value(add(z, w), u, v, t) == 0,
                "separator does not become zero",
            )
            separator_checks += 1

        complexities = {}
        for name, raw_window in windows.items():
            window = sorted(raw_window)
            proposed = incidence_language(window)
            observed = direct_sampled_language(window, u, v, t)
            require(observed == proposed, f"window-language mismatch for {name}")
            require(len(observed) == formula_complexity(window), "formula mismatch")
            translated = sorted((a + 2, b - 3) for a, b in window)
            require(
                direct_sampled_language(translated, u, v, t) == proposed,
                "coordinate translation changed language",
            )
            complexities[name] = len(observed)
            language_checks += 2
        records.append({"u": u, "v": v, "t": t, "index": q,
                        "complexities": complexities})

    return {
        "fixtures": records,
        "annihilator_checks": annihilator_checks,
        "period_separator_checks": separator_checks,
        "direct_language_checks": language_checks,
    }


def audit_threshold_graphs() -> dict[str, object]:
    """Enumerate every residual graph that could beat either size threshold.

    For the claimed low-complexity minimum and its six-edge classification,
    only total size at most six matters, hence n' <= e'-1 <= 5.  For the
    claimed strict minimum through size eight, n' <= e'-2 <= 6.  Thus every
    candidate relevant to either conclusion has at most six residual vertices,
    so this is complete rather than a fixed ambient-grid sample.
    """
    residual_graphs = 0
    low_candidates: list[tuple[int, int, int, int]] = []
    strict_candidates: list[tuple[int, int, int, int]] = []
    for r in range(1, 7):
        for s in range(r, 7):
            if r + s > 6:
                continue
            cells = [(a, b) for a in range(r) for b in range(s)]
            for mask in range(1, 1 << len(cells)):
                edges = [cells[k] for k in range(len(cells)) if mask >> k & 1]
                row_degree = [sum(b == j for a, b in edges) for j in range(s)]
                column_degree = [sum(a == i for a, b in edges) for i in range(r)]
                if 0 in row_degree or 0 in column_degree:
                    continue
                if any(row_degree[b] == column_degree[a] == 1 for a, b in edges):
                    continue
                residual_graphs += 1
                e_prime = len(edges)
                n_prime = r + s
                for isolated_edges in range(0, 9 - e_prime):
                    total_edges = e_prime + isolated_edges
                    if total_edges == 0 or total_edges > 8:
                        continue
                    difference = 1 + n_prime - e_prime
                    if difference <= 0:
                        low_candidates.append((total_edges, r, s, e_prime))
                    if difference < 0:
                        strict_candidates.append((total_edges, r, s, e_prime))

    require(low_candidates, "no low candidates found")
    require(strict_candidates, "no strict candidates found")
    minimum_low = min(record[0] for record in low_candidates)
    minimum_strict = min(record[0] for record in strict_candidates)
    low_at_minimum = sorted(set(x for x in low_candidates if x[0] == minimum_low))
    strict_at_minimum = sorted(
        set(x for x in strict_candidates if x[0] == minimum_strict)
    )
    require(minimum_low == 6, "wrong low-complexity threshold")
    require(low_at_minimum == [(6, 2, 3, 6)], "wrong six-edge classification")
    require(minimum_strict == 8, "wrong strict threshold")
    require(
        strict_at_minimum == [(8, 2, 4, 8), (8, 3, 3, 8)],
        "wrong eight-edge classification",
    )

    # Directly pressure the smallest cases, including isolated-edge deletion.
    examples = {
        "one_edge": [(0, 0)],
        "two_isolated_edges": [(0, 0), (2, 2)],
        "four_cycle": list(product(range(2), repeat=2)),
        "k23": list(product(range(3), range(2))),
        "k23_plus_isolated": list(product(range(3), range(2))) + [(4, 4)],
        "k24": list(product(range(4), range(2))),
        "k33_minus_edge": [
            z for z in product(range(3), repeat=2) if z != (2, 2)
        ],
    }
    example_complexities = {
        name: formula_complexity(sorted(window)) for name, window in examples.items()
    }
    require(example_complexities["one_edge"] == 2, "one-edge boundary")
    require(example_complexities["two_isolated_edges"] == 3, "isolated edges")
    require(example_complexities["four_cycle"] == 5, "four-cycle boundary")
    require(example_complexities["k23"] == 6, "K2,3 boundary")
    require(example_complexities["k23_plus_isolated"] == 7, "isolated repair")
    require(example_complexities["k24"] == 7, "K2,4 boundary")
    require(example_complexities["k33_minus_edge"] == 7, "K3,3-e boundary")
    return {
        "enumerated_residual_graphs": residual_graphs,
        "minimum_low_size": minimum_low,
        "minimum_low_types": low_at_minimum,
        "minimum_strict_size": minimum_strict,
        "minimum_strict_types": strict_at_minimum,
        "adversarial_example_complexities": example_complexities,
    }


def periodic_four_dot_value(
    a: int, b: int, horizontal: tuple[int, ...], vertical: tuple[int, ...]
) -> int:
    n = len(horizontal)
    return horizontal[a % n] ^ vertical[b % n]


def audit_unimodular_transport() -> dict[str, object]:
    bases = [
        ((1, 0), (0, 1)),
        ((1, 1), (0, 1)),
        ((2, 1), (1, 1)),
        ((-1, 2), (0, -1)),
    ]
    coordinate_windows = [
        [(0, 0)],
        [(0, 0), (2, 0), (1, 1), (-1, 3)],
        [(0, 0), (1, 0), (0, 2), (3, 1), (-2, -1)],
    ]
    n = 4
    distinct_configurations = 0
    language_comparisons = 0
    constraint_checks = 0
    for u, v in bases:
        require(abs(determinant(u, v)) == 1, "non-unimodular fixture")
        configurations: dict[tuple[int, ...], tuple[tuple[int, ...], tuple[int, ...]]] = {}
        for h_bits in product((0, 1), repeat=n):
            for v_bits in product((0, 1), repeat=n):
                table = tuple(
                    periodic_four_dot_value(a, b, h_bits, v_bits)
                    for b in range(n) for a in range(n)
                )
                configurations.setdefault(table, (h_bits, v_bits))
        require(len(configurations) == 2 ** (2 * n - 1), "four-dot torus count")
        distinct_configurations += len(configurations)

        for horizontal, vertical in configurations.values():
            def mapped_value(z: tuple[int, int]) -> int:
                coordinates = lattice_coordinates(z, u, v)
                require(coordinates is not None, "unimodular map missed a point")
                return periodic_four_dot_value(
                    coordinates[0], coordinates[1], horizontal, vertical
                )

            for a, b in product(range(n), repeat=2):
                z = physical((a, b), u, v)
                total = sum(
                    mapped_value(sub(z, exponent))
                    for exponent in ((0, 0), u, v, add(u, v))
                )
                require(total % 2 == 0, "mapped four-dot constraint")
                constraint_checks += 1

            for window in coordinate_windows:
                ordinary: set[int] = set()
                mapped: set[int] = set()
                physical_window = [physical(ab, u, v) for ab in window]
                for alpha, beta in product(range(n), repeat=2):
                    ordinary_mask = 0
                    mapped_mask = 0
                    shift = physical((alpha, beta), u, v)
                    for index, ((a, b), site) in enumerate(zip(window, physical_window)):
                        ordinary_mask |= periodic_four_dot_value(
                            alpha + a, beta + b, horizontal, vertical
                        ) << index
                        mapped_mask |= mapped_value(add(shift, site)) << index
                    ordinary.add(ordinary_mask)
                    mapped.add(mapped_mask)
                require(ordinary == mapped, "pattern language not transported")
                language_comparisons += 1
    return {
        "unimodular_bases": len(bases),
        "distinct_periodic_configurations": distinct_configurations,
        "mapped_constraint_checks": constraint_checks,
        "pattern_language_comparisons": language_comparisons,
    }


def polynomial_product(left: set[tuple[int, int]], right: set[tuple[int, int]]) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    for x in left:
        for y in right:
            exponent = add(x, y)
            if exponent in result:
                result.remove(exponent)
            else:
                result.add(exponent)
    return result


def audit_factor_example() -> dict[str, object]:
    directions = ((1, 0), (1, 2), (0, 1))
    polynomial = {(0, 0)}
    for direction in directions:
        require(gcd(abs(direction[0]), abs(direction[1])) == 1, "nonprimitive")
        polynomial = polynomial_product(polynomial, {(0, 0), direction})
    expected = {
        (0, 0), (0, 1), (1, 0), (1, 1),
        (1, 2), (1, 3), (2, 2), (2, 3),
    }
    require(polynomial == expected, "wrong displayed polynomial support")
    require(all(
        determinant(directions[i], directions[j]) != 0
        for i in range(3) for j in range(i + 1, 3)
    ), "parallel factors")
    require({(1, 0), (0, 1)} <= {sub(x, (0, 0)) for x in polynomial},
            "support differences do not span")

    u, v, t = (1, 0), (1, 2), (0, 1)
    checks = 0
    for z in product(range(-12, 13), repeat=2):
        total = sum(witness_value(sub(z, exponent), u, v, t)
                    for exponent in polynomial)
        require(total % 2 == 0, "factor example does not annihilate witness")
        checks += 1
    return {"support": sorted(polynomial), "annihilator_checks": checks}


def main() -> None:
    result = {
        "schema": 1,
        "negative_witness_audit": audit_negative_witnesses(),
        "threshold_graph_audit": audit_threshold_graphs(),
        "unimodular_transport_audit": audit_unimodular_transport(),
        "factor_example_audit": audit_factor_example(),
        "trust_boundary": (
            "Finite checks corroborate arithmetic-line, incidence, transport, and "
            "factor reductions; the universal theorem uses the audited written proof "
            "and the published ordinary four-dot theorem."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["result_sha256"] = hashlib.sha256(encoded).hexdigest()
    expected = json.loads((ROOT / "EXPECTED.json").read_text())
    require(result["result_sha256"] == expected["result_sha256"],
            "result digest differs from EXPECTED.json")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
