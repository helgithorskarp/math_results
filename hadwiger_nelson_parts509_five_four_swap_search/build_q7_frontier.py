#!/usr/bin/env python3
"""Freeze positive q=7 CEGAR witnesses into a compact audit artifact.

The two JSONL inputs are search output and therefore are not trusted.  This
builder checks their shape, preserves the full deletion sets and packs only
the colour words.  ``verify_q7_frontier.py`` performs the independent graph
checks on the resulting artifact without importing PySAT or this program.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from certlib import pack_colours

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
INTERFACE = PARENT / "hadwiger_nelson_parts509_interface_lemma"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()
            if line.strip()]


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior-rows", type=Path, required=True)
    parser.add_argument("--new-rows", type=Path, required=True)
    parser.add_argument("--output", type=Path,
                        default=HERE / "q7_frontier_certificate.json")
    args = parser.parse_args()

    base_path = HERE / "certificate.json"
    base = json.loads(base_path.read_text())
    interface = json.loads((INTERFACE / "interface_L.json").read_text())
    l_words = [row["witness_colouring_L"]
               for row in interface["classes"]]
    pool = base["pool"]
    pool_set = set(pool)
    deleted_s = [389, 412, 413, 415, 442, 443, 493, 496]
    added_q5 = [539, 552, 560, 563, 565, 598, 898]
    selected = ((set(range(374, 509)) - set(deleted_s)) |
                set(added_q5))
    need(len(selected) == 134, "candidate pool order")

    prior = load_jsonl(args.prior_rows)
    new = load_jsonl(args.new_rows)
    need(len(prior) == 45 and len(new) == 5, "expected 45 plus 5 rows")
    need(len({tuple(row["D"]) for row in prior + new}) == 50,
         "frontier rows are not distinct")

    packed_rows = []
    candidate_colourings = []
    for ordinal, row in enumerate(prior + new):
        d = row["D"]
        p = row["class_index"]
        need(d == sorted(set(d)) and set(d) <= pool_set and d,
             "invalid deletion set")
        need(type(p) is int and 0 <= p < len(l_words),
             "invalid interface class")
        vertices = list(range(374)) + [v for v in pool if v not in set(d)]
        word = row["colouring_L_plus_U_minus_D"]
        need(len(word) == len(vertices), "colour word length")
        need(word[:374] == l_words[p], "L word does not match class")
        need(set(word) <= set("0123"), "invalid colour")
        packed_rows.append({
            "D": d,
            "class_index": p,
            "colouring_U_minus_D_2bit": pack_colours(word[374:]),
            "provenance": "prior_q7_cegar" if ordinal < 45
                          else "fifth_selector",
        })
        if ordinal >= 45:
            need(not (selected & set(d)),
                 "new killing set is not disjoint from candidate")
            colours = dict(zip(vertices, word))
            candidate_word = "".join(colours[v] for v in sorted(selected))
            candidate_colourings.append({
                "class_index": p,
                "colouring_selected_pool_2bit":
                    pack_colours(candidate_word),
            })

    result = {
        "schema": "parts509-q7-frontier-v1",
        "scope": "fixed Parts L and sealed S-union-Q5 level-one pool only",
        "base_certificate_sha256": sha256(base_path),
        "raw_input_sha256": {
            "prior_45": sha256(args.prior_rows),
            "new_5": sha256(args.new_rows),
        },
        "q5_count": 7,
        "target_pool_order": 134,
        "target_total_vertices": 508,
        "candidate": {
            "S_deleted": deleted_s,
            "Q5_added": added_q5,
            "verified_compatible_colourings": candidate_colourings,
            "status": "properly_four_colourable_not_a_record_candidate",
        },
        "frontier_killing_sets": packed_rows,
        "frontier_provenance_counts": {
            "prior_q7_cegar": 45,
            "fifth_selector": 5,
        },
        "local_exchange_radius": 2,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"build failed: {error}")
        raise SystemExit(1)
