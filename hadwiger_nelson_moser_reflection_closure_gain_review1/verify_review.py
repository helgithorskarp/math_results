#!/usr/bin/env python3
"""Independent exact review of the capped Moser reflection closure.

The target implementation is not imported.  Field elements are represented
as nested quadratic pairs

    (a + b*sqrt(3)) + (c + d*sqrt(3))*sqrt(11),

which differs from the target's flat multiplication table.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_moser_reflection_closure_gain"
SOURCE = ROOT / "hadwiger_nelson_moser_all_terminal_contacts" / "certificate.json"
ONE = ((144, 0), (0, 0))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def q3_add(x, y):
    return x[0] + y[0], x[1] + y[1]


def q3_sub(x, y):
    return x[0] - y[0], x[1] - y[1]


def q3_mul(x, y):
    return x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def k_add(x, y):
    return q3_add(x[0], y[0]), q3_add(x[1], y[1])


def k_sub(x, y):
    return q3_sub(x[0], y[0]), q3_sub(x[1], y[1])


def k_mul(x, y):
    # K = Q(sqrt(3))[sqrt(11)].
    ac = q3_mul(x[0], y[0])
    bd = q3_mul(x[1], y[1])
    ad_bc = q3_add(q3_mul(x[0], y[1]), q3_mul(x[1], y[0]))
    return q3_add(ac, (11 * bd[0], 11 * bd[1])), ad_bc


def parse_k(row):
    need(type(row) is list and len(row) == 4 and all(type(x) is int for x in row),
         "bad field coefficient row")
    return (row[0], row[1]), (row[2], row[3])


def parse_point(row):
    need(type(row) is list and len(row) == 2, "bad point row")
    return parse_k(row[0]), parse_k(row[1])


def flat_k(x):
    return x[0][0], x[0][1], x[1][0], x[1][1]


def flat_point(p):
    return flat_k(p[0]) + flat_k(p[1])


def norm2(p, q):
    dx = k_sub(p[0], q[0])
    dy = k_sub(p[1], q[1])
    return k_add(k_mul(dx, dx), k_mul(dy, dy))


def exact_edges(points):
    return [(a, b) for a, b in itertools.combinations(range(len(points)), 2)
            if norm2(points[a], points[b]) == ONE]


def reflected(p, q, centre):
    return (k_sub(k_add(p[0], q[0]), centre[0]),
            k_sub(k_add(p[1], q[1]), centre[1]))


def ordered_close(points):
    """Decode the target's documented insertion order, without target code."""
    edges = exact_edges(points)
    neighbours = [[] for _ in points]
    for a, b in edges:
        neighbours[a].append(b)
        neighbours[b].append(a)
    out = list(points)
    index = {p: i for i, p in enumerate(out)}
    routes = []
    for r, ns in enumerate(neighbours):
        for a, b in itertools.combinations(ns, 2):
            z = reflected(points[a], points[b], points[r])
            need(norm2(z, points[a]) == ONE and norm2(z, points[b]) == ONE,
                 "reflection identity failed")
            if z not in index:
                index[z] = len(out)
                out.append(z)
            routes.append((r, a, b, index[z]))
    return out, edges, routes


def canonical_close(points):
    """Independent order-free closure, returning a lexicographically sorted set."""
    points = tuple(sorted(set(points), key=flat_point))
    edges = exact_edges(points)
    neighbours = [set() for _ in points]
    for a, b in edges:
        neighbours[a].add(b)
        neighbours[b].add(a)
    additions = set(points)
    routes = 0
    for r in range(len(points)):
        for a, b in itertools.combinations(sorted(neighbours[r]), 2):
            z = reflected(points[a], points[b], points[r])
            need(norm2(z, points[a]) == ONE and norm2(z, points[b]) == ONE,
                 "canonical reflection contact failed")
            additions.add(z)
            routes += 1
    return tuple(sorted(additions, key=flat_point)), edges, routes


def row_hash(rows):
    h = hashlib.sha256()
    for row in rows:
        h.update((",".join(map(str, row)) + "\n").encode())
    return h.hexdigest()


def ordered_summary(points, edges, routes, next_n):
    degree = [0] * len(points)
    for a, b in edges:
        degree[a] += 1
        degree[b] += 1
    return {
        "points": len(points),
        "unit_edges": len(edges),
        "unit_two_paths": len(routes),
        "next_points": next_n,
        "minimum_degree": min(degree),
        "maximum_degree": max(degree),
        "degree_histogram": {str(k): v for k, v in sorted(Counter(degree).items())},
        "point_sha256": row_hash([flat_point(p) for p in points]),
        "edge_sha256": row_hash(edges),
        "route_sha256": row_hash(routes),
    }


def canonical_hashes(points, edges):
    return {
        "point_sha256": row_hash([flat_point(p) for p in points]),
        "edge_sha256": row_hash(edges),
    }


def proper(word, n, edges, label):
    need(type(word) is str and len(word) == n and set(word) <= set("0123"),
         label + ": malformed colour word")
    need(all(word[a] != word[b] for a, b in edges), label + ": monochromatic edge")


def has_edge(edges, a, b):
    return tuple(sorted((a, b))) in set(edges)


def verify_forcing_chain(word, edges, first, first_old, second, second_old,
                         expected_old_assignment):
    need({i: int(word[i]) for i in expected_old_assignment} == expected_old_assignment,
         "forcing-chain base assignment mismatch")
    need(all(has_edge(edges, first, i) for i in first_old), "missing first forcing edge")
    need(all(has_edge(edges, second, i) for i in second_old), "missing second forcing edge")
    need(has_edge(edges, first, second), "missing forcing-chain edge")
    first_colours = {expected_old_assignment[i] for i in first_old}
    second_colours = {expected_old_assignment[i] for i in second_old}
    need(len(first_colours) == 3 and first_colours == second_colours,
         "forcing-chain old colours do not agree")
    forced = ({0, 1, 2, 3} - first_colours).pop()
    need(second_colours | {forced} == {0, 1, 2, 3}, "chain does not contradict")
    return forced


def verify_rainbow_block(word, edges, blocker, terminals, assignment):
    need({i: int(word[i]) for i in terminals} == assignment,
         "rainbow base assignment mismatch")
    need(set(assignment.values()) == {0, 1, 2, 3}, "terminals are not rainbow")
    need(all(has_edge(edges, blocker, i) for i in terminals), "missing rainbow contact")


def moser_audit(source, s0, e0):
    moser = [parse_point(p) for p in source["M"]]
    index = {p: i for i, p in enumerate(s0)}
    need(all(p in index for p in moser), "Moser point absent from S0")
    old_edges = set(e0)
    medges = [(a, b) for a, b in itertools.combinations(range(7), 2)
              if tuple(sorted((index[moser[a]], index[moser[b]]))) in old_edges]
    need(len(medges) == 11, "wrong Moser edge count")
    count = sum(all(w[a] != w[b] for a, b in medges)
                for w in itertools.product(range(3), repeat=7))
    need(count == 0, "Moser subgraph accepted a three-colouring")
    return len(medges), count


def audit(cert):
    source_bytes = SOURCE.read_bytes()
    source = json.loads(source_bytes)
    need(source["scale"] == 12, "unexpected source scale")
    need(source["basis"] == ["1", "sqrt3", "sqrt11", "sqrt33"],
         "unexpected source basis")
    need(cert["schema"] == "hn-moser-reflection-closure-gain-v1", "wrong target schema")
    need(cert["source_certificate_sha256"] == hashlib.sha256(source_bytes).hexdigest(),
         "source hash mismatch")

    s0 = [parse_point(p) for p in source["C"]]
    need(len(s0) == len(set(s0)) == 25, "source is not 25 distinct points")
    s1, e0, r0 = ordered_close(s0)
    s2, e1, r1 = ordered_close(s1)
    s3, e2, r2 = ordered_close(s2)
    need([len(s0), len(s1), len(s2), len(s3)] == [25, 115, 398, 1020],
         "ordered closure counts differ")
    need([len(e0), len(e1), len(e2)] == [53, 447, 2084],
         "ordered edge counts differ")
    summaries = [
        ordered_summary(s0, e0, r0, len(s1)),
        ordered_summary(s1, e1, r1, len(s2)),
        ordered_summary(s2, e2, r2, len(s3)),
    ]
    need(summaries == cert["rounds"], "target census or ordered hashes differ")

    # Recompute the same closure as sets with an independently sorted order.
    c0 = tuple(sorted(set(s0), key=flat_point))
    c1, ce0, cr0 = canonical_close(c0)
    c2, ce1, cr1 = canonical_close(c1)
    c3, ce2, cr2 = canonical_close(c2)
    need(set(c0) == set(s0) and set(c1) == set(s1) and set(c2) == set(s2)
         and set(c3) == set(s3), "ordered and canonical closures disagree")
    need([len(ce0), len(ce1), len(ce2)] == [53, 447, 2084],
         "canonical edge counts differ")
    need([cr0, cr1, cr2] == [258, 3713, 22980], "canonical route counts differ")

    proper(cert["s0_nonextending_word"], len(s0), e0, "target S0 witness")
    proper(cert["s1_nonextending_word"], len(s1), e1, "target S1 witness")
    proper(cert["s2_four_word"], len(s2), e2, "target S2 four-colouring")
    need(cert["s1_extending_word"] == cert["s2_four_word"][:len(s1)],
         "bad positive S1 restriction")
    need(cert["s0_extending_word"] == cert["s2_four_word"][:len(s0)],
         "bad positive S0 restriction")

    # Independently certify the target's two nonextension witnesses locally.
    target_chain = {0: 0, 1: 0, 11: 3, 13: 3, 18: 1, 19: 1}
    forced_target = verify_forcing_chain(
        cert["s0_nonextending_word"], e1, 29, [0, 11, 18], 33, [1, 13, 19],
        target_chain)
    rainbow = {36: 3, 82: 2, 84: 0, 98: 1}
    verify_rainbow_block(cert["s1_nonextending_word"], e2, 189,
                         list(rainbow), rainbow)

    # Stronger first-round projection: five old vertices suffice.
    refined_s0_word = "1101311202120303023121100"
    proper(refined_s0_word, len(s0), e0, "refined S0 admissibility word")
    refined = {0: 1, 10: 1, 11: 2, 17: 2, 18: 3}
    forced_refined = verify_forcing_chain(
        refined_s0_word, e1, 29, [0, 11, 18], 93, [10, 17, 18], refined)

    medges, three = moser_audit(source, s0, e0)
    need(cert["natural_next_round_points"] == 1020, "bad natural next-round count")
    need(cert["record_candidate"] is False, "target mislabels record status")

    role_indices = sorted(set(target_chain) | set(refined) | set(rainbow)
                          | {29, 33, 93, 189})
    role_coordinates = {str(i): list(flat_point((s1 if i < len(s1) else s2)[i]))
                        for i in role_indices}

    return {
        "status": "ACCEPT_WITH_PROJECTION_REFINEMENTS",
        "target_claim_accepted": True,
        "actual_plane_unit_distance_realization": True,
        "round_points": [25, 115, 398],
        "round_edges": [53, 447, 2084],
        "round_routes": [258, 3713, 22980],
        "next_complete_round_points": 1020,
        "exact_pair_decisions": sum(len(p) * (len(p) - 1) // 2 for p in (s0, s1, s2)),
        "defining_contact_checks": 2 * sum(map(len, (r0, r1, r2))),
        "canonical_hashes": [
            canonical_hashes(c0, ce0),
            canonical_hashes(c1, ce1),
            canonical_hashes(c2, ce2),
        ],
        "moser_edges": medges,
        "moser_named_three_colourings": three,
        "s2_four_colouring_checked": True,
        "target_s0_to_s1_local_core": {
            "old_terminals": sorted(target_chain),
            "old_assignment": "003311",
            "forced_vertex": 29,
            "forced_colour": forced_target,
            "empty_vertex": 33,
        },
        "refined_s0_to_s1_projection": {
            "old_terminals": sorted(refined),
            "old_assignment": "11223",
            "admissibility_word": refined_s0_word,
            "forced_vertex": 29,
            "forced_colour": forced_refined,
            "empty_vertex": 93,
            "terminal_count": 5,
        },
        "refined_s1_to_s2_projection": {
            "old_terminals": sorted(rainbow),
            "old_assignment": "3201",
            "admissibility_word": cert["s1_nonextending_word"],
            "rainbow_blocker": 189,
            "terminal_count": 4,
        },
        "role_coordinates_scaled_by_12": role_coordinates,
        "chromatic_number_each_round": 4,
        "five_chromatic_plane_graph": False,
        "record_candidate": False,
    }


def run_controls(cert):
    rejected = 0
    bad = copy.deepcopy(cert)
    bad["rounds"][1]["unit_edges"] += 1
    for damaged in [bad]:
        try:
            audit(damaged)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("damaged census accepted")

    bad = copy.deepcopy(cert)
    word = list(bad["s2_four_word"])
    source = json.loads(SOURCE.read_text())
    p0 = [parse_point(p) for p in source["C"]]
    p1, _, _ = ordered_close(p0)
    p2, _, _ = ordered_close(p1)
    e2 = exact_edges(p2)
    a, b = e2[0]
    word[b] = word[a]
    bad["s2_four_word"] = "".join(word)
    try:
        audit(bad)
    except ValueError:
        rejected += 1
    else:
        raise ValueError("damaged colouring accepted")

    bad = copy.deepcopy(cert)
    bad["source_certificate_sha256"] = "0" * 64
    try:
        audit(bad)
    except ValueError:
        rejected += 1
    else:
        raise ValueError("damaged source identity accepted")
    need(rejected == 3, "not all controls rejected")
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-certificate", type=Path,
                        default=TARGET / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    cert = json.loads(args.target_certificate.read_text())
    result = audit(cert)
    if args.controls:
        result["corruptions_rejected"] = run_controls(cert)
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(result == expected, "review result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
