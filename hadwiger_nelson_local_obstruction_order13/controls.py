#!/usr/bin/env python3
"""Small exact controls and direct checks of the unique order-13 exception."""
import json
from pathlib import Path
import independent_check as check

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(adjacency):
    n = len(adjacency)
    bits = [((adjacency[i] >> j) & 1) for j in range(1, n) for i in range(j)]
    bits += [0] * ((-len(bits)) % 6)
    payload = bytes(63 + sum(bits[k + i] << (5 - i) for i in range(6))
                    for k in range(0, len(bits), 6))
    return bytes([n + 63]) + payload


def graph(n, edges):
    adjacency = [0] * n
    for u, v in edges:
        require(0 <= u < v < n, "bad control edge")
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return tuple(adjacency)


def colourable(adjacency, colours, omitted_edge=None):
    n = len(adjacency)
    degree_order = sorted(range(n), key=lambda v: adjacency[v].bit_count(), reverse=True)
    assigned = [-1] * n
    def visit(at):
        if at == n:
            return tuple(assigned)
        v = degree_order[at]
        forbidden = 0
        for u in range(n):
            if assigned[u] < 0 or not ((adjacency[v] >> u) & 1):
                continue
            if omitted_edge is not None and {u, v} == set(omitted_edge):
                continue
            forbidden |= 1 << assigned[u]
        for c in range(colours):
            if not ((forbidden >> c) & 1):
                assigned[v] = c
                answer = visit(at + 1)
                if answer is not None:
                    return answer
        assigned[v] = -1
        return None
    return visit(0)


def main():
    fixtures = {}
    k5 = graph(5, [(u, v) for u in range(5) for v in range(u + 1, 5)])
    fixtures["k5_has_k23"] = check.contains_k23(k5)
    require(fixtures["k5_has_k23"], "K5 control")

    k4 = graph(4, [(u, v) for u in range(4) for v in range(u + 1, 4)])
    fixtures["k4_odd_neighbourhood"] = check.odd_neighbourhood(k4)
    require(fixtures["k4_odd_neighbourhood"] == (0, [1, 2, 3]), "K4 control")

    k23 = graph(5, [(u, v) for u in range(2) for v in range(2, 5)])
    require(check.contains_k23(k23), "K2,3 control")

    wheel5 = graph(6, [(0, v) for v in range(1, 6)] +
                   [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5)])
    require(not check.contains_k23(wheel5), "five-wheel should be K2,3-free")
    require(check.odd_neighbourhood(wheel5) == (0, [1, 2, 3, 4, 5]), "five-wheel control")

    wheel6 = graph(7, [(0, v) for v in range(1, 7)] +
                   [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 6)])
    require(not check.contains_k23(wheel6) and check.odd_neighbourhood(wheel6) is None,
            "regular-hexagon wheel positive control")

    line = (HERE / "unique13.g6").read_bytes().strip()
    adjacency = check.decode(line, 13, check.contribution_tables(13))
    require(encode(adjacency) == line, "graph6 round trip")
    require(sum(row.bit_count() for row in adjacency) // 2 == 33, "exception edge count")
    require(not check.contains_k23(adjacency), "exception K2,3 check")
    require(check.odd_neighbourhood(adjacency) == (0, [3, 5, 12, 7, 10]),
            "exception odd-neighbourhood witness")
    require(colourable(adjacency, 4) is None, "exception unexpectedly four-colourable")
    five_colouring = colourable(adjacency, 5)
    require(five_colouring is not None, "exception lacks five-colouring")
    edge_deletion_colourings = 0
    for u in range(13):
        for v in range(u + 1, 13):
            if (adjacency[u] >> v) & 1:
                require(colourable(adjacency, 4, (u, v)) is not None,
                        f"exception edge {u}-{v} is not critical")
                edge_deletion_colourings += 1

    malformed = 0
    for bad in (b"", b"MCQRDPqReqFchs", line[:-1], line + b"?", line[:-1] + b"!"):
        try:
            check.decode(bad, 13, check.contribution_tables(13))
        except ValueError:
            malformed += 1
    require(malformed == 5, "malformed graph6 controls")
    print(json.dumps({
        "all_checks": True,
        "unique_exception_edges": 33,
        "unique_exception_edge_deletions_four_coloured": edge_deletion_colourings,
        "unique_exception_five_colouring": list(five_colouring),
        "positive_unit_hexagon_wheel_passes_local_gate": True,
        "malformed_graph6_rejected": malformed,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
