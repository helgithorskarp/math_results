#!/usr/bin/env python3
"""Deliberately damage coverage and exclusion evidence; every damage must fail.

Uses the standalone checker as the object under test. It does not supply proof
enumeration or oracle logic to either production implementation.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import verify

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def compute():
    certificate = json.loads((HERE / "certificate.json").read_text())
    keys, census = verify.incidence_census()
    good = verify.verify_certificate(certificate, keys, census)
    arc_index = next(i for i, e in enumerate(certificate["entries"])
                     if e["exclusion"]["type"] == "arc_deletion")
    empty_index = next(i for i, e in enumerate(certificate["entries"])
                       if e["exclusion"]["type"] == "empty_star")
    arc = certificate["entries"][arc_index]
    frame = verify.LiteralFrame(verify.NEIGHBORS, verify.rows_from_key(verify.validate_key(arc["key"])),
                                verify.DEFICITS)
    stars = frame.domains()
    first = arc["exclusion"]["steps"][0]
    b, c, supported = next((b, c, x) for b in range(11) for c in range(11) if b != c
                           for x in stars[b] if any(frame.compatible(b, x, c, y) for y in stars[c]))
    empty = certificate["entries"][empty_index]
    empty_frame = verify.LiteralFrame(verify.NEIGHBORS,
                                     verify.rows_from_key(verify.validate_key(empty["key"])), verify.DEFICITS)
    wrong_empty_point = next(i for i, d in enumerate(empty_frame.domains()) if d)
    cases = []

    def add(name, edit):
        damaged = deepcopy(certificate)
        edit(damaged)
        cases.append((name, damaged))

    add("missing_orbit", lambda v: v["entries"].pop(0))
    add("duplicate_orbit", lambda v: v["entries"].append(deepcopy(v["entries"][0])))
    add("unordered_orbits", lambda v: v["entries"].reverse())
    add("wrong_deficit", lambda v: v["outside_deficits"].__setitem__(0, 2))
    add("boolean_deficit", lambda v: v["outside_deficits"].__setitem__(1, True))
    add("false_coverage_count", lambda v: v.__setitem__("incidence_records", 4984))
    add("wrong_red_cap", lambda v: v.__setitem__("red_page_cap", 4))
    add("boolean_schema", lambda v: v.__setitem__("schema", True))
    add("wrong_local_graph", lambda v: v.__setitem__("local_graph", "P-minus-edge"))
    add("boolean_row_word", lambda v: v["entries"][0]["key"].__setitem__(0, True))
    add("changed_low_row", lambda v: v["entries"][0]["key"].__setitem__(0, v["entries"][0]["key"][0] ^ 1))
    add("changed_multiplicity", lambda v: v["entries"][0]["key"][3].__setitem__(0, 1))
    add("false_orbit_size", lambda v: v["entries"][0].__setitem__("orbit_size", v["entries"][0]["orbit_size"] + 1))
    add("false_domain_hash", lambda v: v["entries"][0].__setitem__("domains_sha256", "0" * 64))
    add("false_domain_size", lambda v: v["entries"][0]["domain_sizes"].__setitem__(0, 999))
    add("false_empty_star", lambda v: v["entries"][empty_index]["exclusion"].__setitem__("point", wrong_empty_point))
    add("supported_star_deleted", lambda v: v["entries"][arc_index]["exclusion"]["steps"][0].update(
        {"point": b, "against": c, "removed": [supported]}))
    add("duplicate_removal", lambda v: v["entries"][arc_index]["exclusion"]["steps"][0]["removed"].append(first["removed"][0]))
    add("incomplete_trace", lambda v: v["entries"][arc_index]["exclusion"]["steps"].pop())
    add("trace_after_empty", lambda v: v["entries"][arc_index]["exclusion"]["steps"].append(deepcopy(v["entries"][arc_index]["exclusion"]["steps"][-1])))
    add("false_final_empty_point", lambda v: v["entries"][arc_index]["exclusion"].__setitem__("empty_point", (arc["exclusion"]["empty_point"] + 1) % 11))
    add("unknown_certificate_field", lambda v: v.__setitem__("unproved_bridge", True))
    add("null_exclusion", lambda v: v["entries"][0].__setitem__("exclusion", None))
    rejected = []
    for name, damaged in cases:
        require(verify.pack(damaged) != verify.pack(certificate), "control failed to damage input: " + name)
        try:
            verify.verify_certificate(damaged, keys, census)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("damaged certificate accepted: " + name)
    expected = json.loads((HERE / "expected.json").read_text())
    forged = deepcopy(expected)
    forged["verifier"]["incidence_records"] -= 1
    with tempfile.TemporaryDirectory(prefix="book108-integrity-") as directory:
        path = Path(directory) / "expected.json"
        path.write_text(json.dumps(forged))
        command = [sys.executable] + (["-O"] if not __debug__ else [])
        command += [str(HERE / "verify.py"), "--expected", str(path)]
        answer = subprocess.run(command, capture_output=True, text=True, timeout=45)
        require(answer.returncode != 0 and "verifier expected-summary mismatch" in answer.stderr,
                "forged frozen summary was not rejected by normal checker")
    return {"good_incidence_records": good["incidence_records"],
            "damaged_certificate_rejections": len(rejected), "damage_names": rejected,
            "forged_frozen_summary_rejections": 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--derive", action="store_true")
    args = parser.parse_args()
    result = compute()
    if not args.derive:
        require(verify.pack(result) == verify.pack(json.loads((HERE / "expected.json").read_text())["integrity_controls"]),
                "integrity-control expected-summary mismatch")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
