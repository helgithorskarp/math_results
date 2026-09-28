#!/usr/bin/env python3
"""Regenerate a deduction certificate, using integer masks and a work queue."""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path


def closure(colours, prefix, n):
    domains = [63] * (n + 1)
    processed = [[] for _ in range(6)]
    queue = deque(range(1, prefix + 1))
    trace = []
    for x in queue:
        domains[x] = 1 << (colours[x] - 1)

    def delete(target, bit, x, y):
        if not 1 <= target <= n or not domains[target] & bit:
            return True
        domains[target] &= ~bit
        trace.append([target, bit.bit_length(), min(x, y), max(x, y)])
        if not domains[target]:
            return False
        if domains[target].bit_count() == 1:
            queue.append(target)
        return True

    while queue:
        x = queue.popleft()
        bit = domains[x]
        colour = bit.bit_length() - 1
        if not delete(2 * x, bit, x, x):
            return False, domains, trace
        if x % 2 == 0 and not delete(x // 2, bit, x // 2, x // 2):
            return False, domains, trace
        for y in processed[colour]:
            if not delete(x + y, bit, x, y):
                return False, domains, trace
            if not delete(abs(x - y), bit, abs(x - y), min(x, y)):
                return False, domains, trace
        processed[colour].append(x)
    return True, domains, trace


def prune(colours, prefix, domains, trace):
    locations = {(t, c): i for i, (t, c, _, _) in enumerate(trace)}
    needed = set()

    def need_fixed(vertex, colour, before):
        if vertex <= prefix:
            if colours[vertex] != colour:
                raise ValueError("inconsistent seed in dependency trace")
            return
        for other in range(1, 7):
            if other != colour:
                index = locations[vertex, other]
                if index >= before:
                    raise ValueError("forward dependency in deduction")
                need_step(index)

    def need_step(index):
        if index in needed:
            return
        needed.add(index)
        target, colour, x, y = trace[index]
        for vertex in sorted({x, y, x + y} - {target}):
            need_fixed(vertex, colour, index)

    empty = next(x for x in range(1, len(domains)) if not domains[x])
    for colour in range(1, 7):
        need_step(locations[empty, colour])
    return [trace[index] for index in sorted(needed)]


def encode(proof):
    head = {key: value for key, value in proof.items() if key != "steps"}
    return (json.dumps(head, indent=2)[:-2] + ',\n  "steps": [\n' +
            ",\n".join("    " + json.dumps(step, separators=(",", ":"))
                       for step in proof["steps"]) + "\n  ]\n}\n")


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = (here / "baseline.txt").read_bytes()
    word = data.decode("ascii").strip()
    if len(word) != 536 or not set(word) <= set("123456"):
        raise ValueError("malformed baseline")
    colours = [0] + list(map(int, word))
    open81, domains, trace = closure(colours, 81, 537)
    if open81:
        raise ValueError("the selected prefix was not refuted")
    proof = {
        "format": "schur-domain-deletion-v1",
        "N": 537,
        "colours": 6,
        "prefix": 81,
        "baseline_sha256": hashlib.sha256(data).hexdigest(),
        "steps": prune(colours, 81, domains, trace),
    }
    args.output.write_text(encode(proof))
    controls = []
    for n, prefix in [(537, 80), (536, 81)]:
        unrefuted, masks, _ = closure(colours, prefix, n)
        controls.append({"N": n, "prefix": prefix, "unrefuted": unrefuted,
                         "singleton_domains": sum(m.bit_count() == 1 for m in masks[1:])})
    print(json.dumps({"full_trace_steps": len(trace),
                      "certificate_steps": len(proof["steps"]),
                      "controls": controls}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
