#!/usr/bin/env python3
"""Independent arithmetic and DIMACS audit for the stabilized singleton branches."""

from __future__ import annotations

import hashlib
import sys
from collections import Counter, defaultdict
from pathlib import Path


DEGREES = tuple(range(18, 25))
WEIGHTS = (21, 12, 3, 0, 3, 12, 21)
TOTAL_WEIGHTS = tuple(range(3, 40, 6))
EXPECTED_PROFILE_ROWS = {
    214: (0, 0, 0, 0, 0, 0, 1),
    215: (0, 0, 0, 0, 0, 1, 4),
    216: (0, 0, 0, 0, 1, 4, 12),
    217: (0, 0, 0, 1, 4, 11, 24),
    218: (0, 0, 1, 4, 9, 19, 36),
    219: (0, 1, 3, 6, 13, 25, 47),
    220: (1, 2, 4, 9, 17, 32, 57),
}
EXPECTED_X = (0, 3, 6, 9, 12, 15, 18)
EXPECTED_TYPED_MANIFEST_SHA256 = (
    "e4ba765ae7bad943ea132d8a1ad37824840aea7e7ea3da29ec98c8521617cab2"
)
EXPECTED_STABILIZED_MANIFEST_SHA256 = (
    "ddf8c30014e35fbf005381078d1804089283d3cbddad5ef2c1cb1b36d91315cf"
)
EXPECTED_BASE_X0_SHA256 = (
    "53bb2e87936f68b468cabe69393f867033c8072f4b06987a037c3a93c6986b8c"
)
EXPECTED_STABILIZED_X0_SHA256 = (
    "aa24ffb7e81eb5c514ec8961b2df5fd4a9b15e453f16f31f8c2c349fbd9b2a35"
)


def compositions(total: int, length: int):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first, *tail)


def enumerate_profile_rows() -> dict[int, tuple[int, ...]]:
    profiles: dict[int, Counter[int]] = defaultdict(Counter)
    for counts in compositions(21, len(DEGREES)):
        deviation = sum(
            count * (degree - 21)
            for count, degree in zip(counts, DEGREES, strict=True)
        )
        weight = sum(
            count * value for count, value in zip(counts, WEIGHTS, strict=True)
        )
        profiles[deviation][weight] += 1

    rows = {}
    for cross_edges in range(214, 221):
        left = profiles[cross_edges - 220]
        right = profiles[cross_edges - 221]
        rows[cross_edges] = tuple(
            sum(
                left_weight_count * right[total_weight - left_weight]
                for left_weight, left_weight_count in left.items()
            )
            for total_weight in TOTAL_WEIGHTS
        )
    return rows


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_manifest(path: Path) -> dict[int, tuple[int, int, str]]:
    rows = {}
    for raw_line in path.read_text(encoding="ascii").splitlines():
        if not raw_line or raw_line.startswith("#"):
            continue
        x_text, variables_text, clauses_text, digest = raw_line.split()
        x = int(x_text)
        if x in rows:
            raise AssertionError(f"duplicate manifest branch x={x}")
        rows[x] = (int(variables_text), int(clauses_text), digest)
    return rows


def edge_var(first: int, second: int) -> int:
    """One-based lexicographic index of an edge of K_42."""
    if first > second:
        first, second = second, first
    if not 0 <= first < second < 42:
        raise ValueError((first, second))
    return 41 * first - first * (first - 1) // 2 + second - first


def expected_stabilizer_clauses() -> tuple[tuple[int, ...], ...]:
    z_cross = tuple(edge_var(vertex, 21) for vertex in range(21))
    c0_cross = tuple(edge_var(0, vertex) for vertex in range(22, 42))
    clauses = []
    clauses.extend((first, -second) for first, second in zip(z_cross, z_cross[1:]))
    clauses.extend((literal,) for literal in z_cross[:3])
    clauses.extend((-literal,) for literal in z_cross[13:])
    clauses.extend((first, -second) for first, second in zip(c0_cross, c0_cross[1:]))
    clauses.extend((literal,) for literal in c0_cross[:6])
    clauses.extend((-literal,) for literal in c0_cross[16:])
    return tuple(clauses)


def parse_dimacs_header(line: bytes) -> tuple[int, int]:
    fields = line.decode("ascii").split()
    if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
        raise AssertionError(f"bad DIMACS header: {line!r}")
    return int(fields[2]), int(fields[3])


def parse_clause(line: bytes) -> tuple[int, ...]:
    fields = tuple(map(int, line.split()))
    if not fields or fields[-1] != 0 or 0 in fields[:-1]:
        raise AssertionError(f"bad DIMACS clause: {line!r}")
    return fields[:-1]


def audit_dimacs_pair(base_path: Path, stabilized_path: Path) -> None:
    if sha256(base_path) != EXPECTED_BASE_X0_SHA256:
        raise AssertionError("base x=0 DIMACS digest mismatch")
    if sha256(stabilized_path) != EXPECTED_STABILIZED_X0_SHA256:
        raise AssertionError("stabilized x=0 DIMACS digest mismatch")

    with base_path.open("rb") as base, stabilized_path.open("rb") as stabilized:
        base_header = parse_dimacs_header(base.readline())
        stabilized_header = parse_dimacs_header(stabilized.readline())
        if base_header != (458107, 3782794):
            raise AssertionError(base_header)
        if stabilized_header != (458107, 3782854):
            raise AssertionError(stabilized_header)

        base_count = 0
        for base_line in base:
            stabilized_line = stabilized.readline()
            if base_line != stabilized_line:
                raise AssertionError(f"formula bodies diverge at clause {base_count + 1}")
            base_count += 1
        extra_lines = tuple(stabilized)

    if base_count != base_header[1]:
        raise AssertionError((base_count, base_header))
    extra_clauses = tuple(parse_clause(line) for line in extra_lines)
    if extra_clauses != expected_stabilizer_clauses():
        raise AssertionError("appended symmetry clauses differ from independent construction")
    if base_count + len(extra_clauses) != stabilized_header[1]:
        raise AssertionError("stabilized DIMACS body count differs from header")

    print(f"base_x0_dimacs_sha256={EXPECTED_BASE_X0_SHA256}")
    print(f"stabilized_x0_dimacs_sha256={EXPECTED_STABILIZED_X0_SHA256}")
    print("dimacs_common_prefix_clauses=3782794")
    print("dimacs_appended_clauses=60")
    print("cnf_stream_check=true")


def main() -> None:
    if len(sys.argv) not in (2, 4):
        raise SystemExit(
            "usage: audit_stabilized_branches.py SOURCE_DIR [BASE_X0_CNF STABILIZED_X0_CNF]"
        )
    source_dir = Path(sys.argv[1])

    profile_rows = enumerate_profile_rows()
    if profile_rows != EXPECTED_PROFILE_ROWS:
        raise AssertionError(profile_rows)
    profile_totals = tuple(sum(profile_rows[cross]) for cross in range(214, 221))
    if profile_totals != (1, 5, 17, 40, 69, 95, 122):
        raise AssertionError(profile_totals)

    # Independent singleton accounting.  The two global/internal counts
    # disagree by one for a red singleton and agree for a blue singleton.
    singleton_accounting = (451, 440, 220, 219, 220, 220)
    if singleton_accounting != (
        231 + 220,
        20 + 20 * 21,
        451 - 21 - 100 - 110,
        440 - 2 * 100 - 21,
        451 - 21 - 100 - 110,
        440 - 2 * 110,
    ):
        raise AssertionError(singleton_accounting)

    local_profiles = tuple(
        (x, (4293 - x) // 3, (4287 + x) // 3)
        for x in range(21)
        if (4293 - x) % 3 == (4287 + x) % 3 == 0
    )
    expected_local_profiles = tuple(
        (x, 1431 - x // 3, 1429 + x // 3) for x in EXPECTED_X
    )
    if local_profiles != expected_local_profiles:
        raise AssertionError(local_profiles)

    typed_path = source_dir / "SINGLETON_TYPED_BRANCHES.tsv"
    stabilized_path = source_dir / "SINGLETON_TYPED_STABILIZED_BRANCHES.tsv"
    if sha256(typed_path) != EXPECTED_TYPED_MANIFEST_SHA256:
        raise AssertionError("typed manifest digest mismatch")
    if sha256(stabilized_path) != EXPECTED_STABILIZED_MANIFEST_SHA256:
        raise AssertionError("stabilized manifest digest mismatch")
    typed = read_manifest(typed_path)
    stabilized = read_manifest(stabilized_path)
    if tuple(typed) != EXPECTED_X or tuple(stabilized) != EXPECTED_X:
        raise AssertionError((tuple(typed), tuple(stabilized)))
    for x in EXPECTED_X:
        if typed[x][:2] != (458107, 3782794):
            raise AssertionError(("typed", x, typed[x]))
        if stabilized[x][:2] != (458107, 3782854):
            raise AssertionError(("stabilized", x, stabilized[x]))
        if stabilized[x][1] - typed[x][1] != 60:
            raise AssertionError(("delta", x))

    symmetry_clauses = expected_stabilizer_clauses()
    if len(symmetry_clauses) != 60:
        raise AssertionError(len(symmetry_clauses))
    monotonic = sum(len(clause) == 2 for clause in symmetry_clauses)
    units = sum(len(clause) == 1 for clause in symmetry_clauses)
    if (monotonic, units) != (39, 21):
        raise AssertionError((monotonic, units))

    print("profile_counts_by_M=" + ",".join(map(str, profile_totals)))
    print(f"profile_total={sum(profile_totals)}")
    print("hard_escape_degree_multiset=20^1,21^42")
    print("red_singleton_cross_counts=220,219")
    print("blue_singleton_cross_counts=220,220")
    print("singleton_x_values=" + ",".join(map(str, EXPECTED_X)))
    print(
        "singleton_triangle_pairs="
        + ";".join(f"{red},{blue}" for _, red, blue in local_profiles)
    )
    print("typed_manifest_rows=7")
    print("typed_branch_variables=458107")
    print("typed_branch_clauses=3782794")
    print("stabilized_branch_variables=458107")
    print("stabilized_branch_clauses=3782854")
    print("stabilizer_clause_delta=60")
    print("stabilizer_clause_split=39_monotonic,21_unit")

    if len(sys.argv) == 4:
        audit_dimacs_pair(Path(sys.argv[2]), Path(sys.argv[3]))
    else:
        print("cnf_stream_check=skipped")
    print("independent_checks=true")


if __name__ == "__main__":
    main()
