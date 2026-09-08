#!/usr/bin/env python3
"""Negative controls for the independent one-collision verifier."""
import copy
import json

import verify


def rejected(certificate):
    try:
        verify.run(certificate)
    except (ValueError, KeyError, TypeError, IndexError):
        return True
    return False


def main():
    certificate = json.loads(verify.CERTIFICATE.read_text())
    tests = []

    bad = copy.deepcopy(certificate)
    bad["cases"][0]["representative"] = [0, 1]
    tests.append(("adjacent representative", rejected(bad)))

    bad = copy.deepcopy(certificate)
    bad["cases"][0]["basis_cycles"].pop()
    tests.append(("short rank witness", rejected(bad)))

    bad = copy.deepcopy(certificate)
    bad["cases"][0]["basis_cycles"][0][0] = 999
    tests.append(("out-of-range cycle vertex", rejected(bad)))

    bad = copy.deepcopy(certificate)
    bad["cases"][0]["basis_cycles"][0] = [0, 1, 2, 3]
    tests.append(("absent four-cycle", rejected(bad)))

    bad = copy.deepcopy(certificate)
    bad["cases"][0]["basis_cycles"][-1] = bad["cases"][0]["basis_cycles"][0]
    tests.append(("dependent rank witness", rejected(bad)))

    bad = copy.deepcopy(certificate)
    bad["chromatic_dependency_sha256"]["q11_four_unsat.drat"] = "0" * 64
    tests.append(("wrong imported proof hash", rejected(bad)))

    bad = copy.deepcopy(certificate)
    bad["cases"][0]["five_colouring"][0] = bad["cases"][0]["five_colouring"][1]
    tests.append(("improper quotient colouring", rejected(bad)))

    # Exhaust every binary matrix with at most three columns and compare the
    # eliminator with a definition-level span census.
    rank_fixtures = 0
    for columns in range(4):
        possible_rows = range(1 << columns)
        for row_count in range(4):
            for packed in range((1 << columns) ** row_count):
                rows = []
                value = packed
                for _ in range(row_count):
                    rows.append(value & ((1 << columns) - 1))
                    value >>= columns
                span = {0}
                for row in rows:
                    span |= {x ^ row for x in list(span)}
                expected_rank = (len(span)).bit_length() - 1
                if verify.rank_mod_2(rows) != expected_rank:
                    raise ValueError("small rank fixture failed")
                rank_fixtures += 1

    if not all(ok for _, ok in tests):
        raise ValueError("a malformed certificate was accepted")
    result = {
        "verified": True,
        "malformed_certificates_rejected": len(tests),
        "small_binary_rank_fixtures": rank_fixtures,
        "controls": [name for name, _ in tests],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
