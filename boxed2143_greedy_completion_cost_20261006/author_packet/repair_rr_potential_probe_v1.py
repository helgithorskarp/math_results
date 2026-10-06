#!/usr/bin/env python3
"""Test one specific amortized drift candidate, stopping at its first failure.

Phi=sum of ALL consecutive RR pairs on ORIGINAL-gap paths (including pairs
before the first L). Test exact mean[cost+Phi(next)-Phi(parent)] <=1.
No constants are fitted and a failure does not exclude another potential.
"""
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import platform
import resource
from time import monotonic, perf_counter

from gap_opening_probe_v1 import complete
from kernel import insert_maximum, legal_maximum_gaps, boxed_occurrences
from repair_path_cost_probe_v1 import external_words, formula
from tree_dynamics import cartesian_shape


def original_gaps(tags):
    return [i for i, tag in enumerate(tags) if tag is not None] + [len(tags)]


def potential(p, tags):
    words = external_words(cartesian_shape(p))
    return sum(sum(a == b == "R" for a, b in zip(words[g], words[g][1:]))
               for g in original_gaps(tags))


def advance(p, tags, g, rank):
    p, tags = tuple(p), list(tags)
    initial = g
    prediction = formula(external_words(cartesian_shape(p))[g])
    cost = 0
    while g not in legal_maximum_gaps(p):
        k = max(x for x in legal_maximum_gaps(p) if x < g)
        p = insert_maximum(p, k)
        tags.insert(k, None)
        g += 1
        cost += 1
        assert not boxed_occurrences(p)
    p = insert_maximum(p, g)
    tags.insert(g, rank)
    assert not boxed_occurrences(p)
    assert prediction == cost
    return {"initial_current_gap": initial, "cost": cost, "word": list(p),
            "tags": tags, "phi": potential(p, tags)}


def main():
    start = perf_counter()
    out = Path(__file__).with_name("repair_rr_potential_probe_v1.json")
    assert not out.exists()
    deadline = monotonic() + 60
    stream, states, rows, failure = sha256(), 0, [], None
    for n in range(7):
        completed = 0
        maximum = None
        for source in permutations(range(1, n + 1)):
            if n:
                result = complete(source, deadline, literal=False)
                p, tags = result["output"], result["source_identities"]
            else:
                p, tags = (), []
            phi = potential(p, tags)
            children = [advance(p, tags, g, n + 1) for g in original_gaps(tags)]
            numerator = sum(c["cost"] + c["phi"] for c in children) - (n + 1) * phi
            record = {"source": list(source), "n": n, "word": list(p),
                      "tags": tags, "phi": phi, "children": children,
                      "drift_numerator": numerator, "drift_denominator": n + 1}
            stream.update((json.dumps(record, sort_keys=True,
                                      separators=(",", ":")) + "\n").encode())
            states += 1
            completed += 1
            maximum = numerator if maximum is None else max(maximum, numerator)
            if numerator > n + 1:
                failure = record
                break
        rows.append({"n": n, "source_states_checked": completed,
                     "largest_drift_numerator": maximum, "denominator": n + 1})
        if failure:
            break
    d = {"actor": "literature-researcher-3", "full_target_solved": False,
         "status": "author drift-candidate rejection" if failure else
                   "finite drift controls only; uniform inequality unproved",
         "potential": "sum over original gaps of all RR adjacencies in their paths",
         "tested_drift_constant": 1, "first_failure": failure,
         "states_checked": states, "rows": rows, "stream_sha256": stream.hexdigest(),
         "seconds": perf_counter() - start,
         "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         "python": platform.python_version(), "processes": 1, "native_threads": 1}
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(d, indent=2) + "\n")
    tmp.replace(out)
    print(json.dumps(d))


if __name__ == "__main__":
    main()
