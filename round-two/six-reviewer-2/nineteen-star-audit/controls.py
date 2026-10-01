#!/usr/bin/env python3
"""Exhaustive small native checks, decoding boundaries and literal point transports."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import subprocess

import audit


def affine_boundary():
    # GF(4) = F_2[t]/(t^2+t+1), with bit coordinates 0,1,t,t+1.
    def multiply(a, b):
        raw = 0
        for i in range(2):
            for j in range(2):
                if a & (1 << i) and b & (1 << j):
                    raw ^= 1 << (i + j)
        return raw ^ 7 if raw & 4 else raw
    lines = [audit.bitword(4 * x + (multiply(m, x) ^ b) for x in range(4))
             for m in range(4) for b in range(4)]
    lines += [audit.bitword(4 * x + y for y in range(4)) for x in range(4)]
    words = lines[:-1]
    stats, marks = audit.inspect(words)
    audit.require(not marks and stats["positive_deficits"] == [1, 1, 1, 1, 5] and
                  stats["high_high_pairs"] == 10, "affine m=0 boundary differs")
    return {"blocks":19,"unused_point":16,"positive_deficits":stats["positive_deficits"],
            "m":0,"e":10,"h":5}


def native(executable, neighbors, target):
    p = subprocess.run([str(executable)], input=audit.graph_text(neighbors, target),
                       text=True, capture_output=True, timeout=30)
    audit.require(p.returncode == 0, "native control failed: " + p.stderr)
    result = json.loads(p.stdout)
    audit.require(result["status"] == "COMPLETE", "incomplete native control")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    executable = args.native.resolve()
    graph_checks = 0
    pairs = list(combinations(range(4), 2))
    for mask in range(64):
        rows = [set() for _ in range(4)]
        for i, (a, b) in enumerate(pairs):
            if mask & (1 << i):
                rows[a].add(b); rows[b].add(a)
        for target in range(1, 5):
            result = native(executable, rows, target)
            literal = [list(q) for q in combinations(range(4), target)
                       if all(b in rows[a] for a, b in combinations(q, 2))]
            larger = any(all(b in rows[a] for a, b in combinations(q, 2))
                         for q in combinations(range(4), target + 1))
            audit.require(result["cliques"] == literal and result["larger_clique"] == larger,
                          "native/literal exhaustive control differs")
            graph_checks += 1
    boundary_checks = 0
    for n in (64, 65, 96, 128):
        for occupied in (9, 10):
            # Place the clique across the 64-bit boundary and at the largest index.
            vertices = list(range(n - occupied, n))
            rows = [set(vertices) - {i} if i in vertices else set() for i in range(n)]
            result = native(executable, rows, 9)
            audit.require(result["cliques"] == [list(q) for q in combinations(vertices, 9)],
                          "boundary clique list differs")
            audit.require(result["larger_clique"] == (occupied == 10), "boundary extension differs")
            boundary_checks += 1
    invalid = ["129 9\n", "3 0\n", "3 2\n2 1 1\n0\n0\n",
               "3 2\n1 1\n0\n0\n", "3 2\n0\n0\n0\nextra\n"]
    for text in invalid:
        p = subprocess.run([str(executable)], input=text, text=True, capture_output=True, timeout=30)
        audit.require(p.returncode != 0 and not p.stdout, "malformed native input accepted")
    result = json.loads(args.result.read_text())
    models = [audit.construct((5,)), audit.construct((2, 3))]
    transports = 0
    malformed_packings = 0
    for entry in result["manifest"]["unmarked_classes"]:
        model = models[entry["model"]]
        words = model["anchors"] + [audit.bitword(model["columns"][i]) for i in entry["clique"]]
        stats, marks = audit.inspect(words)
        # Actual arbitrary point relabeling, crossing the anchor/ordinary point boundary.
        permutation = tuple((5 * x + 3) % 17 for x in range(17))
        moved = [audit.transformed(w, permutation) for w in words]
        _, moved_marks = audit.inspect(moved)
        key = min(audit.normalize_mark(moved, pair, models) for pair in moved_marks)
        audit.require(key == (entry["model"], tuple(entry["clique"])), "unmarked key not point invariant")
        transports += 1
    first = result["manifest"]["unmarked_classes"][0]
    model = models[first["model"]]
    words = model["anchors"] + [audit.bitword(model["columns"][i]) for i in first["clique"]]
    damaged = [words[:-1], words[:-1] + [words[0]], words[:-1] + [1 << 17]]
    for candidate in damaged:
        try:
            audit.inspect(candidate)
        except RuntimeError:
            malformed_packings += 1
        else:
            raise RuntimeError("malformed packing accepted")
    _, marks = audit.inspect(words)
    replication = [sum(bool(w & (1 << x)) for w in words) for x in range(17)]
    covered = next((a, b) for a, b in combinations(range(17), 2)
                   if replication[a] == replication[b] == 5 and (a, b) not in marks)
    try:
        audit.normalize_mark(words, covered, models)
    except RuntimeError:
        malformed_packings += 1
    else:
        raise RuntimeError("covered anchor pair accepted")
    print(json.dumps({"status":"COMPLETE", "all_four_vertex_graph_target_checks":graph_checks,
                      "bit_boundary_graphs":boundary_checks,"malformed_native_inputs_rejected":len(invalid),
                      "arbitrarily_relabeled_class_checks":transports,
                      "malformed_packings_or_marks_rejected":malformed_packings,
                      "essential_m_positive_boundary":affine_boundary()},indent=2))


if __name__ == "__main__":
    main()
