"""Independent exact audit for the closed diameter-three theorem."""
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


def radd(a, b):
    return a[0] + b[0], a[1] + b[1]


def rneg(a):
    return -a[0], -a[1]


def rmul(a, b):
    return a[0] * b[0] + 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def cadd(x, y):
    return tuple(radd(a, b) for a, b in zip(x, y))


def csub(x, y):
    return cadd(x, tuple(rneg(a) for a in y))


def cmul(x, y):
    return (
        radd(rmul(x[0], y[0]), rneg(rmul(x[1], y[1]))),
        radd(rmul(x[0], y[1]), rmul(x[1], y[0])),
    )


def sqdist(x, y):
    a, b = csub(x, y)
    return radd(rmul(a, a), rmul(b, b))


def reconstruct_boundary(section):
    need(section["coordinate_map"] == "(s,t) -> (s/2,t*sqrt(3)/2)", "coordinate map")
    one = ((Q(1), Q(0)), (Q(0), Q(0)))
    omega = ((Q(1, 2), Q(0)), (Q(0), Q(1, 2)))
    roots = [one]
    for _ in range(5):
        roots.append(cmul(roots[-1], omega))
    need(cmul(roots[-1], omega) == one and len(set(roots)) == 6, "sixth-root orbit")
    shift = ((Q(3), Q(0)), (Q(0), Q(0)))
    vertices = roots + [cadd(shift, z) for z in roots]
    encoded = [((Q(s, 2), Q(0)), (Q(0), Q(t, 2))) for s, t in section["vertices"]]
    need(vertices == encoded and len(set(vertices)) == 12, "boundary vertices")
    need(section["centres"] == [[0, 0], [6, 0]], "boundary centres")
    distances = {e: sqdist(vertices[e[0]], vertices[e[1]]) for e in combinations(range(12), 2)}
    edges = [list(e) for e, value in distances.items() if value == (1, 0)]
    need(edges == section["edges"] and len(edges) == 13, "boundary edges")
    cross = [e for e in edges if e[0] < 6 <= e[1]]
    need(cross == [section["cross_edge"]] == [[0, 9]], "nonunique boundary cross edge")
    proper = [row for row in product(range(2), repeat=12) if all(row[a] != row[b] for a, b in edges)]
    need(len(proper) == 2, "boundary not connected bipartite")
    need(list(proper[0]) == section["colouring"], "boundary colouring")
    return roots, edges, proper


def orbit_audit(section, roots):
    rows = []
    for j, z in enumerate(roots):
        value = sqdist(roots[0], z)
        need(value[1] == 0 and value[0].denominator == 1, "orbit chord")
        rows.append([j, j % 2, int(value[0]), 4 - int(value[0])])
    need(section["columns"] == ["step", "parity", "chord_squared", "centre_distance_squared"], "orbit columns")
    need(section["rows"] == rows, "orbit rows")
    need(sorted({row[3] for row in rows if row[1] and row[3] > 0}) == [3], "intersection exception")
    return {"orbit_chord_cases": 6, "positive_exceptional_squared_separations": [3]}


def cases_audit(section, edges, proper):
    need(section["unit_anchor_columns"] == ["leaf", "anchor", "left_intersection", "right_intersection"], "unit columns")
    expected_unit = {(leaf, k) for leaf in range(2) for k in range(6)}
    got_unit = set()
    for leaf, k, left, right in section["unit_anchor_rows"]:
        need((leaf, k) in expected_unit and (leaf, k) not in got_unit, "unit row domain")
        cycle = [6 * leaf + j for j in range(6)]
        need(left == (k - 1) % 6 and right == (k + 1) % 6, "unit neighbours")
        rows = [r for r in proper if r[cycle[k]] == 0]
        need(rows and all(r[cycle[left]] == r[cycle[right]] == 1 for r in rows), "unit extension")
        got_unit.add((leaf, k))
    need(got_unit == expected_unit, "unit coverage")

    need(section["one_exception_columns"] == ["exceptional_leaf", "edge_base", "other_leaf_anchor_or_minus1", "chosen_endpoint"], "one-exception columns")
    expected_one = {(leaf, base, anchor) for leaf in range(2) for base in range(6) for anchor in [-1] + list(range(6))}
    got_one = set()
    one_choices = 0
    for leaf, base, anchor, choice in section["one_exception_rows"]:
        key = (leaf, base, anchor)
        need(key in expected_one and key not in got_one and choice in (0, 1), "one-exception row")
        edge = [6 * leaf + base, 6 * leaf + (base + 1) % 6]
        rows = proper if anchor < 0 else [r for r in proper if r[6 * (1 - leaf) + anchor] == 0]
        need(rows and any(r[edge[choice]] == 1 for r in rows), "one-exception choice")
        one_choices += sum(r[x] == 1 for r in rows for x in edge)
        got_one.add(key)
    need(got_one == expected_one, "one-exception coverage")

    need(section["two_exception_columns"] == ["edge0_base", "edge1_base", "chosen0", "chosen1"], "two-exception columns")
    expected_two = {(b0, b1) for b0 in range(6) for b1 in range(6)}
    got_two = set()
    for base0, base1, choice0, choice1 in section["two_exception_rows"]:
        key = (base0, base1)
        need(key in expected_two and key not in got_two and choice0 in (0, 1) and choice1 in (0, 1), "two-exception row")
        e0 = [base0, (base0 + 1) % 6]
        e1 = [6 + base1, 6 + (base1 + 1) % 6]
        need(any(r[e0[choice0]] == r[e1[choice1]] == 1 for r in proper), "two-exception choice")
        got_two.add(key)
    need(got_two == expected_two, "two-exception coverage")
    return {
        "unit_anchor_cases": len(got_unit),
        "one_exception_cases": len(got_one),
        "one_exception_positive_choices_counted": one_choices,
        "two_exception_cases": len(got_two),
    }


def sharpness_audit(section):
    need(section["coordinate_scale"] == 12 and section["basis"] == ["1", "sqrt3", "sqrt11", "sqrt33"], "sharpness field")
    vertices = section["vertices"]
    need(len(vertices) == 7 and len({tuple(tuple(v) for v in p) for p in vertices}) == 7, "sharpness vertices")
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
    need(edges == section["edges"] and len(edges) == 11, "sharpness graph")
    need(section["dominating_pair"] == [0, 3], "dominating pair")
    dominated = {0, 3} | {v for e in edges for v in e if e[0] in (0, 3) or e[1] in (0, 3)}
    need(dominated == set(range(7)), "not dominated")
    colour = section["colours"]
    need(all(colour[a] != colour[b] for a, b in edges), "sharpness four-colouring")
    tested = 0
    for row in product(range(3), repeat=7):
        need(any(row[a] == row[b] for a, b in edges), "sharpness three-colouring")
        tested += 1
    third = section["third_centre"]
    need(section["boundary_pair"] == [0, "third_centre"], "boundary pair")
    need(squared(vertices[0], third) == (1296, 0, 0, 0), "boundary distance is not three")
    need(squared(vertices[3], third) != (0, 0, 0, 0), "third-centre collision")
    return {
        "sharpness_vertices": 7,
        "sharpness_pair_norms": 21,
        "sharpness_edges": 11,
        "sharpness_three_colour_assignments_refuted": tested,
        "sharpness_boundary_squared_distance": 9,
        "sharpness_chromatic_number": 4,
    }


def audit(certificate):
    roots, edges, proper = reconstruct_boundary(certificate["boundary_patch"])
    result = {
        "boundary_vertices": 12,
        "boundary_pair_norms": 66,
        "boundary_edges": len(edges),
        "boundary_cross_edges": 1,
        "boundary_binary_assignments_checked": 4096,
        "boundary_proper_bipartitions": len(proper),
    }
    result.update(orbit_audit(certificate["orbit_chords"], roots))
    result.update(cases_audit(certificate["boundary_cases"], edges, proper))
    result.update(sharpness_audit(certificate["sharpness"]))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", required=True)
    args = parser.parse_args()
    start = time.monotonic()
    raw = (HERE / "certificate.json").read_bytes()
    certificate = json.loads(raw)
    result = audit(certificate)
    for label in ("cross-edge", "unit", "one-exception", "two-exception", "sharpness"):
        bad = json.loads(raw)
        if label == "cross-edge":
            bad["boundary_patch"]["cross_edge"] = [1, 9]
        elif label == "unit":
            bad["boundary_cases"]["unit_anchor_rows"].pop()
        elif label == "one-exception":
            bad["boundary_cases"]["one_exception_rows"][0][3] = 2
        elif label == "two-exception":
            bad["boundary_cases"]["two_exception_rows"].pop()
        else:
            bad["sharpness"]["third_centre"][0][0] = 48
        try:
            audit(bad)
        except ValueError:
            pass
        else:
            raise ValueError("malformed certificate accepted: " + label)
    result.update({
        "status": "PASS",
        "malformed_certificate_rejections": 5,
        "certificate_bytes": len(raw),
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "native_solver_calls": 0,
    })
    if (HERE / "EXPECTED.json").exists():
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected mismatch")
    out = Path(args.work)
    out.mkdir(parents=True, exist_ok=True)
    (out / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({**result, "seconds": time.monotonic() - start}, sort_keys=True))


if __name__ == "__main__":
    main()
