"""Exact author audit of the quadratic-moment reduction; Python stdlib only."""

from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import random

import model

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y)) % 5


def bilinear(matrix, x, y):
    return sum(x[i]*matrix[i][j]*y[j]
               for i in range(len(x)) for j in range(len(y))) % 5


def rank(matrix):
    a = [list(row) for row in matrix]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j] % 5), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        a[r] = [v*pow(a[r][j] % 5, -1, 5) % 5 for v in a[r]]
        for i in range(len(a)):
            if i != r:
                c = a[i][j]
                a[i] = [(x-c*y) % 5 for x, y in zip(a[i], a[r])]
        r += 1
    return r


def diagonalize(matrix):
    """Orthogonal splitting; no normal-form or character-count lookup."""
    n = len(matrix)
    units = [tuple(int(i == j) for j in range(n)) for i in range(n)]
    choices = units + [tuple((a+b) % 5 for a, b in zip(u, v))
                       for u, v in combinations(units, 2)]
    v = next((v for v in choices if bilinear(matrix, v, v)), None)
    if v is None:
        require(all(x % 5 == 0 for row in matrix for x in row),
                "polarization failure")
        return [0]*n
    q = bilinear(matrix, v, v)
    pivot = next(i for i, x in enumerate(v) if x)
    rest = []
    for j, unit in enumerate(units):
        if j != pivot:
            c = bilinear(matrix, v, unit)*pow(q, -1, 5) % 5
            rest.append(tuple((x-c*y) % 5 for x, y in zip(unit, v)))
    require(rank([v]+rest) == n, "orthogonal basis not invertible")
    require(all(bilinear(matrix, v, w) == 0 for w in rest),
            "orthogonal splitting failure")
    if not rest:
        return [q]
    reduced = [[bilinear(matrix, u, w) for w in rest] for u in rest]
    return [q]+diagonalize(reduced)


def form_name(diagonal):
    nonzero = [x for x in diagonal if x % 5]
    sign = 1
    for x in nonzero:
        sign *= model.character(x)
    return {
        (0, 1): "rank0",
        (1, 1): "rank1_square",
        (1, -1): "rank1_nonsquare",
        (2, 1): "rank2_split",
        (2, -1): "rank2_anisotropic",
        (3, 1): "rank3_square_det",
        (3, -1): "rank3_nonsquare_det",
    }[(len(nonzero), sign)]


def audit_forms():
    normals = model.projective_points()
    require(len(normals) == 31 and len(set(normals)) == 31, "projective points")
    counts = Counter()
    for a, b, c, d, e, f in product(range(5), repeat=6):
        matrix = [[a, b, c], [b, d, e], [c, e, f]]
        diagonal = diagonalize(matrix)
        require(sum(x != 0 for x in diagonal) == rank(matrix), "rank mismatch")
        name = form_name(diagonal)
        actual = Counter(model.character(bilinear(matrix, v, v)) for v in normals)
        require(tuple(actual[t] for t in (0, 1, -1)) == model.FORM_COUNTS[name],
                "quadratic character count mismatch")
        counts[name] += 1
    split_locus = {v for v in normals if model.character(v[0]**2+v[1]**2) == 1}
    expected = {(1, 0, t) for t in range(5)} | {(0, 1, t) for t in range(5)}
    require(split_locus == expected, "split square locus")
    for coordinate in (0, 1):
        require(sum(v[coordinate] == 0 for v in normals) == 6, "line size")
        require(sum(v[coordinate] == 0 for v in split_locus) == 5, "locus cover")
    require(sum(counts.values()) == 15625, "symmetric matrix coverage")
    return dict(sorted(counts.items()))


def audit_low_profiles():
    cases = 0
    for a in range(5):
        for b in range(5):
            if a == b:
                continue
            p = [9 if t == a else 15 if t == b else 16 for t in range(5)]
            center = 3*sum(t*n for t, n in enumerate(p)) % 5
            offset = (a-center) % 5
            require(offset != 0 and (b-center-3*offset) % 5 == 0,
                    "nine-plane companion offset")
            moments = [sum((t-center)**k*n for t, n in enumerate(p)) % 5
                       for k in range(1, 5)]
            require(moments == [0, -offset**2 % 5, offset**3 % 5, 1],
                    "nine-plane moments")
            require(pow(moments[2], 3, 5) == offset, "cubic determines offset")
            cases += 1
    return cases


def audit_affine_moments():
    # Arbitrary 72-subsets are controls for the general moment identities;
    # they are not claimed to be line-free witnesses.
    rng = random.Random(20260926)
    points = list(product(range(5), repeat=3))
    normals = model.projective_points()
    for _ in range(32):
        selected = rng.sample(points, 72)
        center = tuple(3*sum(x[i] for x in selected) % 5 for i in range(3))
        centered = [tuple((x[i]-center[i]) % 5 for i in range(3)) for x in selected]
        require(all(sum(x[i] for x in centered) % 5 == 0 for i in range(3)),
                "centered point sum")
        m = [[sum(x[i]*x[j] for x in centered) % 5 for j in range(3)]
             for i in range(3)]
        for v in normals:
            p = Counter(dot(x, v) for x in centered)
            require(sum(t*t*n for t, n in p.items()) % 5 == bilinear(m, v, v),
                    "profile/matrix identity")
        while True:
            a = [[rng.randrange(5) for _ in range(3)] for _ in range(3)]
            if rank(a) == 3:
                break
        shift = tuple(rng.randrange(5) for _ in range(3))
        transformed = [tuple((dot(row, x)+shift[i]) % 5 for i, row in enumerate(a))
                       for x in selected]
        new_center = tuple(3*sum(x[i] for x in transformed) % 5 for i in range(3))
        require(new_center == tuple((dot(row, center)+shift[i]) % 5
                                    for i, row in enumerate(a)), "affine barycenter")
        centered = [tuple((x[i]-new_center[i]) % 5 for i in range(3)) for x in transformed]
        new_m = [[sum(x[i]*x[j] for x in centered) % 5 for j in range(3)]
                 for i in range(3)]
        require(new_m == [[bilinear(m, u, v) for v in a] for u in a],
                "affine moment congruence")
    return 32


def audit_bbb():
    profile = (9, 15, 16, 16, 16)
    center = 3*sum(t*n for t, n in enumerate(profile)) % 5
    second = sum((t-center)**2*n for t, n in enumerate(profile)) % 5
    require((center, second) == (2, 1), "BBB normalization moments")
    counts = Counter()
    for a, b, c in product(range(5), repeat=3):
        m = [[1, a, b], [a, 1, c], [b, c, 1]]
        counts[form_name(diagonalize(m))] += 1
    require(sum(counts.values()) == 125, "BBB matrix coverage")
    return dict(sorted(counts.items()))


def audit_normal_configurations():
    normals = model.projective_points()
    projective_lines = [{v for v in normals if dot(v, p) == 0} for p in normals]
    require(len({frozenset(line) for line in projective_lines}) == 31,
            "projective line coverage")
    require(all(len(line) == 6 for line in projective_lines), "projective line size")
    result = {}
    for kind, diagonal in [("rank2_anisotropic", (1, 2, 0)),
                           ("rank3_square_det", (1, 1, 1))]:
        def q(v):
            return sum(a*x*x for a, x in zip(diagonal, v)) % 5
        locus = {v for v in normals if model.character(q(v)) == 1}
        require(len(locus) == 15, "square-locus size")
        branches = []
        edge = {}
        if kind == "rank2_anisotropic":
            radical = (0, 0, 1)
            branches = [line & locus for line in projective_lines
                        if radical in line and len(line & locus) == 5]
            require(len(branches) == 3 and set.union(*branches) == locus,
                    "rank-two three-line cover")
            require(all(len(a & b) == 0 for a, b in combinations(branches, 2)),
                    "rank-two branch disjointness")
        else:
            conic = [p for p in normals if q(p) == 0]
            require(len(conic) == 6, "conic size")
            tangents = [{v for v in normals if dot(v, p) == 0} for p in conic]
            require(all(line - locus == {p} and len(line & locus) == 5
                        for p, line in zip(conic, tangents)), "tangent sections")
            for v in locus:
                endpoints = tuple(i for i, line in enumerate(tangents) if v in line)
                require(len(endpoints) == 2, "two tangents per external point")
                edge[v] = endpoints
            require(set(edge.values()) == set(combinations(range(6), 2)),
                    "external points biject to K6 edges")
        histogram = Counter()
        graph_types = Counter()
        ordered = sorted(locus)
        # Every subset of size >=11 is tested. Only sizes <=12 survive.
        for size in range(11, 16):
            for values in combinations(ordered, size):
                selected = set(values)
                if any(len(selected & line) >= 5 for line in projective_lines):
                    continue
                histogram[size] += 1
                if branches:
                    occupancy = sorted(len(selected & branch) for branch in branches)
                    require(occupancy in ([3, 4, 4], [4, 4, 4]), "branch occupancies")
                else:
                    omitted_edges = [edge[v] for v in locus-selected]
                    adjacency = {i: set() for i in range(6)}
                    for u, v in omitted_edges:
                        adjacency[u].add(v)
                        adjacency[v].add(u)
                    require(all(adjacency.values()), "complement isolated vertex")
                    unseen = set(range(6))
                    components = []
                    while unseen:
                        stack = [unseen.pop()]
                        component = set(stack)
                        while stack:
                            for v in adjacency[stack.pop()] & unseen:
                                unseen.remove(v)
                                component.add(v)
                                stack.append(v)
                        components.append(len(component))
                    signature = (tuple(sorted(len(v) for v in adjacency.values())),
                                 tuple(sorted(components)))
                    labels = {
                        ((1, 1, 1, 1, 1, 1), (2, 2, 2)): "3K2",
                        ((1, 1, 1, 1, 1, 3), (2, 4)): "K1,3+K2",
                        ((1, 1, 1, 1, 2, 2), (2, 4)): "P4+K2",
                        ((1, 1, 1, 1, 2, 2), (3, 3)): "2P3",
                    }
                    require(signature in labels, "complement graph type")
                    graph_types[labels[signature]] += 1
        expected = {11: 750, 12: 125} if branches else {11: 330, 12: 15}
        require(dict(histogram) == expected, "normal-subset census")
        result[kind] = {"admissible_subset_counts": dict(sorted(histogram.items()))}
        if graph_types:
            require(dict(graph_types) == {"3K2": 15, "K1,3+K2": 60,
                                         "P4+K2": 180, "2P3": 90},
                    "graph census")
            result[kind]["complement_graph_counts"] = dict(sorted(graph_types.items()))
    return result


def main():
    dependencies = json.loads((HERE/"dependencies.json").read_text())
    for relative, expected in dependencies["sha256"].items():
        actual = hashlib.sha256((HERE/relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency hash: {relative}")
    result = {
        "status": "QUADRATIC_MOMENTS72_VERIFIED",
        "symmetric_matrices_audited": audit_forms(),
        "projective_normals": 31,
        "low_profile_moment_cases": audit_low_profiles(),
        "affine_moment_controls": audit_affine_moments(),
        "bbb_diagonal_one_matrices": audit_bbb(),
        "normal_configurations": audit_normal_configurations(),
        "remaining_forms": ["diag(1,0,0)", "diag(1,2,0)", "diag(1,1,1)"],
        "rank_one_a9_bounds": [11, 16],
        "higher_rank_a9_values": [11, 12],
        "optimizer_required": False,
        "prior_drat_proofs_replayed": False,
        "numeric_bounds": [70, 72],
        "72_point_decision": "OPEN",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
