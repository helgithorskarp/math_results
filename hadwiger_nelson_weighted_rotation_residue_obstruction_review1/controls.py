#!/usr/bin/env python3
"""Semantic corruption controls for the independent review checker."""

import argparse
import json
import tempfile
from pathlib import Path

import independent_audit as audit


def must_reject(action, label):
    try:
        action()
    except (ValueError, KeyError, TypeError):
        return
    raise ValueError("corruption survived: " + label)


parser = argparse.ArgumentParser()
parser.add_argument("--contacts", type=Path, required=True)
args = parser.parse_args()

points, _ = audit.load_source(audit.HERE.parent)
counts = audit.difference_counter(points)
differences = sorted(counts)
directions, labels, colour, _ = audit.quotient_audit()
_, representatives, _ = audit.contact_audit(points, args.contacts, directions, labels, colour)
contact_lines = args.contacts.read_text().splitlines()
rejected = 0

with tempfile.TemporaryDirectory(prefix="hn-weighted-review-controls-") as raw:
    temp = Path(raw)
    missing = temp / "missing.txt"
    missing.write_text("\n".join(contact_lines[:-1]) + "\n")
    must_reject(lambda: audit.load_contacts(missing, differences), "missing contact")
    rejected += 1

    false = temp / "false.txt"
    altered = contact_lines[:]
    altered[0] = "0 0"
    false.write_text("\n".join(altered) + "\n")
    must_reject(lambda: audit.load_contacts(false, differences), "false contact")
    rejected += 1

    original = json.loads((audit.TARGET / "auxiliary_certificate.json").read_text())
    bad_five = temp / "bad-five.json"
    changed = json.loads(json.dumps(original))
    changed["five_colouring"] = "0" * 114
    bad_five.write_text(json.dumps(changed))
    must_reject(lambda: audit.auxiliary_audit(points, representatives, bad_five), "five-colouring")
    rejected += 1

    bad_deletion = temp / "bad-deletion.json"
    changed = json.loads(json.dumps(original))
    changed["deletion_four_colourings"][0] = "0" * 114
    bad_deletion.write_text(json.dumps(changed))
    must_reject(lambda: audit.auxiliary_audit(points, representatives, bad_deletion), "deletion witness")
    rejected += 1

print(json.dumps({"status": "PASS", "semantic_corruptions_rejected": rejected}, sort_keys=True))
