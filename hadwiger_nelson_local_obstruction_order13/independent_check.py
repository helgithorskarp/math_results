#!/usr/bin/env python3
"""Independent packed graph6 decoder and full local-obstruction replay."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDERS = (5, 7, 8, 9, 10, 11, 12, 13)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def contribution_tables(n):
    edges = [(i, j) for j in range(1, n) for i in range(j)]
    groups = [edges[k:k + 6] for k in range(0, len(edges), 6)]
    answer = []
    for group in groups:
        row = []
        for value in range(64):
            packed = 0
            for k, (u, v) in enumerate(group):
                if value & (1 << (5 - k)):
                    packed |= (1 << v) << (n * u)
                    packed |= (1 << u) << (n * v)
            row.append(packed)
        answer.append(tuple(row))
    return tuple(answer)


def decode(line, n, tables):
    require(line and line[0] == n + 63 and len(line) == len(tables) + 1,
            "bad graph6 header or length")
    packed = 0
    for table, char in zip(tables, line[1:]):
        value = char - 63
        require(0 <= value < 64, "bad graph6 character")
        packed |= table[value]
    spare = 6 * len(tables) - n * (n - 1) // 2
    require(not spare or not ((line[-1] - 63) & ((1 << spare) - 1)),
            "nonzero graph6 padding")
    mask = (1 << n) - 1
    return tuple((packed >> (n * vertex)) & mask for vertex in range(n))


def contains_k23(adjacency):
    for u, row in enumerate(adjacency):
        for v in range(u + 1, len(adjacency)):
            if (row & adjacency[v]).bit_count() >= 3:
                return True
    return False


def canonical_cycle(cycle):
    words = []
    for word in (cycle, list(reversed(cycle))):
        words.extend(word[k:] + word[:k] for k in range(len(word)))
    return min(words)


def odd_neighbourhood(adjacency):
    n = len(adjacency)
    for center, neighbours in enumerate(adjacency):
        colour = [-1] * n
        parent = [-1] * n
        for root in range(n):
            if not (neighbours >> root) & 1 or colour[root] >= 0:
                continue
            colour[root] = 0
            queue = [root]
            for u in queue:
                pending = adjacency[u] & neighbours
                while pending:
                    bit = pending & -pending
                    pending -= bit
                    v = bit.bit_length() - 1
                    if colour[v] < 0:
                        colour[v] = colour[u] ^ 1
                        parent[v] = u
                        queue.append(v)
                    elif colour[v] == colour[u]:
                        up, vp = [], []
                        x = u
                        while x >= 0:
                            up.append(x); x = parent[x]
                        x = v
                        while x >= 0:
                            vp.append(x); x = parent[x]
                        i, j = len(up) - 1, len(vp) - 1
                        while i >= 0 and j >= 0 and up[i] == vp[j]:
                            i -= 1; j -= 1
                        cycle = up[:i + 2] + list(reversed(vp[:j + 1]))
                        require(len(cycle) % 2 == 1, "BFS returned an even cycle")
                        return center, canonical_cycle(cycle)
    return None


def scan(path, n):
    tables = contribution_tables(n)
    total = k23_free = admissible = 0
    exceptions = []
    with path.open("rb") as source:
        for raw in source:
            line = raw.rstrip(b"\r\n")
            if not line:
                continue
            adjacency = decode(line, n, tables)
            total += 1
            if contains_k23(adjacency):
                continue
            k23_free += 1
            obstruction = odd_neighbourhood(adjacency)
            if obstruction is None:
                admissible += 1
            else:
                center, cycle = obstruction
                exceptions.append({
                    "order": n,
                    "graph6": line.decode("ascii"),
                    "edges": sum(row.bit_count() for row in adjacency) // 2,
                    "odd_neighbourhood": {"center": center, "cycle": cycle},
                })
    return {"total": total, "k23_free": k23_free,
            "locally_admissible": admissible}, exceptions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog-dir", type=Path, required=True)
    args = parser.parse_args()
    expected = json.loads((HERE / "expected.json").read_text())
    report = {"status": expected["status"], "orders": {}, "k23_free_exceptions": []}
    for n in ORDERS:
        row, exceptions = scan(args.catalog_dir / f"crit_{n}_5.g6", n)
        report["orders"][str(n)] = row
        report["k23_free_exceptions"].extend(exceptions)
    require(report == expected, "independent full-catalog report mismatch")
    print((HERE / "expected.json").read_text(), end="")


if __name__ == "__main__":
    main()
