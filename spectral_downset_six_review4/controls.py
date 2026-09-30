#!/usr/bin/env python3
"""Bounded rejection controls and exact checks of the proved inertia template."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile

from census_audit import positive_certificate, read_candidates, run
from exception_audit import inertia


def rejected(function, fragment):
    try:
        function()
    except ValueError as error:
        if fragment not in str(error):
            raise ValueError("unexpected rejection: " + str(error)) from error
        return str(error)
    raise ValueError("corrupt input was accepted")


def main():
    # All subsets of [2], embedded on [6]. Its maximum star has size two.
    f = sum(1 << a for a in (0, 1, 2, 3))
    bins = [[1, 2], [3]]
    if not positive_certificate(f, bins, 6):
        raise ValueError("valid partition control")
    reports = {}
    reports["omitted_member"] = rejected(
        lambda: positive_certificate(f, [[1], [3]], 6), "coverage")
    reports["repeated_member"] = rejected(
        lambda: positive_certificate(f, [[1, 1], [3]], 6), "coverage")
    reports["intersecting_bin"] = rejected(
        lambda: positive_certificate(f, [[1, 3], [2]], 6), "intersecting")
    reports["wrong_number_of_bins"] = rejected(
        lambda: positive_certificate(f, [[1], [2], [3]], 6), "partition size")
    reports["not_a_downset"] = rejected(
        lambda: positive_certificate((1 << 0) | (1 << 3), [[3]], 6), "not a downset")

    # These malformed census inputs fail at the first class. No failed run
    # is treated as a partial or negative mathematical census.
    empty_records = [dict() for _ in range(65)]
    reports["missing_entire_orbit"] = rejected(
        lambda: run(6, deepcopy(empty_records)), "exactly one candidate")
    wrong_orbit = deepcopy(empty_records)
    wrong_orbit[0][0] = {"family": 0, "orbit": 2, "bins": []}
    reports["wrong_orbit_multiplicity"] = rejected(
        lambda: run(6, deepcopy(wrong_orbit)), "orbit multiplicity")
    unsupported = deepcopy(empty_records)
    unsupported[0][0] = {"family": 0, "orbit": 1, "bins": None}
    reports["unsupported_exception"] = rejected(
        lambda: run(6, deepcopy(unsupported)), "unsupported missing partition")
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "duplicate.jsonl"
        record = json.dumps({"family": 0, "orbit": 1, "bins": []}) + "\n"
        path.write_text(record + record)
        reports["duplicate_representative"] = rejected(
            lambda: read_candidates(path), "duplicate candidate")

    # A disjoint bin on six points has at most six nonempty members. The
    # elementary spectrum of J_m-I_m has exactly one nonnegative eigenvalue,
    # including the zero eigenvalue at m=1. An isolated negative empty loop
    # adds no nonnegative eigenvalue. Exact congruence checks all local sizes.
    block_inertias = {}
    for m in range(1, 7):
        matrix = [[int(i != j) for j in range(m)] for i in range(m)]
        result = inertia(matrix)
        if result["positive"] + result["zero"] != 1:
            raise ValueError("inertia block template")
        block_inertias[str(m)] = result
    if inertia([[-1]])["negative"] != 1:
        raise ValueError("negative empty-loop template")
    print(json.dumps({"rejected_mutations": reports,
                      "inertia_bin_templates": block_inertias,
                      "mutation_count": len(reports)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
