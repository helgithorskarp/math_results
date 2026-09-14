#!/usr/bin/env python3
"""Negative controls and small exact fixtures for the 119-image verifier."""
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
    bad["schema"] = "wrong"
    tests.append(("wrong schema", rejected(bad)))

    bad = copy.deepcopy(certificate)
    bad["shells"].pop()
    tests.append(("missing norm shell", rejected(bad)))

    bad = copy.deepcopy(certificate)
    bad["dependencies_sha256"]["g11_one_collision_certificate.json"] = "0" * 64
    tests.append(("wrong predecessor hash", rejected(bad)))

    # This corruption passes syntax and dependency checks, forcing the full
    # enumeration before the canonical event stream is rejected.
    bad = copy.deepcopy(certificate)
    bad["event_stream_sha256"] = "f" * 64
    tests.append(("wrong exhaustive event digest", rejected(bad)))

    # Exhaust all binary row lists with at most three columns and three rows.
    rank_fixtures = 0
    for columns in range(4):
        for row_count in range(4):
            choices = 1 << columns
            for packed in range(choices ** row_count):
                rows = []
                value = packed
                for _ in range(row_count):
                    value, row = divmod(value, choices)
                    rows.append(row)
                span = {0}
                for row in rows:
                    span |= {x ^ row for x in tuple(span)}
                expected = len(span).bit_length() - 1
                if verify.binary_rank(rows) != expected:
                    raise ValueError("small binary-rank fixture")
                rank_fixtures += 1

    # A projected four-cycle survives a disjoint merge and vanishes when two
    # of its own vertices are merged.
    need_survive = verify.projected_rank([[0, 1, 2, 3]], 4, 5)
    need_collapse = verify.projected_rank([[0, 1, 2, 3]], 0, 1)
    if need_survive != (1, 1) or need_collapse != (0, 0):
        raise ValueError("cycle-projection fixture")
    if not all(ok for _, ok in tests):
        raise ValueError("a malformed certificate was accepted")
    print(json.dumps({
        "verified": True,
        "malformed_certificates_rejected": len(tests),
        "small_binary_rank_fixtures": rank_fixtures,
        "cycle_projection_fixtures": 2,
        "controls": [name for name, _ in tests],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
