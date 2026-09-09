#!/usr/bin/env python3
"""Transport, receiver, and corruption controls for the physical certificate."""
import copy
import itertools as it
import json
import random
from pathlib import Path
import interface
import verify


def rejected(call):
    try:
        call()
    except (ValueError, KeyError):
        return
    raise ValueError("deliberate corruption accepted")


def main():
    rng = random.Random(550043)
    pairs = list(it.combinations(range(43), 2))
    transports = witnesses = rejected_inputs = 0
    for trial in range(4):
        labels = list(range(19)) if not trial else rng.sample(range(43), 19)
        for color in (0, 1):
            cut = interface.instantiate(labels, color)
            verify.audit_cut(cut)
            transports += 1
            # Explicitly permute and offset SAT numbers; positive still means red.
            numbers = rng.sample(range(1001, 4001), 903)
            mapping = {"edges": [[*p, "var", x] for p, x in zip(pairs, numbers)]}
            result = interface.receive(cut, mapping)
            wanted = {(u, v): truth for u, v, truth in cut["physical_clause"]}
            expected = [(2*wanted[p]-1)*x for p, x in zip(pairs, numbers) if p in wanted]
            verify.require(result["status"] == "CLAUSE" and sorted(result["clause"]) == sorted(expected),
                           "receiver numbering mismatch")
            # One false template condition makes the blocker tautological.
            one = copy.deepcopy(mapping)
            u, v, truth = cut["physical_clause"][0]
            one["edges"][pairs.index((u, v))] = [u, v, "fixed", truth]
            verify.require(interface.receive(cut, one)["status"] == "TAUTOLOGY", "tautology missed")
            # All template conditions, with 756 other variables still free.
            partial = copy.deepcopy(mapping)
            for e in partial["edges"]:
                if tuple(e[:2]) in wanted:
                    e[2:] = ["fixed", 1-wanted[tuple(e[:2])]]
            verify.require(interface.receive(cut, partial)["status"] == "CONFLICT", "conflict missed")
            # Complete assignments in the counted family; no candidate input is used.
            outside = [v for v in range(43) if v not in labels]
            root_pairs = {tuple(sorted((labels[0], v))) for v in outside}
            chosen = set(rng.sample(sorted(root_pairs), 3))
            graph = {}
            for p in pairs:
                if p in wanted:
                    graph[p] = 1-wanted[p]
                elif p in root_pairs:
                    graph[p] = color if p in chosen else 1-color
                else:
                    graph[p] = rng.randrange(2)
            verify.require(390 <= sum(graph.values()) <= 513, "fixture outside edge window")
            degree = sum(graph[tuple(sorted((labels[0], v)))] == color
                         for v in range(43) if v != labels[0])
            verify.require(degree == 21, "fixture outside root-degree window")
            full = {"edges": [[*p, "fixed", graph[p]] for p in pairs]}
            result = interface.receive(cut, full)
            witness = result["monochromatic_five"]
            five, c = witness["vertices"], witness["color"]
            verify.require(len(set(five)) == 5 and
                           all(graph[e] == c for e in it.combinations(sorted(five), 2)),
                           "invalid literal five-set witness")
            witnesses += 1
    cut = interface.instantiate(list(range(19)), 1)
    for corruption in ("premise", "guard", "empty_proof", "bad_rup"):
        bad = copy.deepcopy(cut)
        if corruption == "premise":
            bad["canonical_premises"][0]["clause"][0] *= -1
        elif corruption == "guard":
            bad["physical_clause"][0][2] ^= 1
        elif corruption == "empty_proof":
            bad["canonical_rup"] = []
        else:
            bad["canonical_rup"] = [bad["canonical_clause"]]
        rejected(lambda: verify.audit_cut(bad))
        rejected_inputs += 1
    mapping = {"edges": [[*p, "var", i+1] for i, p in enumerate(pairs)]}
    duplicate = copy.deepcopy(mapping)
    duplicate["edges"][1][3] = duplicate["edges"][0][3]
    rejected(lambda: interface.receive(cut, duplicate))
    rejected(lambda: interface.receive(cut, {"edges": mapping["edges"][:-1]}))
    rejected(lambda: interface.instantiate([0]*19, 1))
    rejected(lambda: interface.instantiate(list(range(19)), 2))
    rejected_inputs += 4
    # RUP unit checker controls include both satisfiable and conflicting formulas.
    require = verify.require
    require(not verify.propagation([verify.masks([1, 2], 2)], [])[0], "false conflict")
    require(verify.propagation([verify.masks([1], 2), verify.masks([-1], 2)], [])[0],
            "missed conflict")
    print(json.dumps({"status": "CONTROLS_PASS", "transported_proofs": transports,
                      "complete_assignment_witnesses": witnesses,
                      "deliberate_corruptions_rejected": rejected_inputs}, sort_keys=True))


if __name__ == "__main__":
    main()
