#!/usr/bin/env python3
"""Falsifiable cost formula from the accepted boundary-word automaton.

Explore C(T,g)=number of RR adjacencies after an earlier L in the gap path.
Stop at the first mismatch by size, shape word, gap. No universal extrapolation.
"""
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import platform
import resource
from time import perf_counter

from kernel import boxed_occurrences
from tree_dynamics import (cartesian_shape, insert_maximum_shape, shape_legal_gaps,
                           size, tree_word)


@lru_cache(maxsize=None)
def trees(n):
    if n == 0:
        return ((),)
    return tuple(sorted(((l, r) for k in range(n)
                         for l in trees(k) for r in trees(n - 1 - k)),
                        key=tree_word))


def external_words(t, prefix=""):
    if not t:
        return [prefix]
    return external_words(t[0], prefix + "L") + external_words(t[1], prefix + "R")


def formula(word):
    seen_l, previous, count = False, "", 0
    for letter in word:
        count += bool(seen_l and previous == "R" and letter == "R")
        seen_l |= letter == "L"
        previous = letter
    return count


def representative(t):
    if not t:
        return ()
    l, r = t
    return tuple(x + size(r) for x in representative(l)) + (size(t),) + representative(r)


def repair(t, g):
    p, guards, steps = representative(t), 0, []
    assert not boxed_occurrences(p)
    while g not in shape_legal_gaps(t):
        gaps = shape_legal_gaps(t)
        k = max(x for x in gaps if x < g)
        child = p[:k] + (len(p) + 1,) + p[k:]
        next_tree = insert_maximum_shape(t, k)
        assert next_tree == cartesian_shape(child)
        assert not boxed_occurrences(child)
        steps.append({"desired_gap": g, "chosen_gap": k,
                      "legal_gaps": list(gaps), "parent": list(p), "child": list(child)})
        p, t, g = child, next_tree, g + 1
        guards += 1
        assert guards <= len(steps[0]["parent"]), "distance bound failed"
    return guards, {"final_desired_gap": g, "final_word": list(p), "steps": steps}


def main():
    start = perf_counter()
    out = Path(__file__).with_name("repair_path_cost_probe_v1.json")
    assert not out.exists()
    stream, checked, mismatch = sha256(), 0, None
    rows = []
    for n in range(8):
        completed_shapes = 0
        for t in trees(n):
            words = external_words(t)
            assert len(words) == n + 1
            for g, word in enumerate(words):
                predicted = formula(word)
                got, evidence = repair(t, g)
                checked += 1
                stream.update(f"{tree_word(t)}|{g}|{word}|{predicted}|{got}\n".encode())
                if predicted != got:
                    mismatch = {"n": n, "shape": tree_word(t), "gap": g,
                                "gap_path": word, "predicted": predicted,
                                "actual_cost": got, "literal_repair_evidence": evidence}
                    break
            if mismatch:
                break
            completed_shapes += 1
        rows.append({"n": n, "fully_examined_shapes": completed_shapes})
        if mismatch:
            break
    result = {"actor": "literature-researcher-3", "full_target_solved": False,
              "status": "author path-formula rejection" if mismatch else
                        "finite formula controls only; all-size statement unproved",
              "formula": "RR adjacency count after an earlier L",
              "first_mismatch": mismatch, "gaps_checked": checked,
              "complete_rows": rows, "stream_sha256": stream.hexdigest(),
              "seconds": perf_counter() - start,
              "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "python": platform.python_version(), "processes": 1, "native_threads": 1}
    temp = out.with_suffix(".json.tmp")
    temp.write_text(json.dumps(result, indent=2) + "\n")
    temp.replace(out)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
