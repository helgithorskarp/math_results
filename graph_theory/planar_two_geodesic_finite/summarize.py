#!/usr/bin/env python3
"""Check completeness and counts for a ten-residue plantri 11 run."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    totals = []
    selected = []
    for residue in range(10):
        plantri_log = (args.run_dir / f"plantri-{residue}.log").read_text()
        matches = re.findall(r"(\d+) polytopes written to stdout", plantri_log)
        if len(matches) != 1:
            raise ValueError(f"missing or ambiguous plantri completion for residue {residue}")
        generated = int(matches[0])
        filtered = json.loads((args.run_dir / f"filter-{residue}.json").read_text())
        checked = json.loads((args.run_dir / f"check-{residue}.json").read_text())
        if generated != filtered["filter_total"]:
            raise ValueError(f"generator/filter mismatch in residue {residue}")
        if filtered["diameter_at_most_2"] != checked["plane_graph_records_checked"]:
            raise ValueError(f"filter/checker mismatch in residue {residue}")
        if checked["selected_records"] != checked["plane_graph_records_checked"]:
            raise ValueError(f"checker unexpectedly skipped inputs in residue {residue}")
        if checked["order"] != 11 or checked["failures"] != 0:
            raise ValueError(f"checker failure in residue {residue}")
        totals.append(generated)
        selected.append(filtered["diameter_at_most_2"])
    result = {
        "order": 11,
        "residues": 10,
        "generated_by_residue": totals,
        "diameter_at_most_2_by_residue": selected,
        "total_plane_graph_records": sum(totals),
        "diameter_at_most_2_records": sum(selected),
        "failures": 0,
    }
    expected = json.loads((Path(__file__).with_name("EXPECTED.json")).read_text())
    if result != expected:
        raise ValueError("run summary differs from EXPECTED.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
