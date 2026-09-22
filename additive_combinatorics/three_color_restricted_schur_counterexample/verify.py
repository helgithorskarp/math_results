#!/usr/bin/env python3
"""Run finite audits and controls; the universal theorem is in proof.md."""

import argparse
from copy import deepcopy
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path

import audit
import construction


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def must_reject(function, *args):
    try:
        function(*args)
    except ValueError:
        return
    raise RuntimeError("negative control was accepted: " + function.__name__)


def literal_nonconstant(values, count, endpoint):
    """Independent control: enumerate actual multisets, without a DP."""
    bits = 0
    for terms in combinations_with_replacement(values, count):
        total = sum(terms)
        if total <= endpoint and len(set(terms)) >= 2:
            bits |= 1 << total
    return bits


def dp_controls():
    checks = 0
    for mask in range(1 << 7):
        values = [v for v in range(1, 8) if mask & (1 << (v - 1))]
        for count in (2, 3, 4):
            check(audit.nonconstant_sums(values, count, 7) ==
                  literal_nonconstant(values, count, 7), "DP/literal mismatch")
            checks += 1
    # Six has both a constant representation 2+2+2 and a nonconstant one.
    check(bool(audit.nonconstant_sums([1, 2, 3, 6], 3, 6) & (1 << 6)),
          "constant/nonconstant collision was lost")
    return checks


def malformed_controls():
    good = construction.coloring(3)
    cases = []
    for field, value in (("k", 1), ("k", True), ("N", good["N"] + 1)):
        bad = deepcopy(good)
        bad[field] = value
        cases.append(bad)
    for index, field, value in ((1, 0, 5), (1, 0, 3), (0, 2, 3),
                               (0, 0, 1.0)):
        bad = deepcopy(good)
        bad["blocks"][index][field] = value
        cases.append(bad)
    for bad in cases:
        must_reject(audit.validate_coloring, bad)
    first = 56
    good_witness = construction.extension_witnesses(3, first)[0]
    witness_cases = []
    for field, value in (("sum", first + 1), ("color", 0)):
        bad = deepcopy(good_witness)
        bad[field] = value
        witness_cases.append(bad)
    for index, field, value in ((0, 1, 0), (0, 1, 1),
                               (1, 0, good_witness["terms"][0][0])):
        bad = deepcopy(good_witness)
        bad["terms"][index][field] = value
        witness_cases.append(bad)
    for bad in witness_cases:
        must_reject(audit.audit_witness, good, bad)
    # A valid red witness at Q cannot falsely claim to use only the prefix.
    red = construction.extension_witnesses(3, 58)[2]
    must_reject(audit.audit_witness, good, red, first - 1)
    return len(cases) + len(witness_cases) + 1


def run():
    literal_cases = dp_controls()
    malformed = malformed_controls()
    finite = []
    witness_count = 0
    impossible_extension_checks = 0
    for k in range(2, 13):
        record = construction.coloring(k)
        # Expanded expressions here also check the parameter convention.
        first = k**3 + 3 * k**2 + k - 1
        stop = k**3 + 3 * k**2 + 2 * k - 2
        check(record["N"] == stop - 1, "wrong avoiding endpoint")
        check(record["blocks"][-1] == [first, stop - 1, 0], "wrong extension")
        audit.validate_coloring(record)
        dp_counts = audit.audit_nonconstant(record)
        two_values = audit.audit_two_values(record)
        for target in range(first, stop + 1):
            witnesses = construction.extension_witnesses(k, target)
            expected_colors = [1, 2, 0] if target == stop else [1, 2]
            check([w["color"] for w in witnesses] == expected_colors,
                  "missing extension color obstruction")
            for witness in witnesses:
                check(witness["sum"] == target, "wrong target returned")
                original_endpoint = first - 1 if witness["color"] else None
                audit.audit_witness(record, witness, original_endpoint)
                witness_count += 1
        for color in range(3):
            extended = deepcopy(record)
            extended["N"] = stop
            extended["blocks"].append([stop, stop, color])
            must_reject(audit.audit_nonconstant, extended)
            must_reject(audit.audit_two_values, extended)
            impossible_extension_checks += 2
        finite.append({
            "k": k,
            "original_proposed_value": first,
            "avoiding_endpoint": stop - 1,
            "proved_lower_bound": stop,
            "nonconstant_attainable_sums_by_color": dp_counts,
            "two_value_audit": two_values,
            "coloring_sha256": hashlib.sha256(bytes(audit.expand(record))).hexdigest(),
        })
    # Do not expand these colorings. Check compact witnesses at both ends.
    huge = [10**6, 10**30 + 1, 10**100 + 39]
    huge_witnesses = 0
    for k in huge:
        record = construction.coloring(k)
        audit.validate_coloring(record)
        first = k**3 + 3 * k**2 + k - 1
        stop = k**3 + 3 * k**2 + 2 * k - 2
        check(record["N"] == stop - 1, "huge parameter mismatch")
        for target in (first, stop):
            for witness in construction.extension_witnesses(k, target):
                audit.audit_witness(record, witness,
                                    first - 1 if witness["color"] else None)
                huge_witnesses += 1
    result = {
        "status": "ALL_EXACT_CHECKS_PASSED",
        "scope": "Finite validation; the universal theorem is the written proof.",
        "finite_cases": finite,
        "literal_dp_comparisons": literal_cases,
        "constant_nonconstant_collision_control": True,
        "finite_extension_witnesses": witness_count,
        "impossible_extension_rejections": impossible_extension_checks,
        "malformed_certificate_rejections": malformed,
        "large_integer_parameters": huge,
        "large_integer_endpoint_witnesses": huge_witnesses,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["record_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-expected", action="store_true",
                        help="also compare entry by entry with expected.json")
    args = parser.parse_args()
    result = run()
    if args.check_expected:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        check(result == expected, "published expected output mismatch")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
