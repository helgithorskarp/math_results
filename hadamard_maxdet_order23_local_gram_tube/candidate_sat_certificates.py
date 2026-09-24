#!/usr/bin/env python3
"""Generate exact SAT instances for the two exceptional Gram obstructions.

For a scaled inverse ``G^{-1}=P/Q`` and a sign vector
``v_i=(-1)^x_i``, introduce ``y_ij=x_i xor x_j``.  Then

    v^T P v = q_plus - 4 sum_{i<j} P_ij y_ij,

where ``q_plus`` is the value at the all-plus vector.  Thus the necessary
column equation is one exact weighted Boolean equality.  This script emits
Tseitin CNFs for that equality using a ripple-adder network.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from candidate_obstructions import (
    CANDIDATES,
    ORDER,
    candidate_gram,
    gram_matrix,
    read_record,
    scaled_inverse,
)


EXPECTED_CNF = {
    "candidate1_no_column": (
        25541, 88213,
        "1b4feba975193380c1e0d7e5b161c43e6a87454dadbd373b3accb3ea9c727019",
    ),
    "candidate2_forbidden_product": (
        24689, 85298,
        "2af668ee1f3ae525cde318ded8ba5989249c4a2ff1c31ca71e2ade27ca31f822",
    ),
    "candidate2_admissible_control": (
        24689, 85297,
        "383532438d208952cd5bee6a844fd8f0887f212c202179a1149b8fa23e7b2248",
    ),
}


@dataclass
class CNF:
    variable_count: int = 0
    clauses: list[list[int]] | None = None

    def __post_init__(self) -> None:
        if self.clauses is None:
            self.clauses = []

    def new_variable(self) -> int:
        self.variable_count += 1
        return self.variable_count

    def add_clause(self, *literals: int) -> None:
        assert self.clauses is not None
        assert all(literal != 0 for literal in literals)
        self.clauses.append(list(literals))

    def xor(self, left: int, right: int) -> int:
        """Return a fresh variable equivalent to left XOR right."""
        result = self.new_variable()
        self.add_clause(left, right, -result)
        self.add_clause(-left, -right, -result)
        self.add_clause(left, -right, result)
        self.add_clause(-left, right, result)
        return result

    def conjunction(self, left: int, right: int) -> int:
        """Return a fresh variable equivalent to left AND right."""
        result = self.new_variable()
        self.add_clause(-left, -right, result)
        self.add_clause(left, -result)
        self.add_clause(right, -result)
        return result

    def disjunction(self, left: int, right: int) -> int:
        """Return a fresh variable equivalent to left OR right."""
        result = self.new_variable()
        self.add_clause(left, right, -result)
        self.add_clause(-left, result)
        self.add_clause(-right, result)
        return result

    def add_boolean_bits(self, inputs: list[int]) -> tuple[int | None, int | None]:
        """Return the sum and carry literals for two or three Boolean inputs."""
        assert 0 <= len(inputs) <= 3
        if not inputs:
            return None, None
        if len(inputs) == 1:
            return inputs[0], None
        partial = self.xor(inputs[0], inputs[1])
        carry_left = self.conjunction(inputs[0], inputs[1])
        if len(inputs) == 2:
            return partial, carry_left
        result = self.xor(partial, inputs[2])
        carry_right = self.conjunction(partial, inputs[2])
        carry = self.disjunction(carry_left, carry_right)
        return result, carry


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def render_dimacs(cnf: CNF) -> bytes:
    assert cnf.clauses is not None
    lines = [f"p cnf {cnf.variable_count} {len(cnf.clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in cnf.clauses)
    return "".join(lines).encode("ascii")


def add_conditional_weight(
    cnf: CNF,
    accumulator: list[int | None],
    condition: int,
    weight: int,
) -> list[int | None]:
    """Add ``weight * condition`` to a little-endian Boolean accumulator."""
    assert weight > 0
    answer: list[int | None] = []
    carry: int | None = None
    for bit, old in enumerate(accumulator):
        inputs = [literal for literal in (old, carry) if literal is not None]
        if (weight >> bit) & 1:
            inputs.append(condition)
        result, carry = cnf.add_boolean_bits(inputs)
        answer.append(result)
    if carry is not None:
        # The chosen width is the bit length of the sum of every coefficient,
        # so overflow is impossible for a valid gate assignment.
        cnf.add_clause(-carry)
    return answer


def build_instance(
    numerator: list[list[int]],
    scale: int,
    force_x1: bool,
) -> tuple[bytes, dict[str, object]]:
    cnf = CNF()
    # x_i=1 means v_i=-1.  Column negation fixes x_0=0, so it needs no variable.
    x_variables: list[int | None] = [None]
    x_variables.extend(cnf.new_variable() for _ in range(1, ORDER))

    weighted_literals: list[tuple[int, int]] = []
    for left in range(ORDER):
        for right in range(left):
            assert x_variables[left] is not None
            if right == 0:
                parity = x_variables[left]
            else:
                assert x_variables[right] is not None
                parity = cnf.xor(x_variables[left], x_variables[right])
            weight = numerator[left][right]
            assert weight != 0
            weighted_literals.append((parity if weight > 0 else -parity, abs(weight)))

    q_plus = sum(map(sum, numerator))
    difference = q_plus - scale
    assert difference % 4 == 0
    original_target = difference // 4
    negative_shift = sum(
        -numerator[left][right]
        for left in range(ORDER)
        for right in range(left)
        if numerator[left][right] < 0
    )
    target = original_target + negative_shift
    maximum = sum(weight for _, weight in weighted_literals)
    assert 0 <= target <= maximum
    width = maximum.bit_length()

    accumulator: list[int | None] = [None] * width
    for literal, weight in weighted_literals:
        accumulator = add_conditional_weight(cnf, accumulator, literal, weight)
    for bit, literal in enumerate(accumulator):
        desired = (target >> bit) & 1
        if literal is None:
            if desired:
                cnf.add_clause()
        else:
            cnf.add_clause(literal if desired else -literal)

    if force_x1:
        assert x_variables[1] is not None
        cnf.add_clause(x_variables[1])

    data = render_dimacs(cnf)
    metadata: dict[str, object] = {
        "variables": cnf.variable_count,
        "clauses": len(cnf.clauses or []),
        "input_variables_x1_through_x22": x_variables[1:],
        "force_x1": force_x1,
        "scale": scale,
        "q_all_plus": q_plus,
        "original_signed_target": original_target,
        "negative_weight_shift": negative_shift,
        "nonnegative_target": target,
        "maximum_weight_sum": maximum,
        "adder_width": width,
        "cnf_sha256": sha256(data),
    }
    return data, metadata


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 candidate_sat_certificates.py OUTPUT_DIR")
    output = Path(sys.argv[1])
    output.mkdir(parents=True, exist_ok=True)

    base = gram_matrix(read_record())
    specifications = (
        ("candidate1_no_column", 0, False, "UNSAT"),
        ("candidate2_forbidden_product", 1, True, "UNSAT"),
        ("candidate2_admissible_control", 1, False, "SAT"),
    )
    instances = []
    for name, candidate_index, force_x1, expected in specifications:
        candidate = CANDIDATES[candidate_index]
        matrix = candidate_gram(base, candidate["edges"])
        scale, numerator = scaled_inverse(matrix)
        assert scale == candidate["inverse_scale"]
        data, metadata = build_instance(numerator, scale, force_x1)
        assert (
            metadata["variables"],
            metadata["clauses"],
            metadata["cnf_sha256"],
        ) == EXPECTED_CNF[name]
        path = output / f"{name}.cnf"
        path.write_bytes(data)
        instances.append(
            {
                "name": name,
                "candidate_index": candidate_index + 1,
                "candidate_edges": list(candidate["edges"]),
                "candidate_determinant_root": candidate["determinant_root"],
                "mathematical_condition": (
                    "v^T P v = Q and v_0 v_1 = -1"
                    if force_x1
                    else "v^T P v = Q"
                ),
                "expected_status": expected,
                **metadata,
            }
        )

    manifest = {
        "order": ORDER,
        "normalization": "v_0=1; x_i=1 means v_i=-1",
        "instances": instances,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
