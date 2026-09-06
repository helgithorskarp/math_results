#!/usr/bin/env python3
"""Independent exact review of the fixed heptagon--spindle rotation family.

No module from the reviewed package is imported.  Exact arithmetic is supplied
by reviewer-1's earlier collision-review implementation of
Q[t,s]/(Phi_42(t),s^2+11).  New code here derives and checks the unit-contact
reductions and both elimination-envelope cohorts.  Finite fields are rejection
filters only; every survivor is rechecked exactly.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE.parent / "hadwiger_nelson_heptagon_moser_sum_collisions_review1" / "independent_check.py"
SPEC = importlib.util.spec_from_file_location("review1_collision_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load reviewer-owned exact-arithmetic base")
B = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(B)


class CheckError(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise CheckError(message)


def file_info(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def proper(row, edges, n):
    return (len(row) == n and all(isinstance(c, int) and 0 <= c < 4 for c in row)
            and all(row[i] != row[j] for i, j in edges))


def determinant_residual(a, b, x, y):
    """Return |qU+nV|^2-|U*conj(V)-conj(U)*V|^2 exactly."""
    U = B.emul(B.econj(a), b)
    V = B.emul(B.econj(x), y)
    n = B.esub(B.eadd(B.enorm(a), B.enorm(b)), B.OE)
    q = B.esub(B.OE, B.eadd(B.enorm(x), B.enorm(y)))
    S = B.eadd(B.emul(q, U), B.emul(n, V))
    D = B.esub(B.emul(U, B.econj(V)), B.emul(B.econj(U), V))
    return B.esub(B.enorm(S), B.enorm(D))


def h_pair_orbits(H, pairs, zeta):
    lookup = {point: i for i, point in enumerate(H)}
    need(len(lookup) == len(H), "duplicate H point")
    orbits = set()
    for i, j in pairs:
        orbit = frozenset(tuple(sorted((lookup[B.emul(B.etpow(6 * k), H[i])],
                                        lookup[B.emul(B.etpow(6 * k), H[j])])))
                          for k in range(7))
        need(len(orbit) == 7 and orbit <= pairs, "invalid H C7 orbit")
        orbits.add(orbit)
    need(set().union(*orbits) == pairs, "H C7 orbit cover")
    return orbits


def distinct_m_pairs(M, predicate):
    pairs, seen = [], set()
    for i in range(7):
        for j in range(7):
            if i == j:
                continue
            difference = B.esub(M[i], M[j])
            if predicate(difference) and difference not in seen:
                seen.add(difference)
                pairs.append((i, j))
    return pairs, seen


def collision_set(source, H, M, zeta, he, me):
    unit_h_differences = {B.esub(H[i], H[j])
                          for edge in he for i, j in (edge, tuple(reversed(edge)))}
    unit_m_differences = {B.esub(M[i], M[j])
                          for edge in me for i, j in (edge, tuple(reversed(edge)))}
    need((len(unit_h_differences), len(unit_m_differences)) == (84, 14),
         "distinct directed unit differences")
    ratios = Counter()
    for a in unit_h_differences:
        for b in unit_m_differences:
            ratios[B.emul(a, B.econj(b))] += 1
    need(len(ratios) == 252 and sum(ratios.values()) == 1176,
         "unit-difference collision census")
    need(Counter(ratios.values()) == {2: 84, 6: 168}, "collision multiplicities")
    certificate = json.loads((source / "contacts_certificate.json").read_text())
    need(isinstance(certificate, list) and len(certificate) == 36, "collision representatives")
    covered = set()
    for record in certificate:
        r = B.decode_row(record["r"])
        need(B.enorm(r) == B.OE, "nonunit certified rotation")
        orbit = {B.emul(B.etpow(6 * k), r) for k in range(7)}
        need(len(orbit) == 7 and not covered.intersection(orbit), "collision orbit overlap")
        covered.update(orbit)
    need(covered == set(ratios), "certified collision set differs from exact census")
    return covered


def check_unit_contact_bridges(H, M, he, me, collisions):
    h_neighbours = [set() for _ in H]
    m_neighbours = [set() for _ in M]
    for a, b in he:
        h_neighbours[a].add(b); h_neighbours[b].add(a)
    for a, b in me:
        m_neighbours[a].add(b); m_neighbours[b].add(a)

    unit_h = [(i, j, B.esub(H[i], H[j])) for i in range(21) for j in range(21)
              if i != j and B.enorm(B.esub(H[i], H[j])) == B.OE]
    need(len(unit_h) == 84, "directed unit H differences")
    unit_h_root_checks = 0
    missing_m_pairs = set()
    omega = B.etpow(7)
    unit_unit_phases = (B.esub(omega, B.OE), B.escale(omega, -1))
    for p in range(7):
        for q in range(7):
            if p == q:
                continue
            b = B.esub(M[q], M[p])
            common = m_neighbours[p] & m_neighbours[q]
            if common:
                c = min(common)
                u, v = B.esub(M[p], M[c]), B.esub(M[q], M[c])
                need(B.enorm(u) == B.enorm(v) == B.OE, "bad M common neighbour")
                for _, _, a in unit_h:
                    roots = (B.emul(a, B.econj(u)), B.escale(B.emul(a, B.econj(v)), -1))
                    for r in roots:
                        need(B.enorm(r) == B.OE, "unit-H root norm")
                        need(B.enorm(B.eadd(a, B.emul(r, b))) == B.OE, "unit-H root equation")
                        need(r in collisions, "unit-H root outside collision set")
                        unit_h_root_checks += 1
            else:
                missing_m_pairs.add(tuple(sorted((p, q))))
                need(B.enorm(b) == B.OE, "uncovered M pair is not unit")
                for _, _, a in unit_h:
                    for phase in unit_unit_phases:
                        r = B.emul(phase, B.emul(a, B.econj(b)))
                        need(B.enorm(r) == B.OE, "unit-unit root norm")
                        need(B.enorm(B.eadd(a, B.emul(r, b))) == B.OE, "unit-unit equation")
                        need(r in collisions, "unit-unit root outside collision set")
                        unit_h_root_checks += 1
    need(missing_m_pairs == {(3, 6)} and unit_h_root_checks == 7056,
         "unit-H bridge coverage")

    nonunit_h_pairs = {(i, j) for i, j in combinations(range(21), 2)
                       if B.enorm(B.esub(H[i], H[j])) != B.OE}
    covered_h = {(i, j) for i, j in nonunit_h_pairs if h_neighbours[i] & h_neighbours[j]}
    uncovered_h = nonunit_h_pairs - covered_h
    need((len(covered_h), len(uncovered_h)) == (105, 63), "dual-neighbour split")
    unit_m_pairs, unit_m_differences = distinct_m_pairs(M, lambda x: B.enorm(x) == B.OE)
    need(len(unit_m_pairs) == len(unit_m_differences) == 14, "directed unit M differences")
    dual_root_checks = 0
    for i, j in covered_h:
        c = min(h_neighbours[i] & h_neighbours[j])
        u, v = B.esub(H[i], H[c]), B.esub(H[j], H[c])
        a = B.esub(H[j], H[i])
        for p, q in unit_m_pairs:
            b = B.esub(M[p], M[q])
            for r in (B.emul(u, B.econj(b)), B.escale(B.emul(v, B.econj(b)), -1)):
                need(B.enorm(r) == B.OE, "dual root norm")
                need(B.enorm(B.eadd(a, B.emul(r, b))) == B.OE, "dual root equation")
                need(r in collisions, "dual-neighbour root outside collision set")
                dual_root_checks += 1
    need(dual_root_checks == 2940, "dual-neighbour root coverage")
    return uncovered_h, unit_m_pairs, unit_h_root_checks, dual_root_checks


def prepare_formal_pairs(H, M, models):
    he = B.unit_edges_exact(H)
    me = B.unit_edges_exact(M)
    factor = sorted({(7 * i + m, 7 * j + m) for i, j in he for m in range(7)} |
                    {(7 * h + i, 7 * h + j) for h in range(21) for i, j in me})
    need(len(factor) == 525, "factor edge count")
    hnorm = {(i, j): B.enorm(B.esub(H[i], H[j])) for i, j in combinations(range(21), 2)}
    mnorm = {(p, q): B.enorm(B.esub(M[p], M[q]))
             for p in range(7) for q in range(7) if p != q}
    mixed = []
    for i, j in combinations(range(21), 2):
        x = B.esub(H[i], H[j])
        for p in range(7):
            for q in range(7):
                if p == q:
                    continue
                y = B.esub(M[p], M[q])
                Q = B.esub(B.OE, B.eadd(hnorm[i, j], mnorm[p, q]))
                images = []
                for model in models:
                    mod = model[0]
                    v = B.evaluate(B.econj(x), model) * B.evaluate(y, model) % mod
                    vb = B.evaluate(x, model) * B.evaluate(B.econj(y), model) % mod
                    images.append((v, vb, B.evaluate(Q, model)))
                mixed.append(((7 * i + p, 7 * j + q), x, y, images))
    need(len(mixed) == 8820, "mixed formal-pair count")
    return he, me, factor, mixed


def check_event_cover(H, M, events, expected_h_pairs, expected_b_differences, zeta):
    wanted = {(B.esub(H[j], H[i]), b)
              for i, j in expected_h_pairs for b in expected_b_differences}
    covered = set()
    for hi, hj, bi, bj in events:
        a = B.esub(H[hj], H[hi])
        b = B.esub(M[bi], M[bj])
        for k in range(7):
            rotated = B.emul(B.etpow(6 * k), a)
            covered.add((rotated, b))
            covered.add((B.escale(rotated, -1), B.escale(b, -1)))
    need(covered == wanted, "event C7/sign cover is incomplete or redundant")
    return len(covered)


def check_envelopes(source, name, H, M, events, factor, mixed, models, he, me):
    certificate_path = source / f"{name}_certificate.json"
    expected_path = source / f"{name}_expected.json"
    certificate = json.loads(certificate_path.read_text())
    expected = json.loads(expected_path.read_text())
    need([tuple(row[:4]) for row in certificate["cases"]] == events, f"{name} event order")
    need(proper(certificate["H_colouring"], he, 21), f"{name} H colouring")
    need(len({tuple(row) for row in certificate["M_colourings"]}) == len(certificate["M_colourings"]),
         f"{name} duplicate M colouring")
    need(all(proper(row, me, 7) for row in certificate["M_colourings"]), f"{name} M colouring")

    graphs = []
    survivors = exact_edges = colour_checks = 0
    edge_histogram = Counter()
    for case_index, (hi, hj, bi, bj) in enumerate(events):
        a, b = B.esub(H[hj], H[hi]), B.esub(M[bi], M[bj])
        U = B.emul(B.econj(a), b)
        n = B.esub(B.eadd(B.enorm(a), B.enorm(b)), B.OE)
        event_images = [(B.evaluate(U, model), B.evaluate(B.econj(U), model),
                         B.evaluate(n, model)) for model in models]
        extra = []
        for edge, x, y, values in mixed:
            possible = True
            for model, (u, ub, nn), (v, vb, q) in zip(models, event_images, values):
                mod = model[0]
                ss = (q * u + nn * v) % mod
                sb = (q * ub + nn * vb) % mod
                delta = (u * vb - ub * v) % mod
                if (ss * sb + delta * delta) % mod:
                    possible = False
                    break
            if not possible:
                continue
            survivors += 1
            if determinant_residual(a, b, x, y) == B.ZE:
                extra.append(edge)
        extra.sort()
        exact_edges += len(extra)
        row = certificate["cases"][case_index]
        need(row[5] == [list(edge) for edge in extra], f"{name} extra edge list")
        need(isinstance(row[4], int) and 0 <= row[4] < len(certificate["M_colourings"]),
             f"{name} colouring selector")
        colours = [certificate["H_colouring"][i] ^ certificate["M_colourings"][row[4]][j]
                   for i in range(21) for j in range(7)]
        edges = sorted(factor + extra)
        need(proper(colours, edges, 147), f"{name} envelope colouring")
        graphs.append({"event": [hi, hj, bi, bj], "vertices": 147,
                       "edges": [list(edge) for edge in edges]})
        colour_checks += len(edges)
        edge_histogram[len(edges)] += 1

    graph_raw = (json.dumps(graphs, separators=(",", ":")) + "\n").encode()
    need(sha256(graph_raw).hexdigest() == expected["envelope_graph_stream_sha256"],
         f"{name} graph stream hash")
    need(sha256(certificate_path.read_bytes()).hexdigest() == expected["certificate_sha256"],
         f"{name} certificate hash")
    need(colour_checks == expected["colour_edge_checks"], f"{name} edge-check total")
    need(exact_edges == expected["extra_envelope_edges_total"], f"{name} extra-edge total")
    need(survivors == expected["modular_survivors_rechecked_exactly"], f"{name} survivors")
    return {
        "events": len(events),
        "formal_pair_tests": 147 * 146 // 2 * len(events),
        "mixed_pair_tests": len(mixed) * len(events),
        "modular_survivors_rechecked_exactly": survivors,
        "modular_false_positives": survivors - exact_edges,
        "extra_edges": exact_edges,
        "edge_histogram": dict(sorted(edge_histogram.items())),
        "colour_edge_checks": colour_checks,
        "H_colourings": 1,
        "M_colourings": len(certificate["M_colourings"]),
        "graph_stream_sha256": sha256(graph_raw).hexdigest(),
        "certificate": file_info(certificate_path),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    H, M = B.construct_factors()
    need(len(H) == len(set(H)) == 21 and len(M) == len(set(M)) == 7, "factor points")
    zeta = B.etpow(6)
    need({B.emul(zeta, h) for h in H} == set(H), "H is not C7 invariant")
    he, me = B.unit_edges_exact(H), B.unit_edges_exact(M)
    need((len(he), len(me)) == (42, 11), "factor edge counts")
    need(not any(proper(list(row), me, 7) for row in product(range(3), repeat=7)),
         "M has a three-colouring")

    collisions = collision_set(args.source, H, M, zeta, he, me)
    uncovered_h, unit_m_pairs, unit_h_roots, dual_roots = check_unit_contact_bridges(
        H, M, he, me, collisions)

    models = B.finite_models()
    he2, me2, factor, mixed = prepare_formal_pairs(H, M, models)
    need(he2 == he and me2 == me, "factor reconstruction mismatch")
    nonunit_h_pairs = {(i, j) for i, j in combinations(range(21), 2)
                       if B.enorm(B.esub(H[i], H[j])) != B.OE}
    all_orbits = h_pair_orbits(H, nonunit_h_pairs, zeta)
    uncovered_orbits = h_pair_orbits(H, uncovered_h, zeta)
    need((len(all_orbits), len(uncovered_orbits)) == (24, 9), "H orbit counts")

    unit_m_differences = {B.esub(M[i], M[j]) for i, j in unit_m_pairs}
    nonunit_m_pairs, nonunit_m_differences = distinct_m_pairs(M, lambda x: B.enorm(x) != B.OE)
    need(len(nonunit_m_pairs) == len(nonunit_m_differences) == 20, "nonunit M differences")
    unit_events = [(hi, hj, bi, bj) for hi, hj in sorted(min(o) for o in uncovered_orbits)
                   for bi, bj in unit_m_pairs]
    nonunit_events = [(hi, hj, bi, bj) for hi, hj in sorted(min(o) for o in all_orbits)
                      for bi, bj in nonunit_m_pairs]
    need((len(unit_events), len(nonunit_events)) == (126, 480), "event counts")
    unit_cover = check_event_cover(H, M, unit_events,
                                   {(i, j) for i, j in uncovered_h} |
                                   {(j, i) for i, j in uncovered_h},
                                   unit_m_differences, zeta)
    nonunit_cover = check_event_cover(H, M, nonunit_events,
                                      {(i, j) for i, j in nonunit_h_pairs} |
                                      {(j, i) for i, j in nonunit_h_pairs},
                                      nonunit_m_differences, zeta)

    unit_report = check_envelopes(args.source, "contact_envelopes", H, M, unit_events,
                                  factor, mixed, models, he, me)
    nonunit_report = check_envelopes(args.source, "rotation_family", H, M, nonunit_events,
                                     factor, mixed, models, he, me)
    need(nonunit_report["extra_edges"] == 480, "both-nonunit envelope extras")

    result = {
        "all_checks_passed": True,
        "scope": "every rotation of the fixed 21-point H plus rotated 7-point M family",
        "target_graph_claimed": False,
        "factor_check": {
            "H_vertices": len(H), "M_vertices": len(M),
            "H_unit_edges": len(he), "M_unit_edges": len(me),
            "proper_M_three_colourings": 0,
            "formal_vertices_outside_collisions": 147,
            "factor_edges": len(factor),
        },
        "collision_dependency": {
            "exact_collision_rotations": len(collisions),
            "certificate_C7_representatives": 36,
            "entrywise_orbit_cover": True,
            "colouring_verdict_imported_from": "review1 collision review",
        },
        "unit_contact_bridges": {
            "unit_H_directed_differences": 84,
            "unit_H_labelled_root_checks": unit_h_roots,
            "only_M_pair_without_common_unit_neighbour": [3, 6],
            "covered_nonunit_H_pairs": 105,
            "uncovered_nonunit_H_pairs": len(uncovered_h),
            "dual_neighbour_root_checks": dual_roots,
            "every_checked_root_in_collision_set": True,
        },
        "coverage": {
            "uncovered_H_pair_C7_orbits_for_unit_M": len(uncovered_orbits),
            "all_nonunit_H_pair_C7_orbits": len(all_orbits),
            "unit_M_directed_differences": len(unit_m_differences),
            "nonunit_M_directed_differences": len(nonunit_m_differences),
            "unit_M_directed_event_pairs_covered": unit_cover,
            "both_nonunit_directed_event_pairs_covered": nonunit_cover,
            "C7_and_simultaneous_sign_cover_entrywise": True,
        },
        "unit_M_envelopes": unit_report,
        "both_nonunit_envelopes": nonunit_report,
        "finite_field_filter": {
            "models": [{"prime": p, "t": t, "s": s} for p, t, s in models],
            "distinct_from_reviewed_moduli": True,
            "soundness": "exact zero maps to zero; every modular survivor was rechecked in characteristic zero",
        },
        "trust_boundary": {
            "exact_arithmetic": "reviewer-owned Q[t,s]/(Phi42(t),s^2+11) implementation",
            "imported_mathematics": [
                "injectivity of the displayed 24-element number-field basis",
                "the already accepted collision-rotation colouring review",
            ],
            "runtime": "CPython integer and Fraction arithmetic, finite loops, JSON, SHA-256",
        },
        "inputs": {
            "reviewed_source_commit": "edc54718fba597ce37f5377fca70213bda133784",
            "contacts_certificate.json": file_info(args.source / "contacts_certificate.json"),
            "contact_envelopes_expected.json": file_info(args.source / "contact_envelopes_expected.json"),
            "rotation_family_expected.json": file_info(args.source / "rotation_family_expected.json"),
            "reviewer_arithmetic_base": file_info(BASE_PATH),
        },
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS fixed rotation family: collision, unit-contact, and both envelope cohorts")


if __name__ == "__main__":
    main()
