#!/usr/bin/env python3
"""Independent definition-level witness checker; imports no generator code."""
import hashlib
import itertools as it
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matrix(n, edges):
    a = [[False for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        require(0 <= u < n and 0 <= v < n and u != v, "invalid edge")
        a[u][v] = a[v][u] = True
    return a


def gem(a, s):
    for center in s:
        path = [v for v in s if v != center]
        if not all(a[center][v] for v in path):
            continue
        # A simple four-vertex graph with degrees 1,1,2,2 is exactly P4.
        if sorted(sum(a[u][v] for v in path) for u in path) == [1, 1, 2, 2]:
            return True
    return False


def bull(a, s):
    for triangle in it.combinations(s, 3):
        if not all(a[u][v] for u, v in it.combinations(triangle, 2)):
            continue
        x, y = [v for v in s if v not in triangle]
        if a[x][y]:
            continue
        nx = [v for v in triangle if a[x][v]]
        ny = [v for v in triangle if a[y][v]]
        if len(nx) == len(ny) == 1 and nx != ny:
            return True
    return False


def verify_witness(a, w):
    subsets = list(it.combinations(range(len(a)), 5))
    require(type(w) is int and 0 <= w < 2 * len(subsets), "bad witness range")
    require((gem if w % 2 == 0 else bull)(a, subsets[w // 2]), "false witness")


def decode(s, length):
    require(type(s) is str and len(s) == 2 * length, "wrong certificate length")
    b = bytes.fromhex(s)
    require(b.hex() == s, "noncanonical hex")
    return b


def check(data):
    require(set(data) == {"format", "majority", "attachment", "isolation"},
            "unknown/missing field")
    require(data["format"] == "prism-majority-v1", "wrong format")
    require(type(data["majority"]) is list and len(data["majority"]) == 10,
            "wrong rooted-case count")
    # Rooted graphs are reconstructed by their definitions, not bitset codes.
    graphs = [matrix(5, [(i, i + 1) for i in range(3)] + [(4, i) for i in range(4)]),
              matrix(5, list(it.combinations(range(3), 2)) + [(0, 3), (1, 4)])]
    checks = 0
    for fidx, f in enumerate(graphs):
        for apex in range(5):
            cert = decode(data["majority"][5 * fidx + apex], 256)
            old = [v for v in range(5) if v != apex]
            # Literal minority/majority masks in increasing numerical order.
            choices = [(3, 5, 6, 7) if f[apex][v] else (0, 1, 2, 4) for v in old]
            for index in range(256):
                digits = [(index // (4 ** (3 - j))) % 4 for j in range(4)]
                a = matrix(7, list(it.combinations((4, 5, 6), 2)))
                for i, j in it.combinations(range(4), 2):
                    a[i][j] = a[j][i] = f[old[i]][old[j]]
                for i in range(4):
                    mask = choices[i][digits[i]]
                    for j in range(3):
                        a[i][4 + j] = a[4 + j][i] = bool(mask & (1 << j))
                verify_witness(a, cert[index])
                checks += 1
    prism_edges = list(it.combinations(range(3), 2))
    prism_edges += list(it.combinations(range(3, 6), 2))
    prism_edges += [(i, i + 3) for i in range(3)]
    allowed = []
    attachment = decode(data["attachment"], 64)
    for s in range(64):
        a = matrix(7, prism_edges + [(6, j) for j in range(6) if s & (1 << j)])
        if attachment[s] == 255:
            require(not any(gem(a, t) or bull(a, t)
                            for t in it.combinations(range(7), 5)), "false allowed mask")
            allowed.append(s)
            if s:
                ma = sum(a[6][j] for j in range(3)) >= 2
                mb = sum(a[6][j] for j in range(3, 6)) >= 2
                require(ma != mb, "majorities do not partition")
        else:
            verify_witness(a, attachment[s])
            checks += 1
    isolation = decode(data["isolation"], 63)
    for s in range(1, 64):
        a = matrix(8, prism_edges + [(6, 7)] +
                   [(7, j) for j in range(6) if s & (1 << j)])
        verify_witness(a, isolation[s - 1])
        checks += 1
    return {"attachment_cases": 64, "allowed_attachment_masks": allowed,
            "isolation_cases": 63, "majority_cases": 2560,
            "obstruction_witnesses_verified": checks, "status": "PASS"}


def controls(data):
    # Definition controls, plus rejection of a deliberately false obstruction.
    require(gem(matrix(5, [(0, 1), (1, 2), (2, 3)] + [(4, i) for i in range(4)]),
                tuple(range(5))), "gem positive control")
    require(bull(matrix(5, [(0, 1), (1, 2), (2, 0), (0, 3), (1, 4)]),
                 tuple(range(5))), "bull positive control")
    for edges in [[], list(it.combinations(range(5), 2)), [(i, (i + 1) % 5) for i in range(5)]]:
        a = matrix(5, edges)
        require(not gem(a, tuple(range(5))) and not bull(a, tuple(range(5))), "negative control")
    corrupt = dict(data)
    b = bytearray.fromhex(data["attachment"])
    b[0] = 0  # An isolated vertex added to a prism creates no forbidden graph.
    corrupt["attachment"] = b.hex()
    try:
        check(corrupt)
    except ValueError:
        return
    raise ValueError("corrupted certificate accepted")


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name("certificate.json")
    raw = path.read_bytes()
    data = json.loads(raw)
    output = check(data)
    controls(data)
    output["controls"] = "PASS"
    output["certificate_sha256"] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(output, sort_keys=True, indent=2))
