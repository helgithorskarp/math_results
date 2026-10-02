"""Check the complete deterministic exact record, with fail-closed parsing."""
from pathlib import Path
import argparse
import importlib.util
import json
import sys
from hashlib import sha256


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate fixture key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("nonfinite fixture token: " + value)


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=here / "expected.json")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("sendov_effective_actual_profile_stability_checks", here / "checks.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected = json.loads(args.expected.read_text(encoding="utf-8"),
                          object_pairs_hook=unique_pairs, parse_constant=reject_constant)
    record = module.build_record()
    actual_bytes, expected_bytes = module.canonical(record), module.canonical(expected)
    if actual_bytes != expected_bytes:
        raise ValueError("complete typed canonical fixture mismatch")
    print(json.dumps({"status": "PASS", "identity_records": len(record["identities"]),
          "whole_domain_margins": len(record["whole_domain_margins"]),
          "literal_controls": len(record["literal_controls"]),
          "mathematical_damages_rejected": len(record["mathematical_damage_controls"]),
          "canonical_sha256": sha256(actual_bytes).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
