#!/usr/bin/env python3
"""Solver-free exact verifier for vertex-minimality of the T375 relation."""

from __future__ import annotations

import base64
import binascii
import copy
import hashlib
import json
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "hadwiger_nelson_small_triangle_forcer375"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read(path: Path):
    return json.loads(path.read_text())


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value_sha256(value) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def rotate(p: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, c, d = p
    doubled = (-a - c, -b - 3 * d, 3 * a - c, b - d)
    require(all(v % 2 == 0 for v in doubled), "nonintegral orbit")
    return tuple(v // 2 for v in doubled)


def reconstruct_graph():
    appendix = read(PARENT / "appendix.json")
    require(
        type(appendix) is list
        and len(appendix) == 109
        and all(type(p) is list and len(p) == 4 and all(type(x) is int for x in p) for p in appendix),
        "malformed parent appendix",
    )
    orbit = set()
    for row in appendix:
        p = tuple(row)
        for _ in range(3):
            orbit.add(p)
            a, b, c, d = p
            orbit.add((-a, -b, c, d))
            p = rotate(p)
    first = [(0, 0, 12, 0), (-6, 0, -6, 0), (6, 0, -6, 0)]
    require(set(first) <= orbit and len(orbit) == 627, "wrong parent orbit")
    reference = first + sorted(orbit - set(first))
    parent = read(PARENT / "certificate.json")
    keep = parent.get("retained_reference_indices")
    require(
        type(keep) is list
        and keep == sorted(set(keep))
        and len(keep) == 375
        and keep[:3] == [0, 1, 2],
        "malformed parent retained set",
    )
    points = [reference[i] for i in keep]

    def is_unit(p, q) -> bool:
        a, b, c, d = (x - y for x, y in zip(p, q))
        return 3 * a * a + 11 * b * b + c * c + 33 * d * d == 1296 and a * b + c * d == 0

    edges = [[u, v] for u, v in combinations(range(375), 2) if is_unit(points[u], points[v])]
    require(len(set(points)) == 375 and len(edges) == 1661, "wrong reconstructed graph")
    require(value_sha256(points) == parent["point_sha256"], "parent point hash mismatch")
    require(value_sha256(edges) == parent["edge_sha256"], "parent edge hash mismatch")
    word = parent.get("unpinned_colouring")
    require(type(word) is str and len(word) == 375 and set(word) <= set("0123"), "bad parent colouring")
    require(all(word[u] != word[v] for u, v in edges), "parent colouring is improper")
    return points, edges, parent


def exhaustive_forcing_check(n: int, edges: list[list[int]]):
    """Return complete search statistics for terminals fixed to one colour."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    adj = [sorted(row) for row in adj]
    nodes = conflicts = 0

    def dfs(masks: list[int], queue: list[int]) -> bool:
        nonlocal nodes, conflicts
        nodes += 1
        while queue:
            v = queue.pop()
            bit = masks[v]
            require(bit != 0 and bit & (bit - 1) == 0, "bad propagation queue")
            for u in adj[v]:
                if masks[u] & bit:
                    nxt = masks[u] & ~bit
                    if not nxt:
                        conflicts += 1
                        return False
                    masks[u] = nxt
                    if nxt & (nxt - 1) == 0:
                        queue.append(u)
        best = -1
        best_size = 5
        used = 0
        for v, mask in enumerate(masks):
            if mask & (mask - 1) == 0:
                used |= mask
                continue
            size = mask.bit_count()
            if size < best_size or (size == best_size and (best < 0 or len(adj[v]) > len(adj[best]))):
                best, best_size = v, size
        if best < 0:
            return True
        candidates = masks[best] & used
        unused = masks[best] & ~used
        if unused:
            candidates |= unused & -unused
        while candidates:
            bit = candidates & -candidates
            candidates -= bit
            child = masks.copy()
            child[best] = bit
            if dfs(child, [best]):
                return True
        return False

    masks = [15] * n
    for terminal in (0, 1, 2):
        masks[terminal] = 1
    satisfiable = dfs(masks, [0, 1, 2])
    return satisfiable, {"nodes": nodes, "conflicts": conflicts}


def unpack(encoded: str, n: int) -> list[int]:
    require(type(encoded) is str, "non-string packed word")
    try:
        data = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("invalid base64 word") from exc
    require(len(data) == (n + 3) // 4, "wrong packed word length")
    require(n % 4 == 0 or data[-1] >> (2 * (n % 4)) == 0, "nonzero packing padding")
    return [(data[i // 4] >> (2 * (i % 4))) & 3 for i in range(n)]


def validate_certificate(cert, edges):
    require(cert.get("schema") == "t375-terminal-monochromatic-deletion-colourings-v1", "wrong schema")
    require(cert.get("vertices") == 375 and cert.get("edges") == 1661, "wrong dimensions")
    require(cert.get("terminals") == [0, 1, 2], "wrong terminals")
    rows = cert.get("colourings")
    require(type(rows) is list and len(rows) == 372, "wrong witness count")
    require(
        all(type(row) is list and len(row) == 2 and type(row[0]) is int for row in rows),
        "malformed witness row",
    )
    require([row[0] for row in rows] == list(range(3, 375)), "deletions not complete and canonical")
    raw = bytearray()
    edge_tuples = [tuple(edge) for edge in edges]
    for deleted, encoded in rows:
        word = unpack(encoded, 375)
        raw.extend(base64.b64decode(encoded, validate=True))
        require(word[deleted] == 0, "deleted slot is not canonical")
        require(word[0] == word[1] == word[2] == 0, "terminals not monochromatic")
        require(
            all(deleted in (u, v) or word[u] != word[v] for u, v in edge_tuples),
            f"improper deletion colouring for {deleted}",
        )
    digest = hashlib.sha256(raw).hexdigest()
    require(cert.get("packed_words_sha256") == digest, "packed word hash mismatch")
    return digest


def malformed_controls(cert, edges) -> int:
    bad = []
    x = copy.deepcopy(cert)
    x["colourings"] = x["colourings"][:-1]
    bad.append(x)
    x = copy.deepcopy(cert)
    x["colourings"][1][0] = x["colourings"][0][0]
    bad.append(x)
    x = copy.deepcopy(cert)
    x["colourings"][0][1] = "!"
    bad.append(x)
    x = copy.deepcopy(cert)
    data = bytearray(base64.b64decode(x["colourings"][0][1]))
    data[-1] |= 0b11000000
    x["colourings"][0][1] = base64.b64encode(data).decode()
    bad.append(x)
    x = copy.deepcopy(cert)
    x["packed_words_sha256"] = "0" * 64
    bad.append(x)
    x = copy.deepcopy(cert)
    x["terminals"] = [0, 1, 3]
    bad.append(x)
    for candidate in bad:
        try:
            validate_certificate(candidate, edges)
        except ValueError:
            continue
        raise RuntimeError("malformed certificate accepted")
    return len(bad)


def main() -> None:
    points, edges, parent = reconstruct_graph()
    satisfiable, forcing = exhaustive_forcing_check(375, edges)
    require(not satisfiable, "parent forcing relation failed")
    cert = read(HERE / "certificate.json")
    word_hash = validate_certificate(cert, edges)
    controls = malformed_controls(cert, edges)
    provenance = read(HERE / "provenance.json")
    require(provenance["parent_appendix_sha256"] == file_sha256(PARENT / "appendix.json"), "appendix provenance mismatch")
    require(provenance["parent_certificate_sha256"] == file_sha256(PARENT / "certificate.json"), "certificate provenance mismatch")
    result = {
        "verified": True,
        "vertices": len(points),
        "edges": len(edges),
        "terminals": [0, 1, 2],
        "parent_forcing_search": forcing,
        "proper_unpinned_four_colouring": True,
        "deletion_witnesses": 372,
        "packed_words_sha256": word_hash,
        "all_proper_terminal_containing_subgraphs_allow_monochromatic_terminals": True,
        "vertex_minimal_for_marked_relation": True,
        "point_sha256": parent["point_sha256"],
        "edge_sha256": parent["edge_sha256"],
        "malformed_controls_rejected": controls,
        "target_found": False,
    }
    require(result == read(HERE / "expected.json"), "expected output mismatch")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
