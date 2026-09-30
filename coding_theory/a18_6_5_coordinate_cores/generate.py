#!/usr/bin/env python3
"""Construct conflict-clique covers. Search is not the proof trust boundary."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SEED_HASH = "cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d"


def prepare():
    raw = (ROOT / "acl69.txt").read_bytes()
    if hashlib.sha256(raw).hexdigest() != SEED_HASH:
        raise ValueError("wrong seed file")
    words = raw.decode("ascii").splitlines()
    if len(words) != 69 or any(len(s) != 18 or set(s) - set("01")
                              or s.count("1") != 5 for s in words):
        raise ValueError("malformed seed")
    seed = [sum(1 << i for i, c in enumerate(s) if c == "1") for s in words]
    if len(set(seed)) != 69:
        raise ValueError("duplicate seed word")
    owners = {}
    for i, mask in enumerate(seed):
        for triple in itertools.combinations([p for p in range(18) if mask >> p & 1], 3):
            if triple in owners:
                raise ValueError("seed reuses a triple")
            owners[triple] = i
    new = []
    for block in itertools.combinations(range(18), 5):
        mask = sum(1 << p for p in block)
        if mask in seed:
            continue
        blocked_by = {owners[t] for t in itertools.combinations(block, 3) if t in owners}
        new.append((mask, sum(1 << i for i in blocked_by)))
    return seed, new


def coloring(blocks, domains, node_limit):
    """Fixed seed colors, minimum remaining domain, least constrained color."""
    n = len(blocks)
    compatible = [sum(1 << j for j, other in enumerate(blocks)
                      if j != i and (mask & other).bit_count() <= 2)
                  for i, mask in enumerate(blocks)]
    degrees = [m.bit_count() for m in compatible]
    assignment = [-1] * n
    nodes = 0

    def bits(mask):
        while mask:
            bit = mask & -mask
            mask -= bit
            yield bit.bit_length() - 1

    def solve(todo):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit:
            raise RuntimeError("INCOMPLETE: coloring search node limit reached")
        if not todo:
            return True
        v = min(bits(todo), key=lambda w: (domains[w].bit_count(), -degrees[w], w))
        if not domains[v]:
            return False
        neighbors = list(bits(compatible[v] & todo))
        choices = []
        for c in bits(domains[v]):
            bit = 1 << c
            cost = sum(3 if domains[w].bit_count() == 2 else 1
                       for w in neighbors if domains[w] & bit)
            choices.append((cost, c))
        for _, c in sorted(choices):
            bit = 1 << c
            changed = []
            bad = False
            for w in neighbors:
                if domains[w] & bit:
                    changed.append((w, domains[w]))
                    domains[w] ^= bit
                    if not domains[w]:
                        bad = True
                        break
            if not bad:
                assignment[v] = c
                if solve(todo ^ (1 << v)):
                    return True
                assignment[v] = -1
            for w, old in changed:
                domains[w] = old
        return False

    if not solve((1 << n) - 1):
        raise RuntimeError("no coloring found; this does not prove a larger code exists")
    return assignment


def construct(node_limit):
    seed, new = prepare()
    supports = [(p,) for p in range(18)] + [(p, 17) for p in range(17)]
    entries = []
    for support in supports:
        point_mask = sum(1 << p for p in support)
        removed = [i for i, mask in enumerate(seed) if mask & point_mask]
        removed_mask = sum(1 << i for i in removed)
        candidates = [(b, z) for b, z in new if z & removed_mask == z]
        labels = coloring([b for b, _ in candidates], [z for _, z in candidates], node_limit)
        local_colors = {c: ALPHABET[i] for i, c in enumerate(removed)}
        entries.append({"coordinates": list(support),
                        "colors": "".join(local_colors[c] for c in labels)})
    return {"schema": "acl69-coordinate-clique-cover-v1", "seed_sha256": SEED_HASH,
            "alphabet": ALPHABET, "covers": entries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--node-limit", type=int, default=2_000_000)
    args = parser.parse_args()
    if args.output and args.check:
        parser.error("choose --output or --check")
    certificate = construct(args.node_limit)
    if args.check:
        if certificate != json.loads(args.check.read_text()):
            raise RuntimeError("certificate differs from deterministic regeneration")
        print("Regenerated all 35 covers exactly.")
    else:
        text = json.dumps(certificate, indent=2) + "\n"
        if args.output:
            args.output.write_text(text)
        else:
            print(text, end="")


if __name__ == "__main__":
    main()
