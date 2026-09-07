#!/usr/bin/env python3
"""Independent audit of the full-support rank-four completion exclusion.

No target Python module is imported.  Orbit coverage is checked with a direct
enumeration of all invertible 4-by-4 binary matrices, Burnside's lemma, and
lexicographic canonicalization.  Selected CNFs are reconstructed both from
the definition over all five-sets and from the cut decomposition.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path


N = 43
LEFT = 20
STABLE_FIELDS = (
    "orbit_index",
    "row_doubles",
    "column_doubles",
    "variables",
    "clauses",
    "cnf_bytes",
    "cnf_sha256",
    "proof_bytes",
    "proof_sha256",
    "status",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def dot(x: int, y: int) -> int:
    return (x & y).bit_count() & 1


def rank(vectors: tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        value = vector
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)


def image(images: tuple[int, ...], value: int) -> int:
    answer = 0
    for bit, basis_image in enumerate(images):
        if value >> bit & 1:
            answer ^= basis_image
    return answer


def all_gl4() -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Enumerate GL(4,2) by all 2^16 matrices, with the dual action."""
    result = []
    for code in range(1 << 16):
        images = tuple((code >> (4 * bit)) & 15 for bit in range(4))
        if rank(images) != 4:
            continue
        row = tuple(image(images, value) for value in range(16))
        column = [0] * 16
        for candidate in range(16):
            source = sum(dot(images[bit], candidate) << bit for bit in range(4))
            column[source] = candidate
        require(sorted(row) == list(range(16)), "row action is not a permutation")
        require(sorted(column) == list(range(16)), "dual action is not a permutation")
        require(
            all(dot(row[x], column[y]) == dot(x, y)
                for x in range(16) for y in range(16)),
            "duality failure",
        )
        result.append((row, tuple(column)))
    require(len(result) == 20_160, "incorrect GL(4,2) order")
    return tuple(result)


def subset_mask(values) -> int:
    return sum(1 << (value - 1) for value in values)


def mask_values(mask: int) -> tuple[int, ...]:
    return tuple(value for value in range(1, 16) if mask >> (value - 1) & 1)


def act(mask: int, permutation: tuple[int, ...]) -> int:
    return subset_mask(permutation[value] for value in mask_values(mask))


AFFINE_MASKS = {
    subset_mask(y for y in range(1, 16) if dot(w, y))
    for w in range(1, 16)
}


def fixed_subsets(permutation: tuple[int, ...], size: int) -> int:
    seen: set[int] = set()
    cycle_lengths = []
    for start in range(1, 16):
        if start in seen:
            continue
        value = start
        length = 0
        while value not in seen:
            seen.add(value)
            value = permutation[value]
            length += 1
        cycle_lengths.append(length)
    coefficients = [0] * (size + 1)
    coefficients[0] = 1
    for length in cycle_lengths:
        for occupied in range(size, length - 1, -1):
            coefficients[occupied] += coefficients[occupied - length]
    return coefficients[size]


def stable_rows(rows: list[dict]) -> list[dict]:
    return [
        {field: row[field] for field in STABLE_FIELDS}
        for row in sorted(rows, key=lambda item: item["orbit_index"])
    ]


def stable_digest(rows: list[dict]) -> str:
    raw = (json.dumps(stable_rows(rows), sort_keys=True, separators=(",", ":")) + "\n").encode()
    return sha256(raw).hexdigest()


def load_proof_rows(target: Path) -> list[dict]:
    rows = []
    for shard in range(4):
        path = target / f"proof_manifest_shard{shard}.jsonl"
        rows.extend(json.loads(line) for line in path.read_text().splitlines())
    rows.sort(key=lambda item: item["orbit_index"])
    require([row["orbit_index"] for row in rows] == list(range(1348)),
            "proof indices do not cover 0..1347")
    require(all(row["status"] == "UNSAT_PROOF_VERIFIED" for row in rows),
            "unverified proof status")
    require(all(row["variables"] == 443 for row in rows), "variable-count mismatch")
    require(len({row["cnf_sha256"] for row in rows}) == 1348,
            "duplicate CNF hash")
    require(len({row["proof_sha256"] for row in rows}) == 1348,
            "duplicate proof hash")
    return rows


def orbit_audit(rows: list[dict]) -> dict[str, object]:
    group = all_gl4()
    burnside_rows = 0
    burnside_pairs = 0
    for row_action, column_action in group:
        fixed_rows = fixed_subsets(row_action, 5)
        fixed_affine_columns = sum(row_action[w] == w for w in range(1, 16))
        fixed_nonaffine_columns = fixed_subsets(column_action, 8) - fixed_affine_columns
        require(fixed_nonaffine_columns >= 0, "negative nonaffine fixed-set count")
        burnside_rows += fixed_rows
        burnside_pairs += fixed_rows * fixed_nonaffine_columns
    require(burnside_rows % len(group) == burnside_pairs % len(group) == 0,
            "nonintegral Burnside quotient")
    require(burnside_rows // len(group) == 4, "row Burnside count")
    require(burnside_pairs // len(group) == 1348, "pair Burnside count")

    row_masks = sorted({subset_mask(row["row_doubles"]) for row in rows})
    require(len(row_masks) == 4, "manifest row representative count")
    canonical_pairs = set()
    row_orbit_sizes = []
    canonical_row_masks = []
    counts = Counter(subset_mask(row["row_doubles"]) for row in rows)
    blocks = {}
    for row_mask in row_masks:
        row_images = [act(row_mask, row_action) for row_action, _ in group]
        canonical_row = min(row_images)
        normalizers = [index for index, value in enumerate(row_images)
                       if value == canonical_row]
        row_orbit_sizes.append(len(set(row_images)))
        canonical_row_masks.append(canonical_row)
        block_canonicals = set()
        for entry in rows:
            if subset_mask(entry["row_doubles"]) != row_mask:
                continue
            column_mask = subset_mask(entry["column_doubles"])
            require(column_mask not in AFFINE_MASKS, "affine column in new family")
            canonical_column = min(act(column_mask, group[index][1])
                                   for index in normalizers)
            canonical = (canonical_row, canonical_column)
            require(canonical not in canonical_pairs, "equivalent manifest representatives")
            canonical_pairs.add(canonical)
            block_canonicals.add(canonical_column)
        blocks[str(mask_values(row_mask))] = len(block_canonicals)
        require(counts[row_mask] == len(block_canonicals), "row-block duplicate")
    require(len(set(canonical_row_masks)) == 4, "row representatives are equivalent")
    require(len(canonical_pairs) == 1348, "canonical pair count")

    pair_sets = comb(15, 5) * (comb(15, 8) - len(AFFINE_MASKS))
    require(pair_sets == 19_279_260, "family-size arithmetic")
    return {
        "method": "all 2^16 matrices, Burnside lemma, lexicographic canonicalization",
        "gl4_size": len(group),
        "affine_eight_sets": len(AFFINE_MASKS),
        "row_orbits_burnside": burnside_rows // len(group),
        "row_orbit_sizes": sorted(row_orbit_sizes),
        "pair_orbits_burnside": burnside_pairs // len(group),
        "canonical_manifest_pairs": len(canonical_pairs),
        "manifest_blocks": blocks,
        "pair_sets": pair_sets,
    }


PAIRS = list(combinations(range(N), 2))
INTERNAL = [pair for pair in PAIRS if (pair[0] < LEFT) == (pair[1] < LEFT)]
VARIABLE = {pair: index + 1 for index, pair in enumerate(INTERNAL)}


def factor_lists(entry: dict) -> tuple[list[int], list[int]]:
    rows = list(range(1, 16)) + entry["row_doubles"]
    columns = list(range(1, 16)) + entry["column_doubles"]
    require(len(rows) == 20 and len(columns) == 23, "factor-list sizes")
    return rows, columns


def clause_key(vertices: tuple[int, ...], red: bool) -> tuple[int, ...]:
    variables = [VARIABLE[pair] for pair in combinations(vertices, 2)
                 if pair in VARIABLE]
    require(variables, "empty physical Ramsey clause")
    sign = -1 if red else 1
    return tuple(sign * variable for variable in variables)


def cross_colour(u: int, v: int, rows: list[int], columns: list[int]) -> int:
    if u >= LEFT:
        u, v = v, u
    require(u < LEFT <= v, "cross edge expected")
    return dot(rows[u], columns[v - LEFT])


def clauses_by_definition(rows: list[int], columns: list[int]) -> Counter:
    clauses: Counter = Counter()
    for vertices in combinations(range(N), 5):
        cross = [cross_colour(u, v, rows, columns)
                 for u, v in combinations(vertices, 2)
                 if (u < LEFT) != (v < LEFT)]
        if all(cross):
            clauses[clause_key(vertices, True)] += 1
        if not any(cross):
            clauses[clause_key(vertices, False)] += 1
    return clauses


def clauses_by_cut(rows: list[int], columns: list[int]) -> Counter:
    clauses: Counter = Counter()
    sides = (range(LEFT), range(LEFT, N))
    for side in sides:
        for vertices in combinations(side, 5):
            clauses[clause_key(vertices, True)] += 1
            clauses[clause_key(vertices, False)] += 1
    for left_size in range(1, 5):
        right_size = 5 - left_size
        for left_vertices in combinations(range(LEFT), left_size):
            for right_vertices in combinations(range(LEFT, N), right_size):
                cross = [cross_colour(u, v, rows, columns)
                         for u in left_vertices for v in right_vertices]
                vertices = tuple(left_vertices + right_vertices)
                if all(cross):
                    clauses[clause_key(vertices, True)] += 1
                if not any(cross):
                    clauses[clause_key(vertices, False)] += 1
    return clauses


def formula_audit(rows: list[dict]) -> dict[str, object]:
    by_row = {}
    for entry in rows:
        by_row.setdefault(tuple(entry["row_doubles"]), entry["orbit_index"])
    minimum = min(rows, key=lambda entry: entry["clauses"])["orbit_index"]
    maximum = max(rows, key=lambda entry: entry["clauses"])["orbit_index"]
    selected = sorted(set(by_row.values()) | {minimum, maximum})
    results = []
    for index in selected:
        entry = rows[index]
        factors = factor_lists(entry)
        direct = clauses_by_definition(*factors)
        split = clauses_by_cut(*factors)
        require(direct == split, f"physical/split clause disagreement at {index}")
        require(direct.total() == entry["clauses"], f"manifest clause count at {index}")
        results.append({
            "orbit_index": index,
            "clauses": direct.total(),
            "distinct_clause_lines": len(direct),
        })
    return {
        "variables": len(INTERNAL),
        "five_sets_per_reference_case": comb(43, 5),
        "reference_cases": len(selected),
        "selected": results,
    }


def manifest_audit(target: Path, rows: list[dict]) -> dict[str, object]:
    manifest_entries = {}
    for line in (target / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        require(name not in manifest_entries and "/" not in name, "package manifest shape")
        manifest_entries[name] = digest
    files = {path.name for path in target.iterdir() if path.is_file()}
    require(set(manifest_entries) == files - {"SHA256SUMS"}, "package manifest coverage")
    for name, digest in manifest_entries.items():
        require(sha256((target / name).read_bytes()).hexdigest() == digest,
                f"package digest: {name}")
    totals = {
        "clauses": sum(row["clauses"] for row in rows),
        "cnf_bytes": sum(row["cnf_bytes"] for row in rows),
        "proof_bytes": sum(row["proof_bytes"] for row in rows),
    }
    require(totals == {
        "clauses": 190_848_992,
        "cnf_bytes": 7_481_258_038,
        "proof_bytes": 1_124_629_092,
    }, "manifest aggregate totals")
    digest = stable_digest(rows)
    require(digest == "744c2ced26ee6794f7a81d65f1f5250842c0230b40e96ce4dd89438ac658020a",
            "stable proof-record digest")
    return {
        "package_files": len(files),
        "package_bytes": sum(path.stat().st_size for path in target.iterdir() if path.is_file()),
        "proof_records": len(rows),
        "stable_record_sha256": digest,
        **totals,
    }


def replay_audit(review_root: Path, target_rows: list[dict], replay_manifest: Path | None):
    record = json.loads((review_root / "REPLAY.json").read_text())
    claimed = record["full_replay"]
    require(claimed["stable_record_sha256"] == stable_digest(target_rows),
            "replay/target stable digest")
    require(claimed["records"] == len(target_rows) == 1348, "replay record count")
    require(claimed["all_stable_fields_match"], "fresh replay comparison not successful")
    if replay_manifest is not None:
        raw = replay_manifest.read_bytes()
        fresh = [json.loads(line) for line in raw.splitlines()]
        require(stable_rows(fresh) == stable_rows(target_rows),
                "supplied fresh replay differs entrywise")
        require(sha256(raw).hexdigest() == claimed["raw_manifest_sha256"],
                "fresh replay raw-manifest digest")
    return record


def audit(target: Path, replay_manifest: Path | None) -> dict[str, object]:
    rows = load_proof_rows(target)
    root = Path(__file__).resolve().parent
    return {
        "verified": True,
        "status": "INDEPENDENT_FULL_SUPPORT_RANK4_ACCEPTANCE",
        "orbit_coverage": orbit_audit(rows),
        "formula_soundness": formula_audit(rows),
        "target_evidence": manifest_audit(target, rows),
        "fresh_full_replay": replay_audit(root, rows, replay_manifest),
        "scope": {
            "fixed_partition": [20, 23],
            "red_cross_rank": 4,
            "all_nonzero_labels_present": True,
            "row_labels_doubled": 5,
            "column_labels_doubled": 8,
            "nonaffine_column_family_excluded_here": True,
            "affine_column_family_imported_from_h3757_h3761": True,
            "internal_edges_free": 443,
            "all_rank4_profiles_excluded": False,
            "good43_existence_decided": False,
            "ramsey_bound_improved": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent.parent /
        "ramsey_r55_rank4_full_support_completion",
    )
    parser.add_argument("--replay-manifest", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit(args.target, args.replay_manifest)
    if args.check_expected:
        expected = json.loads((Path(__file__).resolve().parent / "EXPECTED.json").read_text())
        require(result == expected, "expected-output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
