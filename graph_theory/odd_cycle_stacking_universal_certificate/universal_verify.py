#!/usr/bin/env python3
"""Exact symbolic verifier for the universal odd-cycle stacking certificate.

The verifier proves a finite family of affine/exponential inequalities.  It
does not test a bounded range of cycle sizes.  In the two generic arms, every
obligation has the form

    A*2**(d+h) + B*2**d + C >= 0,

where d and h have fixed parities and independent lower bounds.  The routine
``prove_arm_nonnegative`` checks A >= 0, then checks the least admissible h
and d; monotonicity proves the inequality for the whole infinite domain.

Fractions are exact.  Denominators are powers of two, and residues modulo
three are computed using their inverses modulo three.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools


@dataclass(frozen=True)
class Affine:
    """The expression p*P + z*Z + c, with P=2**k and Z=2**d."""

    p: Fraction = Fraction(0)
    z: Fraction = Fraction(0)
    c: Fraction = Fraction(0)

    def __add__(self, other: Affine) -> Affine:
        return Affine(self.p + other.p, self.z + other.z, self.c + other.c)

    def __sub__(self, other: Affine) -> Affine:
        return Affine(self.p - other.p, self.z - other.z, self.c - other.c)

    def __rmul__(self, scalar: int | Fraction) -> Affine:
        return Affine(scalar * self.p, scalar * self.z, scalar * self.c)

    def scale_z(self, factor: int | Fraction) -> Affine:
        return Affine(self.p, self.z * factor, self.c)

    def at_fixed_h(self, h: int) -> Affine:
        """Substitute Z=P/2**h, returning an expression with z=0."""
        return Affine(self.p + self.z / (2**h), 0, self.c)

    def at_fixed_z(self, z_value: int) -> Affine:
        return Affine(self.p, 0, self.z * z_value + self.c)

    def canonical(self) -> str:
        return f"({self.p})P+({self.z})Z+({self.c})"


ZERO = Affine()
P = Affine(p=Fraction(1))
Z = Affine(z=Fraction(1))
ONE = Affine(c=Fraction(1))


def first_with_parity(lower: int, parity: int) -> int:
    return lower if lower % 2 == parity else lower + 1


def fraction_mod_three(value: Fraction) -> int:
    denominator = value.denominator % 3
    if denominator == 0:
        raise AssertionError("a coefficient denominator is divisible by three")
    return (value.numerator % 3) * pow(denominator, -1, 3) % 3


def expression_residue(expr: Affine, k_parity: int, d_parity: int) -> int:
    p_mod = 1 if k_parity == 0 else 2
    z_mod = 1 if d_parity == 0 else 2
    return (
        fraction_mod_three(expr.p) * p_mod
        + fraction_mod_three(expr.z) * z_mod
        + fraction_mod_three(expr.c)
    ) % 3


def residue_row(
    values: list[Affine], k_parity: int, d_parity: int
) -> tuple[Affine, Affine, Affine]:
    if len(values) != 3:
        raise AssertionError("every row must have three candidate values")
    row: list[Affine | None] = [None, None, None]
    for value in values:
        residue = expression_residue(value, k_parity, d_parity)
        if row[residue] is not None:
            raise AssertionError("candidate values do not have distinct residues")
        row[residue] = value
    if any(value is None for value in row):
        raise AssertionError("candidate row misses a residue")
    return tuple(row)  # type: ignore[return-value]


def common_row_values() -> list[Affine]:
    # No-special tree at distance d from the main pile.
    return [Z, 4 * P - 2 * Z, 5 * P - 2 * Z]


def left_generic_rows(
    k_parity: int, d_parity: int
) -> tuple[tuple[Affine, Affine, Affine], ...]:
    """Rows at L_d for h=k-d >= 1."""
    values = [
        common_row_values(),
        [2 * P - 2 * Z, 3 * P - 2 * Z, 4 * P - 2 * Z],
        [P + Z - 3 * ONE, Fraction(7, 2) * P - 2 * Z,
         Fraction(9, 2) * P - 2 * Z],
        [Fraction(5, 2) * P - 2 * Z,
         Fraction(7, 2) * P - 2 * Z, 3 * P - 2 * Z - 3 * ONE],
    ]
    return tuple(residue_row(row, k_parity, d_parity) for row in values)


def left_special_rows(
    k_parity: int,
) -> tuple[tuple[Affine, Affine, Affine], ...]:
    """Rows at L_k, the singleton-x vertex."""
    values = [
        [P, 2 * P, 3 * P],
        [ZERO, 2 * P, Fraction(5, 2) * P],
        [Fraction(3, 2) * P, 2 * P - 3 * ONE, Fraction(5, 2) * P],
        [Fraction(3, 2) * P, 2 * P, Fraction(5, 2) * P - 3 * ONE],
    ]
    return tuple(residue_row(row, k_parity, k_parity) for row in values)


def right_generic_rows(
    k_parity: int, d_parity: int
) -> tuple[tuple[Affine, Affine, Affine], ...]:
    """Rows at R_d for h=k-d >= 2."""
    values = [
        common_row_values(),
        [2 * P + Z - 3 * ONE, 3 * P - 2 * Z, 4 * P - 2 * Z],
        [P - 2 * Z, Fraction(7, 2) * P - 2 * Z,
         Fraction(9, 2) * P - 2 * Z],
        [Fraction(5, 2) * P - 2 * Z,
         Fraction(7, 2) * P - 2 * Z, 3 * P - 2 * Z - 3 * ONE],
    ]
    return tuple(residue_row(row, k_parity, d_parity) for row in values)


def right_y_rows(
    k_parity: int,
) -> tuple[tuple[Affine, Affine, Affine], ...]:
    """Rows at R_(k-1), the singleton-y vertex."""
    values = [
        [Fraction(1, 2) * P, 3 * P, 4 * P],
        [2 * P, Fraction(5, 2) * P - 3 * ONE, 3 * P],
        [ZERO, Fraction(5, 2) * P, Fraction(7, 2) * P],
        [Fraction(3, 2) * P, Fraction(5, 2) * P,
         Fraction(11, 4) * P - 3 * ONE],
    ]
    return tuple(
        residue_row(row, k_parity, (k_parity - 1) % 2) for row in values
    )


def right_middle_rows(
    k_parity: int,
) -> tuple[tuple[Affine, Affine, Affine], ...]:
    """Rows at R_k, the vertex between the two singleton vertices."""
    values = [
        [P, 2 * P, 3 * P],
        [P, 2 * P, 3 * P - 3 * ONE],
        [Fraction(1, 2) * P, Fraction(5, 2) * P, 3 * P - 3 * ONE],
        [Fraction(3, 2) * P, 2 * P - 3 * ONE,
         Fraction(5, 2) * P - 3 * ONE],
    ]
    return tuple(residue_row(row, k_parity, k_parity) for row in values)


def scaled_rows(
    rows: tuple[tuple[Affine, Affine, Affine], ...], factor: int | Fraction
) -> tuple[tuple[Affine, Affine, Affine], ...]:
    return tuple(tuple(value.scale_z(factor) for value in row) for row in rows)


def fixed_h_rows(
    rows: tuple[tuple[Affine, Affine, Affine], ...], h: int
) -> tuple[tuple[Affine, Affine, Affine], ...]:
    return tuple(tuple(value.at_fixed_h(h) for value in row) for row in rows)


def fixed_z_rows(
    rows: tuple[tuple[Affine, Affine, Affine], ...], z_value: int
) -> tuple[tuple[Affine, Affine, Affine], ...]:
    return tuple(tuple(value.at_fixed_z(z_value) for value in row) for row in rows)


class ProofLedger:
    def __init__(self) -> None:
        self.digest = hashlib.sha256()
        self.arm_inequalities = 0
        self.k_inequalities = 0
        self.residue_rows = 0

    def record(self, text: str) -> None:
        self.digest.update((text + "\n").encode("ascii"))

    def prove_arm_nonnegative(
        self,
        expr: Affine,
        *,
        d_min: int,
        h_min: int,
        d_parity: int,
        h_parity: int,
        label: str,
    ) -> None:
        """Prove expr>=0 for an infinite parity-restricted arm domain."""
        d0 = first_with_parity(d_min, d_parity)
        h0 = first_with_parity(h_min, h_parity)
        if expr.p < 0:
            raise AssertionError(f"negative P coefficient in {label}: {expr}")
        least_bracket = expr.p * (2**h0) + expr.z
        if least_bracket < 0:
            raise AssertionError(f"negative arm bracket in {label}: {expr}")
        least_value = (2**d0) * least_bracket + expr.c
        if least_value < 0:
            raise AssertionError(f"negative arm endpoint in {label}: {expr}")
        self.arm_inequalities += 1
        self.record(
            f"ARM|{label}|{expr.canonical()}|d>={d_min}:{d_parity}|"
            f"h>={h_min}:{h_parity}|d0={d0}|h0={h0}|"
            f"bracket={least_bracket}|value={least_value}"
        )

    def prove_k_nonnegative(
        self,
        expr: Affine,
        *,
        k_min: int,
        k_parity: int,
        label: str,
    ) -> None:
        """Prove a*2**k+c>=0 on one parity class, k>=k_min."""
        if expr.z != 0:
            raise AssertionError(f"uneliminated Z in {label}: {expr}")
        k0 = first_with_parity(k_min, k_parity)
        if expr.p < 0:
            raise AssertionError(f"negative P coefficient in {label}: {expr}")
        least_value = expr.p * (2**k0) + expr.c
        if least_value < 0:
            raise AssertionError(f"negative k endpoint in {label}: {expr}")
        self.k_inequalities += 1
        self.record(
            f"K|{label}|{expr.canonical()}|k>={k_min}:{k_parity}|"
            f"k0={k0}|value={least_value}"
        )


def bellman_differences(
    source: tuple[tuple[Affine, Affine, Affine], ...],
    parent: tuple[tuple[Affine, Affine, Affine], ...],
) -> list[tuple[str, Affine]]:
    """Return every children-minus-parent Bellman difference."""
    splits = ((0, 0, 0), (1, 0, 1), (2, 0, 2), (3, 0, 3), (3, 1, 2))
    result: list[tuple[str, Affine]] = []
    for parent_mask, left_mask, right_mask in splits:
        for left_residue, right_residue in itertools.product(range(3), repeat=2):
            parent_residue = (left_residue + right_residue) % 3
            difference = (
                source[left_mask][left_residue]
                + source[right_mask][right_residue]
                - parent[parent_mask][parent_residue]
            )
            label = (
                f"m{parent_mask}={left_mask}+{right_mask}:"
                f"r{parent_residue}={left_residue}+{right_residue}"
            )
            result.append((label, difference))
    return result


def prove_arm_edge(
    ledger: ProofLedger,
    low_rows: tuple[tuple[Affine, Affine, Affine], ...],
    high_rows: tuple[tuple[Affine, Affine, Affine], ...],
    *,
    d_min: int,
    h_min: int,
    d_parity: int,
    h_parity: int,
    edge_label: str,
) -> None:
    for direction, source, parent in (
        ("up", low_rows, high_rows),
        ("down", high_rows, low_rows),
    ):
        for local_label, difference in bellman_differences(source, parent):
            ledger.prove_arm_nonnegative(
                difference,
                d_min=d_min,
                h_min=h_min,
                d_parity=d_parity,
                h_parity=h_parity,
                label=f"{edge_label}:{direction}:{local_label}",
            )


def prove_k_edge(
    ledger: ProofLedger,
    rows_a: tuple[tuple[Affine, Affine, Affine], ...],
    rows_b: tuple[tuple[Affine, Affine, Affine], ...],
    *,
    k_min: int,
    k_parity: int,
    edge_label: str,
) -> None:
    for direction, source, parent in (
        ("a_to_b", rows_a, rows_b),
        ("b_to_a", rows_b, rows_a),
    ):
        for local_label, difference in bellman_differences(source, parent):
            ledger.prove_k_nonnegative(
                difference,
                k_min=k_min,
                k_parity=k_parity,
                label=f"{edge_label}:{direction}:{local_label}",
            )


def empty_root_options(row_zero: tuple[Affine, Affine, Affine]) -> list[tuple[int, Affine]]:
    """All zero-, one-, or two-tree no-singleton forest options."""
    options = [(0, ZERO)]
    options.extend((residue, row_zero[residue]) for residue in range(3))
    options.extend(
        (
            (left_residue + right_residue) % 3,
            row_zero[left_residue] + row_zero[right_residue],
        )
        for left_residue, right_residue in itertools.product(range(3), repeat=2)
    )
    return options


def forest_differences(
    rows: tuple[tuple[Affine, Affine, Affine], ...],
    *,
    target_residue: int,
    required: Affine,
) -> list[tuple[str, Affine]]:
    """Enumerate every reduced ancestry-forest decomposition."""
    specials: list[tuple[int, Affine, str]] = [
        (residue, rows[3][residue], f"together:r{residue}")
        for residue in range(3)
    ]
    specials.extend(
        (
            (left_residue + right_residue) % 3,
            rows[1][left_residue] + rows[2][right_residue],
            f"separate:r{left_residue}+{right_residue}",
        )
        for left_residue, right_residue in itertools.product(range(3), repeat=2)
    )
    result: list[tuple[str, Affine]] = []
    for special_residue, special_cost, special_label in specials:
        for empty_residue, empty_cost in empty_root_options(rows[0]):
            if (special_residue + empty_residue) % 3 != target_residue:
                continue
            result.append(
                (
                    f"{special_label}:empty_r{empty_residue}",
                    special_cost + empty_cost - required,
                )
            )
    return result


def validate_rows_and_bases(ledger: ProofLedger) -> None:
    # Generic nonnegativity.  Parity cases also invoke residue_row and hence
    # certify that every displayed triple has exactly one entry per residue.
    for d_parity, h_parity in itertools.product(range(2), repeat=2):
        k_parity = (d_parity + h_parity) % 2
        for side, rows, d_min, h_min in (
            ("left", left_generic_rows(k_parity, d_parity), 0, 1),
            ("right", right_generic_rows(k_parity, d_parity), 1, 2),
        ):
            ledger.residue_rows += 4
            for mask, residue in itertools.product(range(4), range(3)):
                ledger.prove_arm_nonnegative(
                    rows[mask][residue],
                    d_min=d_min,
                    h_min=h_min,
                    d_parity=d_parity,
                    h_parity=h_parity,
                    label=f"nonnegative:{side}:m{mask}:r{residue}",
                )

    for k_parity in range(2):
        for name, rows in (
            ("left_x", left_special_rows(k_parity)),
            ("right_y", right_y_rows(k_parity)),
            ("right_middle", right_middle_rows(k_parity)),
        ):
            ledger.residue_rows += 4
            for mask, residue in itertools.product(range(4), range(3)):
                ledger.prove_k_nonnegative(
                    rows[mask][residue],
                    k_min=3,
                    k_parity=k_parity,
                    label=f"nonnegative:{name}:m{mask}:r{residue}",
                )

    # The three one-leaf bases: pile at L_0, singleton x at L_k, singleton y
    # at R_(k-1).  These are identities, checked in both k parities.
    for k_parity in range(2):
        left_zero = fixed_z_rows(left_generic_rows(k_parity, 0), 1)
        left_x = left_special_rows(k_parity)
        right_y = right_y_rows(k_parity)
        bases = (
            left_zero[0][1] - ONE,
            left_x[1][0],
            right_y[2][0],
        )
        if bases != (ZERO, ZERO, ZERO):
            raise AssertionError(f"leaf-base identity failed in parity {k_parity}")
        ledger.record(f"BASE|kpar={k_parity}|pile=1|x=0|y=0")


def validate_bellman_inequalities(ledger: ProofLedger) -> None:
    # Infinite generic edges.  Z denotes 2**d at the lower-d endpoint, so the
    # upper-d endpoint is obtained by Z -> 2Z.
    for d_parity, h_parity in itertools.product(range(2), repeat=2):
        k_parity = (d_parity + h_parity) % 2
        left_low = left_generic_rows(k_parity, d_parity)
        left_high = scaled_rows(left_generic_rows(k_parity, 1 - d_parity), 2)
        prove_arm_edge(
            ledger,
            left_low,
            left_high,
            d_min=0,
            h_min=2,
            d_parity=d_parity,
            h_parity=h_parity,
            edge_label="left_generic_d_to_d+1",
        )

        right_low = right_generic_rows(k_parity, d_parity)
        right_high = scaled_rows(right_generic_rows(k_parity, 1 - d_parity), 2)
        prove_arm_edge(
            ledger,
            right_low,
            right_high,
            d_min=1,
            h_min=3,
            d_parity=d_parity,
            h_parity=h_parity,
            edge_label="right_generic_d_to_d+1",
        )

    # The cycle edge L_0--R_1 and the four center-transition edge types.
    for k_parity in range(2):
        left_zero = fixed_z_rows(left_generic_rows(k_parity, 0), 1)
        right_one = fixed_z_rows(right_generic_rows(k_parity, 1), 2)
        prove_k_edge(
            ledger,
            left_zero,
            right_one,
            k_min=3,
            k_parity=k_parity,
            edge_label="pile_seam_L0_R1",
        )

        left_h1 = fixed_h_rows(
            left_generic_rows(k_parity, (k_parity - 1) % 2), 1
        )
        left_x = left_special_rows(k_parity)
        prove_k_edge(
            ledger,
            left_h1,
            left_x,
            k_min=3,
            k_parity=k_parity,
            edge_label="left_h1_to_x",
        )

        middle = right_middle_rows(k_parity)
        prove_k_edge(
            ledger,
            left_x,
            middle,
            k_min=3,
            k_parity=k_parity,
            edge_label="x_to_middle",
        )

        right_y = right_y_rows(k_parity)
        prove_k_edge(
            ledger,
            middle,
            right_y,
            k_min=3,
            k_parity=k_parity,
            edge_label="middle_to_y",
        )

        right_h2 = fixed_h_rows(
            right_generic_rows(k_parity, k_parity), 2
        )
        prove_k_edge(
            ledger,
            right_y,
            right_h2,
            k_min=3,
            k_parity=k_parity,
            edge_label="y_to_right_h2",
        )


def validate_forest_bounds(ledger: ProofLedger) -> None:
    threshold = Fraction(5, 2) * P - 3 * ONE
    outer_threshold = Fraction(5, 2) * P

    # Both infinite outer arms (h>=3).  The target residue is that of
    # M_k=5P/2-6, which equals the residue of the threshold.
    for d_parity, h_parity in itertools.product(range(2), repeat=2):
        k_parity = (d_parity + h_parity) % 2
        target_residue = expression_residue(threshold, k_parity, d_parity)
        for side, rows, d_min in (
            ("left", left_generic_rows(k_parity, d_parity), 0),
            ("right", right_generic_rows(k_parity, d_parity), 1),
        ):
            for label, difference in forest_differences(
                rows,
                target_residue=target_residue,
                required=outer_threshold,
            ):
                ledger.prove_arm_nonnegative(
                    difference,
                    d_min=d_min,
                    h_min=3,
                    d_parity=d_parity,
                    h_parity=h_parity,
                    label=f"forest_outer:{side}:{label}",
                )

    # The six central vertices are L_(k-2), L_(k-1), L_k, R_k,
    # R_(k-1), R_(k-2).  Their required bound is 5P/2-3.
    for k_parity in range(2):
        target_residue = expression_residue(threshold, k_parity, k_parity)
        central_rows = (
            (
                "left_h2",
                fixed_h_rows(left_generic_rows(k_parity, k_parity), 2),
            ),
            (
                "left_h1",
                fixed_h_rows(
                    left_generic_rows(k_parity, (k_parity - 1) % 2), 1
                ),
            ),
            ("left_x", left_special_rows(k_parity)),
            ("right_middle", right_middle_rows(k_parity)),
            ("right_y", right_y_rows(k_parity)),
            (
                "right_h2",
                fixed_h_rows(right_generic_rows(k_parity, k_parity), 2),
            ),
        )
        for name, rows in central_rows:
            for label, difference in forest_differences(
                rows,
                target_residue=target_residue,
                required=threshold,
            ):
                ledger.prove_k_nonnegative(
                    difference,
                    k_min=3,
                    k_parity=k_parity,
                    label=f"forest_central:{name}:{label}",
                )


def main() -> None:
    ledger = ProofLedger()
    validate_rows_and_bases(ledger)
    validate_bellman_inequalities(ledger)
    validate_forest_bounds(ledger)
    print("UNIVERSAL ODD-CYCLE CERTIFICATE VERIFIED FOR EVERY k >= 3")
    print(f"residue_rows={ledger.residue_rows}")
    print(f"arm_inequalities={ledger.arm_inequalities}")
    print(f"fixed_k_inequalities={ledger.k_inequalities}")
    print(f"proof_obligation_sha256={ledger.digest.hexdigest()}")


if __name__ == "__main__":
    main()
