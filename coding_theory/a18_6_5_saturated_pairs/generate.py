#!/usr/bin/env python3
"""Propose exhaustive clique-classification trees; verify.py is the checker."""
import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED_HASH = "cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d"


def prepare():
    raw = (ROOT / "acl69.txt").read_bytes()
    if hashlib.sha256(raw).hexdigest() != SEED_HASH:
        raise ValueError("wrong seed file")
    rows = raw.decode("ascii").splitlines()
    if len(rows) != 69 or any(len(s) != 18 or set(s) - set("01")
                              or s.count("1") != 5 for s in rows):
        raise ValueError("malformed seed")
    seed = [sum(1 << p for p, c in enumerate(s) if c == "1") for s in rows]
    if len(set(seed)) != 69:
        raise ValueError("duplicate seed word")
    owners = {}
    for i, word in enumerate(seed):
        for triple in itertools.combinations([p for p in range(18) if word >> p & 1], 3):
            if triple in owners:
                raise ValueError("seed reuses a triple")
            owners[triple] = i
    candidates = []
    for block in itertools.combinations(range(18), 5):
        word = sum(1 << p for p in block)
        if word in seed:
            continue
        blocked = {owners[t] for t in itertools.combinations(block, 3) if t in owners}
        candidates.append((word, sum(1 << i for i in blocked)))
    return seed, candidates


def classification(words, node_limit, seconds):
    """Classify all compatible 16-subsets using a binary decision tree."""
    adjacency = [sum(1 << j for j, other in enumerate(words)
                     if i != j and (word & other).bit_count() <= 2)
                 for i, word in enumerate(words)]
    started = time.monotonic()
    nodes = 0
    witnesses = []

    def color(active):
        classes = []
        last = None
        while active:
            available = active
            part = 0
            while available:
                bit = available & -available
                last = bit.bit_length() - 1
                part |= bit
                active ^= bit
                available &= ~bit
                available &= ~adjacency[last]
            classes.append(part)
        return classes, last

    def visit(active, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit or (nodes % 128 == 0
                                  and time.monotonic() - started > seconds):
            raise RuntimeError("INCOMPLETE: classification resource limit reached")
        if len(chosen) == 16:
            witness = sorted(chosen)
            witnesses.append(witness)
            return {"w": witness}
        classes, vertex = color(active)
        if len(classes) < 16 - len(chosen):
            return {"c": classes}
        return {"v": vertex,
                "i": visit(active & adjacency[vertex], chosen + [vertex]),
                "o": visit(active & ~(1 << vertex), chosen)}

    tree = visit((1 << len(words)) - 1, [])
    if len(witnesses) != len({tuple(w) for w in witnesses}):
        raise RuntimeError("duplicate classification witness")
    return tree, witnesses


def construct(node_limit, seconds):
    seed, candidates = prepare()
    saturated = [p for p in range(18) if sum(w >> p & 1 for w in seed) == 20]
    entries = []
    for p, q in itertools.combinations(saturated, 2):
        support = (1 << p) | (1 << q)
        removed = [i for i, w in enumerate(seed) if w & support]
        removed_mask = sum(1 << i for i in removed)
        residual = ([seed[i] for i in removed]
                    + [w for w, blocked in candidates
                       if blocked & removed_mask == blocked])
        if len(seed) - len(removed) != 34:
            raise RuntimeError("unexpected retained-core size")
        first = sorted(w for w in residual if not w >> q & 1)
        tree, witnesses = classification(first, node_limit, seconds)
        proofs = [{"avoid": q, "tree": tree}]
        mode = "one-side"
        if witnesses:
            if len(witnesses) != 1 or any(w & support == 0 for w in residual):
                raise RuntimeError("completion bound not certified by this mechanism")
            second = sorted(w for w in residual if not w >> p & 1)
            other_tree, other_witnesses = classification(second, node_limit, seconds)
            if len(other_witnesses) != 1:
                raise RuntimeError("coupled classification is not unique")
            left = [first[v] for v in witnesses[0]]
            right = [second[v] for v in other_witnesses[0]]
            if all((a & b).bit_count() <= 2 for a in left for b in right):
                raise RuntimeError("coupled witnesses are compatible; no bound certified")
            mode = "coupled"
            proofs.append({"avoid": p, "tree": other_tree})
        entries.append({"coordinates": [p, q], "mode": mode, "proofs": proofs})
    return {"schema": "acl69-saturated-pair-classification-v1",
            "seed_sha256": SEED_HASH, "cases": entries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--node-limit", type=int, default=200_000)
    parser.add_argument("--seconds-per-tree", type=float, default=10)
    args = parser.parse_args()
    if args.output and args.check:
        parser.error("choose --output or --check")
    result = construct(args.node_limit, args.seconds_per_tree)
    if args.check:
        if result != json.loads(args.check.read_text()):
            raise RuntimeError("certificate differs from deterministic regeneration")
        print("Regenerated all 66 pair classifications exactly.")
    elif args.output:
        args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n")
    else:
        print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()
