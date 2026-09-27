#!/usr/bin/env python3
"""Independent exact audit of the extended-target full-prior cell.

This checker imports only the already accepted review's independent positive-
series exponential and explicit group-orbit primitives.  The new weighted
middle histograms, supporting-plane controls, and weighted radial envelopes
are implemented here and do not import the target checker.
"""

import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations, product
import json
from math import comb, exp, factorial, log
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
EPSILON = F(1, 1024)
BASE = None


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ceiling(value):
    return -((-value.numerator) // value.denominator)


def pin_and_load():
    global BASE
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed input: {relative}")
    path = HERE.parent / "gaussian_deep_flap_cell_review2" / "independent_check.py"
    spec = spec_from_file_location("accepted_deep_flap_review2", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    BASE = module
    return manifest


def simplex_and_supporting_plane_controls():
    uniform = [F(1, 16)] * 16
    vertices = []
    reflected = []
    for selected in range(16):
        vertex = [F(31 if label == selected else 15, 256)
                  for label in range(16)]
        backward = [2 * uniform[label] - vertex[label] for label in range(16)]
        require(sum(vertex) == sum(backward) == 1, "prior mass")
        require(min(vertex) == F(15, 256), "prior floor")
        require(backward[selected] == F(1, 256)
                and all(backward[label] == F(17, 256)
                        for label in range(16) if label != selected),
                "reflected prior")
        vertices.append(vertex)
        reflected.append(backward)

    # Exact finite-space hinge tests use different dimensions and data from
    # the target controls.  They test the common-subgradient inequality at
    # every denominator-eight barycentric point of four selected vertices.
    controls = 0
    chosen = [0, 2, 5, 11]

    def mixture(weights, rows):
        return [sum(weight * row[column] for weight, row in zip(weights, rows))
                for column in range(len(rows[0]))]

    def hinge(values, threshold):
        return sum(max(value - threshold, 0) for value in values)

    for seed in range(9):
        source_rows = []
        target_rows = []
        for label in range(16):
            source_raw = [((seed + 3 * label + 5 * column) ** 2 % 29) + 1
                          for column in range(7)]
            target_raw = [((2 * seed + 7 * label + 4 * column) ** 2 % 31) + 1
                          for column in range(7)]
            source_rows.append([F(value, sum(source_raw)) for value in source_raw])
            target_rows.append([F(value, sum(target_raw)) for value in target_raw])
        for threshold in [F(k, 20) for k in range(16)]:
            target_at_uniform = hinge(mixture(uniform, target_rows), threshold)
            bounds = []
            for index in chosen:
                bounds.append(
                    hinge(mixture(vertices[index], source_rows), threshold)
                    + hinge(mixture(reflected[index], target_rows), threshold)
                    - 2 * target_at_uniform
                )
            for a in range(9):
                for b in range(9 - a):
                    for c in range(9 - a - b):
                        coefficients = [F(a, 8), F(b, 8), F(c, 8),
                                        F(8 - a - b - c, 8)]
                        prior = [sum(coefficient * vertices[index][label]
                                     for coefficient, index in zip(coefficients, chosen))
                                 for label in range(16)]
                        adverse = (hinge(mixture(prior, source_rows), threshold)
                                   - hinge(mixture(prior, target_rows), threshold))
                        require(adverse <= sum(coefficient * bound
                                               for coefficient, bound
                                               in zip(coefficients, bounds)),
                                "supporting-plane inequality")
                        controls += 1

    # Independently reconstruct the 24 transformations and their induced
    # action on all labels.  Both X and Y must give the same label map.
    maps = []
    for permutation in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            if signs[0] * signs[1] * signs[2] != 1:
                continue
            def transform(point):
                return tuple(signs[k] * point[permutation[k]] for k in range(3))
            xmap = tuple(BASE.X.index(transform(point)) for point in BASE.X)
            ymap = tuple(BASE.Y.index(transform(point)) for point in BASE.Y)
            require(xmap == ymap, "source/target label covariance")
            maps.append(xmap)
    require(len(set(maps)) == 24, "tetrahedral transformation count")
    require({mapping[0] for mapping in maps} == set(range(4)), "core transitivity")
    require({mapping[4] for mapping in maps} == set(range(4, 16)),
            "flap transitivity")
    return {
        "simplex_vertices": 16,
        "supporting_plane_controls": controls,
        "tetrahedral_transformations": 24,
        "label_orbits": [4, 12],
    }


def weighted_middle_histograms(step, half_grid, bits):
    scale = 1 << bits
    denominator = 256 * scale * scale
    coordinates = sorted({coordinate for centre in BASE.X + BASE.Y
                          for coordinate in centre})
    tables = {
        coordinate: [BASE.exp_neg_fraction(
            (step * index - coordinate) ** 2 / 2, bits)
            for index in range(-half_grid, half_grid + 1)]
        for coordinate in coordinates
    }
    source_atoms = [[tables[value] for value in centre] for centre in BASE.X]
    target_atoms = [[tables[value] for value in centre] for centre in BASE.Y]
    histograms = [Counter(), Counter()]
    peaks = [0, 0]
    stream = sha256()
    representatives = total = 0
    for point, multiplicity in BASE.group_orbits(half_grid):
        indices = tuple(value + half_grid for value in point)
        source_upper = [
            atom[0][indices[0]][1] * atom[1][indices[1]][1]
            * atom[2][indices[2]][1] for atom in source_atoms
        ]
        target_lower = [
            atom[0][indices[0]][0] * atom[1][indices[1]][0]
            * atom[2][indices[2]][0] for atom in target_atoms
        ]
        target_upper = [
            atom[0][indices[0]][1] * atom[1][indices[1]][1]
            * atom[2][indices[2]][1] for atom in target_atoms
        ]
        sx = sum(source_upper)
        yl = sum(target_lower)
        yu = sum(target_upper)
        reference_target = yl // (16 * scale * scale)
        for kind, labels in enumerate((range(4), range(4, 16))):
            for label in labels:
                source = ceiling(F(15 * sx + 16 * source_upper[label], denominator))
                backward_target = ceiling(F(
                    17 * yu - 16 * target_upper[label], denominator))
                histograms[kind][source] += multiplicity
                histograms[kind][backward_target] += multiplicity
                histograms[kind][reference_target] -= 2 * multiplicity
                peaks[kind] = max(peaks[kind], source)
                stream.update(
                    f"{kind}:{point}:{multiplicity}:{source}:"
                    f"{backward_target}:{reference_target}\n".encode()
                )
        representatives += 1
        total += multiplicity
    require(total == (2 * half_grid + 1) ** 3, "middle lattice coverage")
    return histograms, peaks, representatives, stream.hexdigest()


def direct_fixed_label_histogram(step, half_grid, bits, label):
    scale = 1 << bits
    denominator = 256 * scale * scale
    coordinates = sorted({coordinate for centre in BASE.X + BASE.Y
                          for coordinate in centre})
    tables = {
        coordinate: [BASE.exp_neg_fraction(
            (step * index - coordinate) ** 2 / 2, bits)
            for index in range(-half_grid, half_grid + 1)]
        for coordinate in coordinates
    }
    source_atoms = [[tables[value] for value in centre] for centre in BASE.X]
    target_atoms = [[tables[value] for value in centre] for centre in BASE.Y]
    histogram = Counter()
    peak = 0
    for point in product(range(-half_grid, half_grid + 1), repeat=3):
        indices = tuple(value + half_grid for value in point)
        source_upper = [
            atom[0][indices[0]][1] * atom[1][indices[1]][1]
            * atom[2][indices[2]][1] for atom in source_atoms
        ]
        target_lower = [
            atom[0][indices[0]][0] * atom[1][indices[1]][0]
            * atom[2][indices[2]][0] for atom in target_atoms
        ]
        target_upper = [
            atom[0][indices[0]][1] * atom[1][indices[1]][1]
            * atom[2][indices[2]][1] for atom in target_atoms
        ]
        source = ceiling(F(15 * sum(source_upper) + 16 * source_upper[label],
                           denominator))
        backward_target = ceiling(F(
            17 * sum(target_upper) - 16 * target_upper[label], denominator))
        reference_target = sum(target_lower) // (16 * scale * scale)
        histogram[source] += 1
        histogram[backward_target] += 1
        histogram[reference_target] -= 2
        peak = max(peak, source)
    return histogram, peak


def signed_window_max(histogram, left, right):
    require(left < right, "nonempty middle window")
    candidates = sorted({left, right} | {
        value for value in histogram if left < value < right
    })
    items = sorted(histogram.items())
    total_count = sum(count for _, count in items)
    total_sum = sum(value * count for value, count in items)
    require(total_count == 0, "signed histogram coefficient sum")
    below_count = below_sum = index = 0
    best = argmax = None
    for threshold in candidates:
        while index < len(items) and items[index][0] <= threshold:
            value, count = items[index]
            below_count += count
            below_sum += value * count
            index += 1
        hinge = total_sum - below_sum + threshold * below_count
        if best is None or hinge > best:
            best, argmax = hinge, threshold
    return best, argmax, len(candidates)


def middle_audit(progress=False):
    control_histograms, control_peaks, _, _ = weighted_middle_histograms(
        F(1, 3), 2, 42)
    for kind, (label, orbit_size) in enumerate(((0, 4), (4, 12))):
        direct_histogram, direct_peak = direct_fixed_label_histogram(
            F(1, 3), 2, 42, label)
        require(control_histograms[kind]
                == Counter({value: orbit_size * count
                            for value, count in direct_histogram.items()}),
                "label-averaged orbit histogram")
        require(control_peaks[kind] == direct_peak, "orbit source peak")

    step, half_grid, bits = F(1, 16), 120, 54
    histograms, peaks, representatives, digest = weighted_middle_histograms(
        step, half_grid, bits)
    scale = 1 << bits
    gaussian_low, gaussian_high = BASE.gaussian_constant_bounds(104)
    growth = 1 + step ** 2 / 8
    one_hinge_quadrature = step ** 2 * (1 + growth + growth ** 2) / 8
    tail = (3 * growth ** 2
            * F(BASE.exp_neg_fraction(F(18), 96)[1], 1 << 96) / 6)
    rows = []
    for kind, orbit_size in enumerate((4, 12)):
        maximum, argmax, candidates = signed_window_max(
            histograms[kind], F(scale, 512), F(9 * scale, 32))
        discrete = (F(maximum, scale * orbit_size) * step ** 3
                    * (gaussian_low if maximum < 0 else gaussian_high))
        final_upper = discrete + 4 * one_hinge_quadrature + 2 * tail + EPSILON
        peak = F(peaks[kind], scale) + 3 * step ** 2 / 8 + F(61, 100) * EPSILON
        require(final_upper < -F(1, 256), "weighted middle margin")
        require(peak < F(9, 32), "weighted source peak")
        rows.append({
            "type": ("core", "flap")[kind],
            "candidate_thresholds": candidates,
            "polygon_maximum_units": str(maximum),
            "argmax_over_C": str(F(argmax, scale)),
            "discrete_adverse_upper": str(discrete),
            "final_adverse_upper": str(final_upper),
            "source_peak_upper": str(peak),
        })
    require(F(BASE.exp_neg_fraction(F(18), 96)[1], 1 << 96)
            < min(F(peak, scale) for peak in peaks), "outside-cube peak")
    if progress:
        print("independent middle complete", flush=True)
    return {
        "precision_bits": bits,
        "sites": (2 * half_grid + 1) ** 3,
        "explicit_group_orbits": representatives,
        "stream_sha256": digest,
        "small_unquotiented_sites_per_type": 125,
        "quadrature_four_hinges": str(4 * one_hinge_quadrature),
        "positive_omitted_tail_two_hinges": str(2 * tail),
        "rows": rows,
    }


def weighted_root_proposal(threshold_s, record, source_lower):
    dots, norms = record
    terms = [(dot / BASE.Q, norm / (2 * BASE.Q))
             for dot, norm in zip(dots, norms)]
    threshold = float(threshold_s) ** 2 / 2
    low, high = 2.25, float(threshold_s) + 4
    for _ in range(38):
        radius = (low + high) / 2
        exponents = [threshold - radius * radius / 2 + radius * dot - norm
                     for dot, norm in terms]
        largest = max(exponents)
        scaled = [exp(value - largest) for value in exponents]
        scaled_total = (15 * sum(scaled)
                        + (0 if source_lower else 16 * max(scaled)))
        if largest + log(scaled_total) > log(256):
            low = radius
        else:
            high = radius
    return (int(low * BASE.ROOT_Q) - 10 if source_lower
            else ceiling(F.from_float(high) * BASE.ROOT_Q) + 10)


def check_weighted_root(threshold_s, record, root, source_lower):
    require(root > F(9, 4) * BASE.ROOT_Q, "root below monotone region")
    dots, norms = record
    threshold_units = threshold_s ** 2 / 2 * (1 << BASE.EXP_POWER)
    require(threshold_units.denominator == 1, "threshold fixed-point scale")
    base = int(threshold_units) - root * root * (1 << (BASE.D - BASE.ROOT_BITS))
    values = []
    for dot, norm in zip(dots, norms):
        exponent = base + 2 * root * dot - norm * (1 << BASE.ROOT_BITS)
        low, high = BASE.exp_signed_dyadic(exponent)
        values.append(low if source_lower else high)
    total = 15 * sum(values) + (0 if source_lower else 16 * max(values))
    slack = total - 256 * BASE.EXP_Q if source_lower else 256 * BASE.EXP_Q - total
    require(slack > 0, "weighted radial root was not certified")
    return slack


def weighted_radial_band(n, step, start, stop, progress=False):
    patches = BASE.make_patches(n)
    windows = int((stop - start) / step)
    require(start + windows * step == stop, "radial window coverage")
    previous_source = None
    minimum_volume = minimum_s = minimum_slack = None
    stream = sha256()
    began = time.monotonic()
    for index in range(windows + 1):
        threshold_s = start + index * step
        source_roots = []
        target_roots = []
        for patch in patches:
            source = weighted_root_proposal(threshold_s, patch["source"], True)
            target = weighted_root_proposal(threshold_s, patch["target"], False)
            for record, root, lower in ((patch["source"], source, True),
                                        (patch["target"], target, False)):
                slack = check_weighted_root(threshold_s, record, root, lower)
                minimum_slack = slack if minimum_slack is None else min(
                    minimum_slack, slack)
            source_roots.append(source)
            target_roots.append(target)
            stream.update(
                f"{index}:{patch['index']}:{source}:{target}\n".encode())
        if previous_source is not None:
            volume = F(0)
            for patch, source, target in zip(
                    patches, previous_source, target_roots):
                difference = F(source ** 3 - target ** 3, BASE.ROOT_Q ** 3)
                jacobian = (patch["jacobian_low"] if difference >= 0
                            else patch["jacobian_high"])
                volume += 8 * patch["area"] * jacobian * difference
            require(volume > F(1, 2), "weighted radial volume margin")
            if minimum_volume is None or volume < minimum_volume:
                minimum_volume, minimum_s = volume, threshold_s - step
        previous_source = source_roots
        if progress and index % 40 == 0:
            print(f"independent radial n={n} row={index}/{windows} "
                  f"seconds={time.monotonic() - began:.1f}", flush=True)
    return {
        "n": n,
        "start": str(start),
        "stop": str(stop),
        "step": str(step),
        "patches": len(patches),
        "windows": windows,
        "verified_roots": 2 * (windows + 1) * len(patches),
        "minimum_relative_slack_units": minimum_slack,
        "volume_lower": str(minimum_volume),
        "worst_S": str(minimum_s),
        "stream_sha256": stream.hexdigest(),
    }


def analytic_controls():
    inherited_tail = BASE.analytic_tail_audit()
    inner = F(141, 32) + F(9, 2) * EPSILON + EPSILON ** 2 / 2
    weighted_inner = inner + F(1, 15)
    require(weighted_inner < F(49, 8), "weighted inner ball")
    require(sum(F(3) ** power / factorial(power) for power in range(6))
            > F(256, 15), "minimum-mass logarithm")
    require(comb(447, 15) == 3427492026504451783224489079,
            "lattice prior count")
    require(ceiling(F(7104 * 15, 256)) == 417
            and 7104 - 16 * 417 == 432, "lattice prior floor")
    # A component-box displacement is at most sqrt(3)/2048 < 1/1024.
    require(F(3, 2048 ** 2) < EPSILON ** 2, "Euclidean displacement")
    return {
        "inherited_tail": inherited_tail,
        "inner_exponent_upper": str(inner),
        "weighted_inner_exponent_upper": str(weighted_inner),
        "minimum_mass": "15/256",
        "log_inverse_minimum_mass_upper": "3",
        "lattice_prior_count": comb(447, 15),
        "minimum_mass_units": 417,
        "free_units": 432,
        "diffuse_adverse_transfer": "1/1024",
    }


def rejected_weighted_radial_mutations():
    patch = BASE.make_patches(12)[0]
    rejected = 0
    for record, source_lower, direction in (
            (patch["source"], True, 1),
            (patch["target"], False, -1)):
        root = weighted_root_proposal(F(6), record, source_lower)
        root += direction * BASE.ROOT_Q // 4
        try:
            check_weighted_root(F(6), record, root, source_lower)
        except AssertionError:
            rejected += 1
    require(rejected == 2, "weighted radial mutation rejection")
    return rejected


def audit(progress=False):
    manifest = pin_and_load()
    supporting = simplex_and_supporting_plane_controls()
    analytic = analytic_controls()
    rejected = rejected_weighted_radial_mutations()
    middle = middle_audit(progress)
    radial = [
        weighted_radial_band(48, F(1, 32), F(7, 2), F(4), progress),
        weighted_radial_band(32, F(1, 16), F(4), F(6), progress),
        weighted_radial_band(24, F(1, 16), F(6), F(12), progress),
        weighted_radial_band(12, F(1, 8), F(12), F(64), progress),
    ]
    require(sum(row["verified_roots"] for row in radial) == 396168,
            "weighted radial endpoint count")
    return {
        "status": "INDEPENDENT_EXTENDED_TARGET_PRIOR_CELL_REVIEW_PASS",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_files": len(manifest["files"]),
        "method": ("accepted independent positive-series exponentials; explicit "
                   "24-transformation orbits; new high-precision weighted replay"),
        "supporting_plane": supporting,
        "analytic": analytic,
        "rejected_weighted_radial_mutations": rejected,
        "middle": middle,
        "radial_bands": radial,
        "total_verified_radial_endpoints": 396168,
        "verdict": ("accept the stated variance-one all-threshold 105-parameter "
                    "cell; unrestricted and all-variance majorisation remain open"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=HERE / "REVIEW_EXPECTED.json")
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    result = audit(args.progress)
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.emit:
        args.expected.write_text(raw)
    else:
        require(result == json.loads(args.expected.read_text()),
                "review record differs")
    print(result["status"])
    print("record_sha256", sha256(raw.encode()).hexdigest())


if __name__ == "__main__":
    main()
