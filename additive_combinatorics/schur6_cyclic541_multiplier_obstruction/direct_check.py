#!/usr/bin/env python3
"""Independent residue-set enumeration. No hypergraph or solver is imported."""
import hashlib
import json


def sumfree(p, values):
    return not any((a + b) % p in values for a in values for b in values)


def cosets(p, order):
    # Independent subgroup construction: all roots of X^order - 1.
    roots = {x for x in range(1, p) if pow(x, order, p) == 1}
    if len(roots) != order or p - 1 not in roots:
        raise ValueError("invalid subgroup order")
    result = []
    remaining = set(range(1, p))
    while remaining:
        x = min(remaining)
        block = frozenset(x * a % p for a in roots)
        if not block <= remaining:
            raise ValueError("cosets overlap")
        result.append(block)
        remaining -= block
    return result


def enumerate_direct(p, blocks, target):
    """Branch on actual residue unions and their modular sumsets."""
    n = len(blocks)
    masks = [sum(1 << a for a in b) for b in blocks]
    sums = [
        [sum(1 << z for z in {(a + b) % p for a in x for b in y}) for y in blocks]
        for x in blocks
    ]
    answers, nodes = [], 0

    def add(chosen, aset, sumset, v):
        enlarged = aset | masks[v]
        new_sums = sumset | sums[v][v]
        for u in chosen:
            new_sums |= sums[u][v]
        return enlarged, new_sums

    def visit(chosen, aset, sumset, candidates):
        nonlocal nodes
        nodes += 1
        if len(chosen) == target:
            answers.append(tuple(chosen))
            return
        for offset, v in enumerate(candidates):
            if len(chosen) + len(candidates) - offset < target:
                break
            enlarged, new_sums = add(chosen, aset, sumset, v)
            if enlarged & new_sums:
                raise ValueError("candidate filtering failed")
            selected = chosen + [v]
            tail = []
            for w in candidates[offset + 1:]:
                aset2, sumset2 = add(selected, enlarged, new_sums, w)
                if not aset2 & sumset2:
                    tail.append(w)
            visit(selected, enlarged, new_sums, tail)

    if not masks[0] & sums[0][0]:
        candidates = []
        for v in range(1, n):
            aset, sumset = add([0], masks[0], sums[0][0], v)
            if not aset & sumset:
                candidates.append(v)
        visit([0], masks[0], sums[0][0], candidates)
    return answers, nodes


def run():
    blocks = cosets(541, 10)
    eight, n8 = enumerate_direct(541, blocks, 8)
    nine, n9 = enumerate_direct(541, blocks, 9)
    if not eight or nine:
        raise ValueError("claimed maximum failed")
    # Directly check each complete returned set, including equal summands.
    for selected in eight:
        values = set().union(*(blocks[i] for i in selected))
        if len(values) != 80 or not sumfree(541, values):
            raise ValueError("invalid extremal set")
    raw = json.dumps(eight, separators=(",", ":")).encode()
    return {
        "normalized_maximum_sets": len(eight),
        "normalized_catalog_sha256": hashlib.sha256(raw).hexdigest(),
        "enumeration_nodes_target8": n8,
        "enumeration_nodes_target9": n9,
    }, eight


if __name__ == "__main__":
    print(json.dumps(run()[0], indent=2, sort_keys=True))
