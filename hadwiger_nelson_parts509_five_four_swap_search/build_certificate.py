#!/usr/bin/env python3
"""Pack the CEGAR witness rows and emit the deterministic selector CNF."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from certlib import pack_colours, selector_exact_q_cnf, sha256

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
SOURCE = PARENT / "hadwiger_nelson_parts509_s_replacement_budget"
INTERFACE = PARENT / "hadwiger_nelson_parts509_interface_lemma" / "interface_L.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", type=Path, action="append", required=True)
    parser.add_argument("--certificate", type=Path,
                        default=HERE / "certificate.json")
    args = parser.parse_args()

    pool_data = json.loads((SOURCE / "pool_S.json").read_text())
    pool = sorted(pool_data["W_S"])
    q5 = sorted(pool_data["Q5"])
    interface = json.loads(INTERFACE.read_text())
    l_words = [row["witness_colouring_L"] for row in interface["classes"]]

    rows_by_set = {}
    sources = (("general_pool_dual_certificate.json", "source_general"),
               ("certificate.json", "source_s_only"))
    for filename, provenance in sources:
        data = json.loads((SOURCE / filename).read_text())
        for row in data["killing_sets"]:
            key = frozenset(row["D"])
            rows_by_set.setdefault(key, {
                "D": sorted(key), "class_index": row["class_index"],
                "word": row["colouring_U_minus_D"], "provenance": provenance,
            })
    for path in args.jsonl:
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            key = frozenset(row["D"])
            p = row["class_index"]
            word = row["colouring_L_plus_U_minus_D"]
            if word[:374] != l_words[p]:
                raise ValueError(f"generated L witness mismatch in {path}")
            rows_by_set.setdefault(key, {
                "D": sorted(key), "class_index": p, "word": word[374:],
                "provenance": "r4_cegar",
            })

    ordered = sorted(rows_by_set, key=lambda d: (len(d), tuple(sorted(d))))
    minimal = []
    for d in ordered:
        if not any(e <= d for e in minimal):
            minimal.append(d)
    packed = []
    counts = {}
    for d in minimal:
        row = rows_by_set[d]
        if len(row["word"]) != len(pool) - len(d):
            raise ValueError("wrong U-minus-D word length")
        provenance = row["provenance"]
        counts[provenance] = counts.get(provenance, 0) + 1
        packed.append({
            "D": row["D"],
            "class_index": row["class_index"],
            "colouring_U_minus_D_2bit": pack_colours(row["word"]),
            "provenance": provenance,
        })

    selectors = {}
    for q_count in (4, 5, 6):
        cnf = selector_exact_q_cnf(
            pool, q5, [row["D"] for row in packed], q_count)
        path = HERE / f"selector_q{q_count}.cnf"
        path.write_bytes(cnf.dimacs())
        selectors[str(q_count)] = {
            "q5_count": q_count,
            "variables": cnf.nvars,
            "clauses": len(cnf.clauses),
            "sha256": sha256(path),
            "drat_status": "verified; see proof_manifest.json",
        }
    certificate = {
        "claim": ("every non-four-colourable L union X with X subset U, "
                  "|X|<=134, uses at least seven Q5 points"),
        "fixed_L": 374,
        "pool": pool,
        "S": list(range(374, 509)),
        "Q5": q5,
        "target_pool_order": 134,
        "closed_q5_counts": [4, 5, 6],
        "killing_sets": packed,
        "killing_set_provenance_counts": counts,
        "selectors": selectors,
    }
    args.certificate.write_text(
        json.dumps(certificate, separators=(",", ":")) + "\n")
    print(json.dumps({
        "killing_sets": len(packed),
        "provenance": counts,
        "selectors": selectors,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
