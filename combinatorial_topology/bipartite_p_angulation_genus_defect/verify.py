#!/usr/bin/env python3
"""Definition-level audit of the bipartite clean-angulation parity gap."""

import hashlib
import itertools as it
import json
from collections import Counter


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_directed_cycle(cycle):
    """Rotate a directed cycle to its lexicographically least presentation."""
    cycle = tuple(cycle)
    return min(cycle[i:] + cycle[:i] for i in range(len(cycle)))


def canonical_unoriented_cycle(cycle):
    """Canonicalize a cycle up to rotation and direction."""
    cycle = tuple(cycle)
    return min(canonical_directed_cycle(cycle),
               canonical_directed_cycle(cycle[::-1]))


def cube_adjacency():
    return tuple(tuple(v ^ (1 << bit) for bit in range(3)) for v in range(8))


def cube_reference_faces():
    faces = []
    for free_a in range(3):
        for free_b in range(free_a + 1, 3):
            fixed = ({0, 1, 2} - {free_a, free_b}).pop()
            for value in (0, 1):
                start = value << fixed
                face = (start,
                        start ^ (1 << free_a),
                        start ^ (1 << free_a) ^ (1 << free_b),
                        start ^ (1 << free_b))
                faces.append(canonical_unoriented_cycle(face))
    require(len(set(faces)) == 6, "cube reference-face construction failed")
    return frozenset(faces)


def cyclic_rows(adjacency):
    """All cyclic neighbour orders, fixing the least neighbour first."""
    choices = []
    for neighbours in adjacency:
        first = min(neighbours)
        rest = tuple(v for v in neighbours if v != first)
        choices.append(tuple((first,) + order for order in it.permutations(rest)))
    yield from it.product(*choices)


def trace_faces(rows):
    successor = []
    for row in rows:
        successor.append({u: row[(i + 1) % len(row)] for i, u in enumerate(row)})
    unseen = {(v, u) for v, row in enumerate(rows) for u in row}
    faces = []
    while unseen:
        first = min(unseen)
        dart = first
        face = []
        while True:
            require(dart in unseen, "face permutation repeated a dart")
            unseen.remove(dart)
            u, v = dart
            face.append(u)
            dart = (v, successor[v][u])
            if dart == first:
                break
        faces.append(tuple(face))
    return tuple(faces)


def orientable_genus(vertex_count, edge_count, face_count):
    twice_genus = 2 - vertex_count + edge_count - face_count
    require(twice_genus >= 0 and twice_genus % 2 == 0,
            "Euler characteristic is not orientable")
    return twice_genus // 2


def audit_defect(p, r, t, other_lengths, reference_face_count):
    """Check the claimed identities from an independently traced face list."""
    other_lengths = tuple(other_lengths)
    require(p >= 4 and p % 2 == 0, "p must be even and at least four")
    require(all(length % 2 == 0 for length in other_lengths),
            "bipartite face has odd length")
    require(all(length >= p + 2 for length in other_lengths),
            "non-reference face is too short")
    require(len(other_lengths) == t - 2 * r, "face-count identity failed")
    require(sum(other_lengths) == p * t, "dart-count identity failed")
    require(sum((length - (p + 2)) // 2 for length in other_lengths)
            == (p + 2) * r - t, "parity-gap identity failed")
    if r == 0:
        require(t == 0, "minimum-genus system loses a reference face")
    else:
        require(2 * r + 1 <= t <= min((p + 2) * r, reference_face_count),
                "bipartite defect bound failed")
        endpoint = t == (p + 2) * r
        require(endpoint == all(length == p + 2 for length in other_lengths),
                "endpoint characterization failed")


def cube_audit():
    adjacency = cube_adjacency()
    reference = cube_reference_faces()
    edge_count = sum(map(len, adjacency)) // 2
    require(edge_count == 12, "wrong cube edge count")
    counts = Counter()
    stream = hashlib.sha256()
    total = 0
    for rows in cyclic_rows(adjacency):
        total += 1
        faces = trace_faces(rows)
        require(sum(map(len, faces)) == 2 * edge_count, "dart partition failed")
        require(all(len(face) % 2 == 0 for face in faces),
                "odd face in a bipartite graph")
        short = {canonical_unoriented_cycle(face)
                 for face in faces if len(face) == 4}
        require(short <= reference, "non-reference square face")
        t = len(reference - short)
        r = orientable_genus(8, edge_count, len(faces))
        other = tuple(sorted(len(face) for face in faces if len(face) != 4))
        audit_defect(4, r, t, other, len(reference))
        key = (r, t, other)
        counts[key] += 1
        stream.update((json.dumps([rows, faces, key], separators=(",", ":"))
                       + "\n").encode())
    require(total == 256, "cube rotation-system count failed")
    require(sum(counts.values()) == total, "profile count failed")
    return {
        "fixture": "labelled cube",
        "vertices": 8,
        "edges": edge_count,
        "reference_faces": len(reference),
        "rotation_systems": total,
        "profiles": [
            {
                "genus_excess": r,
                "missing_faces": t,
                "nonreference_face_lengths": list(lengths),
                "count": count,
            }
            for (r, t, lengths), count in sorted(counts.items())
        ],
        "rotation_face_stream_sha256": stream.hexdigest(),
    }


def main():
    report = {
        "claim": "bipartite clean-p-angulation parity gap",
        "identity": "(p+2)r-t = 1/2 sum_i(ell_i-(p+2))",
        "cube": cube_audit(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
