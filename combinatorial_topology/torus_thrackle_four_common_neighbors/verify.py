"""Check a supplied rotation certificate without importing its constructor.

Exact finite checks, not a search. The disc-and-band realization theorem and
classification of closed orientable surfaces are explained in PROOF.md.
"""
import argparse
from collections import Counter
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_cycle(cycle):
    cycle = tuple(cycle)
    return min(cycle[i:] + cycle[:i] for i in range(len(cycle)))


def shift(vertex):
    if vertex in ("u", "v"):
        return vertex
    return vertex[0] + "".join(str((int(x) + 1) % 4) for x in vertex[1:])


def rank_mod(rows, prime):
    """Ordinary Gaussian elimination over the specified prime field."""
    matrix = [[x % prime for x in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    for col in range(len(matrix[0])):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(x * inv) % prime for x in matrix[rank]]
        for i in range(rank + 1, len(matrix)):
            factor = matrix[i][col]
            matrix[i] = [(a - factor*b) % prime
                         for a, b in zip(matrix[i], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def verify(data):
    require(data["schema"] == "oriented-ribbon-thrackle-v1", "schema")
    paths, rotations = data["paths"], data["rotations"]
    labels = {f"{s}{i}" for s in ("e", "f") for i in range(4)}
    crossings = {f"x{i}{j}" for i in range(4) for j in range(4) if i != j}
    originals = {"u", "v"} | {f"w{i}" for i in range(4)}
    require(set(paths) == labels, "eight original edges")
    neighbors, segments, owners = {}, {}, {}
    for edge, path in sorted(paths.items()):
        i = int(edge[1])
        require(path[0] == ("u" if edge[0] == "e" else "v")
                and path[-1] == f"w{i}", "original endpoints")
        require(len(path) == 5 and len(set(path)) == 5, "simple edge path")
        wanted = ({f"x{i}{j}" for j in range(4) if j != i} if edge[0] == "e"
                  else {f"x{j}{i}" for j in range(4) if j != i})
        require(set(path[1:-1]) == wanted, "exact crossing incidence")
        for a, b in zip(path, path[1:]):
            key = tuple(sorted((a, b)))
            require(key not in segments, "duplicate segment")
            segments[key] = len(segments)
            owners[key] = edge
            neighbors.setdefault(a, set()).add(b)
            neighbors.setdefault(b, set()).add(a)
    require(set(neighbors) == originals | crossings, "planarization vertices")
    require(set(rotations) == set(neighbors), "rotation domain")
    for v, rotation in rotations.items():
        require(len(rotation) == len(set(rotation))
                and set(rotation) == neighbors[v], "rotation incidence")
        if v in crossings:
            names = [owners[tuple(sorted((v, x)))] for x in rotation]
            require(len(names) == 4 and names[0] == names[2]
                    and names[1] == names[3] and names[0] != names[1],
                    "crossing must alternate")
    pair_counts = Counter()
    for e, f in combinations(sorted(paths), 2):
        shared = set(paths[e]) & set(paths[f])
        endpoints = {paths[e][0], paths[e][-1]} & {paths[f][0], paths[f][-1]}
        require(len(shared) == 1, "each original edge pair meets once")
        require(shared == endpoints if endpoints else shared <= crossings,
                "endpoint versus interior crossing")
        pair_counts["adjacent" if endpoints else "independent"] += 1
    reached, todo = set(), ["u"]
    while todo:
        v = todo.pop()
        if v not in reached:
            reached.add(v)
            todo.extend(neighbors[v] - reached)
    require(reached == set(neighbors), "connected")
    for v, rotation in rotations.items():
        require(canonical_cycle(tuple(map(shift, rotation)))
                == canonical_cycle(rotations[shift(v)]), "cyclic symmetry")

    # Follow each directed segment by the next outgoing segment in the
    # terminal vertex's cyclic order: face permutation sigma o alpha.
    darts = {(a, b) for a in neighbors for b in neighbors[a]}
    unused, faces = set(darts), []
    while unused:
        start = min(unused)
        dart, face = start, []
        while dart in unused:
            unused.remove(dart)
            a, b = dart
            face.append(a)
            rotation = rotations[b]
            dart = (b, rotation[(rotation.index(a) + 1) % len(rotation)])
        require(dart == start, "closed face orbit")
        faces.append(face)
    expected_faces = set()
    for orbit in data["face_orbits"]:
        f, generated = orbit["representative"], set()
        for _ in range(4):
            generated.add(canonical_cycle(f))
            f = list(map(shift, f))
        require(len(generated) == orbit["size"], "face orbit size")
        require(not expected_faces & generated, "disjoint face orbits")
        expected_faces.update(generated)
    require({canonical_cycle(f) for f in faces} == expected_faces, "face inventory")
    V, E, F = len(neighbors), len(segments), len(faces)
    require((V, E, F) == (18, 32, 14), "torus Euler certificate")
    require(sum(map(len, faces)) == 2*E, "all ribbon sides")

    # An independent cell-chain check, including coefficients of odd
    # characteristic, tests the oriented face gluing and the homology.
    vertices = {v: i for i, v in enumerate(sorted(neighbors))}
    d1 = []
    for a, b in segments:
        vector = [0] * V
        vector[vertices[a]], vector[vertices[b]] = -1, 1
        d1.append(vector)
    d2 = []
    for face in faces:
        vector = [0] * E
        for a, b in zip(face, face[1:] + face[:1]):
            key = tuple(sorted((a, b)))
            vector[segments[key]] += 1 if (a, b) == key else -1
        require(all(sum(vector[e]*d1[e][v] for e in range(E)) == 0
                    for v in range(V)), "boundary squared zero over integers")
        d2.append(vector)
    require(all(sum(row[e] for row in d2) == 0 for e in range(E)),
            "oriented faces cancel over integers")
    homology = {}
    for prime in (2, 3):
        r1, r2 = rank_mod(d1, prime), rank_mod(d2, prime)
        betti = [V-r1, E-r1-r2, F-r2]
        require(betti == [1, 2, 1], "surface homology")
        homology[str(prime)] = {"ranks": [r1, r2], "betti": betti}

    # P_i = e_i + f_i (mod 2). All four relative classes exhaust H_1.
    P = []
    for i in range(4):
        vector = [0]*E
        for edge in (f"e{i}", f"f{i}"):
            for a, b in zip(paths[edge], paths[edge][1:]):
                vector[segments[tuple(sorted((a, b)))]] ^= 1
        P.append(vector)
    h = [[a ^ b for a, b in zip(p, P[0])] for p in P]
    boundary_rank = rank_mod(d2, 2)
    for i, j in combinations(range(4), 2):
        cycle = [a ^ b for a, b in zip(h[i], h[j])]
        require(rank_mod(d2 + [cycle], 2) == boundary_rank + 1,
                "four distinct relative homology classes")
    total = [sum(h[i][e] for i in range(4)) % 2 for e in range(E)]
    require(rank_mod(d2 + [total], 2) == boundary_rank, "sum of four classes")
    require(rank_mod(d2 + h, 2) == boundary_rank + 2, "classes span H1")
    return {
        "original_vertices": 6, "original_edges": 8, "crossings": 12,
        "edge_pairs": dict(sorted(pair_counts.items())),
        "planarization": {"V": V, "E": E, "F": F, "chi": V-E+F, "genus": 1},
        "face_lengths": dict(sorted(Counter(map(len, faces)).items())),
        "face_orbit_sizes": [o["size"] for o in data["face_orbits"]],
        "homology": homology, "distinct_relative_classes": 4,
    }


def self_test(data):
    cases = []
    bad = deepcopy(data)
    bad["paths"]["e0"][2] = bad["paths"]["e0"][1]
    cases.append(("repeated path vertex", bad))
    bad = deepcopy(data)
    bad["rotations"]["x01"][1], bad["rotations"]["x01"][2] = (
        bad["rotations"]["x01"][2], bad["rotations"]["x01"][1])
    cases.append(("nonalternating crossing", bad))
    bad = deepcopy(data)
    bad["rotations"]["u"][0] = bad["rotations"]["u"][1]
    cases.append(("missing ribbon dart", bad))
    bad = deepcopy(data)
    bad["face_orbits"].pop()
    cases.append(("omitted face orbit", bad))
    rejected = []
    for label, bad in cases:
        try:
            verify(bad)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError("accepted damaged certificate: " + label)
    return rejected


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path,
                        default=Path(__file__).with_name("certificate.json"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    result = verify(certificate)
    if args.self_test:
        result["rejected_mutations"] = self_test(certificate)
    print(json.dumps(result, sort_keys=True, indent=2))
