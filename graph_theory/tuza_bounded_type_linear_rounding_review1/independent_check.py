#!/usr/bin/env python3
"""Independent exact interface checks for bounded-type triangle rounding.

This checker imports no target module.  It checks the target audit hash, then
uses separate small exhaustive calculations for pendant tags, row-normalized
flow rounding, the color-repair exclusion inequality, Hall margins, size-band
induction, small-class filler identities, and the complete-graph parity lower
bound.  These checks support, but do not replace, the universal Keevash
specialization and induction audited in REVIEW.md.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from json import dumps, loads
from math import comb
from pathlib import Path
import sys


TARGET_AUDIT_SHA256 = (
    "3524a0deed1930285cc68ab6953d912034bc7aa85170b7a7be437dd3e4f027fd"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ceil_fraction(value):
    return -(-value.numerator // value.denominator)


def pendant_checks():
    instances = 0
    worst_column_deletion = 0
    for vertices in range(1, 41):
        for roles_per_copy in (1, 2, 3):
            for copies in range(1, 101):
                total = roles_per_copy * copies
                low, extra = divmod(total, vertices)
                roles = [low + (index < extra) for index in range(vertices)]
                columns = ceil_fraction(Fraction(total, vertices))
                deficient = [index for index, value in enumerate(roles)
                             if value < columns]
                missing = {(row, position % columns)
                           for position, row in enumerate(deficient)}
                require(len(missing) == len(deficient), "duplicate pendant omission")
                row_missing = [sum(row == x for row, _ in missing)
                               for x in range(vertices)]
                column_missing = [sum(column == y for _, column in missing)
                                  for y in range(columns)]
                require(all(columns - row_missing[x] == roles[x]
                            for x in range(vertices)), "wrong pendant row degree")
                require(vertices * columns - len(missing) == total,
                        "wrong pendant edge total")
                bound = ceil_fraction(Fraction(vertices, columns))
                require(max(column_missing, default=0) <= bound,
                        "pendant column deletion bound failed")
                require(max(column_missing, default=0)
                        - min(column_missing, default=0) <= 1,
                        "pendant omissions are not equitable")
                worst_column_deletion = max(
                    worst_column_deletion, max(column_missing, default=0)
                )
                instances += 1
    return {
        "instances": instances,
        "worst_column_deletion": worst_column_deletion,
    }


def column_targets(rows, columns, quota):
    values = [Fraction(0) for _ in range(columns)]
    for neighbors in rows:
        weight = Fraction(quota, len(neighbors))
        for column in neighbors:
            values[column] += weight
    return values


def has_rounded_selection(rows, columns, quota):
    values = column_targets(rows, columns, quota)
    choices = [tuple(combinations(sorted(neighbors), quota)) for neighbors in rows]
    for selected in product(*choices):
        counts = [0] * columns
        for row in selected:
            for column in row:
                counts[column] += 1
        if all(value.numerator // value.denominator <= count
               <= ceil_fraction(value)
               for value, count in zip(values, counts)):
            return True
    return False


def flow_checks():
    exhaustive = 0
    quota_two = 0
    for columns in range(2, 6):
        nonempty = [frozenset(j for j in range(columns) if mask >> j & 1)
                    for mask in range(1, 1 << columns)]
        for row_count in range(1, 4):
            for rows in product(nonempty, repeat=row_count):
                require(has_rounded_selection(rows, columns, 1),
                        "row-normalized quota-one rounding failed")
                exhaustive += 1
        large = [row for row in nonempty if len(row) >= 2]
        # Deterministic coverage of structurally different quota-two rows.
        stride = max(1, len(large) ** 3 // 600)
        for index, rows in enumerate(product(large, repeat=3)):
            if index % stride:
                continue
            require(has_rounded_selection(rows, columns, 2),
                    "row-normalized quota-two rounding failed")
            quota_two += 1
    return {
        "quota_one_exhaustive_instances": exhaustive,
        "quota_two_deterministic_instances": quota_two,
    }


def color_bound_checks():
    cases = 0
    worst_ratio = Fraction(0)
    for classes in range(1, 13):
        minimum_part = 64 * (classes + 1)
        for discrepancy in range(0, 41):
            for scale in (1, 2, 5):
                order = scale * classes * minimum_part
                palette = 64 * order
                edge_count = 16 * (discrepancy + 1) * order
                excluded = (
                    (Fraction(4 * order, palette)
                     + Fraction(2 * (classes + 1), minimum_part)) * edge_count
                    + 2 * order
                    + Fraction(discrepancy * order * order, palette)
                    + 2 * discrepancy * (classes + 1)
                )
                require(excluded <= Fraction(7 * edge_count, 32) < edge_count,
                        "color-repair exclusion margin failed")
                worst_ratio = max(worst_ratio, excluded / edge_count)
                cases += 1
    return {
        "boundary_cases": cases,
        "worst_excluded_ratio": str(worst_ratio),
        "proved_uniform_cap": "7/32",
    }


def hall_parameter_checks():
    cases = 0
    worst_fraction = Fraction(0)
    for small_classes in range(1, 9):
        for core_classes in range(1, 9):
            for labels in range(0, 5):
                discrepancy = 3 * small_classes
                bound = 2 ** (core_classes + labels) * (small_classes + 3)
                quota = 8 * bound * (
                    discrepancy + small_classes * core_classes + 1
                )
                alpha = Fraction(1, core_classes + 1)
                eta = min(
                    alpha / 64,
                    alpha / (8 * discrepancy),
                    alpha / (16 * core_classes),
                )
                used_degree = (
                    Fraction(2 * core_classes) * eta * quota / alpha
                    + small_classes * core_classes * bound
                )
                require(used_degree <= Fraction(quota, 4),
                        "globally ordered Hall margin failed")
                require(quota >= 8 * discrepancy * bound
                        and quota >= 8 * small_classes * core_classes * bound,
                        "quota does not dominate flow discrepancies")
                delta = small_classes + 1
                for _ in range(core_classes + labels):
                    delta = 2 * delta + 2
                require(delta < bound, "column-discrepancy recurrence failed")
                worst_fraction = max(worst_fraction, used_degree / quota)
                cases += 1
    return {
        "parameter_cases": cases,
        "largest_forbidden_degree_fraction": str(worst_fraction),
    }


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(1, total - parts + 2):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def induction_band_checks():
    cases = 0
    for classes in range(2, 7):
        epsilon = [Fraction(1, classes)]
        eta = []
        for _ in range(classes):
            local_eta = epsilon[-1] / (128 * (classes + 1))
            eta.append(local_eta)
            epsilon.append(min(
                epsilon[-1] / 2,
                local_eta / (2 * classes * classes),
            ) / 2)
        for comp in compositions(36, classes):
            proportions = [Fraction(value, 36) for value in comp]
            empty = [j for j in range(classes)
                     if not any(epsilon[j + 1] <= value < epsilon[j]
                                for value in proportions)]
            require(empty, "size hierarchy has no empty band")
            j = empty[0]
            core = [value for value in proportions if value >= epsilon[j]]
            exceptional = [value for value in proportions if value < epsilon[j]]
            core_mass = sum(core)
            exceptional_mass = sum(exceptional)
            require(core_mass >= Fraction(1, classes), "core too small")
            require(all(value >= epsilon[j] * core_mass for value in core),
                    "core is not comparable")
            require(all(value < epsilon[j + 1] for value in exceptional),
                    "empty band did not separate scales")
            require(exceptional_mass < eta[j] * core_mass,
                    "exceptional union too large")
            cases += 1
    return {"positive_compositions_checked": cases}


def small_class_filler_checks():
    records = 0
    for class_count in range(1, 5):
        sizes = [index + 2 for index in range(class_count)]
        edge_types = list(combinations_with_replacement(range(class_count), 2))
        capacities = {
            edge_type: (
                comb(sizes[edge_type[0]], 2)
                if edge_type[0] == edge_type[1]
                else sizes[edge_type[0]] * sizes[edge_type[1]]
            )
            for edge_type in edge_types
        }
        triangle_types = [
            pattern
            for pattern in combinations_with_replacement(range(class_count), 3)
            if all(pattern.count(index) <= sizes[index]
                   for index in set(pattern))
        ]
        remaining = {edge_type: Fraction(value)
                     for edge_type, value in capacities.items()}
        profile = []
        for pattern_index, pattern in enumerate(triangle_types):
            incidence = {}
            for pair in combinations(pattern, 2):
                edge_type = tuple(pair)
                incidence[edge_type] = incidence.get(edge_type, 0) + 1
            possible = min(
                remaining[edge_type] / multiplicity
                for edge_type, multiplicity in incidence.items()
            )
            mass = possible / (2 * (pattern_index + 2))
            profile.append((pattern, mass))
            for edge_type, multiplicity in incidence.items():
                remaining[edge_type] -= multiplicity * mass
        for edge_type, mass in remaining.items():
            profile.append((edge_type, mass))
        for removed in range(class_count):
            kept = {edge_type: Fraction(0) for edge_type in edge_types
                    if removed not in edge_type}
            filler = {edge_type: Fraction(0) for edge_type in kept}
            discarded_mass = Fraction(0)
            for pattern, mass in profile:
                pairs = list(combinations(pattern, 2))
                if removed in pattern:
                    discarded_mass += mass
                    for pair in pairs:
                        edge_type = tuple(pair)
                        if removed not in edge_type:
                            filler[edge_type] += mass
                else:
                    for pair in pairs:
                        kept[tuple(pair)] += mass
            incident_capacity = sum(
                value for edge_type, value in capacities.items()
                if removed in edge_type
            )
            require(discarded_mass <= incident_capacity,
                    "small-class loss exceeds incident capacity")
            require(all(kept[edge_type] + filler[edge_type]
                        == capacities[edge_type] for edge_type in kept),
                    "filler does not restore residual capacity")
            records += 1
    return {"removed_class_cases": records}


def parity_checks():
    cases = []
    for order in range(4, 102, 2):
        edges = comb(order, 2)
        fractional = Fraction(edges, 3)
        integral_upper = Fraction(edges - order // 2, 3)
        require(fractional - integral_upper == Fraction(order, 6),
                "complete-graph parity lower bound failed")
        cases.append(order)
    return {
        "even_orders_checked": len(cases),
        "gap_lower_bound": "N/6",
    }


def main():
    require(len(sys.argv) in (2, 3),
            "usage: independent_check.py TARGET_AUDIT [EXPECTED|-]")
    target_bytes = Path(sys.argv[1]).read_bytes()
    require(sha256(target_bytes).hexdigest() == TARGET_AUDIT_SHA256,
            "target audit hash mismatch")
    loads(target_bytes)
    result = {
        "status": "PASS",
        "target_audit_sha256": TARGET_AUDIT_SHA256,
        "pendant_tags": pendant_checks(),
        "row_normalized_flow": flow_checks(),
        "color_repair_bound": color_bound_checks(),
        "ordered_hall_margin": hall_parameter_checks(),
        "induction_empty_band": induction_band_checks(),
        "small_class_fillers": small_class_filler_checks(),
        "complete_graph_parity": parity_checks(),
        "trust_boundary": (
            "Finite exact interface checks only. The universal Keevash "
            "specialization and the strong induction remain human-audited."
        ),
    }
    rendered = dumps(result, sort_keys=True, indent=2) + "\n"
    if len(sys.argv) == 3 and sys.argv[2] != "-":
        require(rendered == Path(sys.argv[2]).read_text(),
                "output does not match expected JSON")
        print(dumps({"status": "PASS", "expected_sha256":
                     sha256(rendered.encode()).hexdigest()}, sort_keys=True))
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
