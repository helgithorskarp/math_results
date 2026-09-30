#!/usr/bin/env python3
"""Independent exact replay using direct sets and maximal clique enumeration."""
import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED_HASH = "cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def cliques(adjacency, active, target):
    """All target-subsets of maximal cliques, with sound conflict-cover pruning."""
    if target == 0:
        return [()]
    found = set()

    def upper(vertices):
        remaining = set(vertices)
        count = 0
        while remaining:
            count += 1
            group = set(remaining)
            while group:
                v = min(group)
                remaining.remove(v)
                group.remove(v)
                group.difference_update(adjacency[v])
        return count

    def visit(selected, possible, excluded, budget):
        budget[0] += 1
        if budget[0] > 20_000 or (budget[0] % 128 == 0
                                and time.monotonic() - budget[1] > 10):
            raise RuntimeError("INCOMPLETE: independent enumeration limit")
        if not possible and not excluded:
            if len(selected) >= target:
                found.update(itertools.combinations(sorted(selected), target))
            return
        if len(selected) < target and (len(selected) + len(possible) < target
                                      or len(selected) + upper(possible) < target):
            return
        pivot = max(possible | excluded, key=lambda v: (len(possible & adjacency[v]), -v))
        for vertex in sorted(possible - adjacency[pivot]):
            child_budget = [0, time.monotonic()] if not selected else budget
            visit(selected + [vertex], possible & adjacency[vertex],
                  excluded & adjacency[vertex], child_budget)
            possible.remove(vertex)
            excluded.add(vertex)

    visit([], set(active), set(), [0, time.monotonic()])
    return sorted(found)


def verify():
    raw = (ROOT / "acl69.txt").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SEED_HASH, "wrong seed hash")
    rows = raw.decode("ascii").splitlines()
    require(len(rows) == 69 and all(len(s) == 18 and set(s) <= set("01")
                                  and s.count("1") == 5 for s in rows), "malformed seed")
    seed = [frozenset(p for p, c in enumerate(s) if c == "1") for s in rows]
    require(len(set(seed)) == 69
            and min(2 * (5 - len(a & b)) for a, b in itertools.combinations(seed, 2)) == 6,
            "invalid historical baseline")
    saturated = {p for p in range(18) if sum(p in w for w in seed) == 20}
    require(saturated == {0, 1, 2, 5, 7, 8, 9, 10, 12, 14, 15, 16}, "wrong saturated set")
    cores = {(p, q): [w for w in seed if p not in w and q not in w]
             for p, q in itertools.combinations(range(18), 2)}
    require(min(map(len, cores.values())) == 34, "minimum pair-core size differs")
    all_minimum = [pair for pair, core in cores.items() if len(core) == 34]
    supports = [pair for pair in all_minimum if not set(pair) <= saturated]
    require(len(all_minimum) == 82 and len(supports) == 16, "wrong complete cohort")
    universe = [frozenset(t) for t in itertools.combinations(range(18), 5)]
    require(len(universe) == 8568, "wrong full universe")
    cases = []
    for p, q in supports:
        core = cores[p, q]
        words = [w for w in universe if w not in core and all(len(w & d) <= 2 for d in core)]
        words.sort(key=lambda w: sum(1 << v for v in w))
        n = len(words)
        adjacency = [frozenset(j for j, b in enumerate(words) if i != j and len(a & b) <= 2)
                     for i, a in enumerate(words)]
        zeros = [i for i, w in enumerate(words) if p not in w and q not in w]
        states = []
        for selection in range(1 << len(zeros)):
            chosen = [v for i, v in enumerate(zeros) if selection >> i & 1]
            if any(len(words[a] & words[b]) >= 3 for a, b in itertools.combinations(chosen, 2)):
                continue
            h = len(chosen)
            small = 16 - h
            large = max(small, (32 - h) // 2)
            require(small >= 0, "uncovered zero-word threshold")
            allowed = set(range(n))
            for v in chosen:
                allowed.intersection_update(adjacency[v])
            orientations = []
            for point in ([p] if large == small else [p, q]):
                other = q if point == p else p
                left = {v for v in allowed if point in words[v] and other not in words[v]}
                right = {v for v in allowed if other in words[v] and point not in words[v]}
                families = cliques(adjacency, left, large)
                digest = hashlib.sha256()
                right_count = 0
                queries = set()
                maximum = 0
                for a in families:
                    active = set(right)
                    for v in a:
                        active.intersection_update(adjacency[v])
                    opposite = cliques(adjacency, active, small)
                    digest.update((json.dumps([a, opposite], separators=(",", ":")) + "\n").encode())
                    right_count += len(opposite)
                    for b in opposite:
                        anchor = set(chosen) | set(a) | set(b)
                        require(len(anchor) == h + large + small, "overlapping anchor parts")
                        available = set(range(n))
                        for v in anchor:
                            available.intersection_update(adjacency[v])
                        available.difference_update(zeros)
                        bound = 69 - len(core) - len(anchor)
                        key = (frozenset(available), bound)
                        maximum = max(maximum, len(available))
                        if key not in queries:
                            require(not cliques(adjacency, available, bound + 1),
                                    "compatible anchor has an extension to size 70")
                            queries.add(key)
                orientations.append({"larger_coordinate": point, "left_families": len(families),
                                     "right_families": right_count, "extension_queries": len(queries),
                                     "maximum_extension_words": maximum, "families_sha256": digest.hexdigest()})
            states.append({"zero_selection": selection, "zero_count": h,
                           "thresholds": [large, small], "orientations": orientations})
        cases.append({"coordinates": [p, q], "core_size": len(core), "residual_words": n,
                      "zero_words": len(zeros), "states": states})
    return {"schema": "acl69-minimum-pair-core-report-v1", "seed_sha256": SEED_HASH,
            "minimum_core_size": 34, "all_minimum_pairs": len(all_minimum),
            "previous_saturated_pairs": 66, "new_pairs": len(cases), "cases": cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect", type=Path, default=ROOT / "expected.json")
    args = parser.parse_args()
    result = verify()
    require(result == json.loads(args.expect.read_text()), "independent replay differs from expected report")
    print(json.dumps({"verified_new_pairs": result["new_pairs"],
                      "all_minimum_pair_cores": result["all_minimum_pairs"],
                      "core_size": result["minimum_core_size"], "completion_maximum": 69}))


if __name__ == "__main__":
    main()
