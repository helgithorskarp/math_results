#!/usr/bin/env python3
"""Root-linked four-deck LP for a dense order-24 occurrence in good45.

The model is symmetry-free and acts on the whole occurrence family.  It uses
the two orientations of the m=2,3,4 McKay--Radziszowski identities and the
proved mixed degree-four identity.  Local (4,5,k) graphs are relaxed to their
induced four-vertex decks, with universal degree/codegree constraints.  For
the complete order-24 e>=126 tail, the deck is restricted to the exact
catalogue-conditional convex hull.  It additionally distinguishes one dense
degree-24 root and couples the exact degree histogram of its neighbourhood to
the ambient degree counts and a selected relaxed exterior graph across the
root cut.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import json
from math import comb
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp
from scipy.linalg import qr
from scipy.sparse import coo_matrix, vstack


HERE = Path(__file__).resolve().parent
N = 45
EMIN = {20: 68, 21: 77, 22: 88, 23: 101, 24: 116}
EMAX = {20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
P4 = ("i4", "k2ii", "2k2", "p3i", "k3i", "k13", "p4", "c4", "t31", "t32")
P4_EDGES = dict(zip(P4, (0, 1, 2, 2, 3, 3, 3, 4, 4, 5)))
TRIPLE_INCIDENCE = {
    "i4": (4, 0, 0, 0),
    "k2ii": (2, 2, 0, 0),
    "2k2": (0, 4, 0, 0),
    "p3i": (1, 2, 1, 0),
    "k3i": (0, 3, 0, 1),
    "k13": (1, 0, 3, 0),
    "p4": (0, 2, 2, 0),
    "c4": (0, 0, 4, 0),
    "t31": (0, 1, 2, 1),
    "t32": (0, 0, 2, 2),
}
TAUS = (7, 8, 9, 10)
I3_MIN_44 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
             9: 1, 10: 4, 11: 7, 12: 10, 13: 17, 14: 25, 15: 38,
             16: 56, 17: 68}
E100_PATTERNS = (37, 303, 123, 746, 196, 438, 1203, 371, 876, 552)
E100_DEGREE_HISTOGRAM = (0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 16, 2, 0, 0)


def degree_wedge_bounds(k: int, e: int) -> tuple[int, int]:
    lo, hi, total = max(0, k - 18), 13, 2 * e
    assert k * lo <= total <= k * hi
    q, r = divmod(total - k * lo, k)
    low = (k - r) * comb(lo + q, 2) + r * comb(lo + q + 1, 2)
    degrees = [lo] * k
    remaining = total - k * lo
    for i in range(k):
        add = min(remaining, hi - lo)
        degrees[i] += add
        remaining -= add
    assert remaining == 0
    high = sum(comb(d, 2) for d in degrees)
    return low, high


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integer-occurrences", action="store_true")
    parser.add_argument("--integer-decks", action="store_true")
    parser.add_argument("--integer-root", action="store_true")
    parser.add_argument("--time-limit", type=float, default=900.0)
    parser.add_argument("--rational-limit", type=int, default=10**8)
    parser.add_argument("--witness", type=Path)
    parser.add_argument("--verify-witness", type=Path)
    parser.add_argument("--fix-root-pair", type=int)
    parser.add_argument(
        "--objective", choices=("feasible", "min-n24", "max-n24", "max-root-pair", "tiebreak"),
        default="feasible",
    )
    args = parser.parse_args()
    variables: list[tuple] = [("n", d) for d in range(20, 25)]
    for role in ("h", "q"):
        for d in range(20, 25):
            k = d if role == "h" else 44 - d
            for e in range(EMIN[k], EMAX[k] + 1):
                variables.append(("y", role, d, e))
                variables.extend(("p", role, d, e, name) for name in P4)

    # Exact invariant types of the complete order-24 e>=126 catalogue tail.
    tail_rows = []
    for row_index, line in enumerate((HERE / "scan24e126plus.tsv").read_text().splitlines()):
        values = list(map(int, line.split()))
        n, e = values[:2]
        assert n == 24 and 126 <= e <= 132 and values[16] == 0
        patterns = tuple(values[6:16])
        tail_rows.append((e, patterns, values[17]))
        for role, d in (("h", 24), ("q", 20)):
            variables.append(("s", role, d, row_index))

    # Join every member of the complete dense tail to its exact catalogue
    # four-deck row, transversal number, and degree histogram.  Identical
    # joined feature rows can be merged because all following constraints are
    # linear in precisely these features.
    tail_lookup = {(e, patterns): i for i, (e, patterns, _mult) in enumerate(tail_rows)}
    tau_lines = (HERE / "final_all.txt").read_text().splitlines()
    joint_lines = (HERE / "dense_joint.tsv").read_text().splitlines()
    assert len(tau_lines) == len(joint_lines) == 15913
    root_counter = Counter()
    for expected_index, (tau_line, joint_line) in enumerate(zip(tau_lines, joint_lines)):
        tv = tau_line.split()
        jv = list(map(int, joint_line.split()))
        assert int(tv[0]) == jv[0] == expected_index
        assert int(tv[1]) == jv[2] and int(tv[2]) == jv[5]
        tau = int(tv[3])
        assert tau in TAUS
        e, tri, i3 = jv[2:5]
        patterns = tuple(jv[5:15])
        degrees = tuple(jv[15:])
        assert len(degrees) == 24 and sum(degrees) == 2 * e
        assert min(degrees) >= 0 and max(degrees) <= 13
        histogram = tuple(Counter(degrees)[j] for j in range(14))
        tail_index = tail_lookup[(e, patterns)]
        root_counter[(tail_index, tau, tri, i3, histogram)] += 1
    root_types = sorted(root_counter)
    for root_index in range(len(root_types)):
        variables.append(("a", root_index))

    # Variables for vertices on the H and exterior/Q sides of the selected
    # root, disaggregated by the selected root's transversal number.
    for tau in TAUS:
        for j in range(14):
            for d in range(20, 25):
                boundary_degree = d - 1 - j
                if 0 <= boundary_degree <= 17:
                    variables.append(("zh", tau, j, d))
        for j in range(2, 14):
            for d in range(20, 25):
                trace_size = d - 19 + j
                if tau <= trace_size <= 18:
                    variables.append(("zq", tau, j, d))
        for e in range(EMIN[20], EMAX[20] + 1):
            variables.append(("rqy", tau, e))
            variables.extend(("rqp", tau, e, name) for name in P4)

    where = {v: i for i, v in enumerate(variables)}
    eq: list[tuple[str, dict[int, Fraction], Fraction]] = []
    ub: list[tuple[str, dict[int, Fraction], Fraction]] = []

    def terms(items):
        out = defaultdict(Fraction)
        for variable, coefficient in items:
            if coefficient:
                out[where[variable]] += Fraction(coefficient)
        return dict(out)

    def add_eq(name, items, rhs=0):
        eq.append((name, terms(items), Fraction(rhs)))

    def add_ub(name, items, rhs=0):
        ub.append((name, terms(items), Fraction(rhs)))

    def root_items(tau=None, field=None, value=None):
        result = []
        for i, (_tail_index, rtau, tri, i3, histogram) in enumerate(root_types):
            if tau is not None and rtau != tau:
                continue
            coefficient = 1
            if field == "tri": coefficient = tri
            elif field == "i3": coefficient = i3
            elif field == "e": coefficient = tail_rows[_tail_index][0]
            elif field is not None and field.startswith("hist"):
                coefficient = histogram[int(field[4:])]
            if value is not None:
                coefficient *= value
            result.append((("a", i), coefficient))
        return result

    add_eq("vertices", [(('n', d), 1) for d in range(20, 25)], 45)
    for role in ("h", "q"):
        for d in range(20, 25):
            k = d if role == "h" else 44 - d
            ys = [(('y', role, d, e), 1) for e in range(EMIN[k], EMAX[k] + 1)]
            add_eq(f"{role}{d}_occurrences", ys + [(('n', d), -1)])
            for e in range(EMIN[k], EMAX[k] + 1):
                y = ('y', role, d, e)
                ps = [('p', role, d, e, name) for name in P4]
                add_eq(
                    f"{role}{d}e{e}_foursets",
                    [(p, 1) for p in ps] + [(y, -comb(k, 4))],
                )
                add_eq(
                    f"{role}{d}e{e}_edgeincidence",
                    [(p, P4_EDGES[p[-1]]) for p in ps]
                    + [(y, -e * comb(k - 2, 2))],
                )
                # Wedges = P3 + 3 K3, derived from four-deck incidence.
                wedge_items = []
                for p in ps:
                    tri = Fraction(TRIPLE_INCIDENCE[p[-1]][3], k - 3)
                    path = Fraction(TRIPLE_INCIDENCE[p[-1]][2], k - 3)
                    wedge_items.append((p, path + 3 * tri))
                low, high = degree_wedge_bounds(k, e)
                add_ub(f"{role}{d}e{e}_wedge_upper", wedge_items + [(y, -high)])
                add_ub(f"{role}{d}e{e}_wedge_lower", [(p, -c) for p, c in wedge_items] + [(y, low)])
                # Common neighbours of an edge are independent and have size <=4.
                tri_items = [
                    (p, Fraction(TRIPLE_INCIDENCE[p[-1]][3], k - 3)) for p in ps
                ]
                add_ub(f"{role}{d}e{e}_edge_common", [(p, 3*c) for p, c in tri_items] + [(y, -4*e)])
                # Common nonneighbours of a nonedge form a (4,3)-graph, order <=8.
                i3_items = [
                    (p, Fraction(TRIPLE_INCIDENCE[p[-1]][0], k - 3)) for p in ps
                ]
                add_ub(
                    f"{role}{d}e{e}_nonedge_common",
                    [(p, 3*c) for p, c in i3_items]
                    + [(y, -8 * (comb(k, 2) - e))],
                )

    # Replace each dense order-24 four-deck by its exact complete-tail hull.
    for role, d in (("h", 24), ("q", 20)):
        for e in range(126, 133):
            selectors = [
                (('s', role, d, i), 1)
                for i, (edge_count, _patterns, _mult) in enumerate(tail_rows)
                if edge_count == e
            ]
            add_eq(f"tail_{role}{d}e{e}_mass", selectors + [(('y', role, d, e), -1)])
            for j, name in enumerate(P4):
                add_eq(
                    f"tail_{role}{d}e{e}_{name}",
                    [
                        (('s', role, d, i), patterns[j])
                        for i, (edge_count, patterns, _mult) in enumerate(tail_rows)
                        if edge_count == e
                    ] + [(('p', role, d, e, name), -1)],
                )

    def pattern_items(role: str, d: int, triple_class: int | None = None, name: str | None = None):
        k = d if role == "h" else 44 - d
        result = []
        for e in range(EMIN[k], EMAX[k] + 1):
            for pname in P4:
                coefficient = 0.0
                if triple_class is not None:
                    coefficient = Fraction(TRIPLE_INCIDENCE[pname][triple_class], k - 3)
                elif name is not None and pname == name:
                    coefficient = 1.0
                if coefficient:
                    result.append((('p', role, d, e, pname), coefficient))
        return result

    # Global m=2 identity (height-3501 excess equation).
    m2 = []
    for d in range(20, 25):
        m = 44 - d
        m2.append((('n', d), comb(m, 2) - Fraction(d * (45 - 2*d), 2)))
        for e in range(EMIN[d], EMAX[d] + 1):
            m2.append((('y', 'h', d, e), -e))
        for e in range(EMIN[m], EMAX[m] + 1):
            m2.append((('y', 'q', d, e), -e))
    add_eq("global_m2", m2)

    def g3_items(role: str):
        result = []
        for d in range(20, 25):
            k = d if role == "h" else 44 - d
            for e in range(EMIN[k], EMAX[k] + 1):
                result.append((('y', role, d, e), (48 - 3*k) * e))
            result += [(v, 6*c) for v, c in pattern_items(role, d, triple_class=3)]
            result += [(v, 3*c) for v, c in pattern_items(role, d, triple_class=2)]
        return result

    def i3_items(role: str):
        return [item for d in range(20, 25) for item in pattern_items(role, d, triple_class=0)]

    def r12_items(role: str):
        result = []
        for d in range(20, 25):
            k = d if role == "h" else 44 - d
            result += [(v, (159 - 12*k)*c) for v, c in pattern_items(role, d, triple_class=3)]
            result += [(v, 6*c) for v, c in pattern_items(role, d, name="t31")]
            result += [(v, 16*c) for v, c in pattern_items(role, d, name="t32")]
        return result

    def i4_items(role: str):
        return [item for d in range(20, 25) for item in pattern_items(role, d, name="i4")]

    add_eq("global_m3", g3_items("h") + [(v, -3*c) for v, c in i3_items("q")])
    add_eq("complement_m3", g3_items("q") + [(v, -3*c) for v, c in i3_items("h")])
    add_eq("global_m4", r12_items("h") + [(v, -12*c) for v, c in i4_items("q")])
    add_eq("complement_m4", r12_items("q") + [(v, -12*c) for v, c in i4_items("h")])

    def a_items(role: str):
        result = []
        for d in range(20, 25):
            k = d if role == "h" else 44 - d
            constant_degree = (
                N*(N-3)*k - (N*N+2*N-6)*k*k + 3*N*k**3 - 2*k**4
            )
            for e in range(EMIN[k], EMAX[k] + 1):
                constant = constant_degree + 2*(N*N+N-8)*e - 12*e*e \
                    - 12*(N-1)*k*e + 12*k*k*e
                result.append((('y', role, d, e), constant))
            result += [(v, 12*(N-2)*c) for v, c in pattern_items(role, d, triple_class=3)]
            result += [(v, (12*(N+2)-24*k)*c) for v, c in pattern_items(role, d, triple_class=2)]
            for name, coefficient in (("c4",72),("k13",24),("p4",24),("t31",24),("t32",32)):
                result += [(v, coefficient*c) for v, c in pattern_items(role, d, name=name)]
        return result

    def b_items(role: str):
        # The role stores Q, whose complement is the minus-neighbourhood Y.
        result = []
        for d in range(20, 25):
            k = d if role == "h" else 44 - d
            root_degree = 44 - k
            for e in range(EMIN[k], EMAX[k] + 1):
                ey = comb(k, 2) - e
                constant = 4*ey*ey + (4*root_degree**2 - 2*(N-2)*root_degree)*ey
                result.append((('y', role, d, e), constant))
            result += [(v, (2*(N-8)+4*root_degree)*c)
                       for v, c in pattern_items(role, d, triple_class=1)]
            for name, coefficient in (("k3i",-12),("2k2",-8),("p3i",-8),("k2ii",-24)):
                result += [(v, coefficient*c) for v, c in pattern_items(role, d, name=name)]
        return result

    add_eq("mixed", a_items("h") + b_items("q"))
    add_eq("complement_mixed", a_items("q") + b_items("h"))

    # Select one concrete feature type from the complete dense tail, dominated
    # by the corresponding aggregate catalogue-hull mass already present in
    # the global model.
    add_eq("selected_root_mass", root_items(), 1)
    for tail_index in range(len(tail_rows)):
        selected = [(("a", i), 1) for i, rt in enumerate(root_types) if rt[0] == tail_index]
        if selected:
            add_ub(
                f"selected_h_dominance_{tail_index}",
                selected + [(('s', 'h', 24, tail_index), -1)],
            )

    # Select the corresponding order-20 Q relaxation from the aggregate
    # degree-24 exterior occurrence.  Four-deck componentwise domination is a
    # necessary condition for selecting one actual occurrence from the sum.
    for e in range(EMIN[20], EMAX[20] + 1):
        add_ub(
            f"selected_q_mass_dominance_e{e}",
            [(('rqy', tau, e), 1) for tau in TAUS]
            + [(('y', 'q', 24, e), -1)],
        )
        for name in P4:
            add_ub(
                f"selected_q_{name}_dominance_e{e}",
                [(('rqp', tau, e, name), 1) for tau in TAUS]
                + [(('p', 'q', 24, e, name), -1)],
            )

    for tau in TAUS:
        selected_mass = root_items(tau=tau)
        add_eq(
            f"selected_q_mass_tau{tau}",
            [(('rqy', tau, e), 1) for e in range(EMIN[20], EMAX[20] + 1)]
            + [(v, -c) for v, c in selected_mass],
        )
        for e in range(EMIN[20], EMAX[20] + 1):
            y = ('rqy', tau, e)
            ps = [('rqp', tau, e, name) for name in P4]
            add_eq(
                f"selected_q_tau{tau}_e{e}_foursets",
                [(p, 1) for p in ps] + [(y, -comb(20, 4))],
            )
            add_eq(
                f"selected_q_tau{tau}_e{e}_edgeincidence",
                [(p, P4_EDGES[p[-1]]) for p in ps]
                + [(y, -e * comb(18, 2))],
            )
            tri_items = [(p, Fraction(TRIPLE_INCIDENCE[p[-1]][3], 17)) for p in ps]
            i3_items_selected = [(p, Fraction(TRIPLE_INCIDENCE[p[-1]][0], 17)) for p in ps]
            add_ub(
                f"selected_q_tau{tau}_e{e}_edge_common",
                [(p, 3*c) for p, c in tri_items] + [(y, -4*e)],
            )
            add_ub(
                f"selected_q_tau{tau}_e{e}_nonedge_common",
                [(p, 3*c) for p, c in i3_items_selected]
                + [(y, -8*(comb(20, 2)-e))],
            )
            if e == 100:
                # The published complete e=100 boundary contains exactly one
                # order-20 graph.  Its deck and degree histogram are therefore
                # forced whenever this selected component has positive mass.
                for name, count in zip(P4, E100_PATTERNS):
                    add_eq(
                        f"selected_q_tau{tau}_e100_exact_{name}",
                        [(('rqp', tau, 100, name), 1), (y, -count)],
                    )

        # The selected H degree histogram is exact.  The selected Q degree
        # histogram has exact zeroth, first, and wedge moments from its
        # selected four-deck.
        for j in range(14):
            hvars = [(('zh', tau, j, d), 1) for d in range(20, 25)
                     if ('zh', tau, j, d) in where]
            add_eq(
                f"selected_h_hist_tau{tau}_j{j}",
                hvars + [(v, -c) for v, c in root_items(tau=tau, field=f"hist{j}")],
            )
        qvars = [(('zq', tau, j, d), 1) for j in range(2, 14) for d in range(20, 25)
                 if ('zq', tau, j, d) in where]
        add_eq(
            f"selected_q_vertices_tau{tau}",
            qvars + [(v, -20*c) for v, c in selected_mass],
        )
        for j, count in enumerate(E100_DEGREE_HISTOGRAM):
            if count:
                add_ub(
                    f"selected_q_e100_degree_tau{tau}_j{j}",
                    [(('rqy', tau, 100), count)]
                    + [(v, -c) for v, c in qvars if v[2] == j],
                )
        add_eq(
            f"selected_q_degree_sum_tau{tau}",
            [(v, j*c) for v, c in qvars for j in [v[2]]]
            + [(('rqy', tau, e), -2*e) for e in range(EMIN[20], EMAX[20] + 1)],
        )
        selected_wedges = []
        for e in range(EMIN[20], EMAX[20] + 1):
            for name in P4:
                triple = TRIPLE_INCIDENCE[name]
                selected_wedges.append((('rqp', tau, e, name),
                                         -Fraction(triple[2] + 3*triple[3], 17)))
        add_eq(
            f"selected_q_wedges_tau{tau}",
            [(v, comb(v[2], 2)*c) for v, c in qvars] + selected_wedges,
        )

        # Both descriptions count the same cut edges, within every tau slice
        # of the convex disjunction.
        hcut = [(('zh', tau, j, d), d - 1 - j)
                for j in range(14) for d in range(20, 25)
                if ('zh', tau, j, d) in where]
        qcut = [(('zq', tau, j, d), d - 19 + j)
                for j in range(2, 14) for d in range(20, 25)
                if ('zq', tau, j, d) in where]
        add_eq(f"selected_cut_tau{tau}", hcut + [(v, -c) for v, c in qcut])

        # For every independent triple C in H, at most four exterior traces
        # avoid C.  Each trace complement is a (4,4)-graph, giving the exact
        # classical lower table used on the left.
        add_ub(
            f"selected_independent_triples_tau{tau}",
            [(v, I3_MIN_44[24-(v[3]-19+v[2])]*c) for v, c in qvars]
            + [(v, -4*c) for v, c in root_items(tau=tau, field="i3")],
        )

        # Exact second-moment cut bounds.  If xy is an edge of Q (a nonedge
        # of G), then the common H-nonneighbours of x,y form a (4,3)-graph
        # and have size at most 8.  If xy is a nonedge of Q, their common
        # H-neighbours form a (3,5)-graph and have size at most 13.  Summing
        # the resulting trace-intersection bounds over all exterior pairs
        # gives the first inequality below.
        add_ub(
            f"selected_column_codegrees_tau{tau}",
            [(v, comb(d-1-j, 2)) for v, _c in hcut for j, d in [(v[2], v[3])]]
            + [(v, -v[2]*(v[3]-19+v[2])*c) for v, c in qvars]
            + [(('rqy', tau, e), 29*e) for e in range(EMIN[20], EMAX[20] + 1)]
            + [(v, -2470*c) for v, c in selected_mass],
        )

        # Dually, an H-edge has at most eight common boundary neighbours; for
        # an H-nonedge the common boundary-nonneighbour set has size at most
        # 13.  Summing over all H-pairs produces a complementary row-codegree
        # constraint, still using only exact selected-root features.
        add_ub(
            f"selected_row_codegrees_tau{tau}",
            [(v, comb(v[3]-19+v[2], 2)*c) for v, c in qvars]
            + [(v, -(v[3]-1-v[2])*(23-v[2])) for v, _c in hcut]
            + [(v, -15*c) for v, c in root_items(tau=tau, field="e")]
            + [(v, 1932*c) for v, c in selected_mass],
        )

    # The 44 nonroot vertices around the distinguished degree-24 root exhaust
    # the global ambient degree counts.
    for d in range(20, 25):
        allocations = [
            (variable, 1) for variable in variables
            if variable[0] in ("zh", "zq") and variable[3] == d
        ]
        add_eq(
            f"selected_ambient_degree_{d}",
            allocations + [(('n', d), -1)],
            -1 if d == 24 else 0,
        )

    # A single dense degree-24 neighbourhood.  Complementation covers the
    # dual order-24 role at degree 20.
    add_ub(
        "dense_occurrence",
        [(('y', 'h', 24, e), -1) for e in range(126, 133)],
        -1,
    )
    if args.fix_root_pair is not None:
        add_eq(
            "fixed_root_pair",
            [
                (("a", i), tail_rows[tail_index][0])
                for i, (tail_index, _tau, _tri, _i3, _histogram) in enumerate(root_types)
            ]
            + [
                (("rqy", tau, e), e)
                for tau in TAUS for e in range(EMIN[20], EMAX[20] + 1)
            ],
            args.fix_root_pair,
        )

    if args.verify_witness:
        payload = json.loads(args.verify_witness.read_text())
        exact = [Fraction(0) for _ in variables]
        seen_variables = set()
        for item in payload["positive"]:
            variable = tuple(item["variable"])
            if variable not in where or variable in seen_variables:
                raise SystemExit(f"invalid witness variable: {variable}")
            seen_variables.add(variable)
            exact[where[variable]] = Fraction(int(item["numerator"]), int(item["denominator"]))
        equality_failures = [
            (name, sum(exact[j]*c for j, c in row.items()) - rhs)
            for name, row, rhs in eq
            if sum(exact[j]*c for j, c in row.items()) != rhs
        ]
        inequality_failures = [
            (name, rhs - sum(exact[j]*c for j, c in row.items()))
            for name, row, rhs in ub
            if rhs - sum(exact[j]*c for j, c in row.items()) < 0
        ]
        domain_failures = [variables[i] for i, value in enumerate(exact) if value < 0]
        integral_kinds = set(payload.get("integral_variable_kinds", []))
        integrality_failures = [
            variables[i] for i, value in enumerate(exact)
            if variables[i][0] in integral_kinds and value.denominator != 1
        ]
        print("variables", len(variables), "equalities", len(eq), "inequalities", len(ub))
        print("root_types", len(root_types), "joined_records", sum(root_counter.values()))
        print(
            "witness_check",
            "exact" if not equality_failures and not inequality_failures
            and not domain_failures and not integrality_failures else "failed",
            "positive", len(seen_variables),
            "equality_failures", len(equality_failures),
            "inequality_failures", len(inequality_failures),
            "domain_failures", len(domain_failures),
            "integrality_failures", len(integrality_failures),
        )
        if equality_failures or inequality_failures or domain_failures or integrality_failures:
            raise SystemExit(1)
        return

    def matrix(rows):
        rr, cc, vv, rhs = [], [], [], []
        for i, (_name, row, b) in enumerate(rows):
            for j, value in row.items():
                rr.append(i); cc.append(j); vv.append(float(value))
            rhs.append(float(b))
        return coo_matrix((vv, (rr, cc)), shape=(len(rows), len(variables))).tocsr(), np.array(rhs)

    aeq, beq = matrix(eq)
    aub, bub = matrix(ub)
    objective = np.zeros(len(variables))
    if args.objective == "min-n24":
        objective[where[("n", 24)]] = 1
    elif args.objective == "max-n24":
        objective[where[("n", 24)]] = -1
    elif args.objective == "max-root-pair":
        for i, (tail_index, _tau, _tri, _i3, _histogram) in enumerate(root_types):
            objective[where[("a", i)]] = -tail_rows[tail_index][0]
        for tau in TAUS:
            for e in range(EMIN[20], EMAX[20] + 1):
                objective[where[("rqy", tau, e)]] = -e
    elif args.objective == "tiebreak":
        for i in range(len(variables)):
            objective[i] = ((7919*i + 104729) % 1009) / 1009.0
    integral_indices: set[int] = set()
    if args.integer_occurrences or args.integer_decks or args.integer_root:
        matrix_all = vstack((aeq, aub), format="csr")
        lower = np.concatenate((beq, np.full(len(ub), -np.inf)))
        upper = np.concatenate((beq, bub))
        integrality = np.zeros(len(variables), dtype=np.uint8)
        for variable, index in where.items():
            if args.integer_decks or (
                args.integer_root and variable[0] in ("n", "a", "zh", "zq", "rqy", "rqp")
            ) or (args.integer_occurrences and variable[0] in ("n", "y")):
                integrality[index] = 1
                integral_indices.add(index)
        result = milp(
            objective, integrality=integrality,
            bounds=Bounds(np.zeros(len(variables)), np.full(len(variables), np.inf)),
            constraints=LinearConstraint(matrix_all, lower, upper),
            options={"presolve": True, "time_limit": args.time_limit},
        )
    else:
        result = linprog(
            objective, A_ub=aub, b_ub=bub, A_eq=aeq, b_eq=beq,
            bounds=(0, None), method="highs",
            options={"presolve": True},
        )
    print("variables", len(variables), "equalities", len(eq), "inequalities", len(ub))
    print("root_types", len(root_types), "joined_records", sum(root_counter.values()))
    print("status", result.status, result.message)
    if result.success:
        print("objective", args.objective, result.fun)
        if args.objective == "max-root-pair":
            print("root_pair_sum", -result.fun)
        print("positive_variables", int(np.count_nonzero(result.x > 1e-9)))
        print("degree_counts", *(f"{d}:{result.x[where[('n',d)]]:.12g}" for d in range(20,25)))
        print("dense_mass", sum(result.x[where[('y','h',24,e)]] for e in range(126,133)))
        for name, row, rhs in eq[-7:]:
            activity = sum(result.x[j]*float(c) for j,c in row.items())
            print("identity", name, "activity", f"{activity:.12g}", "residual", f"{activity-float(rhs):.3g}")
        rational = [Fraction(float(x)).limit_denominator(args.rational_limit) for x in result.x]
        equality_failures = []
        for name, row, rhs in eq:
            residual = sum(rational[j]*c for j,c in row.items()) - rhs
            if residual:
                equality_failures.append((name, residual))
        inequality_failures = []
        minimum_slack = None
        for name, row, rhs in ub:
            slack = rhs - sum(rational[j]*c for j,c in row.items())
            if minimum_slack is None or slack < minimum_slack:
                minimum_slack = slack
            if slack < 0:
                inequality_failures.append((name, slack))
        domain_failures = sum(x < 0 for x in rational)
        print(
            "rational_reconstruction", "exact" if not equality_failures and not inequality_failures and not domain_failures else "failed",
            "limit", args.rational_limit,
            "max_denominator", max(x.denominator for x in rational),
            "equality_failures", len(equality_failures),
            "inequality_failures", len(inequality_failures),
            "domain_failures", domain_failures,
            "minimum_slack", minimum_slack,
        )
        for failure in equality_failures[:5]:
            print("equality_failure", *failure)
        for failure in inequality_failures[:5]:
            print("inequality_failure", *failure)

        # A HiGHS basic solution is sparse.  Project its positive support onto
        # exact rational equalities plus all numerically active inequalities,
        # using rank-revealing QR only to choose a square subsystem.  The
        # resulting point is accepted only after definition-level Fraction
        # checks of every original row and domain.
        support = [i for i, x in enumerate(result.x) if x > 1e-9]
        candidate_rows = [("eq", i, row, rhs) for i, (_name, row, rhs) in enumerate(eq)]
        for i, (_name, row, rhs) in enumerate(ub):
            activity = sum(result.x[j]*float(c) for j,c in row.items())
            scale = max(1.0, abs(float(rhs)), abs(activity))
            if float(rhs) - activity <= 1e-8 * scale:
                candidate_rows.append(("ub", i, row, rhs))
        # Preserve every nonzero integral coordinate exactly during rational
        # projection of a MILP incumbent.  Zero coordinates are outside the
        # positive support and are already fixed to zero.
        for j in sorted(integral_indices):
            if result.x[j] > 1e-9:
                nearest = round(float(result.x[j]))
                if abs(float(result.x[j]) - nearest) > 1e-6:
                    raise RuntimeError(f"nonintegral MILP incumbent at {variables[j]}")
                candidate_rows.append(("int", j, {j: Fraction(1)}, Fraction(nearest)))
        dense = np.array([
            [float(row.get(j, 0)) for j in support]
            for _kind, _index, row, _rhs in candidate_rows
        ])
        if dense.size:
            _q, rmat, col_order = qr(dense, mode="economic", pivoting=True)
            diag = np.abs(np.diag(rmat))
            rank = int(np.count_nonzero(diag > (diag[0] if len(diag) else 1) * 1e-10))
        else:
            col_order, rank = np.array([], dtype=int), 0
        pivot_positions = list(map(int, col_order[:rank]))
        free_positions = [i for i in range(len(support)) if i not in set(pivot_positions)]
        pivot_columns = [support[i] for i in pivot_positions]
        free_columns = [support[i] for i in free_positions]
        pivot_dense = dense[:, pivot_positions]
        _q, rmat, row_order = qr(pivot_dense.T, mode="economic", pivoting=True)
        chosen_rows = list(map(int, row_order[:rank]))

        exact = [Fraction(0) for _ in variables]
        for j in free_columns:
            exact[j] = Fraction(float(result.x[j])).limit_denominator(args.rational_limit)
        matrix = []
        vector = []
        for row_number in chosen_rows:
            _kind, _index, row, rhs = candidate_rows[row_number]
            matrix.append([row.get(j, Fraction(0)) for j in pivot_columns])
            vector.append(rhs - sum(row.get(j, Fraction(0))*exact[j] for j in free_columns))

        # Exact Gauss-Jordan elimination on the selected nonsingular system.
        exact_projection = "exact"
        try:
            for column in range(rank):
                pivot = next(i for i in range(column, rank) if matrix[i][column])
                matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
                vector[column], vector[pivot] = vector[pivot], vector[column]
                value = matrix[column][column]
                matrix[column] = [x / value for x in matrix[column]]
                vector[column] /= value
                for i in range(rank):
                    if i == column or not matrix[i][column]:
                        continue
                    value = matrix[i][column]
                    matrix[i] = [a - value*b for a, b in zip(matrix[i], matrix[column])]
                    vector[i] -= value*vector[column]
            for j, value in zip(pivot_columns, vector):
                exact[j] = value
        except (StopIteration, ZeroDivisionError):
            exact_projection = "singular_selection"

        exact_eq_fail = []
        exact_ub_fail = []
        exact_min_slack = None
        if exact_projection == "exact":
            for name, row, rhs in eq:
                residual = sum(exact[j]*c for j,c in row.items()) - rhs
                if residual:
                    exact_eq_fail.append((name, residual))
            for name, row, rhs in ub:
                slack = rhs - sum(exact[j]*c for j,c in row.items())
                if exact_min_slack is None or slack < exact_min_slack:
                    exact_min_slack = slack
                if slack < 0:
                    exact_ub_fail.append((name, slack))
            if any(x < 0 for x in exact):
                exact_projection = "negative_coordinate"
            elif exact_eq_fail:
                exact_projection = "equality_failure"
            elif exact_ub_fail:
                exact_projection = "inequality_failure"
        print(
            "exact_projection", exact_projection,
            "support", len(support), "rank", rank, "free", len(free_columns),
            "max_denominator", max((x.denominator for x in exact), default=1),
            "equality_failures", len(exact_eq_fail),
            "inequality_failures", len(exact_ub_fail),
            "minimum_slack", exact_min_slack,
        )
        if exact_projection == "exact":
            print(
                "exact_degree_counts",
                *(f"{d}:{exact[where[('n', d)]]}" for d in range(20, 25)),
            )
            print(
                "exact_dense_mass",
                sum(exact[where[('y', 'h', 24, e)]] for e in range(126, 133)),
            )
        for failure in exact_eq_fail[:5]:
            print("exact_equality_failure", *failure)
        for failure in exact_ub_fail[:5]:
            print("exact_inequality_failure", *failure)
        if exact_projection == "exact" and args.witness:
            payload = {
                "status": "EXACT_RATIONAL_FEASIBLE_FOUR_DECK_RELAXATION",
                "variables": len(variables),
                "equalities": len(eq),
                "inequalities": len(ub),
                "integral_variable_kinds": sorted({variables[i][0] for i in integral_indices}),
                "positive": [
                    {"variable": list(variables[i]), "numerator": str(x.numerator),
                     "denominator": str(x.denominator)}
                    for i, x in enumerate(exact) if x
                ],
            }
            args.witness.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            print("witness", args.witness)
    else:
        print("certificate_available", bool(
            not (args.integer_occurrences or args.integer_decks)
            and result.ineqlin.marginals is not None
        ))


if __name__ == "__main__":
    main()
