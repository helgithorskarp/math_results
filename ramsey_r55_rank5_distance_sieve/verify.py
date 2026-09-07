"""Literal physical certificate checker: imports no factor or counting code."""
from itertools import combinations
import json
import re
import sys


def decode(graph):
    if not isinstance(graph, dict) or set(graph) != {"n", "red_hex"} or type(graph["n"]) is not int or graph["n"] != 43:
        raise ValueError("exact graph fields with n=43 required")
    h = graph["red_hex"]
    if not isinstance(h, str) or re.fullmatch(r"[0-9a-f]{226}", h) is None or int(h, 16) >= 2**903:
        raise ValueError("invalid 903-bit graph")
    bits = int(h, 16)
    adjacency = [[False]*43 for _ in range(43)]
    k = 0
    for u in range(43):
        for v in range(u+1, 43):
            adjacency[u][v] = adjacency[v][u] = bool((bits >> k) & 1)
            k += 1
    return adjacency


def verify(graph, certificate):
    adj = decode(graph)
    if not isinstance(certificate, dict) or set(certificate) != {"color", "vertices"}:
        raise ValueError("exact certificate fields required")
    c, vs = certificate["color"], certificate["vertices"]
    if c not in ("red", "blue") or not isinstance(vs, list) or len(vs) != 5:
        raise ValueError("invalid color or five-set")
    if any(type(x) is not int or not 0 <= x < 43 for x in vs) or vs != sorted(set(vs)):
        raise ValueError("invalid physical vertices")
    if any(adj[u][v] != (c == "red") for u, v in combinations(vs, 2)):
        raise ValueError("certificate has a wrong physical pair")
    return "VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE"


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        graph = json.load(f)
    with open(sys.argv[2], encoding="utf-8") as f:
        certificate = json.load(f)
    print(verify(graph, certificate))
