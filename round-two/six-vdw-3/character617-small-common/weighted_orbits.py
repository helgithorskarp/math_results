"""Verify all five anchored versions, retain one graph representative per orbit."""
import argparse
import hashlib
import json
from pathlib import Path


def choice_signature(choice, scalar):
    return (tuple(choice["balance"]), tuple(sorted(t * scalar % 617 for t in choice["B0"])),
            choice["outside"], choice["allowed_prefix_bad_budget"], tuple(choice["coefficients"]))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--mode", choices=("producer", "checker"), required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    d = json.loads(args.input.read_text())
    records = d["records"]
    raw = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(raw).hexdigest() != d["records_sha256"] or len(records) != 1860:
        raise ValueError("Whole independently checked weighted prefix domain")
    lookup = {tuple(r["A"]): r for r in records}
    if len(lookup) != len(records):
        raise ValueError("Physical prefix duplicates")
    squares = sorted({q * q % 617 for q in range(1, 617)})
    canonical = []
    covered = set()
    for r in records:
        a = tuple(r["A"])
        if a in covered:
            continue
        if args.mode == "producer":
            scalars = [pow(q, -1, 617) for q in a]
        else:
            # Entire308-scalar group orbit, independently selecting all members
            # that contain1. No use of producer's five-inverse enumeration.
            scalars = [s for s in squares if 1 in {s * q % 617 for q in a}]
        members = {}
        for scalar in scalars:
            member = tuple(sorted(q * scalar % 617 for q in a))
            expected = sorted(choice_signature(c, scalar) for c in r["choices"])
            if member not in lookup or expected != sorted(choice_signature(c, 1) for c in lookup[member]["choices"]):
                raise ValueError("Whole physical common choices or weighted coefficients do not transport")
            members[member] = scalar
        if len(members) != 5 or any(m in covered for m in members):
            raise ValueError("Not a disjoint five-member anchored orbit")
        canonical.append(lookup[min(members)])
        covered.update(members)
    canonical.sort(key=lambda r: r["A"])
    if len(canonical) != 372 or len(covered) != 1860:
        raise ValueError("Whole372 anchored orbit coverage")
    raw = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()
    incidences = {"11/13": 0, "12/12": 0}
    for r in canonical:
        for c in r["choices"]:
            key = "/".join(map(str, c["balance"]))
            incidences[key] += sum(c["coefficients"][:c["allowed_prefix_bad_budget"] + 1])
    if incidences != {"11/13": 908, "12/12": 20339}:
        raise ValueError("Transported physical incidence counts differ from complete anchored domain")
    result = {"schema": "character617-weighted-canonical-prefixes-v1", "parent_records_sha256": d["records_sha256"],
              "parent_prefixes": 1860, "canonical_prefixes": 372, "anchored_versions_per_orbit": 5,
              "physical_column_incidences": incidences,
              "records_sha256": hashlib.sha256(raw).hexdigest(), "records": canonical}
    args.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
