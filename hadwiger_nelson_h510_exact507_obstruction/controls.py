#!/usr/bin/env python3
"""Small exhaustive controls for quotient K2,3 detection and fibre accounting."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_verifier():
    spec = importlib.util.spec_from_file_location("exact507", HERE / "verify.py")
    if not spec or not spec.loader:
        raise ValueError("verifier import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def brute_k23(qadj):
    for a, b in combinations(range(len(qadj)), 2):
        if len(qadj[a] & qadj[b]) >= 3:
            return True
    return False


def quotient_small(adjacency, pair):
    n = len(adjacency)
    u, v = pair
    owner = list(range(n))
    owner[v] = u
    labels = sorted(set(owner))
    index = {label: i for i, label in enumerate(labels)}
    qadj = [set() for _ in labels]
    for a in range(n):
        for b in adjacency[a]:
            x, y = index[owner[a]], index[owner[b]]
            if x == y:
                return None, None
            qadj[x].add(y)
    return qadj, [index[u]]


def main():
    verifier = load_verifier()
    cases = 0
    positive = 0
    stream = sha256()
    vertices = 6
    pairs = list(combinations(range(vertices), 2))
    for word in range(1 << len(pairs)):
        adjacency = [set() for _ in range(vertices)]
        for bit, (u, v) in enumerate(pairs):
            if word & (1 << bit):
                adjacency[u].add(v)
                adjacency[v].add(u)
        if brute_k23(adjacency):
            continue
        for pair in pairs:
            if pair[1] in adjacency[pair[0]]:
                continue
            qadj, merged = quotient_small(adjacency, pair)
            verifier.require(qadj is not None, "control edge collapse")
            expected = brute_k23(qadj)
            observed = verifier.first_k23(qadj, merged) is not None
            verifier.require(observed == expected, "local/brute K2,3 disagreement")
            cases += 1
            positive += observed
            stream.update(f"{word}:{pair}:{int(observed)}\n".encode())

    shapes = [((0, 1, 2, 3),), ((0, 1, 2), (3, 4)), ((0, 1), (2, 3), (4, 5))]
    normalized = [verifier.canonical_groups(groups) for groups in shapes]
    verifier.require(
        [sorted(map(len, groups)) for groups in normalized] == [[4], [2, 3], [2, 2, 2]],
        "fibre shape normalization",
    )

    malformed = 0
    for groups in [((0, 1),), ((0, 1, 2),), ((0, 1), (1, 2), (3, 4))]:
        try:
            verifier.canonical_groups(groups)
        except ValueError:
            malformed += 1
    verifier.require(malformed == 3, "malformed fibre controls")

    result = {
        "status": "CONTROLS_OK",
        "exhaustive_six_vertex_quotients": cases,
        "quotients_with_new_k23": positive,
        "control_stream_sha256": stream.hexdigest(),
        "fibre_shapes": [[len(group) for group in groups] for groups in normalized],
        "malformed_fibres_rejected": malformed,
    }
    expected = json.loads((HERE / "controls_expected.json").read_text()) if (HERE / "controls_expected.json").exists() else None
    if expected is not None:
        verifier.require(result == expected, "control expected output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
