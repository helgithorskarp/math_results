"""Forced-port graph and exact additive-charge criterion for a checked patch."""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

import marked_corona


def analyze(witness):
    checks = marked_corona.check_witness(witness)
    grid = witness.get("grid", "square")
    if grid == "hex":
        import hex_domain as domain
    else:
        domain = marked_corona
    count = len(domain.boundary(witness["tile"]))
    incidences, pairs = {}, set()
    for record in witness["patch"]:
        cells, ports = domain.oriented(witness["tile"], record["reflect"], record["turns"])
        tx, ty = record["translation"]
        for i, (edge, side) in enumerate(ports):
            key = tuple((x + tx, y + ty) for x, y in edge)
            if key in incidences:
                pairs.add(tuple(sorted((i, incidences[key]))))
            else:
                incidences[key] = i
    graph = [set() for _ in range(count)]
    for i, j in pairs:
        graph[i].add(j)
        graph[j].add(i)
    remaining, components = set(range(count)), []
    patterns = []
    while remaining:
        start = min(remaining)
        remaining.remove(start)
        parity, queue, bipartite = {start: 0}, deque([start]), True
        while queue:
            i = queue.popleft()
            for j in sorted(graph[i]):
                if j not in parity:
                    parity[j] = 1 - parity[i]
                    remaining.remove(j)
                    queue.append(j)
                elif parity[i] == parity[j]:
                    bipartite = False
        left = sorted(i for i in parity if parity[i] == 0)
        right = sorted(i for i in parity if parity[i] == 1)
        component = {"vertices": sorted(parity), "bipartite": bipartite}
        if bipartite:
            component.update({"parts": [left, right], "counts": [len(left), len(right)]})
            if len(left) != len(right):
                positive, negative = (left, right) if len(left) > len(right) else (right, left)
                pattern = [0] * count
                for i in positive:
                    pattern[i] = 1
                for i in negative:
                    pattern[i] = -1
                alternative = {**witness, "signs": pattern}
                marked_corona.check_witness(alternative)
                patterns.append({"counts": [len(positive), len(negative)], "signs": pattern})
        components.append(component)
    return {"grid": grid, "depth": witness["depth"], "ports": count,
            "contact_pairs": sorted(pairs), "components": components,
            "admissible_nonzero_charge": bool(patterns),
            "single_component_markings": patterns, "witness_checks": checks}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("witness", type=Path)
    args = parser.parse_args()
    raw = args.witness.read_bytes()
    result = analyze(json.loads(raw))
    result["witness_sha256"] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
