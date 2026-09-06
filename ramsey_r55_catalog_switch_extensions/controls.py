#!/usr/bin/env python3
"""Exhaustive physical controls for native generation and K5 interpretation."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from audit import expected
from physical import decode, rows, check_physical, require


def encode(n, mask):
    bits = f"{mask:0{n*(n-1)//2}b}"
    bits += "0"*((-len(bits)) % 6)
    return chr(n+63)+"".join(chr(63+int(bits[i:i+6],2)) for i in range(0,len(bits),6))


def reject(function):
    try:
        function()
    except ValueError:
        return
    raise RuntimeError("Invalid physical clause accepted")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("generator", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    # All four-vertex graphs; deterministic five/six-vertex boundary fixtures.
    records = [encode(4, mask) for mask in range(64)]
    records += [encode(5, mask) for mask in (0, 1, 31, 341, 682, 1023)]
    records += [encode(6, mask) for mask in (0, 1, 21845, 32767)]
    total = positives = 0
    with TemporaryDirectory(prefix="catalog-switch-controls-") as tmp:
        tmp = Path(tmp)
        data, cnf = tmp/"test.g6", tmp/"test.cnf"
        data.write_text("\n".join(records)+"\n")
        for index, record in enumerate(records):
            process = subprocess.run([str(args.generator.resolve()), str(data), str(index), str(cnf)],
                                     capture_output=True, text=True)
            require(process.returncode == 0, process.stderr)
            graph = decode(record)
            n = len(graph)
            formula = rows(cnf, 2*n-1)
            require(formula == expected(graph), "Native vs exhaustive-table mismatch")
            check_physical(graph, formula)
            five_sets = [list(combinations(vs, 2)) for vs in combinations(range(n+1), 5)]
            for word in range(1 << (2*n-1)):
                values = {i+1: word >> i & 1 for i in range(2*n-1)}
                spin = {0: 0, **{i: values[i] for i in range(1, n)}}
                red = {(u, v): graph[u][v]^spin[u]^spin[v] if v<n else values[n+u]
                       for u, v in combinations(range(n+1), 2)}
                valid = not any(len({red[edge] for edge in pairs}) == 1 for pairs in five_sets)
                satisfies = all(any(values[abs(x)] == (x>0) for x in row) for row in formula)
                require(valid == satisfies, "Global physical/CNF truth mismatch")
                positives += valid
                total += 1
        empty = [[0]*5 for _ in range(5)]
        check_physical(empty, {frozenset((1,2,3,4)), frozenset((1,2,3,5,6,7,8))})
        bad = [(1,), (1,2,3,4,5), (1,2,3,5,6,7,-8), (1,2,4,5,6,7,8), (-1,2,3,4)]
        for row in bad:
            reject(lambda row=row: check_physical(empty, {frozenset(row)}))
        for bad_record in ("", "A", "C", "C?@", "~???", "C\x00"):
            reject(lambda bad_record=bad_record: decode(bad_record))
    report = {"status": "PASS", "input_graphs": len(records), "physical_assignments": total,
              "valid_assignments": positives, "rejected_bad_physical_clauses": len(bad),
              "rejected_bad_graph6_records": 6}
    text = json.dumps(report, indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
