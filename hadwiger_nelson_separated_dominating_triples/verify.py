"""Independent exact audit of the separated-triple continuum ingredients."""
import argparse
import hashlib
import json
import math
import time
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


# Exact real coordinates in Q(sqrt(3)).
def radd(a, b):
    return a[0] + b[0], a[1] + b[1]


def rneg(a):
    return -a[0], -a[1]


def rmul(a, b):
    return a[0] * b[0] + 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def csub(x, y):
    return tuple(radd(a, rneg(b)) for a, b in zip(x, y))


def cmul(x, y):
    return (
        radd(rmul(x[0], y[0]), rneg(rmul(x[1], y[1]))),
        radd(rmul(x[0], y[1]), rmul(x[1], y[0])),
    )


def sqdist(x, y):
    a, b = csub(x, y)
    return radd(rmul(a, a), rmul(b, b))


def orbit_audit(section):
    one = ((Q(1), Q(0)), (Q(0), Q(0)))
    omega = ((Q(1, 2), Q(0)), (Q(0), Q(1, 2)))
    roots = [one]
    for _ in range(5):
        roots.append(cmul(roots[-1], omega))
    need(cmul(roots[-1], omega) == one and len(set(roots)) == 6, "sixth roots")
    rows = []
    for j, z in enumerate(roots):
        d = sqdist(z, one)
        need(d[1] == 0 and d[0].denominator == 1, "nonintegral chord")
        rows.append([j, j % 2, int(d[0]), 4 - int(d[0])])
    need(section["columns"] == ["step", "parity", "chord_squared", "centre_distance_squared"], "orbit columns")
    need(section["rows"] == rows, "orbit rows")

    cycle_edges = [(j, (j + 1) % 6) for j in range(6)]
    proper = [row for row in product(range(2), repeat=6) if all(row[a] != row[b] for a, b in cycle_edges)]
    need(len(proper) == 2, "C6 bipartitions")
    for j in range(6):
        need(any(row[0] == row[j] for row in proper) == (j % 2 == 0), "parity extension")

    # If two distinct unit circles meet in p,q then |p-q|^2=4-d^2.
    # Odd orbit separation is incompatible with prescribing p,q alike.
    positive_odd = sorted({row[3] for row in rows if row[1] and row[3] > 0})
    need(positive_odd == [3], "unique positive intersection exception")
    return {
        "orbit_chord_cases": 6,
        "binary_circle_assignments_checked": 64,
        "proper_circle_bipartitions": 2,
        "positive_exceptional_squared_separations": positive_odd,
    }


def central_audit(section):
    need(section["columns"] == ["type0", "type1", "second_base", "chosen0", "chosen1"], "central columns")
    expected_keys = set()
    for t0 in ("unit", "sqrt3"):
        for t1 in ("unit", "sqrt3"):
            if t0 == t1 == "unit":
                continue  # This would force |a0-a1|<=2, contrary to >3.
            first = {0} if t0 == "unit" else {0, 1}
            desired0 = 0 if t0 == "unit" else 1  # colours2 and3 as bits0 and1
            for base in range(6):
                second = {base} if t1 == "unit" else {base, (base + 1) % 6}
                desired1 = 1 if t1 == "unit" else 0
                if first & second:
                    continue  # Actual anchor sets are disjoint.
                expected_keys.add((t0, t1, base))

    got = {}
    for row in section["rows"]:
        need(len(row) == 5, "central row length")
        t0, t1, base, x, y = row
        key = (t0, t1, base)
        need(key in expected_keys and key not in got, "central row domain")
        first = {0} if t0 == "unit" else {0, 1}
        second = {base} if t1 == "unit" else {base, (base + 1) % 6}
        desired0 = 0 if t0 == "unit" else 1
        desired1 = 1 if t1 == "unit" else 0
        need(x in first and y in second, "choice outside anchor")
        need(((x - y) & 1) == (desired0 ^ desired1), "incompatible central colours")
        got[key] = (x, y)
    need(set(got) == expected_keys, "incomplete central cases")

    # Independently exhaust every candidate pair rather than trusting the rows.
    alternatives = 0
    for t0, t1, base in sorted(expected_keys):
        first = {0} if t0 == "unit" else {0, 1}
        second = {base} if t1 == "unit" else {base, (base + 1) % 6}
        desired0 = 0 if t0 == "unit" else 1
        desired1 = 1 if t1 == "unit" else 0
        valid = [(x, y) for x, y in product(first, second) if ((x - y) & 1) == (desired0 ^ desired1)]
        need(valid, "uncovered independently enumerated case")
        alternatives += len(valid)
    need(len(expected_keys) == 11, "unexpected central case count")
    return {
        "central_same_orbit_cases": len(expected_keys),
        "central_valid_endpoint_choices": alternatives,
        "different_orbit_case_is_independent": True,
        "unit_unit_case_excluded_by_triangle_inequality": True,
    }


def sharpness_audit(section):
    need(section["coordinate_scale"] == 12, "sharpness scale")
    need(section["basis"] == ["1", "sqrt3", "sqrt11", "sqrt33"], "sharpness basis")
    vertices = section["vertices"]
    need(len(vertices) == 7, "sharpness order")
    need(len({tuple(tuple(v) for v in p) for p in vertices}) == 7, "sharpness collision")
    radicals = (1, 3, 11, 33)

    def squared(a, b):
        total = dict.fromkeys(radicals, 0)
        for x, y in zip(a, b):
            delta = [s - t for s, t in zip(x, y)]
            for i, r in enumerate(radicals):
                for j, s in enumerate(radicals):
                    g = math.gcd(r, s)
                    total[r * s // (g * g)] += delta[i] * delta[j] * g
        return tuple(total[r] for r in radicals)

    edges = [list(e) for e in combinations(range(7), 2) if squared(vertices[e[0]], vertices[e[1]]) == (144, 0, 0, 0)]
    need(edges == section["edges"] and len(edges) == 11, "sharpness edge set")
    need(section["dominating_pair"] == [0, 3], "sharpness dominating pair")
    covered = {0, 3} | {v for e in edges for v in e if e[0] in (0, 3) or e[1] in (0, 3)}
    need(covered == set(range(7)), "Moser pair does not dominate")
    need(squared(vertices[0], vertices[3]) == (432, 0, 0, 0), "Moser centre distance")

    colour = section["colours"]
    need(len(colour) == 7 and all(type(x) is int and 0 <= x < 4 for x in colour), "sharpness colours")
    need(all(colour[a] != colour[b] for a, b in edges), "sharpness colouring")
    tested = 0
    for row in product(range(3), repeat=7):
        need(any(row[a] == row[b] for a, b in edges), "Moser three-colouring")
        tested += 1

    third = section["third_centre"]
    need(section["separated_pair"] == [0, "third_centre"], "separated pair label")
    need(squared(vertices[0], third) == (2304, 0, 0, 0), "separated centre distance")
    need(squared(vertices[3], third) != (0, 0, 0, 0), "third centre collision")
    return {
        "sharpness_vertices": 7,
        "sharpness_pair_norms": 21,
        "sharpness_edges": 11,
        "sharpness_dominating_pair_verified": True,
        "sharpness_three_colour_assignments_refuted": tested,
        "sharpness_separated_pair_squared_distance": 16,
        "sharpness_chromatic_number": 4,
    }


def audit(certificate):
    return {
        **orbit_audit(certificate["orbit_chords"]),
        **central_audit(certificate["central_same_orbit_choices"]),
        **sharpness_audit(certificate["sharpness"]),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", required=True)
    args = parser.parse_args()
    start = time.monotonic()
    raw = (HERE / "certificate.json").read_bytes()
    certificate = json.loads(raw)
    result = audit(certificate)

    for label in ("orbit", "central-choice", "central-coverage", "sharp-edge", "far-centre"):
        bad = json.loads(raw)
        if label == "orbit":
            bad["orbit_chords"]["rows"][1][3] = 2
        elif label == "central-choice":
            bad["central_same_orbit_choices"]["rows"][0][3] = 5
        elif label == "central-coverage":
            bad["central_same_orbit_choices"]["rows"].pop()
        elif label == "sharp-edge":
            bad["sharpness"]["edges"].pop()
        else:
            bad["sharpness"]["third_centre"][0][0] = 36
        try:
            audit(bad)
        except ValueError:
            pass
        else:
            raise ValueError("malformed certificate accepted: " + label)

    result.update(
        {
            "status": "PASS",
            "malformed_certificate_rejections": 5,
            "certificate_bytes": len(raw),
            "certificate_sha256": hashlib.sha256(raw).hexdigest(),
            "native_solver_calls": 0,
        }
    )
    if (HERE / "EXPECTED.json").exists():
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected mismatch")
    out = Path(args.work)
    out.mkdir(parents=True, exist_ok=True)
    (out / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({**result, "seconds": time.monotonic() - start}, sort_keys=True))


if __name__ == "__main__":
    main()
