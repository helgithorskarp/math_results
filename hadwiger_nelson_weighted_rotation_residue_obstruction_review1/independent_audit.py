#!/usr/bin/env python3
"""Independent audit for the weighted-rotation residue obstruction.

No target module is imported and the target quotient certificate is not read.
The only mathematical target witness read is the positive 114-vertex source
index/colour certificate, whose geometry is reconstructed from the pinned
Parts coordinate table.
"""

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_weighted_rotation_residue_obstruction"
SOURCE_RELATIVE = Path("hadwiger_nelson_parts509_completion_census_degree9/points.tsv")
SOURCE_SHA256 = "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50"
TARGET_HASHES = {
    "PROOF.md": "cb39635256c08ec436b7e10a536c46b52f539f46dbf4e265910d77ae6652fed9",
    "auxiliary_certificate.json": "d72104cef4f003f2f3378f70b5e6c27a56b9da2775c4840c8a373178d2c95b8e",
    "direct_contacts.cpp": "a4e47509f27abfeb00b9e6cdaec13491c480854d193af976a29286d78310564d",
    "exact.py": "3d8833b6aef761e148b5b5c61fc1f3eb1aade17f9000898da80fff0df9e36802",
    "verify.py": "d1ba0249be4bc456e29194f34e72bea54338b3348722e81049c3ed0ed3bf3b85",
}
ZERO = (0, 0, 0, 0)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale(x, coefficient):
    return tuple(coefficient * a for a in x)


def subtract(x, y):
    return add(x, scale(y, -1))


def conjugate(x):
    return x[0], x[1], -x[2], -x[3]


def multiply(x, y):
    """Product in basis 1,sqrt(33),alpha,beta."""
    a, b, c, d = x
    A, B, C, D = y
    return (
        a * A + 33 * b * B - 3 * c * C - 11 * d * D,
        a * B + b * A - c * D - d * C,
        a * C + c * A + 11 * (b * D + d * B),
        a * D + d * A + 3 * (b * C + c * B),
    )


def norm(x):
    return multiply(x, conjugate(x))


def alpha_times(x):
    # alpha*(a+b sqrt33+c alpha+d beta)=(-3c,-d,a,3b).
    return -3 * x[2], -x[3], x[0], 3 * x[1]


def weighted_unit(d, r):
    """Exact definition-level test through the sqrt(13) decomposition."""
    p = add(scale(d, 3), scale(r, 5))
    q = alpha_times(subtract(r, d))
    base = add(norm(p), scale(norm(q), 13))
    cross = add(multiply(p, conjugate(q)), multiply(q, conjugate(p)))
    # d and r have denominator 12, while p/8 + sqrt(13) q/8
    # has denominator 96.
    return base == (96 * 96, 0, 0, 0) and cross == ZERO


def load_source(repository_root):
    path = repository_root / SOURCE_RELATIVE
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "Parts source hash")
    rows = [tuple(map(int, line.split())) for line in raw.decode().splitlines() if line and not line.startswith("#")]
    rows = rows[:374]
    require(len(rows) == 374 and all(len(row) == 16 for row in rows), "source shape")
    keep = (0, 5, 9, 12)
    require(all(row[i] == 0 for row in rows for i in range(16) if i not in keep), "source leaves E")
    require(all(row[i] % 8 == 0 for row in rows for i in keep), "source denominator is not 12")
    points = [tuple(row[i] // 8 for i in keep) for row in rows]
    require(len(set(points)) == 374, "source collision")
    return points, raw


def difference_counter(points):
    return Counter(subtract(a, b) for a in points for b in points)


def root33_mod(bits):
    """Lift the unique t root of 4t^2+t-2 with sqrt(33)=1+8t."""
    if bits <= 0:
        return 0
    t = 0
    modulus = 1
    for _ in range(max(0, bits - 3)):
        if (4 * t * t + t - 2) % (2 * modulus):
            t += modulus
        modulus *= 2
    answer = (1 + 8 * t) % (1 << bits)
    require((answer * answer - 33) % (1 << bits) == 0, "sqrt(33) lift")
    return answer


def local_residue(z):
    """Map an integral E element to O/4 in coordinates 1,w."""
    denominator = lcm(*(x.denominator for x in z))
    a, b, c, d = [int(x * denominator) for x in z]
    two_power = 0
    odd = denominator
    while odd % 2 == 0:
        two_power += 1
        odd //= 2
    modulus = 1 << (two_power + 2)
    root = root33_mod(two_power + 2)
    odd_inverse = pow(3 * odd, -1, modulus)
    first = (3 * a + 3 * b * root + 3 * c + d * root) * odd_inverse % modulus
    second = (6 * c + 2 * d * root) * odd_inverse % modulus
    divisor = 1 << two_power
    require(first % divisor == second % divisor == 0, "nonintegral local element")
    return (first // divisor) % 4, (second // divisor) % 4


def quotient_audit():
    elements = list(product(range(4), repeat=2))
    units = {(a, b) for a, b in elements if (a * a - a * b + b * b) % 4 == 1}
    require(units == {(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)}, "unit residues")
    vertical = {(2, 0), (0, 2), (2, 2)}
    directions = (
        {(0, 0, a, b) for a, b in units}
        | {(a, b, a, b) for a, b in units}
        | {(a, b, 0, 0) for a, b in vertical}
    )
    require(len(directions) == 15, "quotient directions")

    def colour(z):
        a, b, c, d = z
        a0, a1 = a & 1, a >> 1
        b0, b1 = b & 1, b >> 1
        c0, c1 = c & 1, c >> 1
        d0, d1 = d & 1, d >> 1
        low = a1 ^ b1 ^ c1 ^ d1 ^ b0 ^ (a0 & b0) ^ ((a0 ^ b0) & (c0 ^ d0)) ^ (c0 & d0)
        high = a1 ^ c0 ^ d0
        return low + 2 * high

    labels = list(product(range(4), repeat=4))
    edges = set()
    for z in labels:
        for direction in directions:
            other = tuple((a + b) % 4 for a, b in zip(z, direction))
            require(colour(z) != colour(other), "quotient colouring")
            edges.add(tuple(sorted((z, other))))
    require(len(edges) == 1920, "quotient edge count")
    return directions, labels, colour, {
        "quotient_vertices": len(labels),
        "quotient_directions": len(directions),
        "quotient_edges": len(edges),
    }


def load_contacts(path, differences):
    rows = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = tuple(map(int, line.split()))
        require(len(row) == 2 and all(0 <= i < len(differences) for i in row), "contact row")
        rows.append(row)
    require(len(rows) == len(set(rows)) == 78, "oriented contact count")
    require(all(weighted_unit(differences[i], differences[j]) for i, j in rows), "false contact")
    return rows


def contact_audit(points, contacts, directions, labels, colour):
    counts = difference_counter(points)
    differences = sorted(counts)
    index = {d: i for i, d in enumerate(differences)}
    rows = load_contacts(contacts, differences)
    rowset = set(rows)
    representatives = []
    for i, j in rows:
        opposite = (index[scale(differences[i], -1)], index[scale(differences[j], -1)])
        require(opposite in rowset and opposite != (i, j), "missing opposite contact")
        if (i, j) < opposite:
            representatives.append((differences[i], differences[j]))
    require(len(representatives) == 39, "unoriented contact count")

    one = (144, 0, 0, 0)
    four_thirds = (192, 0, 0, 0)
    types = Counter()
    physical_edges = 0
    reduced = set()
    for d, r in representatives:
        if d == ZERO and norm(r) == one:
            types["horizontal"] += 1
        elif r == ZERO and norm(d) == four_thirds:
            types["vertical"] += 1
        elif d == r and norm(d) == one:
            types["diagonal"] += 1
        else:
            raise ValueError("mixed contact in Parts374 support")
        rd = local_residue(tuple(F(x, 12) for x in d))
        rr = local_residue(tuple(F(x, 12) for x in r))
        residue_direction = rd + rr
        require(residue_direction in directions, "contact escapes quotient")
        reduced.add(residue_direction)
        physical_edges += counts[d] * counts[r]
    require(types == {"horizontal": 15, "vertical": 9, "diagonal": 15}, "contact types")
    require(physical_edges == 1211200, "weighted edge count")

    # Every source point itself must lie in the chosen local integer ring.
    source_residues = [local_residue(tuple(F(x, 12) for x in p)) for p in points]
    require(len(source_residues) == 374, "source residues")

    return differences, representatives, {
        "source_vertices": len(points),
        "source_differences": len(differences),
        "differences_sha256": hashlib.sha256(
            (str(len(differences)) + "\n" + "".join(" ".join(map(str, d)) + "\n" for d in differences)).encode()
        ).hexdigest(),
        "source_integral_residues": len(source_residues),
        "oriented_contacts": len(rows),
        "oriented_contacts_sha256": hashlib.sha256(contacts.read_bytes()).hexdigest(),
        "directions_up_to_sign": len(representatives),
        "direction_types": dict(sorted(types.items())),
        "reduced_directions_used": len(reduced),
        "physical_weighted_vertices": len(points) ** 2,
        "physical_unit_edges": physical_edges,
    }


def auxiliary_audit(points, representatives, certificate_path):
    cert = json.loads(certificate_path.read_text())
    ids = cert.get("source_indices")
    require(
        isinstance(ids, list)
        and len(ids) == 114
        and ids == sorted(set(ids))
        and all(isinstance(i, int) and 0 <= i < len(points) for i in ids),
        "auxiliary indices",
    )
    subset = [points[i] for i in ids]
    one = (144, 0, 0, 0)
    four_thirds = (192, 0, 0, 0)
    unit_edges = []
    extra_edges = []
    for i, j in combinations(range(114), 2):
        value = norm(subtract(subset[i], subset[j]))
        if value == one:
            unit_edges.append((i, j))
        elif value == four_thirds:
            extra_edges.append((i, j))
    edges = sorted(unit_edges + extra_edges)
    require((len(unit_edges), len(extra_edges), len(edges)) == (379, 156, 535), "auxiliary edges")

    five = cert.get("five_colouring", "")
    require(len(five) == 114 and set(five) <= set("01234"), "five-colouring word")
    require(all(five[a] != five[b] for a, b in edges), "bad five-colouring")
    deletions = cert.get("deletion_four_colourings")
    require(isinstance(deletions, list) and len(deletions) == 114, "deletion witnesses")
    for omitted, word in enumerate(deletions):
        require(len(word) == 114 and set(word) <= set("0123"), "deletion word")
        require(all(word[a] != word[b] for a, b in edges if omitted not in (a, b)), "bad deletion witness")

    clauses = [[4 * v + c + 1 for c in range(4)] for v in range(114)]
    clauses.extend([[-4 * a - c - 1, -4 * b - c - 1] for a, b in edges for c in range(4)])
    clauses.append([1])
    cnf = f"p cnf 456 {len(clauses)}\n" + "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    require(len(clauses) == 2255, "CNF clause count")

    subset_counts = difference_counter(subset)
    weighted_edges = sum(subset_counts.get(d, 0) * subset_counts.get(r, 0) for d, r in representatives)
    require(weighted_edges == 71477, "weighted auxiliary support edge count")

    return cnf, {
        "auxiliary_vertices": 114,
        "auxiliary_unit_edges": len(unit_edges),
        "auxiliary_four_thirds_edges": len(extra_edges),
        "auxiliary_edges": len(edges),
        "auxiliary_five_colouring_checked": True,
        "auxiliary_deletion_four_colourings_checked": len(deletions),
        "auxiliary_cnf_variables": 456,
        "auxiliary_cnf_clauses": len(clauses),
        "auxiliary_cnf_sha256": hashlib.sha256(cnf.encode()).hexdigest(),
        "weighted_auxiliary_vertices": len(subset) ** 2,
        "weighted_auxiliary_unit_edges": weighted_edges,
    }


def mixed_escape_audit(directions, labels, colour):
    alpha = (F(0), F(0), F(1), F(0))
    one = (F(1), F(0), F(0), F(0))
    d = scale(alpha, F(1, 15))
    r = scale(alpha, F(3, 5))
    omega = scale(subtract(alpha, one), F(1, 2))
    require(norm(omega) == one, "escape rotation")
    d = multiply(omega, d)
    r = multiply(omega, r)

    p = scale(add(scale(d, 3), scale(r, 5)), F(1, 8))
    q = scale(alpha_times(subtract(r, d)), F(1, 8))
    require(add(norm(p), scale(norm(q), 13)) == one, "escape base norm")
    require(add(multiply(p, conjugate(q)), multiply(q, conjugate(p))) == (F(0),) * 4, "escape cross term")
    residue_direction = local_residue(d) + local_residue(r)
    require(residue_direction == (2, 1, 2, 1) and residue_direction not in directions, "escape residue")
    monochromatic = 0
    for z in labels:
        other = tuple((a + b) % 4 for a, b in zip(z, residue_direction))
        require(colour(z) == colour(other), "escape does not break displayed colouring")
        monochromatic += 1
    return {
        "mixed_escape_residue": list(residue_direction),
        "mixed_escape_monochromatic_translates": monochromatic,
        "mixed_escape_is_single_unit_contact": True,
    }


def source_hash_audit(target_dir, repository_root, source_raw):
    observed = {}
    for name, expected in TARGET_HASHES.items():
        digest = hashlib.sha256((target_dir / name).read_bytes()).hexdigest()
        require(digest == expected, f"target hash: {name}")
        observed[name] = digest
    require(hashlib.sha256(source_raw).hexdigest() == SOURCE_SHA256, "source hash repeated")
    return {
        "target_files_hashed": len(observed),
        "target_sha256": observed,
        "source_table": str(SOURCE_RELATIVE),
        "source_table_sha256": SOURCE_SHA256,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-dir", type=Path, default=TARGET)
    parser.add_argument("--repository-root", type=Path, default=HERE.parent)
    parser.add_argument("--contacts", type=Path)
    parser.add_argument("--prepare", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()

    points, source_raw = load_source(args.repository_root)
    counts = difference_counter(points)
    differences = sorted(counts)
    directions, labels, colour, quotient_result = quotient_audit()
    cert_path = args.target_dir / "auxiliary_certificate.json"

    if args.prepare:
        args.prepare.mkdir(parents=True, exist_ok=False)
        difference_text = str(len(differences)) + "\n" + "".join(" ".join(map(str, d)) + "\n" for d in differences)
        (args.prepare / "differences.txt").write_text(difference_text)
        # CNF does not depend on weighted contacts, so build it with an empty
        # representative list here; its weighted-edge field is ignored.
        ids = json.loads(cert_path.read_text())["source_indices"]
        subset = [points[i] for i in ids]
        edges = []
        for i, j in combinations(range(114), 2):
            if norm(subtract(subset[i], subset[j])) in ((144, 0, 0, 0), (192, 0, 0, 0)):
                edges.append((i, j))
        clauses = [[4 * v + c + 1 for c in range(4)] for v in range(114)]
        clauses.extend([[-4 * a - c - 1, -4 * b - c - 1] for a, b in edges for c in range(4)])
        clauses.append([1])
        cnf = f"p cnf 456 {len(clauses)}\n" + "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
        (args.prepare / "auxiliary.cnf").write_text(cnf)
        print(json.dumps({
            "status": "PREPARED",
            "differences": len(differences),
            "differences_sha256": hashlib.sha256(difference_text.encode()).hexdigest(),
            "auxiliary_cnf_sha256": hashlib.sha256(cnf.encode()).hexdigest(),
        }, indent=2, sort_keys=True))
        if args.contacts is None:
            return

    require(args.contacts is not None, "--contacts is required for a complete audit")
    differences2, representatives, contact_result = contact_audit(points, args.contacts, directions, labels, colour)
    require(differences2 == differences, "difference reconstruction changed")
    cnf, auxiliary_result = auxiliary_audit(points, representatives, cert_path)
    result = {
        "status": "PASS",
        **quotient_result,
        **contact_result,
        **auxiliary_result,
        **mixed_escape_audit(directions, labels, colour),
        **source_hash_audit(args.target_dir, args.repository_root, source_raw),
        "record_improvement": False,
    }
    require(result["auxiliary_cnf_sha256"] == hashlib.sha256(cnf.encode()).hexdigest(), "CNF hash drift")
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(result == expected, "result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
