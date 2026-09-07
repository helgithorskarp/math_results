#!/usr/bin/env python3
"""Independent compact audit of the row-triple/support-band exclusion.

This module deliberately imports none of the production enumerator or CNF
generator.  It reconstructs GL(4,2) from ordered bases, redoes the orbit
partition, derives the CNF dimensions analytically, and audits the single
checked proof record.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import comb
from pathlib import Path
import re
import sys


HEX64 = re.compile(r"[0-9a-f]{64}")


def binary_rank(values):
    basis = {}
    for value in values:
        current = value
        while current:
            pivot = current.bit_length() - 1
            if pivot in basis:
                current ^= basis[pivot]
            else:
                basis[pivot] = current
                break
    return len(basis)


def map_value(images, value):
    result = 0
    for bit, image in enumerate(images):
        if value & (1 << bit):
            result ^= image
    return result


def all_linear_maps():
    maps = []
    for images in permutations(range(1, 16), 4):
        if binary_rank(images) == 4:
            maps.append(tuple(map_value(images, value) for value in range(16)))
    return maps


def image_mask(mask, transformation):
    result = 0
    for value in range(1, 16):
        if mask & (1 << (value - 1)):
            result |= 1 << (transformation[value] - 1)
    return result


def dual_map(transformation):
    images = [0] * 16
    for candidate in range(16):
        source = sum(((transformation[1 << i] & candidate).bit_count() & 1) << i
                     for i in range(4))
        images[source] = candidate
    for x in range(16):
        for y in range(16):
            left = (transformation[x] & images[y]).bit_count() & 1
            right = (x & y).bit_count() & 1
            if left != right:
                raise RuntimeError("inverse-transpose action failure")
    return tuple(images)


def values(mask):
    return [value for value in range(1, 16) if mask & (1 << (value - 1))]


def at_most_dimensions(n, bound):
    if bound >= n:
        return 0, 0
    if bound < 0:
        return 0, 1
    if bound == 0:
        return 0, n
    return (n - 1) * bound, bound * (2 * n - 3) + n - 1


def bounded_compositions(parts, total, cap):
    return sum(sum(entry) == total for entry in product(range(1, cap + 1),
                                                        repeat=parts))


def independent_formula_dimensions(canonical_supports, symmetry_clauses,
                                   support_maximum=None):
    # Variable blocks before cardinality encodings.
    variables = 443 + 23 * 16 + 15 * 23 + 15
    clauses = {
        "one_hot_columns": 23 * (1 + comb(16, 2)),
        "sorted_columns": 22 * sum(range(1, 16)),
        "zero_forbidden_on_columns": 23,
        "nonzero_multiplicity_cap_five": 15 * 18,
        "support_equivalences": 15 * 24,
        "support_symmetry": symmetry_clauses,
        "column_span_four": 15,
        "contact_truth_tables": 15 * 23 * 16,
    }
    if support_maximum is not None:
        aux, card_clauses = at_most_dimensions(15, support_maximum)
        variables += aux
        clauses["support_upper_bound"] = card_clauses

    # Two tripled row labels, each with contact count in [10,13].
    aux, card_clauses = at_most_dimensions(23, 13)
    variables += 2 * 2 * aux
    clauses["tripled_row_contacts"] = 2 * 2 * card_clauses

    # Each tripled row class has three physical pairs.  For each pair, 18 XOR
    # bits are defined and at least eight must be true.
    aux, card_clauses = at_most_dimensions(18, 10)
    variables += 6 * (18 + aux)
    clauses["equal_row_pair_distance"] = 6 * (4 * 18 + card_clauses)

    # Every one of C(23,2) column pairs has an equality gate, 21 XOR bits, and
    # a gated at-least-eight constraint.
    aux, card_clauses = at_most_dimensions(21, 13)
    variables += comb(23, 2) * (1 + 21 + aux)
    clauses["equal_column_pair_distance"] = comb(23, 2) * (
        16 + 4 * 21 + card_clauses
    )

    # The zero row has 19 variable incident edges.  The other A vertices have
    # 42, and B vertices have 41 because their edge to the zero row is blue.
    degree_variables = 0
    degree_clauses = 0
    for count, incident in ((1, 19), (19, 42), (23, 41)):
        lower_aux, lower_clauses = at_most_dimensions(incident, incident - 18)
        upper_aux, upper_clauses = at_most_dimensions(incident, 24)
        degree_variables += count * (lower_aux + upper_aux)
        degree_clauses += count * (lower_clauses + upper_clauses)
    variables += degree_variables
    clauses["degree_18_24"] = degree_clauses

    # Every five-set receives a blue-K5 prevention clause.  A red-K5 clause is
    # omitted precisely when the set contains the zero row and at least one B
    # vertex, because that cross edge is fixed blue.
    red_impossible = comb(42, 4) - comb(19, 4)
    ramsey_clauses = 2 * comb(43, 5) - red_impossible
    clauses["physical_five_sets"] = ramsey_clauses
    return {
        "variables": variables,
        "clauses": sum(clauses.values()),
        "ramsey_clauses": ramsey_clauses,
        "clause_breakdown": clauses,
        "degree_auxiliary_variables": degree_variables,
        "canonical_valid_supports": canonical_supports,
    }


def file_hash(path):
    digest = sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main():
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    support_data = json.loads((directory / "support_orbits.json").read_text())
    metadata = json.loads((directory / "base_metadata.json").read_text())
    proof = json.loads((directory / "proof_result.json").read_text())
    result = json.loads((directory / "RESULT.json").read_text())

    group = all_linear_maps()
    if len(group) != 20160:
        raise RuntimeError("ordered bases did not reconstruct GL(4,2)")
    pair_rep = (1, 2)
    pair_orbit = {tuple(sorted((transformation[pair_rep[0]],
                                transformation[pair_rep[1]])))
                  for transformation in group}
    if len(pair_orbit) != comb(15, 2):
        raise RuntimeError("distinct nonzero row-label pairs are not one orbit")
    row_stabilizer = [transformation for transformation in group
                      if tuple(sorted((transformation[1], transformation[2]))) == pair_rep]
    if len(row_stabilizer) != 192:
        raise RuntimeError("unexpected row-profile stabilizer")
    column_stabilizer = [dual_map(transformation)
                         for transformation in row_stabilizer]

    valid_masks = [mask for mask in range(1 << 15)
                   if mask.bit_count() >= 5 and binary_rank(values(mask)) == 4]
    canonical_all = {min(image_mask(mask, transformation)
                         for transformation in column_stabilizer)
                     for mask in range(1 << 15)}
    canonical_valid = {}
    for mask in valid_masks:
        representative = min(image_mask(mask, transformation)
                             for transformation in column_stabilizer)
        canonical_valid.setdefault(representative, set()).add(mask)
    expected_records = []
    for representative, members in sorted(canonical_valid.items()):
        full_orbit = {image_mask(representative, transformation)
                      for transformation in column_stabilizer}
        if full_orbit != members:
            raise RuntimeError("support orbit is incomplete")
        expected_records.append({
            "labels": values(representative),
            "mask": representative,
            "orbit_size": len(full_orbit),
            "support_size": representative.bit_count(),
        })
    if support_data["records"] != expected_records:
        raise RuntimeError("published support representatives do not match audit")
    if support_data["column_action"] != "inverse-transpose of row stabilizer":
        raise RuntimeError("support table does not declare the dual action")
    if support_data["row_stabilizer_size"] != len(row_stabilizer):
        raise RuntimeError("support-table stabilizer mismatch")
    if support_data["support_orbits"] != len(expected_records):
        raise RuntimeError("support-table orbit-count mismatch")
    if support_data["valid_support_masks"] != len(valid_masks):
        raise RuntimeError("support-table mask-count mismatch")

    counts_by_size = Counter(record["support_size"] for record in expected_records)
    masks_by_size = Counter()
    for record in expected_records:
        masks_by_size[record["support_size"]] += record["orbit_size"]
    band_indices = [index for index, record in enumerate(expected_records)
                    if 5 <= record["support_size"] <= 8]
    variable_map = metadata["variable_map"]
    symmetry_clauses = variable_map["support_symmetry_clauses"]
    dimensions = independent_formula_dimensions(
        len(canonical_valid), symmetry_clauses,
        variable_map["nonzero_support_maximum"],
    )
    formula = metadata["formula"]
    if any(formula[key] != dimensions[key]
           for key in ("variables", "clauses", "ramsey_clauses")):
        raise RuntimeError("independent formula dimensions disagree with metadata")
    if variable_map["degree_auxiliary_variables"] != dimensions["degree_auxiliary_variables"]:
        raise RuntimeError("degree auxiliary count mismatch")
    expected_symmetry = (1 << 15) - len(canonical_all) if variable_map["support_symmetry_break"] else 0
    if symmetry_clauses != expected_symmetry:
        raise RuntimeError("support symmetry count mismatch")
    expected_canonical = len(canonical_valid) if variable_map["support_symmetry_break"] else None
    if variable_map["canonical_valid_supports"] != expected_canonical:
        raise RuntimeError("canonical support metadata mismatch")
    if result["formula"] != formula:
        raise RuntimeError("RESULT formula identity differs from metadata")
    if variable_map["nonzero_support_maximum"] != 8:
        raise RuntimeError("proof formula does not encode the support band")
    if not variable_map["support_symmetry_break"]:
        raise RuntimeError("proof formula lacks support canonicalization")
    if proof["status"] != "UNSAT_PROOF_VERIFIED":
        raise RuntimeError("single proof was not externally verified")
    for key in ("cnf_sha256", "proof_sha256", "solver_sha256", "checker_sha256"):
        if HEX64.fullmatch(proof[key]) is None:
            raise RuntimeError(f"malformed proof-record hash: {key}")
    if proof["cnf_sha256"] != formula["sha256"]:
        raise RuntimeError("proof formula hash mismatch")
    for key in ("variables", "clauses"):
        if proof[key] != formula[key]:
            raise RuntimeError(f"proof formula dimension mismatch: {key}")
    if proof["cnf_bytes"] != formula["bytes"] or proof["proof_bytes"] <= 0:
        raise RuntimeError("proof file-size metadata mismatch")

    compositions = {size: bounded_compositions(size, 23, 5)
                    for size in range(5, 9)}
    band_supports = sum(masks_by_size[size] for size in range(5, 9))
    factor_multiset_pairs = len(pair_orbit) * sum(
        masks_by_size[size] * compositions[size] for size in range(5, 9)
    )
    expected_result = {
        "support_orbits": len(band_indices),
        "support_sets": band_supports,
        "row_support_set_pairs": len(pair_orbit) * band_supports,
        "factor_multiset_pairs": factor_multiset_pairs,
        "proof_cases": 1,
        "proof_bytes_total": proof["proof_bytes"],
        "cnf_bytes_total": proof["cnf_bytes"],
        "distinct_cnf_hashes": 1,
        "distinct_proof_hashes": 1,
    }
    for key, value in expected_result.items():
        location = result["proofs"] if key in {
            "proof_cases", "proof_bytes_total", "cnf_bytes_total",
            "distinct_cnf_hashes", "distinct_proof_hashes"
        } else result["scope"]
        if location[key] != value:
            raise RuntimeError(f"RESULT aggregate mismatch: {key}")

    evidence = {
        "status": "INDEPENDENT_AUDIT_ROW_TRIPLE_SUPPORT_5_8_EXCLUSION",
        "gl4_size": len(group),
        "row_pair_orbit_size": len(pair_orbit),
        "row_stabilizer_size": len(row_stabilizer),
        "all_support_orbits": len(expected_records),
        "all_support_sets": len(valid_masks),
        "support_orbits_by_size": dict(sorted(counts_by_size.items())),
        "support_sets_by_size": dict(sorted(masks_by_size.items())),
        "band_support_orbits": len(band_indices),
        "band_support_sets": band_supports,
        "bounded_compositions_by_size": compositions,
        "factor_multiset_pairs": factor_multiset_pairs,
        "formula_dimensions": dimensions,
        "proof_cases": 1,
        "proof_bytes_total": expected_result["proof_bytes_total"],
        "cnf_bytes_total": expected_result["cnf_bytes_total"],
        "cnf_hashes_distinct": expected_result["distinct_cnf_hashes"],
        "proof_hashes_distinct": expected_result["distinct_proof_hashes"],
        "base_cnf_sha256": formula["sha256"],
        "proof_record_sha256": file_hash(directory / "proof_result.json"),
    }
    print(json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    main()
