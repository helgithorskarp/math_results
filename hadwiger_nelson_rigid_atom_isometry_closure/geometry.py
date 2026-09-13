"""Exact atoms, isometry enumeration, strict edges, and canonical hashes."""

from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
from itertools import combinations

import arithmetic as K


def divide(z, w):
    return K.mul(K.mul(z, K.conj(w)), K.inverse_real(K.norm(w)))


def moser():
    alpha = (F(0), F(0), F(1), F(0))
    beta = (F(0), F(0), F(0), F(1))
    omega = K.scale(K.add(K.ONE, alpha), F(1, 2))
    eta = K.scale(K.add(K.scale(K.ONE, 5), beta), F(1, 6))
    return [K.ZERO, K.ONE, omega, K.add(K.ONE, omega), eta,
            K.mul(eta, omega), K.mul(eta, K.add(K.ONE, omega))]


def golomb():
    rows = [(0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
            (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
            (18, 0, -18, 0), (6, 0, 0, 2), (-3, -3, 3, -1),
            (-3, 3, -3, -1)]
    return [(F(a, 36), F(b, 36), F(c, 36), F(d, 12))
            for a, b, c, d in rows]


def strict_edges(points):
    return [(a, b) for a, b in combinations(range(len(points)), 2)
            if K.norm(K.sub(points[a], points[b])) == K.ONE]


def copies_on_seed(atom, seed):
    """All copy point sets sharing at least two distinct seed points."""
    target_by_norm = defaultdict(list)
    for a in range(len(seed)):
        for b in range(len(seed)):
            if a != b:
                target_by_norm[K.norm(K.sub(seed[b], seed[a]))].append((a, b))
    seed_set = set(seed)
    copies = {}
    for reflected in (False, True):
        source = [K.conj(z) if reflected else z for z in atom]
        for i in range(len(source)):
            for j in range(len(source)):
                if i == j:
                    continue
                source_delta = K.sub(source[j], source[i])
                for a, b in target_by_norm[K.norm(source_delta)]:
                    rotation = divide(K.sub(seed[b], seed[a]), source_delta)
                    if K.norm(rotation) != K.ONE:
                        raise ValueError("nonunit isometry multiplier")
                    translation = K.sub(seed[a], K.mul(rotation, source[i]))
                    copy = frozenset(K.add(translation, K.mul(rotation, z)) for z in source)
                    if len(copy) != len(atom):
                        raise ValueError("isometry collapsed an atom")
                    if len(copy & seed_set) < 2:
                        raise ValueError("defining coincidences were lost")
                    copies.setdefault(copy, (reflected, i, j, a, b))
    return copies


def stream_hash(rows):
    return hashlib.sha256(("\n".join(rows) + "\n").encode()).hexdigest()


def closure_geometry(name):
    m, g = moser(), golomb()
    if name == "moser_self":
        seed, atoms = m, {"moser": m}
    elif name == "golomb_self":
        seed, atoms = g, {"golomb": g}
    elif name == "mixed_aligned":
        seed = m + [z for z in g if z not in set(m)]
        atoms = {"moser": m, "golomb": g}
    else:
        raise ValueError("unknown closure")
    inventories = {atom_name: copies_on_seed(atom, seed)
                   for atom_name, atom in atoms.items()}
    point_set = set(seed)
    for copies in inventories.values():
        for copy in copies:
            point_set.update(copy)
    points = list(seed) + sorted(point_set - set(seed))
    if len(points) != len(set(points)):
        raise ValueError("duplicate canonical points")
    edges = strict_edges(points)
    seed_set = set(seed)
    sharing = {atom_name: {str(k): v for k, v in sorted(
        Counter(len(copy & seed_set) for copy in copies).items())}
        for atom_name, copies in inventories.items()}
    point_rows = ["|".join(map(str, point)) for point in points]
    edge_rows = [f"{a} {b}" for a, b in edges]
    return {
        "name": name,
        "seed_vertices": len(seed),
        "copy_point_sets": {atom_name: len(copies)
                            for atom_name, copies in inventories.items()},
        "sharing_distribution": sharing,
        "vertices": len(points),
        "edges": len(edges),
        "point_stream_sha256": stream_hash(point_rows),
        "edge_stream_sha256": stream_hash(edge_rows),
    }, points, edges
