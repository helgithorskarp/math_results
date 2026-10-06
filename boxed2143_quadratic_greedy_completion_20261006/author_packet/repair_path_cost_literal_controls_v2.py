#!/usr/bin/env python3
"""Definition-level controls supplementing the preserved optimized v1 probe.

All 626 shapes/4707 gaps through size 7; complete quadruple occurrence sets
for each hypothetical original maximum insertion and EVERY actual auxiliary
child. Same-author verification only, not an independent team check.
"""
from hashlib import sha256
import json
from pathlib import Path
import platform
import resource
from time import perf_counter

from kernel import blockers
from repair_path_cost_probe_v1 import (
    external_words, formula, repair, representative, trees,
)
from tree_dynamics import tree_word
from verify_kernel import direct_occurrences


def main():
    root = Path(__file__).resolve().parent
    out = root / "repair_path_cost_literal_controls_v2.json"
    assert not out.exists(), "Preserve the original output"
    start = perf_counter()
    stream, old_stream = sha256(), sha256()
    gaps = auxiliary_children = hypothetical_occurrences = 0
    rows = []
    for n in range(8):
        shape_count = size_gaps = size_auxiliaries = 0
        for t in trees(n):
            p = representative(t)
            assert not direct_occurrences(p)
            words = external_words(t)
            for g, word in enumerate(words):
                predicted = formula(word)
                cost, evidence = repair(t, g)
                assert predicted == cost
                coverage = sum(b.blocks(g) for b in blockers(p))
                assert coverage == predicted
                hypothetical = p[:g] + (n + 1,) + p[g:]
                occurrences = direct_occurrences(hypothetical)
                assert len(occurrences) == predicted
                for step in evidence["steps"]:
                    assert not direct_occurrences(tuple(step["child"]))
                    auxiliary_children += 1
                    size_auxiliaries += 1
                record = {
                    "n": n, "shape": tree_word(t), "gap": g,
                    "path": word, "D": predicted, "cost": cost,
                    "blocker_coverage": coverage,
                    "hypothetical_full_occurrence_set": occurrences,
                    "repair_trace": evidence,
                }
                stream.update((json.dumps(record, sort_keys=True,
                                          separators=(",", ":")) + "\n").encode())
                old_stream.update(f"{tree_word(t)}|{g}|{word}|{predicted}|{cost}\n".encode())
                hypothetical_occurrences += len(occurrences)
                gaps += 1
                size_gaps += 1
            shape_count += 1
        rows.append({"n": n, "complete_shapes": shape_count,
                     "complete_gaps": size_gaps,
                     "actual_auxiliary_children": size_auxiliaries})
    old = json.loads((root / "repair_path_cost_probe_v1.json").read_text())
    assert old_stream.hexdigest() == old["stream_sha256"]
    assert gaps == old["gaps_checked"]
    sources = [Path(__file__).name, "repair_path_cost_probe_v1.py",
               "kernel.py", "tree_dynamics.py", "verify_kernel.py"]
    result = {
        "actor": "literature-researcher-3", "full_target_solved": False,
        "status": "PASS same-author complete literal controls; whole review pending",
        "domain": "ALL shapes n0..7 and EVERY external gap",
        "rows": rows, "gaps_checked": gaps,
        "actual_auxiliary_children_literal_checked": auxiliary_children,
        "hypothetical_maximum_children_literal_checked": gaps,
        "hypothetical_occurrences_total": hypothetical_occurrences,
        "stream_sha256": stream.hexdigest(),
        "preserved_v1_stream_sha256": old_stream.hexdigest(),
        "source_sha256": {name: sha256((root / name).read_bytes()).hexdigest()
                          for name in sources},
        "seconds": perf_counter() - start,
        "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "python": platform.python_version(), "processes": 1, "native_threads": 1,
    }
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(result, indent=2) + "\n")
    tmp.replace(out)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
