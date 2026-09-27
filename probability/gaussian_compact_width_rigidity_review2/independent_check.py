#!/usr/bin/env python3
"""Independent exact checks for compact Gaussian-width rigidity.

The checker imports no target module.  It validates the exposed-pair and
graph-span mechanisms directly on rational contractions, reconstructs a
symmetric operator from rotated quadratic moments, and checks an exact
compact segment model for the large-radius union/intersection conclusion.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def qform(a, v):
    return sum((a[i][j] * v[i] * v[j]
                for i in range(len(v)) for j in range(len(v))), F(0))


def transpose(a):
    return list(map(list, zip(*a)))


def matmul(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


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
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                multiple = a[i][col]
                a[i] = [x - multiple * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def independent_rows(rows):
    basis = []
    old_rank = 0
    for row in rows:
        new_rank = rank(basis + [row])
        if new_rank > old_rank:
            basis.append(row)
            old_rank = new_rank
    return basis


def apply_linear(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def graph_fixture():
    source = [tuple(map(F, row)) for row in
              ((0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2),
               (1, 1, 1), (-1, 1, 2), (2, -1, 1))]
    contraction = [[F(1), F(0), F(0)],
                   [F(0), F(1, 2), F(0)],
                   [F(0), F(0), F(1, 3)]]
    target = [apply_linear(contraction, x) for x in source]
    graph = [x + y for x, y in zip(source, target)]
    signature = [[F((1 if i < 3 else -1) if i == j else 0)
                  for j in range(6)] for i in range(6)]

    losses = {}
    for i, j in combinations(range(len(source)), 2):
        difference = sub(graph[i], graph[j])
        loss = dot(sub(source[i], source[j]), sub(source[i], source[j]))
        loss -= dot(sub(target[i], target[j]), sub(target[i], target[j]))
        require(loss == qform(signature, difference) >= 0, "graph loss identity")
        losses[i, j] = loss
    require(any(value > 0 for value in losses.values()), "strict contraction fixture")

    basis = independent_rows([sub(point, graph[0]) for point in graph[1:]])
    compression = [[sum((signature[k][k] * u[k] * v[k] for k in range(6)), F(0))
                    for v in basis] for u in basis]
    require(len(basis) == 3 and rank(compression) == 2,
            "nonisometric graph compression")

    # A rational orthogonal map gives a totally null graph span.
    orthogonal = [[F(0), F(-1), F(0)], [F(1), F(0), F(0)],
                  [F(0), F(0), F(-1)]]
    isometric_graph = [x + apply_linear(orthogonal, x) for x in source]
    iso_basis = independent_rows([sub(point, isometric_graph[0])
                                  for point in isometric_graph[1:]])
    iso_compression = [[sum((signature[k][k] * u[k] * v[k] for k in range(6)), F(0))
                        for v in iso_basis] for u in iso_basis]
    require(len(iso_basis) == 3 and all(value == 0 for row in iso_compression for value in row),
            "isometric graph span is not null")

    # At differentiability directions of the finite support function, the
    # symmetrized gradient is the unique exposed maximum-minus-minimum pair.
    exposed = 0
    strict_exposed = 0
    for seed in range(1, 121):
        direction = tuple(F(((seed + 3 * j) ** 2 + 5 * j) % 29 - 14)
                          for j in range(6))
        values = [dot(direction, point) for point in graph]
        maximum = max(values)
        minimum = min(values)
        if values.count(maximum) != 1 or values.count(minimum) != 1:
            continue
        i, j = values.index(maximum), values.index(minimum)
        gradient = sub(graph[i], graph[j])
        pair = (min(i, j), max(i, j))
        require(qform(signature, gradient) == losses[pair] >= 0,
                "exposed-pair gradient sign")
        exposed += 1
        strict_exposed += int(losses[pair] > 0)
    require(exposed >= 50 and strict_exposed > 0, "insufficient exposed controls")

    # The log-sum-exp trace identity depends only on the posterior weights.
    posterior_cases = 0
    for seed in range(1, 25):
        weights = [F((seed + i * i + 1) ** 2) for i in range(len(source))]
        total = sum(weights, F(0))
        weights = [w / total for w in weights]
        mean_x = tuple(sum((w * x[k] for w, x in zip(weights, source)), F(0))
                       for k in range(3))
        mean_y = tuple(sum((w * y[k] for w, y in zip(weights, target)), F(0))
                       for k in range(3))
        trace_gap = sum((w * (dot(x, x) - dot(y, y))
                         for w, x, y in zip(weights, source, target)), F(0))
        trace_gap -= dot(mean_x, mean_x) - dot(mean_y, mean_y)
        ordered_loss = sum((weights[i] * weights[j] *
                            (F(0) if i == j else losses[min(i, j), max(i, j)])
                            for i in range(len(source)) for j in range(len(source))), F(0))
        require(trace_gap == ordered_loss / 2 > 0, "posterior loss identity")
        posterior_cases += 1

    # A noncontraction is rejected at the same definition-level interface.
    expansion = [[F(2), F(0), F(0)], [F(0), F(1), F(0)],
                 [F(0), F(0), F(1)]]
    expanded = [apply_linear(expansion, x) for x in source]
    require(any(dot(sub(source[i], source[j]), sub(source[i], source[j]))
                - dot(sub(expanded[i], expanded[j]), sub(expanded[i], expanded[j])) < 0
                for i, j in combinations(range(len(source)), 2)),
            "expansion negative control")
    return {
        "sites": len(source),
        "pairs": len(losses),
        "strict_pairs": sum(value > 0 for value in losses.values()),
        "graph_span_rank": len(basis),
        "compressed_operator_rank": rank(compression),
        "isometric_compression_zero": True,
        "unique_exposed_directions": exposed,
        "strict_exposed_directions": strict_exposed,
        "posterior_cases": posterior_cases,
    }


def symmetric_coordinates(dimension):
    return [(i, j) for i in range(dimension) for j in range(i, dimension)]


def moment_row(vector, coordinates):
    # Half of L_A[(v.z)^2] is v^T A v.  Off-diagonal symmetric entries occur twice.
    return [vector[i] * vector[j] * (1 if i == j else 2) for i, j in coordinates]


def moment_isolation():
    results = {}
    total = 0
    for dimension in range(1, 7):
        coordinates = symmetric_coordinates(dimension)
        vectors = []
        for i in range(dimension):
            vectors.append(tuple(F(k == i) for k in range(dimension)))
        for i in range(dimension):
            for j in range(i + 1, dimension):
                vectors.append(tuple(F(k == i or k == j) for k in range(dimension)))
        matrix = [moment_row(vector, coordinates) for vector in vectors]
        require(len(matrix) == len(coordinates) and rank(matrix) == len(coordinates),
                "quadratic moments do not isolate symmetric operator")

        coefficients = [F(((7 * i + dimension) % 19) - 9, i + 1)
                        for i in range(len(coordinates))]
        values = [dot(row, coefficients) for row in matrix]
        require(all(value == 0 for value in values) == all(value == 0 for value in coefficients),
                "moment reconstruction control")
        results[str(dimension)] = len(coordinates)
        total += len(coordinates)
    return {"dimensions": results, "full_rank_moments": total}


def compact_segment_model():
    # K=[-e1,e1], T(x)=x/2.  Under normalized spherical measure in R3,
    # integral |theta_1|=1/2, so m(K)=1/2, m(TK)=1/4 and omega=1/4.
    radius = F(1)
    omega = F(1, 4)
    theorem_radius = max(2 * radius, 16 * radius * radius / omega)
    require(theorem_radius == 64, "large-radius cutoff")

    # Factoring out pi, the union of radius-r balls over a segment of length d
    # is 4r^3/3 + d r^2.  The intersection is the endpoint lens
    # 4r^3/3 - d r^2 + d^3/12.
    r = theorem_radius
    union_difference = r * r  # d=2 minus d=1
    intersection_difference = r * r - F(7, 12)
    guaranteed_margin = 2 * omega * r * r
    require(union_difference >= guaranteed_margin > 0,
            "segment union strict margin")
    require(intersection_difference >= guaranteed_margin > 0,
            "segment intersection strict margin")

    # The pointwise cubic remainder used in the general radial proof.
    cubic_remainder = F(3) + F(27, 4) + F(27, 16)
    require(cubic_remainder == F(183, 16) < 12, "radial cubic enclosure")
    volume_error = F(4, 3) * 12
    require(volume_error == 16, "radial volume error")
    return {
        "source_half_mean_width": F(1, 2),
        "target_half_mean_width": F(1, 4),
        "width_gap": omega,
        "theorem_radius": theorem_radius,
        "union_difference_over_pi": union_difference,
        "intersection_difference_over_pi": intersection_difference,
        "guaranteed_difference_over_pi": guaranteed_margin,
        "radial_remainder_coefficient": cubic_remainder,
    }


def provenance():
    metadata = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    for item in metadata["files"]:
        digest = sha256((HERE / item["relative_path"]).read_bytes()).hexdigest()
        require(digest == item["sha256"], "reviewed source bytes changed")
    return metadata["target"], len(metadata["files"])


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def main():
    target, pins = provenance()
    record = encode({
        "status": "INDEPENDENT_COMPACT_WIDTH_REVIEW_PASS",
        "target": target,
        "pinned_files": pins,
        "graph_fixture": graph_fixture(),
        "moment_isolation": moment_isolation(),
        "compact_segment": compact_segment_model(),
        "negative_controls": 2,
        "method": (
            "definition-level graph span and exposed pairs; rotated quadratic "
            "moment reconstruction; exact capsule/lens compact model"
        ),
        "trust_boundary": (
            "finite exact corroboration only; distributional limits, convex "
            "support-function regularity, and accepted eventual-majorisation "
            "dependencies remain human-reviewed mathematics"
        ),
    })
    raw = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps({"record": record, "record_sha256": sha256(raw).hexdigest()},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
