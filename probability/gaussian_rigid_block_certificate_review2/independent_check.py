#!/usr/bin/env python3
"""Independent exact checks for the rigid-block contraction certificate.

This program does not import the target checker.  Its interval argument is
the elementary norm enclosure from the manuscript, not the target's
pairwise Bernstein-polynomial calculation.  Fractions are exact throughout.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_rigid_block_certificate"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def norm2(a):
    return dot(a, a)


def transpose(a):
    return list(map(list, zip(*a)))


def matmul(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def matsub(a, b):
    return [[x - y for x, y in zip(arow, brow)]
            for arow, brow in zip(a, b)]


def frobenius2(a):
    return sum((x * x for row in a for x in row), F(0))


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def rank(rows):
    a = [list(row) for row in rows]
    if not a:
        return 0
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        p = a[row][col]
        a[row] = [x / p for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                q = a[i][col]
                a[i] = [x - q * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def determinant(matrix):
    a = [list(row) for row in matrix]
    answer = F(1)
    for col in range(len(a)):
        pivot = next((i for i in range(col, len(a)) if a[i][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            answer = -answer
        value = a[col][col]
        answer *= value
        for i in range(col + 1, len(a)):
            multiplier = a[i][col] / value
            a[i] = [x - multiplier * y for x, y in zip(a[i], a[col])]
    return answer


V = [tuple(map(F, row)) for row in
     ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]
CENTERS = [tuple(map(F, row)) for row in
           ((-16, 0, 0), (16, 0, 0), (0, 16, 0))]


def rotate(v, t, axis):
    if axis is None:
        return v
    cosine = (1 - t * t) / (1 + t * t)
    sine = 2 * t / (1 + t * t)
    out = list(v)
    i, j = (0, 1) if axis == "z" else (1, 2)
    out[i] = cosine * v[i] - sine * v[j]
    out[j] = sine * v[i] + cosine * v[j]
    return tuple(out)


def family(t):
    source, target, owners = [], [], []
    for owner, (center, axis) in enumerate(zip(CENTERS, (None, "z", "x"))):
        for v in V:
            source.append(add(center, v))
            target.append(add(scale(1 - t, center), rotate(v, t, axis)))
            owners.append(owner)
    return source, target, owners


def scatter(rows):
    mean = tuple(sum((row[j] for row in rows), F(0)) / len(rows)
                 for j in range(3))
    centered = [sub(row, mean) for row in rows]
    return [[sum((row[i] * row[j] for row in centered), F(0))
             for j in range(3)] for i in range(3)]


def direct_fixture():
    t = F(1, 16384)
    source, target, owners = family(t)
    pairs = list(combinations(range(12), 2))
    source_d2 = {(i, j): norm2(sub(source[i], source[j])) for i, j in pairs}
    losses = {(i, j): source_d2[i, j] - norm2(sub(target[i], target[j]))
              for i, j in pairs}
    within = [loss for pair, loss in losses.items()
              if owners[pair[0]] == owners[pair[1]]]
    cross = [loss for pair, loss in losses.items()
             if owners[pair[0]] != owners[pair[1]]]
    require(len(within) == 18 and all(loss == 0 for loss in within),
            "within-block distances")
    require(len(cross) == 48 and min(cross) > 0, "cross contractions")
    require(all(scatter(source[4 * b:4 * b + 4]) ==
                [[F(4) if i == j else F(0) for j in range(3)] for i in range(3)]
                for b in range(3)), "block scatter")

    diameter2 = max(source_d2.values())
    error = sum((norm2(sub(y, x)) for x, y in zip(source, target)), F(0))
    expected_error = 3072 * t * t + 64 * t * t / (1 + t * t)
    require(diameter2 == 1160 and error == expected_error, "family invariants")
    factor = 8 + 2 * diameter2 / 4
    require(factor == 588 and error <= 4 and min(cross) >= factor * error,
            "displayed-frame guard")

    paired = [source[i] + target[i] for i in range(12)]
    paired_rank = rank([sub(row, paired[0]) for row in paired[1:]])
    require(paired_rank == 6, "paired affine rank")

    a = sub(source[4], source[5])
    b = sub(target[4], target[5])
    endpoint_derivative = 2 * dot(b, sub(b, a))
    require(norm2(a) == norm2(b) and endpoint_derivative == norm2(sub(b, a)) > 0,
            "straight interpolation re-expands a preserved edge")
    return {
        "parameter": t,
        "diameter_squared": diameter2,
        "energy": error,
        "minimum_cross_loss": min(cross),
        "cross_margin": min(cross) - factor * error,
        "tight_pairs": len(within),
        "strict_pairs": len(cross),
        "paired_affine_rank": paired_rank,
        "straight_endpoint_derivative": endpoint_derivative,
    }


def interval_enclosure():
    # The center differences have 512 <= |D|^2 <= 1024, hence |D| <= 32.
    center_d2 = [norm2(sub(a, b)) for a, b in combinations(CENTERS, 2)]
    offset_d2 = [norm2(sub(a, b)) for a in V for b in V]
    require(min(center_d2) == 512 and max(center_d2) == 1024,
            "center-distance enclosure")
    require(max(offset_d2) == 8 < 16, "offset enclosure")

    # Each moving tetrahedron vertex has perpendicular norm squared two, so
    # |R(t)v-v|^2=8t^2/(1+t^2)<9t^2.  Two rotations therefore perturb an
    # offset difference by less than 6t.  Substitution in the exact distance
    # expansion gives the following uniform coefficient at t <= 1/4.
    cross_coefficient = F(7, 4) * 512 - 20 * 32 - 48 - 36 * F(1, 4)
    require(cross_coefficient == 199 > 192, "uniform cross-loss coefficient")

    ratio = F(588 * 3136, 192)
    require(ratio == 9604 < 16384, "uniform cross-budget interval")
    require(F(3136, 16384 * 16384) < 4, "uniform displacement interval")

    # Independently check the universal scalar slack in the motion proof.
    # 8+2q^2-[185/32+(5/2)q] = 2(q-5/8)^2+23/16.
    left = (F(71, 32), F(-5, 2), F(2))
    right = (2 * F(25, 64) + F(23, 16), -4 * F(5, 8), F(2))
    require(left == right, "square completion")
    return {
        "cross_loss_lower_coefficient": cross_coefficient,
        "guard_ratio": ratio,
        "motion_interval_denominator": 16384,
        "square_completion_remainder": F(23, 16),
        "method": "exact norm enclosure; no Bernstein coefficients",
    }


def procrustes_identity_fixture():
    # Stretch the centered tetrahedron anisotropically, then choose C=A M so
    # that A^T C is a prescribed non-diagonal positive definite matrix.  Thus
    # Q=I is a valid polar alignment, while A^T A and C^T C do not commute.
    diagonal = [[F(1), F(0), F(0)],
                [F(0), F(2), F(0)],
                [F(0), F(0), F(3)]]
    a = matmul([list(row) for row in V], diagonal)
    positive = [[F(4), F(1), F(0)],
                [F(1), F(4), F(1)],
                [F(0), F(1), F(4)]]
    inverse_scatter = [[F(1, 4), F(0), F(0)],
                       [F(0), F(1, 16), F(0)],
                       [F(0), F(0), F(1, 36)]]
    m = matmul(inverse_scatter, positive)
    c = matmul(a, m)
    ata = matmul(transpose(a), a)
    atc = matmul(transpose(a), c)
    require(ata == [[F(4), F(0), F(0)], [F(0), F(16), F(0)],
                    [F(0), F(0), F(36)]], "source scatter")
    require(atc == positive and atc == transpose(atc),
            "aligned cross-covariance symmetry")
    require(all(determinant([row[:k] for row in atc[:k]]) > 0
                for k in range(1, 4)), "aligned cross-covariance positivity")

    ctc = matmul(transpose(c), c)
    require(matmul(ata, ctc) != matmul(ctc, ata),
            "noncommuting covariance control")

    aa = matmul(a, transpose(a))
    cc = matmul(c, transpose(c))
    gram_error = frobenius2(matsub(aa, cc))
    displacement = sum((norm2(sub(tuple(x), tuple(y))) for x, y in zip(a, c)),
                       F(0))
    u = [[x + y for x, y in zip(arow, crow)] for arow, crow in zip(a, c)]
    v = [[x - y for x, y in zip(arow, crow)] for arow, crow in zip(a, c)]
    utu = matmul(transpose(u), u)
    vtv = matmul(transpose(v), v)
    utv = matmul(transpose(u), v)
    rhs = (trace(matmul(utu, vtv)) + trace(matmul(utv, utv))) / 2
    require(gram_error == rhs, "Procrustes trace identity")
    require(gram_error >= F(4, 2) * displacement,
            "Procrustes displacement bound")
    return {
        "gram_error": gram_error,
        "aligned_displacement": displacement,
        "trace_square_term": trace(matmul(utv, utv)) / 2,
        "source_scatter_floor": 4,
        "covariances_commute": False,
    }


def provenance():
    data = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    for item in data["files"]:
        digest = sha256((HERE / item["relative_path"]).read_bytes()).hexdigest()
        require(digest == item["sha256"], "reviewed source bytes changed")
    return data["target"], len(data["files"])


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def main():
    target_metadata, pins = provenance()
    direct = direct_fixture()
    interval = interval_enclosure()
    procrustes = procrustes_identity_fixture()

    # A zero-angle boundary must collapse the paired affine rank; this catches
    # accidental rank assertions that ignore the parameter restriction t>0.
    boundary_source, boundary_target, _ = family(F(0))
    paired = [boundary_source[i] + boundary_target[i] for i in range(12)]
    require(rank([sub(row, paired[0]) for row in paired[1:]]) == 3,
            "zero-angle boundary control")

    record = encode({
        "status": "INDEPENDENT_RIGID_BLOCK_REVIEW_PASS",
        "target": target_metadata,
        "pinned_files": pins,
        "direct_fixture": direct,
        "whole_interval": interval,
        "procrustes_fixture": procrustes,
        "negative_controls": 1,
        "trust_boundary": (
            "finite exact corroboration only; rotation-logarithm estimates, "
            "continuous-motion transfer, and historical novelty remain "
            "human-reviewed mathematics"
        ),
    })
    raw = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps({"record": record, "record_sha256": sha256(raw).hexdigest()},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
