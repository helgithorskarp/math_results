#!/usr/bin/env python3
"""Small independent fixtures for the syntax guard; runs no native checker."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from binary_drat_framing import BinaryDratFraming, inspect


def controls():
    # Expected: additions, deletions, literals, empty clauses, max variable.
    valid = [
        (b"", (0, 0, 0, 0, 0)),
        (b"a\x00", (1, 0, 0, 1, 0)),  # Syntax accepts a false refutation.
        (b"d\x00", (0, 1, 0, 1, 0)),
        (b"a\x02\x03\x80\x01\x00dad\x00a\x00", (2, 1, 5, 1, 64)),
        (b"a\xfe\xff\xff\xff\x07\xff\xff\xff\xff\x07\x00",
         (1, 0, 2, 0, 1073741823)),
    ]
    invalid = {
        "bad_prefix": b"x\x00",
        "missing_clause": b"a",
        "unterminated_clause": b"a\x02",
        "truncated_literal": b"a\x80",
        "signed_zero": b"a\x01\x00",
        "noncanonical_literal": b"a\x82\x00",
        "signed_int_overflow": b"a\x80\x80\x80\x80\x08\x00",
        "excess_continuation": b"a\x80\x80\x80\x80\x80\x01\x00",
        "bad_prefix_after_clause": b"a\x00x\x00",
    }
    fields = ("additions", "deletions", "literals", "empty_clauses", "max_variable")
    for data, expected in valid:
        for chunk in (1, 2, 7, 65536):
            checker = BinaryDratFraming()
            for start in range(0, len(data), chunk):
                checker.feed(data[start:start + chunk])
            result = checker.finish()
            if tuple(result[f] for f in fields) != expected:
                raise ValueError("valid fixture count mismatch")
            if result["bytes"] != len(data) or result["sha256"] != sha256(data).hexdigest():
                raise ValueError("valid fixture identity mismatch")
    for name, data in invalid.items():
        for chunk in (1, 2, 7, 65536):
            checker = BinaryDratFraming()
            try:
                for start in range(0, len(data), chunk):
                    checker.feed(data[start:start + chunk])
                checker.finish()
            except ValueError:
                continue
            raise ValueError(f"malformed fixture accepted: {name}")
    return {"valid_fixtures": len(valid), "malformed_fixtures": list(invalid),
            "chunk_sizes": [1, 2, 7, 65536], "fixture_runs": 56,
            "false_empty_clause_passes_syntax_as_expected": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, action="append", default=[])
    args = parser.parse_args()
    result = {"status": "FRAMING_CONTROLS_PASSED", "controls": controls(),
              "native_checks": 0, "full_corpus_framing_audited": False,
              "global_unsat_accepted": False, "samples": []}
    for path in args.sample:
        before = path.stat()
        sample = inspect(path)
        after = path.stat()
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError("sample changed while being read")
        metadata = json.loads(path.with_suffix(".json").read_text())
        if (sample["sha256"] != metadata["proof_sha256"]
                or sample["bytes"] != metadata["proof_bytes"]):
            raise ValueError("sample differs from its archived identity")
        result["samples"].append({"index": metadata["index"], **sample})
    print(json.dumps(result, indent=2, sort_keys=True))
