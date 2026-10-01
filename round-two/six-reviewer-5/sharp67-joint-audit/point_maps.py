"""Exact full point-isomorphism quotient of the normalized equality inventory.

Pair/triple invariants only prune. Complete five-block equality decides leaves.
No chosen center, marked pair, or anchor structure is required to be preserved.
"""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import argparse
import time
from check import canonical, digest, decode, packing, require


def structure(words):
    packing(words, 67)
    blocks = frozenset(decode(w) for w in words)
    degrees = tuple(sum(i in b for b in blocks) for i in range(18))
    pairs = tuple(tuple(sum({i, j} <= b for b in blocks) if i != j else 0
                        for j in range(18)) for i in range(18))
    triples = frozenset(frozenset(t) for b in blocks for t in combinations(sorted(b), 3))
    keys = tuple((degrees[i], tuple(sorted(pairs[i][j] for j in range(18) if j != i)))
                 for i in range(18))
    return blocks, pairs, triples, keys


def maps(source, target, first_only=False):
    sb, sp, st, sk = source
    tb, tp, tt, tk = target
    if sorted(sk) != sorted(tk):
        return [], 0
    result = []
    assignment = {}
    used = set()
    nodes = 0
    begun = time.monotonic()

    def domain(v):
        previous = list(assignment)
        answer = []
        for w in range(18):
            if w in used or sk[v] != tk[w]:
                continue
            if any(sp[v][a] != tp[w][assignment[a]] for a in previous):
                continue
            if any((frozenset((v, a, b)) in st) !=
                   (frozenset((w, assignment[a], assignment[b])) in tt)
                   for a, b in combinations(previous, 2)):
                continue
            answer.append(w)
        return answer

    def visit():
        nonlocal nodes
        nodes += 1
        require(nodes <= 2000000 and time.monotonic() - begun < 20,
                "INCOMPLETE point-isomorphism guard")
        if len(assignment) == 18:
            perm = [assignment[v] for v in range(18)]
            if frozenset(frozenset(perm[v] for v in b) for b in sb) == tb:
                result.append(perm)
            return
        possibilities = [(domain(v), v) for v in range(18) if v not in assignment]
        candidates, vertex = min(possibilities, key=lambda x: (len(x[0]), x[1]))
        for image in candidates:
            assignment[vertex] = image
            used.add(image)
            visit()
            used.remove(image)
            del assignment[vertex]
            if first_only and result:
                return

    visit()
    return sorted(result), nodes


def quotient(exact):
    begun = time.monotonic()
    codes = {r["code_sha256"]: r["blocks"] for r in exact["equality"]}
    require(len(codes) == exact["equality_distinct_codes"] == 107, "complete normalized equality input")
    hashes = sorted(codes)
    objects = {h: structure(codes[h]) for h in hashes}
    classes = []
    memberships = []
    calls = 0
    nodes = 0
    peak = 0
    for h in hashes:
        require(time.monotonic() - begun < 60, "INCOMPLETE whole-quotient guard")
        found = False
        for i, cls in enumerate(classes):
            candidate, n = maps(objects[h], objects[cls["representative"]], True)
            calls += 1
            nodes += n
            peak = max(peak, n)
            if candidate:
                memberships.append({"code_sha256": h, "class": i, "point_map": candidate[0]})
                found = True
                break
        if not found:
            i = len(classes)
            automorphisms, n = maps(objects[h], objects[h])
            calls += 1
            nodes += n
            peak = max(peak, n)
            identity = list(range(18))
            require(identity in automorphisms and len(automorphisms) == len({tuple(p) for p in automorphisms}), "point group identity/duplicates")
            group = {tuple(p) for p in automorphisms}
            for a in automorphisms:
                require(sorted(a) == identity, "point permutation")
                for b in automorphisms:
                    require(tuple(a[b[i]] for i in range(18)) in group, "point group closure")
            classes.append({"representative": h, "automorphism_order": len(automorphisms),
                            "automorphisms": automorphisms})
            memberships.append({"code_sha256": h, "class": i, "point_map": identity})
    require(len(memberships) == 107, "quotient input coverage")
    for i, cls in enumerate(classes):
        cls["normalized_count"] = sum(r["class"] == i for r in memberships)
    return {"status": "COMPLETE", "inventory_sha256": digest(exact), "classes": classes,
            "memberships": memberships, "isomorphism_class_count": len(classes),
            "point_group_order_histogram": dict(sorted(Counter(c["automorphism_order"] for c in classes).items())),
            "map_calls": calls, "nodes": nodes, "peak_query_nodes": peak,
            "seconds": time.monotonic() - begun}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    obj = quotient(json.loads(args.input.read_text()))
    seconds = obj.pop("seconds")
    args.output.write_bytes(canonical(obj))
    args.output.with_suffix(".time.json").write_bytes(canonical({"seconds": seconds}))
    print(json.dumps({**{k: v for k, v in obj.items() if k not in ("classes", "memberships")}, "seconds": seconds}))
