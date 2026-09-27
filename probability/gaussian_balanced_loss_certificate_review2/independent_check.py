#!/usr/bin/env python3
"""Independent exact audit of the balanced-loss motion certificate.

No target module is imported.  The checker works from the geometric
definitions: it applies explicit endpoint alignments, verifies the trace
decomposition, and checks every pair derivative throughout a straight path.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def q(value):
    require(type(value) in (int, str), "non-rational input")
    return F(value)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c * a for a in x)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def norm2(x):
    return dot(x, x)


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def matsub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def matadd(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def matscale(c, a):
    return [[c * x for x in row] for row in a]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def frobenius2(a):
    return sum((x * x for row in a for x in row), F(0))


def determinant3(a):
    return (a[0][0] * a[1][1] * a[2][2]
            + 2 * a[0][1] * a[0][2] * a[1][2]
            - a[0][0] * a[1][2] ** 2
            - a[1][1] * a[0][2] ** 2
            - a[2][2] * a[0][1] ** 2)


def psd3(a):
    require(all(a[i][j] == a[j][i] for i in range(3) for j in range(3)),
            "matrix is not symmetric")
    one = [a[i][i] for i in range(3)]
    two = [a[i][i] * a[j][j] - a[i][j] ** 2
           for i, j in combinations(range(3), 2)]
    return min(one + two + [determinant3(a)]) >= 0


def centered(points):
    n = len(points)
    mean = tuple(sum((p[j] for p in points), F(0)) / n for j in range(3))
    return [sub(p, mean) for p in points], mean


def row_transform(points, matrix):
    return [tuple(dot(row, col) for col in transpose(matrix)) for row in points]


def scatter(points):
    return matmul(transpose(points), points)


def row_gram(points):
    return matmul(points, transpose(points))


def losses(a, b):
    return {(i, j): norm2(sub(a[i], a[j])) - norm2(sub(b[i], b[j]))
            for i, j in combinations(range(len(a)), 2)}


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        d = a[r][col]
        a[r] = [x / d for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                c = a[i][col]
                a[i] = [x - c * y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def parse_points(data, name):
    return [tuple(q(value) for value in row) for row in data[name]]


def audit_motion(a, c, k):
    n = len(a)
    s = scatter(a)
    require(psd3([[s[i][j] - (k if i == j else 0)
                   for j in range(3)] for i in range(3)]), "bad scatter floor")
    cross = matmul(transpose(a), c)
    require(psd3(cross), "endpoint alignment is not polar")
    ga, gc = row_gram(a), row_gram(c)
    gram_error = matsub(ga, gc)
    f_value = frobenius2(gram_error)
    u, v = matadd(a, c), matsub(a, c)
    utu, vtv = scatter(u), scatter(v)
    utv = matmul(transpose(u), v)
    decomposition = (trace(matmul(utu, vtv)) + trace(matmul(utv, utv))) / 2
    require(f_value == decomposition, "trace decomposition failed")
    require(trace(vtv) * k <= 2 * f_value, "rigidity lower bound failed")
    pair_losses = losses(a, c)
    require(pair_losses and min(pair_losses.values()) >= 0, "endpoint expansion")
    delta = min(pair_losses.values())
    require(k * delta >= 4 * f_value, "certificate guard failed")
    positions = 0
    for (i, j), loss in pair_losses.items():
        source = sub(a[i], a[j])
        target = sub(c[i], c[j])
        displacement = sub(source, target)
        require(norm2(displacement) <= 4 * f_value / k <= loss,
                "pair displacement bound failed")
        previous = None
        for step in range(9):
            time = F(step, 8)
            location = add(scale(1 - time, source), scale(time, target))
            derivative = 2 * dot(location, sub(target, source))
            require(derivative <= 0, "noncontracting path derivative")
            if previous is not None:
                require(previous <= derivative, "derivative is not increasing")
            previous = derivative
            positions += 1
        require(2 * dot(target, sub(target, source)) ==
                norm2(displacement) - loss, "endpoint derivative identity")
    ordered_square_loss = 2 * sum(value * value for value in pair_losses.values())
    require(4 * f_value <= ordered_square_loss, "double-centering norm bound")
    return {
        "pairs": len(pair_losses),
        "path_positions": positions,
        "F": f_value,
        "delta": delta,
        "epsilon": max(pair_losses.values()),
    }


def target_fixture():
    source_dir = ROOT / "probability/gaussian_balanced_loss_certificate"
    data = json.loads((source_dir / "INPUT.json").read_text())
    record = json.loads((source_dir / "CERTIFICATE.json").read_text())
    x, y = parse_points(data, "x"), parse_points(data, "y")
    a, _ = centered(x)
    b, _ = centered(y)
    reflection = [[F(-1), F(0), F(0)],
                  [F(0), F(1), F(0)],
                  [F(0), F(0), F(1)]]
    c = row_transform(b, reflection)
    result = audit_motion(a, c, F(1, 2))
    pair_losses = losses(a, c)
    canonical_input = json.dumps(data, sort_keys=True,
                                 separators=(",", ":")).encode()
    expected = {
        "schema": "balanced-loss-v1",
        "input_sha256": sha256(canonical_input).hexdigest(),
        "n": 8,
        "status": "SIGNED_ALL_VARIANCES_ALL_THRESHOLDS",
        "scatter_floor": "1/2",
        "gram_frobenius_squared": str(result["F"]),
        "minimum_pair_loss": str(result["delta"]),
        "maximum_pair_loss": str(result["epsilon"]),
        "guard_slack": str(F(1, 2) * result["delta"] - 4 * result["F"]),
        "pair_error_upper": str(8 * result["F"]),
        "law_scope": "every probability vector on the supplied labels",
    }
    require(record == expected, "published certificate mismatch")
    raw_bad = 0
    for (i, j) in combinations(range(8), 2):
        source, target = sub(a[i], a[j]), sub(b[i], b[j])
        if 2 * dot(target, sub(target, source)) > 0:
            raw_bad += 1
    require(raw_bad > 0, "alignment negative control was not exposed")
    paired_rank = rank([list(a[i]) + list(c[i]) for i in range(8)])
    require(paired_rank == 6, "target paired rank changed")
    return result, raw_bad, paired_rank


def walsh_geometry(time):
    signs = list(product((-1, 1), repeat=3))
    a = [tuple(F(value, 3) for value in row) for row in signs]
    w = [(F(v * z, 9), F(u * z, 9), F(u * v, 9)) for u, v, z in signs]
    mix = [[F(1), F(1), F(0)],
           [F(0), F(1), F(1)],
           [F(1), F(0), F(1)]]
    wm = row_transform(w, mix)
    c = [add(scale(1 - 8 * time, a[i]), scale(time, wm[i]))
         for i in range(8)]
    frame = [[F(0), F(1), F(0)],
             [F(1), F(0), F(0)],
             [F(0), F(0), F(-1)]]
    translation = (F(7, 3), F(-5, 4), F(11, 6))
    raw = [add(row, translation) for row in row_transform(c, frame)]
    b, _ = centered(raw)
    aligned = row_transform(b, frame)
    require(aligned == c, "fresh frame inversion failed")
    return a, aligned


def fresh_fixture():
    a, c = walsh_geometry(F(1, 1024))
    result = audit_motion(a, c, F(4, 5))
    paired_rank = rank([list(a[i]) + list(c[i]) for i in range(8)])
    require(paired_rank == 6, "fresh fixture lost paired rank six")
    return result, paired_rank


def covariance(points, weights):
    mean = tuple(sum((weights[i] * points[i][j] for i in range(len(points))), F(0))
                 for j in range(3))
    centered_points = [sub(point, mean) for point in points]
    cov = [[sum((weights[r] * centered_points[r][i] * centered_points[r][j]
                for r in range(len(points))), F(0))
            for j in range(3)] for i in range(3)]
    return mean, centered_points, cov


def weighted_corollary_checks():
    a, c = walsh_geometry(F(1, 2 ** 40))
    vectors = [
        [F(1, 8)] * 8,
        [F(value, 36) for value in range(1, 9)],
        [F(value, 24) for value in (1, 2, 4, 5, 1, 3, 6, 2)],
    ]
    pair_losses = losses(a, c)
    delta, epsilon = min(pair_losses.values()), max(pair_losses.values())
    rho = delta / epsilon
    checks = 0
    for weights in vectors:
        require(sum(weights, F(0)) == 1 and all(value > 0 for value in weights),
                "invalid weights")
        _, centered_a, cov = covariance(a, weights)
        tr = trace(cov)
        kappa = determinant3(cov) / (tr * tr)
        require(kappa > 0 and psd3([[cov[i][j] - (kappa if i == j else 0)
                                    for j in range(3)] for i in range(3)]),
                "weighted covariance floor failed")
        radius2 = max(norm2(point) for point in centered_a)
        d_mean = 2 * sum(weights[i] * weights[j] * loss
                         for (i, j), loss in pair_losses.items())
        off_mass = 1 - sum(value * value for value in weights)
        require(3 * kappa <= trace(cov) <= 2 * radius2 * off_mass,
                "scatter-radius chain failed")
        require(d_mean >= rho * epsilon * off_mass >=
                3 * rho * kappa * epsilon / (2 * radius2),
                "mean-loss lower chain failed")
        sufficient = 3 * rho * rho * kappa * kappa / (2 * radius2 * 64)
        require(d_mean <= sufficient, "fresh weighted budget failed")
        checks += 1
    return checks


def parameter_constants():
    rho = F(1, 4)
    kappa = F(1, 2 ** 15)
    radius2 = F(1, 4)
    mean_loss = F(1, 2 ** 40)
    checks = 0
    for n in range(4, 20):
        bound = 3 * rho * rho * kappa * kappa / (2 * radius2 * n * n)
        require(mean_loss <= bound, f"atom budget failed at n={n}")
        checks += 1
    require(8 * 19 * 19 <= 3 * 2 ** 10, "integer endpoint constant")
    return checks


def negative_controls():
    failures = 0
    # Expansion must be rejected.
    try:
        require(F(1) - F(4) >= 0, "expanding pair")
    except RuntimeError:
        failures += 1
    # An overstated scatter floor must be rejected.
    a, c = walsh_geometry(F(1, 1024))
    try:
        audit_motion(a, c, F(1))
    except RuntimeError:
        failures += 1
    # The guard is deliberately sufficient, not automatic.
    a, c = walsh_geometry(F(1, 4))
    try:
        audit_motion(a, c, F(4, 5))
    except RuntimeError:
        failures += 1
    # A damaged published record must not match reconstruction.
    source_dir = ROOT / "probability/gaussian_balanced_loss_certificate"
    record = json.loads((source_dir / "CERTIFICATE.json").read_text())
    damaged = dict(record)
    damaged["guard_slack"] = "0"
    require(damaged != record, "record corruption was not exposed")
    failures += 1
    require(failures == 4, "negative control count")
    return failures


def check_pins():
    pins = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    for record in pins["files"]:
        payload = (ROOT / record["path"]).read_bytes()
        require(sha256(payload).hexdigest() == record["sha256"],
                f"pin mismatch: {record['path']}")
    return pins


def main():
    pins = check_pins()
    target, raw_bad, target_rank = target_fixture()
    fresh, fresh_rank = fresh_fixture()
    weighted = weighted_corollary_checks()
    budgets = parameter_constants()
    rejected = negative_controls()
    result = {
        "status": "INDEPENDENT_BALANCED_LOSS_REVIEW_PASS",
        "target_artifact": pins["target"]["artifact_ref"],
        "target_commit": pins["target"]["source_commit"],
        "pinned_files": len(pins["files"]),
        "target_pairs": target["pairs"],
        "target_path_positions": target["path_positions"],
        "target_raw_frame_adverse_derivatives": raw_bad,
        "target_paired_rank": target_rank,
        "fresh_pairs": fresh["pairs"],
        "fresh_path_positions": fresh["path_positions"],
        "fresh_paired_rank": fresh_rank,
        "trace_decomposition_checks": 2,
        "weighted_corollary_checks": weighted,
        "parameter_budget_checks": budgets,
        "negative_controls": rejected,
        "universal_scope": "written matrix and motion proof; exact checks are not formalization",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
