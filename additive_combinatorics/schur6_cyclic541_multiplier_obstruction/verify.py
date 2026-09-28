#!/usr/bin/env python3
"""Compare two exact enumerations, literal small controls, and compact evidence."""
import json
from pathlib import Path

import classify
import direct_check


def main():
    report, catalog = classify.run()
    direct, other_catalog = direct_check.run()
    classify.require(catalog == other_catalog, "entrywise catalog disagreement")
    classify.require(all(report[k] == v for k, v in direct.items()), "report disagreement")
    cases, subsets = [], 0
    for p, d in [(7, 2), (7, 6), (13, 2), (13, 4), (17, 2), (19, 6), (31, 10)]:
        blocks = direct_check.cosets(p, d)
        orbits, edges = classify.orbit_hypergraph(p, blocks[0])
        classify.require([set(x) for x in orbits] == blocks, "coset disagreement")
        literal = {}
        for mask in range(1 << len(blocks)):
            selected = tuple(i for i in range(len(blocks)) if mask >> i & 1)
            values = set().union(*(blocks[i] for i in selected))
            valid = direct_check.sumfree(p, values)
            encoded = not any(all(mask >> i & 1 for i in edge) for edge in edges)
            classify.require(valid == encoded, "small encoding mismatch")
            if valid and selected and selected[0] == 0:
                literal.setdefault(len(selected), []).append(selected)
            subsets += 1
        for target in range(1, len(blocks) + 1):
            expected = sorted(literal.get(target, []))
            encoded, _ = classify.enumerate_normalized(orbits, edges, target)
            checked, _ = direct_check.enumerate_direct(p, blocks, target)
            classify.require(encoded == checked == expected, "small enumeration mismatch")
        cases.append([p, d])
    # Check the algebraic obstruction when a stabilizer contains sixth roots.
    sixth = {x for x in range(1, 541) if pow(x, 6, 541) == 1}
    obstruction = next((a, b, (a + b) % 541) for a in sorted(sixth)
                       for b in sorted(sixth) if (a + b) % 541 in sixth)
    report.update({"status": "ALL_EXACT_CHECKS_PASSED", "small_cases": cases,
                   "small_subsets_checked": subsets, "sixth_root_obstruction": list(obstruction)})
    expected_file = Path(__file__).with_name("expected.json")
    classify.require(report == json.loads(expected_file.read_text()), "expected output mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
