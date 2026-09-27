"""Definition-level exact checks for the strict screw R5 barrier.

No target module is imported.  The 24 reference sites are reconstructed from
the displayed paraboloid formulas, the strict witness is decoded separately,
and the determinant identity is checked by exact tensor-grid interpolation
rather than the author's symbolic polynomial implementation.
"""

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET_COMMIT = "57e474d503119b7c67cdfe4ce92bc4616ed4312a"
DELTA = Q(1, 2 ** 136)
ETA = Q(1, 2 ** 56)
ERROR = Q(1, 2 ** 20)
SCALE = 1 - Q(1, 2 ** 145)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git_bytes(commit, path):
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def pins():
    records = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    for record in records:
        raw = git_bytes(record["commit"], record["path"])
        require(hashlib.sha256(raw).hexdigest() == record["sha256"],
                "reviewed source drift")
    return len(records)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def minus(x, y):
    return tuple(a - b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def matrix_vector(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def determinant(matrix):
    work = [list(row) for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, len(work)):
            ratio = work[row][column] / value
            for index in range(column, len(work)):
                work[row][index] -= ratio * work[column][index]
    return answer


def rank(matrix):
    work = [list(row) for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next((index for index in range(row, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[pivot], work[row] = work[row], work[pivot]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for index in range(len(work)):
            if index != row and work[index][column]:
                factor = work[index][column]
                work[index] = [a - factor * b
                               for a, b in zip(work[index], work[row])]
        row += 1
        if row == len(work):
            break
    return row


def squared_distances(points):
    return [[norm2(minus(p, q)) for q in points] for p in points]


def rotate90(u):
    return (-u[1], u[0])


def c_map(u):
    ju = rotate90(u)
    return (u[0] - ju[0], u[1] - ju[1])


def a_point(v):
    return (v[0], v[1], (1 + norm2(v)) / 2)


def b_point(u):
    return (u[0], u[1], -norm2(u))


def tb_point(u):
    ju = rotate90(u)
    return (ju[0], ju[1], 1 - norm2(u))


def reconstruct_reference():
    e1, e2 = (Q(1), Q(0)), (Q(0), Q(1))
    u_values = ((Q(0), Q(0)), e1, (-e1[0], -e1[1]),
                (Q(2), Q(0)), (Q(-2), Q(0)), e2,
                (-e2[0], -e2[1]), (Q(1), Q(1)))
    a_parameters = [c_map(u) for u in u_values]
    for u in ((Q(0), Q(0)), e1):
        center = c_map(u)
        for direction in (e1, e2):
            for sign in (Q(-1), Q(1)):
                a_parameters.append((center[0] + sign * direction[0] / 4,
                                     center[1] + sign * direction[1] / 4))
    # Match the immutable label ordering A8,A9,A10,A11,A12,... used by the
    # published witness: direction first, then negative/positive displacement.
    sites = []
    for index, v in enumerate(a_parameters):
        sites.append({"label": f"A{index}", "group": "A", "parameter": v,
                      "source": a_point(v), "target": a_point(v)})
    for offset, u in enumerate(u_values, 16):
        sites.append({"label": f"B{offset}", "group": "B", "parameter": u,
                      "source": b_point(u), "target": tb_point(u)})
    return sites


def parse_fraction(value):
    require(type(value) in (str, int), "nonrational witness coordinate")
    return Q(value)


def decode_witness(raw):
    require(isinstance(raw, dict) and set(raw) == {"sites"}, "witness schema")
    decoded = []
    for site in raw["sites"]:
        require(set(site) == {"label", "source", "target"}, "witness site schema")
        decoded.append({"label": site["label"],
                        "source": tuple(map(parse_fraction, site["source"])),
                        "target": tuple(map(parse_fraction, site["target"]))})
    return decoded


def centered_scatter(points):
    center = tuple(sum((point[j] for point in points), Q(0)) / len(points)
                   for j in range(3))
    shifted = [minus(point, center) for point in points]
    return [[sum((point[i] * point[j] for point in shifted), Q(0))
             for j in range(3)] for i in range(3)]


def tau(distance_matrix, sites):
    lookup = {site["label"]: index for index, site in enumerate(sites)}
    r = {lookup["B16"]: Q(1), lookup["A0"]: Q(-3, 2),
         lookup["A1"]: Q(1, 4), lookup["A2"]: Q(1, 4)}
    s = {lookup["A0"]: Q(-1), lookup["A1"]: Q(1, 2),
         lookup["A2"]: Q(1, 2)}
    value = -sum((ri * sj * distance_matrix[i][j]
                  for i, ri in r.items() for j, sj in s.items()), Q(0)) / 2
    return value, sum(map(abs, r.values()), Q(0)) * sum(map(abs, s.values()), Q(0)) / 2


def general_loss(v, u, matrix, translation, pulled_translation, d):
    identity = [[Q(i == j) for j in range(3)] for i in range(3)]
    b = b_point(u)
    displacement = tuple(x - y + z for x, y, z in
                         zip(matrix_vector(matrix, b), b, translation))
    return 2 * dot(a_point(v), displacement) - 2 * dot(pulled_translation, b) - d


def axis_finite_difference_controls():
    # The fourth-difference statement is affine in the 16 displayed entries.
    # Zero plus every coordinate basis vector is therefore a universal check.
    cases = []
    cases.append(([Q(0)] * 9, [Q(0)] * 3, [Q(0)] * 3, Q(0)))
    for position in range(16):
        values = [Q(0)] * 16
        values[position] = Q(1)
        cases.append((values[:9], values[9:12], values[12:15], values[15]))
    coefficients = (Q(1), Q(-4), Q(6), Q(-4), Q(1))
    for matrix_entries, translation, pulled, d in cases:
        matrix = [matrix_entries[3 * row:3 * row + 3] for row in range(3)]
        values = []
        for x in map(Q, (-2, -1, 0, 1, 2)):
            u = (x, Q(0))
            values.append(general_loss(c_map(u), u, matrix, translation, pulled, d))
        fourth = dot(coefficients, values)
        require(fourth == 48 * (1 - matrix[2][2]), "axis fourth difference")
    return len(cases)


def determinant_grid_controls():
    # Both sides have coordinatewise degrees at most (4,2,2).  Equality on
    # this 5x3x3 exact grid therefore proves the polynomial identity.
    checked = 0
    for alpha, v1, v2 in itertools.product(map(Q, (-2, -1, 0, 1, 2)),
                                            map(Q, (-1, 0, 1)),
                                            map(Q, (-1, 0, 1))):
        k = 1 - 2 * alpha * alpha
        x1 = (1 - alpha) * v1 - (1 + alpha) * v2
        x2 = (1 + alpha) * v1 + (1 - alpha) * v2
        h0 = ((k, Q(0), x1),
              (Q(0), k, x2),
              (x1, x2, Q(1, 4) - v1 * v1 - v2 * v2))
        expected = k * (k / 4 - 3 * (v1 * v1 + v2 * v2))
        require(determinant(h0) == expected, "determinant interpolation grid")
        checked += 1
    return checked


def constant_controls():
    root_delta, root_eta = Q(1, 2 ** 68), Q(1, 2 ** 28)
    checked = 0
    for n in range(3, 17):
        require(2 * n * DELTA / Q(1, 16) < Q(1, 2), "polar invertibility")
        require(DELTA <= Q(1, 16) ** 2 / (12 * n * 128), "polar error")
        require(3 * n * n * DELTA < 1024 * DELTA, "point alignment")
        checked += 3
    guards = (
        root_delta * root_delta == DELTA,
        root_eta * root_eta == ETA,
        64 * root_delta <= 1,
        DELTA + 1600 * root_delta < ETA,
        128 + ETA < 144,
        ETA + 145 * root_eta < ERROR,
        4800 * root_delta < ERROR,
        3 * DELTA < Q(1, 2),
        Q(1, 16) + 5 * ERROR <= Q(9, 128),
        Q(1, 8) + 14 * ERROR <= Q(9, 64),
        1 + 12 * ERROR <= 2,
        (1 - SCALE * SCALE) * 128 < DELTA,
    )
    require(all(guards), "global perturbation guard")
    checked += len(guards)
    k_floor = 1 - 2 * Q(41, 64) ** 2
    v_ceiling = 2 * Q(9, 128) ** 2
    determinant_floor = k_floor * (k_floor / 4 - 3 * v_ceiling)
    determinant_error = 864 * ERROR
    require((k_floor, v_ceiling, determinant_floor, determinant_error,
             determinant_floor - determinant_error) ==
            (Q(367, 2048), Q(81, 8192), Q(11377, 2 ** 22),
             Q(27, 32768), Q(7921, 2 ** 22)), "determinant margin")
    checked += 1
    return checked, determinant_floor - determinant_error


def audit():
    pin_count = pins()
    sites = reconstruct_reference()
    require(len(sites) == 24 and len({site["label"] for site in sites}) == 24,
            "reference labels")
    source = [site["source"] for site in sites]
    target = [site["target"] for site in sites]
    source_distances = squared_distances(source)
    target_distances = squared_distances(target)

    within_tight = cross_identity = 0
    for i, j in itertools.combinations(range(24), 2):
        loss = source_distances[i][j] - target_distances[i][j]
        if sites[i]["group"] == sites[j]["group"]:
            require(loss == 0, "within-group rigidity")
            within_tight += 1
        else:
            a_site, b_site = ((sites[i], sites[j]) if sites[i]["group"] == "A"
                              else (sites[j], sites[i]))
            predicted = norm2(minus(a_site["parameter"], c_map(b_site["parameter"])))
            require(loss == predicted, "cross-loss formula")
            cross_identity += 1
    require((within_tight, cross_identity) == (148, 128), "pair partition")
    reference_losses = [source_distances[i][j] - target_distances[i][j]
                        for i, j in itertools.combinations(range(24), 2)]
    require(sum(loss == 0 for loss in reference_losses) == 156,
            "reference tight-pair count")

    scatter_minors = {}
    for group in ("A", "B"):
        scatter = centered_scatter([site["source"] for site in sites
                                    if site["group"] == group])
        shifted = [[scatter[i][j] - (Q(1, 16) if i == j else 0)
                    for j in range(3)] for i in range(3)]
        minors = [determinant([row[:size] for row in shifted[:size]])
                  for size in (1, 2, 3)]
        require(all(value > 0 for value in minors), "scatter floor")
        scatter_minors[group] = [str(value) for value in minors]
    diameter = max(value for matrix in (source_distances, target_distances)
                   for row in matrix for value in row)
    require(diameter == Q(369, 4) and diameter < 128, "diameter")
    require(max(norm2(site["source"]) for site in sites if site["group"] == "B") == 20,
            "B radius")
    source_tau = tau(source_distances, sites)
    target_tau = tau(target_distances, sites)
    require(source_tau == (Q(0), Q(3)) and target_tau == (Q(1), Q(3)),
            "intrinsic halfway functional")

    saved = decode_witness(json.loads(
        git_bytes(TARGET_COMMIT,
                  "probability/gaussian_strict_screw_motion_barrier/WITNESS.json")
    ))
    expected = [{"label": site["label"], "source": site["source"],
                 "target": tuple(SCALE * value for value in site["target"])}
                for site in sites]
    require(saved == expected, "strict witness is not the reconstructed formula")
    strict_source = [site["source"] for site in saved]
    strict_target = [site["target"] for site in saved]
    strict_source_distances = squared_distances(strict_source)
    strict_target_distances = squared_distances(strict_target)
    strict_losses = [strict_source_distances[i][j] - strict_target_distances[i][j]
                     for i, j in itertools.combinations(range(24), 2)]
    require(all(loss > 0 for loss in strict_losses), "strict witness has a contact")
    target_error = max(abs(strict_target_distances[i][j] - target_distances[i][j])
                       for i, j in itertools.combinations(range(24), 2))
    require(target_error < DELTA, "strict witness outside metric box")
    maximum_ratio = max(strict_target_distances[i][j] / strict_source_distances[i][j]
                        for i, j in itertools.combinations(range(24), 2))
    require(maximum_ratio == SCALE * SCALE, "exact Lipschitz ratio")

    anchor_matrix = [list(p) + list(q) + [Q(1), norm2(p) - norm2(q)]
                     for p, q in zip(strict_source, strict_target)]
    require(rank(anchor_matrix) == 8, "anchor rank")
    require(rank([row[:7] for row in anchor_matrix]) == 7, "paired affine rank")

    axis_cases = axis_finite_difference_controls()
    determinant_cases = determinant_grid_controls()
    constant_cases, determinant_margin = constant_controls()
    state = {
        "diameter": str(diameter),
        "scatter_minors": scatter_minors,
        "target_error": str(target_error),
        "minimum_strict_loss": str(min(strict_losses)),
        "maximum_ratio": str(maximum_ratio),
        "determinant_margin": str(determinant_margin),
    }
    state_hash = hashlib.sha256(
        json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "status": "INDEPENDENT_STRICT_SCREW_R5_REVIEW_PASS",
        "target_commit": TARGET_COMMIT,
        "source_pins": pin_count,
        "sites": len(sites),
        "pairs": 276,
        "within_group_pairs": within_tight,
        "cross_formula_pairs": cross_identity,
        "reference_tight_pairs": sum(loss == 0 for loss in reference_losses),
        "strict_pairs": sum(loss > 0 for loss in strict_losses),
        "strict_target_metric_error": str(target_error),
        "axis_affine_basis_cases": axis_cases,
        "determinant_interpolation_cases": determinant_cases,
        "constant_cases": constant_cases,
        "determinant_margin": str(determinant_margin),
        "anchor_augmented_rank": rank(anchor_matrix),
        "paired_affine_rank": rank([row[:7] for row in anchor_matrix]) - 1,
        "exact_state_sha256": state_hash,
        "trust_boundary": "Exact independent controls plus human perturbation audit; not formalized",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
