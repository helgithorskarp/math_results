#!/usr/bin/env python3
"""Directed controls for the uniform obstruction to ONE raw-RR potential.

The all-size proof is separate. Every family parent gap is checked by the
accepted shape/kernel functions; all parents/prefixes/children through size
28 also receive full literal occurrence scans. n64 is explicitly shape-only.
"""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import platform
import resource
from time import perf_counter

from kernel import insert_maximum, legal_maximum_gaps
from repair_path_cost_probe_v1 import external_words, formula
from tree_dynamics import cartesian_shape, insert_maximum_shape, shape_legal_gaps
from verify_kernel import direct_occurrences


def phi(p):
    return sum(sum(a == b == "R" for a, b in zip(w, w[1:]))
               for w in external_words(cartesian_shape(p)))


def main():
    root = Path(__file__).resolve().parent
    out = root / "repair_rr_drift_family_v1.json"
    assert not out.exists(), "Preserve the original output"
    start = perf_counter()
    stream, rows = sha256(), []
    literal_children = shape_children = prefix_steps = 0
    for n, q in [(2, 1), (4, 1), (8, 2), (27, 3), (64, 4)]:
        b = n - q - 1
        p = tuple(range(1, b + 1)) + tuple(range(n, n - q - 1, -1))
        assert sorted(p) == list(range(1, n + 1))
        t = cartesian_shape(p)
        assert legal_maximum_gaps(p) == shape_legal_gaps(t) == tuple(range(n + 1))
        assert all(formula(w) == 0 for w in external_words(t))
        parent_phi = phi(p)
        assert parent_phi == q * (q + 1) // 2
        if n + 1 <= 28:
            assert not direct_occurrences(p)
        # Independently locate each rank arrival in the actual source order;
        # no auxiliaries arise because each desired gap is legal.
        previous = ()
        for rank in range(1, n + 1):
            restriction = tuple(x for x in p if x <= rank)
            g = restriction.index(rank)
            assert g in legal_maximum_gaps(previous)
            assert insert_maximum(previous, g) == restriction
            if n + 1 <= 28:
                assert not direct_occurrences(restriction)
            previous = restriction
            prefix_steps += 1
        children = []
        for g in range(n + 1):
            child = insert_maximum(p, g)
            assert cartesian_shape(child) == insert_maximum_shape(t, g)
            child_phi = phi(child)
            if g <= b:
                predicted = parent_phi + q + 1
            else:
                index = g - b
                r = q + 1 - index
                predicted = index * (index - 1) // 2 + r * (r + 1) // 2
            assert child_phi == predicted
            literal = n + 1 <= 28
            if literal:
                assert not direct_occurrences(child)
                literal_children += 1
            shape_children += 1
            children.append({"gap": g, "cost": 0, "child_phi": child_phi,
                             "full_literal_scan": literal})
        mean = Fraction(sum(c["child_phi"] for c in children), n + 1) - parent_phi
        expected = Fraction((q + 1) * (6 * n - q * (q + 5)), 6 * (n + 1))
        assert mean == expected
        if n == q ** 3 and q >= 2:
            assert mean >= Fraction(q + 1, 3)
        row = {"n": n, "q": q, "b": b, "parent": p,
               "parent_phi": parent_phi, "children": children,
               "conditional_drift_numerator": mean.numerator,
               "conditional_drift_denominator": mean.denominator,
               "parent_prefix_literal_scans": n + 1 if n + 1 <= 28 else 0}
        rows.append(row)
        stream.update((json.dumps(row, sort_keys=True,
                                  separators=(",", ":")) + "\n").encode())
    sources = [Path(__file__).name, "repair_path_cost_probe_v1.py", "kernel.py",
               "tree_dynamics.py", "verify_kernel.py"]
    result = {
        "actor": "literature-researcher-3", "full_target_solved": False,
        "status": "PASS directed controls; uniform raw-RR drift obstruction AUTHOR pending whole check",
        "potential": "sum of all RR adjacencies over ORIGINAL gap paths",
        "rows": rows, "shape_children_checked": shape_children,
        "children_full_literal_checked": literal_children,
        "rank_arrival_steps_checked": prefix_steps,
        "stream_sha256": stream.hexdigest(),
        "source_sha256": {name: sha256((root / name).read_bytes()).hexdigest()
                          for name in sources},
        "seconds": perf_counter() - start,
        "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "python": platform.python_version(), "processes": 1, "native_threads": 1,
        "excluded": "unconditional mean bounds, other potentials, full target410",
    }
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(result, indent=2) + "\n")
    tmp.replace(out)
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}))


if __name__ == "__main__":
    main()
