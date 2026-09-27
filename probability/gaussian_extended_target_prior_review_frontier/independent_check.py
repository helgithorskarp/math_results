#!/usr/bin/env python3
"""Independent exact checks for the extended-target full-prior cell review.

This standard-library checker does not import the target verifier.  It checks
the actual sixteen-label simplex and tetrahedral label action, exercises the
supporting-plane inequality on exact synthetic component densities, and
independently interprets the committed middle/radial certificate record.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from math import comb
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
TARGET = REPO / "probability/gaussian_extended_target_prior_cell"
TARGET_COMMIT = "4e006ae51713af09a45229d9df59341a6f4fd03c"
TARGET_HASHES = {
    ".gitignore": "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "EXPECTED.json": "f1882e7c29809ef2b2fe81ca68b3fe8d3a365bc4e49e509c1358cd90a8a94ac4",
    "INPUTS.json": "8b5581787b1131a6ca738c0b7e9f45b59e2d75f398b1f38ed0b494cd8b62f3c1",
    "PROOF.md": "a65f95bd3b24aa5d8aebbad375bcee30e9be3aa09eefbb57910f1f916c31c649",
    "README.md": "3f269dd7f295e4cd3b29df13caa35ba38356af4dce018869f025edd395c51c88",
    "SHA256SUMS": "ad989554ae693743b2d2ce10928fe674152cd6b88fc5c7d92f7f506b608beb65",
    "SOURCES.md": "5d58d8bc3d9645ff572dbaeadd74fedb807b0edfaa9016b6fa779cab45b82da6",
    "common.py": "384e96774be99c5730e8022fb53ed389c144b4047465399f386c54c9448d01d4",
    "middle_certificate.py": "3078217795dc09354a72c32a0e0b239c98aa53cea670d687298ff51d12a0835d",
    "radial_certificate.py": "b44f9b1b6c54cc8345ecc10f6e5c4897a47a337dc16076304f97f958f447e099",
    "verify.py": "d6100b15d545317ff8bb220cac6f751f2ebdd3f77f1a878296247bcd17dabbdb",
}


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def pin_sources():
    mutations = 0
    for name, expected in TARGET_HASHES.items():
        data = (TARGET / name).read_bytes()
        need(sha256(data).hexdigest() == expected, f"target source drift: {name}")
        need(sha256(data + b"independent-review-mutation").hexdigest() != expected,
             f"mutation accepted: {name}")
        mutations += 1
    inputs = json.loads((TARGET / "INPUTS.json").read_text())["files"]
    for relative, expected in inputs.items():
        need(sha256((TARGET / relative).read_bytes()).hexdigest() == expected,
             f"dependency drift: {relative}")
    return {
        "target_files": len(TARGET_HASHES),
        "dependency_files": len(inputs),
        "mutations_rejected": mutations,
    }


V = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
LABELS = tuple([("core", i) for i in range(4)] +
               [("flap", i, j) for i in range(4) for j in range(4) if i != j])
LABEL_INDEX = {label: index for index, label in enumerate(LABELS)}


def sites():
    source = [tuple(F(a, 2) for a in v) for v in V]
    target = [tuple(F(63 * a, 128) for a in v) for v in V]
    for i in range(4):
        for j in range(4):
            if i != j:
                source.append(tuple(F(V[j][k] - 2 * V[i][k], 2) for k in range(3)))
                target.append(tuple(F(63 * (V[j][k] + 2 * V[i][k]), 128)
                                    for k in range(3)))
    return tuple(source), tuple(target)


def apply_matrix(matrix, vector):
    return tuple(sum(F(a) * b for a, b in zip(row, vector)) for row in matrix)


def tetrahedral_group():
    group = []
    for perm in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            if signs[0] * signs[1] * signs[2] != 1:
                continue
            matrix = tuple(tuple(signs[row] * int(perm[row] == col)
                                 for col in range(3)) for row in range(3))
            images = tuple(apply_matrix(matrix, v) for v in V)
            need(set(images) == set(V), "matrix does not preserve the tetrahedron")
            sigma = tuple(V.index(image) for image in images)
            group.append((matrix, sigma))
    need(len(group) == 24 and len({sigma for _, sigma in group}) == 24,
         "wrong tetrahedral group order")
    return tuple(group)


def mapped_label(label, sigma):
    if label[0] == "core":
        return ("core", sigma[label[1]])
    return ("flap", sigma[label[1]], sigma[label[2]])


def symmetry_controls():
    source, target = sites()
    group = tetrahedral_group()
    for endpoint in (source, target):
        for matrix, sigma in group:
            for index, label in enumerate(LABELS):
                image = LABEL_INDEX[mapped_label(label, sigma)]
                need(apply_matrix(matrix, endpoint[index]) == endpoint[image],
                     "site/label equivariance failed")
    core_orbit = {LABEL_INDEX[mapped_label(LABELS[0], sigma)] for _, sigma in group}
    flap_orbit = {LABEL_INDEX[mapped_label(LABELS[4], sigma)] for _, sigma in group}
    need(core_orbit == set(range(4)), "core action is not transitive")
    need(flap_orbit == set(range(4, 16)), "flap action is not transitive")

    # An exact radial rational kernel on an invariant cube independently tests
    # that asymmetric prior vertices reduce to one curve per label orbit.
    points = tuple(product(range(-4, 5), repeat=3))
    kernels = []
    for endpoint in (source, target):
        table = []
        for point in points:
            z = tuple(F(a, 2) for a in point)
            table.append(tuple(1 / (1 + sum((a - b) ** 2 for a, b in zip(z, site)))
                               for site in endpoint))
        kernels.append(tuple(table))
    p0 = tuple(F(1, 16) for _ in range(16))
    vertices = []
    reflected = []
    for chosen in range(16):
        p = tuple(F(31 if i == chosen else 15, 256) for i in range(16))
        q = tuple(2 * p0[i] - p[i] for i in range(16))
        vertices.append(p)
        reflected.append(q)
        need(sum(p) == sum(q) == 1 and min(q) == F(1, 256), "bad reflected prior")

    def hinge_profile(weights, table, threshold):
        return sum(max(sum(w * a for w, a in zip(weights, row)) - threshold, 0)
                   for row in table)

    comparisons = 0
    for threshold in (F(0), F(1, 64), F(1, 16), F(1, 8), F(1, 4)):
        reference = hinge_profile(p0, kernels[1], threshold)
        curves = []
        for i in range(16):
            curves.append(hinge_profile(vertices[i], kernels[0], threshold) +
                          hinge_profile(reflected[i], kernels[1], threshold) -
                          2 * reference)
        need(len(set(curves[:4])) == 1, "core curves do not agree")
        need(len(set(curves[4:])) == 1, "flap curves do not agree")
        comparisons += 16
    return {
        "group_order": len(group),
        "core_orbit": len(core_orbit),
        "flap_orbit": len(flap_orbit),
        "invariant_cube_sites": len(points),
        "exact_curve_comparisons": comparisons,
    }


def normalized_rows(seed, modulus, bins=7):
    rows = []
    for label in range(16):
        raw = [((seed + 11 * label + 7 * j) ** 2 + 3 * label + j) % modulus + 1
               for j in range(bins)]
        total = sum(raw)
        rows.append(tuple(F(value, total) for value in raw))
    return tuple(rows)


def mix(weights, rows):
    return tuple(sum(w * row[j] for w, row in zip(weights, rows))
                 for j in range(len(rows[0])))


def hinge(values, threshold):
    return sum(max(value - threshold, 0) for value in values)


def supporting_plane_controls():
    p0 = tuple(F(1, 16) for _ in range(16))
    vertices = [tuple(F(31 if i == chosen else 15, 256) for i in range(16))
                for chosen in range(16)]
    reflected = [tuple(2 * p0[i] - p[i] for i in range(16)) for p in vertices]
    barycentric = tuple(compositions(2, 16))
    checks = 0
    digest = sha256()
    for seed in range(4):
        source = normalized_rows(seed + 2, 47)
        target = normalized_rows(seed + 13, 53)
        for threshold in (F(k, 24) for k in range(13)):
            G0 = hinge(mix(p0, target), threshold)
            certificates = [hinge(mix(p, source), threshold) +
                            hinge(mix(q, target), threshold) - 2 * G0
                            for p, q in zip(vertices, reflected)]
            maximum = max(certificates)
            for counts in barycentric:
                p = tuple(F(15, 256) + F(counts[i], 32) for i in range(16))
                gap = hinge(mix(p, source), threshold) - hinge(mix(p, target), threshold)
                average = sum(F(counts[i], 2) * certificates[i] for i in range(16))
                need(gap <= average <= maximum, "supporting-plane bound failed")
                checks += 1
            digest.update(f"{seed}:{threshold}:{maximum}\n".encode())
    return {
        "simplex_dimension": 15,
        "barycentric_points_per_case": len(barycentric),
        "exact_inequalities": checks,
        "certificate_digest": digest.hexdigest(),
    }


def exp_neg_interval(q, terms=20):
    """Independent rational alternating-series enclosure for exp(-q)."""
    halvings = 0
    reduced = F(q)
    while reduced > F(1, 8):
        reduced /= 2
        halvings += 1
    partial = F(1)
    term = F(1)
    lower = upper = None
    for n in range(1, terms + 1):
        term *= -reduced / n
        partial += term
        if n % 2:
            lower = partial
        else:
            upper = partial
    need(lower is not None and upper is not None and 0 < lower <= upper <= 1,
         "bad exponential enclosure")
    for _ in range(halvings):
        lower, upper = lower * lower, upper * upper
    return lower, upper


def certificate_record_controls():
    record = json.loads((TARGET / "EXPECTED.json").read_text())
    need(record["status"] == "EXTENDED_TARGET_PRIOR_CELL_PASS", "bad status")
    middle = record["middle"]
    need(middle["sites"] == 241 ** 3 and middle["orbits"] == 597861,
         "middle coverage mismatch")
    need(sum(row["knots"] for row in middle["rows"]) == 2026098,
         "middle knot count mismatch")
    for row in middle["rows"]:
        need(F(row["bound"]) < -F(1, 256), "middle margin failed")
        need(F(row["peak"]) < F(9, 32), "peak margin failed")
    need({row["arg"] for row in middle["rows"]} == {"1/512", "9/32"},
         "middle endpoints not both exposed")

    bands = record["radial_bands"]
    need([band["start"] for band in bands] == ["7/2", "4", "6", "12"],
         "radial starts mismatch")
    need([band["stop"] for band in bands] == ["4", "6", "12", "64"],
         "radial stops mismatch")
    for first, second in zip(bands, bands[1:]):
        need(first["stop"] == second["start"], "radial gap")
    for band in bands:
        need(F(band["start"]) + band["windows"] * F(band["step"]) == F(band["stop"]),
             "window count mismatch")
        need(F(band["lower"]) > F(1, 2), "radial volume margin failed")
        need(band["minimum_slack"] > 0, "radial bracket slack failed")
    need(sum(band["windows"] for band in bands) == 560, "radial window total")
    need(sum(band["roots"] for band in bands) == 396168, "radial endpoint total")

    endpoints = record["endpoints"]
    tail = endpoints["tail"]
    need(F(tail["mean_support_lower"]) > F(1, 4), "support mean margin failed")
    need(F(tail["far_error_at_64"]) < F(21, 100), "far-tail error failed")
    need(F(endpoints["new_inner_exponent_upper"]) < F(49, 8), "inner ball failed")
    overlap_lower = exp_neg_interval(F(49, 8))[0]
    need(overlap_lower > F(1, 512), "threshold overlap failed")
    frontier = endpoints["frontier"]
    need(frontier["minimum_mass_units"] == 417 and frontier["free_units"] == 432,
         "lattice prior budget failed")
    need(frontier["labelled_priors"] == comb(447, 15), "lattice prior count failed")
    return {
        "middle_sites": middle["sites"],
        "middle_knots": sum(row["knots"] for row in middle["rows"]),
        "radial_windows": sum(band["windows"] for band in bands),
        "radial_endpoints": sum(band["roots"] for band in bands),
        "labelled_priors": frontier["labelled_priors"],
        "threshold_overlap_lower_2^-80_units": (overlap_lower * (1 << 80)).__floor__(),
    }


def main():
    result = {
        "status": "INDEPENDENT_EXTENDED_TARGET_PRIOR_REVIEW_PASS",
        "target_commit": TARGET_COMMIT,
        "pins": pin_sources(),
        "symmetry": symmetry_controls(),
        "supporting_plane": supporting_plane_controls(),
        "certificate_record": certificate_record_controls(),
        "trust_boundary": (
            "The full middle histogram and radial cover are replayed by the target "
            "production verifier; this independent checker audits their reduction, "
            "symmetry, exact margins, and complete record semantics."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
