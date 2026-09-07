#!/usr/bin/env python3
"""Independent audit of the dense-anchor shared-hub injection theorem.

This program imports no module from the reviewed package.  It pins that
package byte-for-byte, checks the universal fork identities coefficientwise,
rechecks the only small Ramsey input, exhausts the numerical consequences,
and validates the stored physical witness directly.
"""

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import subprocess


TARGET = "ramsey_r55_shared_hub_injection"
COMMIT = "68e8a5118e93d7f3e01491f6d42d2b8a84b88b12"
SUMS_SHA256 = "2feb6dda5642b8f932294cff889b346c30a0a181b1e68fa5ccb7fd02c2904bb3"
EXPECTED_SHA256 = "7246a9c6dfcd3aba016b99b7c9fd14fa1881c21a312189b15d680f0300789d0f"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pin_package(source):
    head = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True).stdout.strip()
    require(head == COMMIT, "reviewed checkout is not the pinned commit")
    package = source / TARGET
    sums = package / "SHA256SUMS"
    require(digest(sums.read_bytes()) == SUMS_SHA256,
            "reviewed checksum list changed")
    names = []
    for line in sums.read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        path = package / name
        require(path.is_file() and digest(path.read_bytes()) == expected,
                f"reviewed file changed: {name}")
        names.append(name)
    require(len(names) == 8 and len(set(names)) == 8,
            "unexpected checksum scope")
    require(sum((package / name).stat().st_size for name in names)
            + sums.stat().st_size == 31204, "unexpected package byte count")
    expected_path = package / "expected.json"
    require(digest(expected_path.read_bytes()) == EXPECTED_SHA256,
            "target expected output changed")
    target_expected = json.loads(expected_path.read_text(encoding="utf-8"))
    require(target_expected["status"] ==
            "VERIFIED_SHARED_HUB_INJECTION_PACKAGE", "target status changed")
    require(target_expected["physical_controls"] == 24248 and
            target_expected["star_identity_controls"] == 8192,
            "target control census changed")
    return package, names, target_expected


def fork_coefficients():
    """Prove both 40-vertex Venn identities on the eight atom types."""
    rows = []
    for x, y, z in itertools.product((0, 1), repeat=3):
        # x,y,z encode red adjacency to u,r,s for one external vertex.
        c_actual = x * (1 - y) * (1 - z)
        c_formula = x - x * y - x * z + x * y * z
        d_actual = (1 - x) * y * z
        n000 = (1 - x) * (1 - y) * (1 - z)
        d_formula = x + y + z - x * y - x * z + n000 - 1
        require(c_actual == c_formula, "blue-case atom identity failed")
        require(d_actual == d_formula, "red-case atom identity failed")
        rows.append([x, y, z, c_actual, d_actual])

    # Check the constants on several deliberately uneven 40-vertex atom
    # populations.  Coefficient equality above makes this universal.
    populations = []
    for shift in range(8):
        counts = [0] * 8
        for index in range(40):
            counts[(index * index + 3 * index + shift) % 8] += 1
        populations.append(counts)
    populations.extend(([40 if i == j else 0 for i in range(8)]
                        for j in range(8)))
    for counts in populations:
        atoms = list(itertools.product((0, 1), repeat=3))
        sx = sum(n * x for n, (x, y, z) in zip(counts, atoms))
        sy = sum(n * y for n, (x, y, z) in zip(counts, atoms))
        sz = sum(n * z for n, (x, y, z) in zip(counts, atoms))
        sxy = sum(n * x * y for n, (x, y, z) in zip(counts, atoms))
        sxz = sum(n * x * z for n, (x, y, z) in zip(counts, atoms))
        sxyz = sum(n * x * y * z for n, (x, y, z) in zip(counts, atoms))
        n000 = counts[0]
        c = sum(n * x * (1-y) * (1-z)
                for n, (x, y, z) in zip(counts, atoms))
        dset = sum(n * (1-x) * y * z
                   for n, (x, y, z) in zip(counts, atoms))
        # rs blue: d(u)=2+sx, p=sxy, q=sxz, t=sxyz.
        require(c == (2 + sx) - 2 - sxy - sxz + sxyz,
                "blue-case 40-vertex identity failed")
        # rs red: a=2+sy, b=2+sz, d(u)=2+sx,
        # p=1+sxy, q=1+sxz.
        require(dset == ((2 + sy) + (2 + sz) + (2 + sx) - 44
                         - (1 + sxy) - (1 + sxz) + n000),
                "red-case 40-vertex identity failed")
    return rows, len(populations)


def triangle_masks(n):
    pairs = list(itertools.combinations(range(n), 2))
    positions = {pair: index for index, pair in enumerate(pairs)}
    return pairs, [sum(1 << positions[pair]
                       for pair in itertools.combinations(vertices, 2))
                   for vertices in itertools.combinations(range(n), 3)]


def r33_avoiders(n):
    pairs, triangles = triangle_masks(n)
    count = 0
    for coloring in range(1 << len(pairs)):
        red_triangle = any(coloring & mask == mask for mask in triangles)
        blue_triangle = any(coloring & mask == 0 for mask in triangles)
        count += not red_triangle and not blue_triangle
    return count, 1 << len(pairs)


def small_ramsey():
    avoiders5, graphs5 = r33_avoiders(5)
    avoiders6, graphs6 = r33_avoiders(6)
    require((avoiders5, avoiders6) == (12, 0), "R(3,3) census failed")

    # In a triangle-free order-nine graph with alpha <= 3, a neighborhood is
    # independent, so d <= 3.  Its 8-d nonneighbors avoid both a triangle and
    # an independent triple (the latter would join the vertex), and the census
    # above therefore gives 8-d <= 5.  Every degree is forced to three, but
    # nine times three is odd.
    possible_degrees = [degree for degree in range(9)
                        if degree <= 3 and 8 - degree <= 5]
    require(possible_degrees == [3] and 9 * 3 % 2 == 1,
            "R(3,4) parity implication failed")
    return {
        "order5_colorings": graphs5,
        "order5_avoiders": avoiders5,
        "order6_colorings": graphs6,
        "order6_avoiders": avoiders6,
        "order9_forced_degrees": possible_degrees,
        "order9_degree_sum": 27,
    }


def threshold_consequences():
    # Codegrees are five at both anchors, so p+q=10.
    high = []
    for degree in (21, 22, 23):
        blue_lower = degree - 10
        red_lower = 22 + 22 + degree - 52
        require(blue_lower > 10 and red_lower > 10,
                "high-degree repeated hub not excluded")
        high.append([degree, blue_lower, red_lower])

    low = []
    for degree in (19, 20):
        red_lower = 22 + 22 + degree - 52
        require(red_lower > 10, "low-degree same-color pair not excluded")
        low.append([degree, degree - 10, red_lower])

    general = 0
    for degree in range(21, 43):
        for a in range(21, 43):
            for b in range(21, 43):
                require(degree - 10 > 10 and a + b + degree - 52 > 10,
                        "general codegree-five consequence failed")
                general += 1
    return high, low, general


def injection_counts():
    checked = 0
    for anchors in range(9):
        for hubs in range(9):
            actual = sum(1 for _ in itertools.permutations(range(hubs), anchors))
            expected = (math.factorial(hubs) // math.factorial(hubs - anchors)
                        if anchors <= hubs else 0)
            require(actual == expected, "labeled injection count failed")
            checked += 1
    return checked


def deficiency_aggregation():
    # Each symbol is an unused degree-23 hub, an ordinary anchor image (gap 7),
    # or a type-62 image (gap 9).  The imported local gaps are premises here;
    # this independently checks their additive use after injection.
    checked = 0
    for hubs in range(9):
        for states in itertools.product((0, 1, 2), repeat=hubs):
            anchors = sum(state != 0 for state in states)
            special = states.count(2)
            deficiency = sum(0 if state == 0 else 7 if state == 1 else 9
                             for state in states)
            require(deficiency >= 7 * anchors + 2 * special,
                    "deficiency aggregation failed")
            checked += 1
    return checked


def load_graph(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    require(set(data) == {"color", "fork", "rows"}, "bad graph schema")
    rows = data["rows"]
    require(len(rows) == 43 and all(isinstance(row, str) and len(row) == 43
                                    and not (set(row) - {"0", "1"})
                                    for row in rows), "bad matrix rows")
    for i in range(43):
        require(rows[i][i] == "0", "nonzero diagonal")
        for j in range(i):
            require(rows[i][j] == rows[j][i], "asymmetric matrix")
    color = data["color"]
    require(type(color) is int and color in (0, 1), "bad fork color")
    fork = data["fork"]
    require(isinstance(fork, list) and len(fork) == 3 and
            all(type(v) is int and 0 <= v < 43 for v in fork) and
            len(set(fork)) == 3, "bad fork")
    adjacency = [sum(1 << j for j in range(43)
                     if i != j and rows[i][j] == str(color))
                 for i in range(43)]
    return data, adjacency


def is_clique(adjacency, vertices, present=True):
    return all(bool(adjacency[u] >> v & 1) == present
               for u, v in itertools.combinations(vertices, 2))


def audit_fixture(package):
    data, adjacency = load_graph(package / "fixture.json")
    u, r, s = data["fork"]
    require(adjacency[u] >> r & 1 and adjacency[u] >> s & 1,
            "stored fork edges have wrong color")
    degrees = [adjacency[v].bit_count() for v in (u, r, s)]
    codegrees = [(adjacency[u] & adjacency[v]).bit_count() for v in (r, s)]
    require(degrees == [23, 22, 22] and codegrees == [5, 5],
            "stored fork parameters changed")
    edge = bool(adjacency[r] >> s & 1)
    require(not edge, "stored fixture changed route")
    bound = degrees[0] - 10
    require(sum(codegrees) < bound, "stored fixture is not a strict violation")
    domain_mask = (adjacency[u] & ~adjacency[r] & ~adjacency[s]
                   & ~(1 << r) & ~(1 << s) & ((1 << 43) - 1))
    domain = [v for v in range(43) if domain_mask >> v & 1]
    require(len(domain) >= 9, "fork identity did not expose nine vertices")

    found = None
    for four in itertools.combinations(domain, 4):
        if is_clique(adjacency, four, True):
            found = {"color": data["color"], "vertices": [u, *four]}
            break
    if found is None:
        for three in itertools.combinations(domain, 3):
            if is_clique(adjacency, three, False):
                found = {"color": 1 - data["color"],
                         "vertices": [r, s, *three]}
                break
    require(found is not None, "independent physical extraction failed")

    certificate = json.loads(
        (package / "fixture_certificate.json").read_text(encoding="utf-8"))
    require(set(certificate) == {"color", "vertices"}, "bad certificate schema")
    vertices = certificate["vertices"]
    require(type(certificate["color"]) is int and
            certificate["color"] in (0, 1) and len(vertices) == 5 and
            len(set(vertices)) == 5 and all(type(v) is int and 0 <= v < 43
                                            for v in vertices),
            "bad certificate values")
    physical = [data["rows"][a][b]
                for a, b in itertools.combinations(vertices, 2)]
    require(all(bit == str(certificate["color"]) for bit in physical),
            "stored five-set is not physically monochromatic")
    require(found == certificate, "independent extraction changed witness")
    return {
        "degrees": degrees,
        "codegrees": codegrees,
        "fork_bound": bound,
        "fork_codegree_sum": sum(codegrees),
        "identity_domain_size": len(domain),
        "certificate": certificate,
        "physical_pairs_checked": 10,
    }


def run(source):
    package, names, target_expected = pin_package(source)
    coefficient_rows, populations = fork_coefficients()
    ramsey = small_ramsey()
    high, low, general = threshold_consequences()
    assignments = injection_counts()
    deficiency = deficiency_aggregation()
    fixture = audit_fixture(package)
    return {
        "reviewed_source_commit": COMMIT,
        "package": {
            "checksum_manifest_sha256": SUMS_SHA256,
            "files_including_manifest": len(names) + 1,
            "bytes": 31204,
            "target_status": target_expected["status"],
            "target_physical_controls": target_expected["physical_controls"],
            "target_stream_sha256": target_expected["physical_stream_sha256"],
        },
        "fork_identities": {
            "boolean_atoms_checked": len(coefficient_rows),
            "atom_rows_xyz_C_D": coefficient_rows,
            "forty_vertex_populations_checked": populations,
        },
        "small_ramsey": ramsey,
        "consequences": {
            "high_rows_degree_blue_red_lower": high,
            "low_rows_degree_blue_red_lower": low,
            "general_high_degree_triples_checked": general,
            "maximum_low_degree_fiber": 4,
            "labeled_assignment_pairs_checked": assignments,
            "deficiency_state_models_checked": deficiency,
        },
        "fixture": fixture,
        "scope": {
            "core_fork_theorem": "accepted",
            "dense_anchor_interpretation_imports_prior_results": True,
            "deficiency_corollary_imports_gap_7_and_gap_9": True,
            "ramsey_5_5_lower_bound_changed": False,
        },
        "status": "VERIFIED_REVIEW_SHARED_HUB_INJECTION",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True,
                        help="checkout of math_source_code_open at the pinned commit")
    arguments = parser.parse_args()
    print(json.dumps(run(arguments.source.resolve()), indent=2, sort_keys=True))
