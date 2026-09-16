#!/usr/bin/env python3
"""Exact positive-word checker for the frozen EI19 first lens closure."""

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from intervals import I, ONE, Q, norm, subtract

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_ei19_terminal_boundary"
SOURCE_CERT_SHA256 = "59e5ead5664daebcc2a68d83c14320976723b69eac7a566a5b4256946ae66fc4"
SOURCE_CHECKER_SHA256 = "de149b5ae8d09bdd9115f6d844e2532503923e2761cf6eb5532a7f0a1f50b6a2"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def replay_source_geometry():
    cert_path = SOURCE / "geometry_certificate.json"
    checker_path = SOURCE / "geometry.py"
    require(hashlib.sha256(cert_path.read_bytes()).hexdigest() == SOURCE_CERT_SHA256,
            "source geometry hash")
    require(hashlib.sha256(checker_path.read_bytes()).hexdigest() == SOURCE_CHECKER_SHA256,
            "source checker hash")
    spec = importlib.util.spec_from_file_location("ei19_source_geometry", checker_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = module.verify(cert_path)
    require(report["status"] == "EXACT ISOLATED EI19 SUPPORT VERIFIED",
            "source geometry replay")
    return json.loads(cert_path.read_text()), report

def source_intervals(certificate):
    denominator = certificate["point_denominator"]
    radius = Fraction(1, certificate["radius_denominator"])
    points = []
    for vertex, row in enumerate(certificate["centre_numerators"]):
        point = []
        for numerator in row:
            midpoint = Fraction(numerator, denominator)
            r = Fraction(0) if vertex in (0, 1) else radius
            point.append(I(I.rational(midpoint-r).lo, I.rational(midpoint+r).hi))
        points.append(tuple(point))
    return points

def first_lens_closure(points):
    answer = list(points)
    included = []
    four = I.rational(4)
    quarter = I.rational(Fraction(1, 4))
    half = I.rational(Fraction(1, 2))
    for i, j in combinations(range(19), 2):
        a, b = points[i], points[j]
        dx, dy = subtract(b, a)
        d2 = norm((dx, dy))
        require(d2.lo > 0 and not d2.contains(4),
                f"unresolved duplicate/tangent source pair {i},{j}")
        if d2.lo > four.hi:
            continue
        require(d2.hi < four.lo, f"unresolved circle existence {i},{j}")
        factor = (ONE/d2-quarter).sqrt()
        mx, my = (a[0]+b[0])*half, (a[1]+b[1])*half
        for sign in (-1, 1):
            s = I.rational(sign)
            answer.append((mx-s*dy*factor, my+s*dx*factor))
        included.append((i, j))
    return answer, included

def three_colour_exhaustion(edges):
    neighbours = [set() for _ in range(19)]
    for u, v in edges:
        neighbours[u].add(v); neighbours[v].add(u)
    colours = [-1]*19
    colours[0], colours[1] = 0, 1
    nodes = 0
    def visit():
        nonlocal nodes
        nodes += 1
        left = [v for v in range(19) if colours[v] < 0]
        if not left:
            return True
        forbidden = {v:{colours[w] for w in neighbours[v] if colours[w]>=0}
                     for v in left}
        vertex = max(left, key=lambda v:(len(forbidden[v]),len(neighbours[v]),-v))
        for colour in range(3):
            if colour not in forbidden[vertex]:
                colours[vertex] = colour
                if visit(): return True
        colours[vertex] = -1
        return False
    require(not visit(), "EI19 unexpectedly three-colourable")
    return nodes

def validate_word(points, word):
    require(len(word)==len(points) and set(word)<=set("0123"), "word schema")
    same = different = 0
    unit_gap = coordinate_gap = None
    for i, j in combinations(range(len(points)), 2):
        p, q = points[i], points[j]
        if word[i] != word[j]:
            gap = max(max(b.lo-a.hi, a.lo-b.hi) for a,b in zip(p,q))
            require(gap > 0, f"different-colour labels could coincide: {i},{j}")
            coordinate_gap = gap if coordinate_gap is None else min(coordinate_gap,gap)
            different += 1
            continue
        lower = upper = 0
        for a,b in zip(p,q):
            lo,hi = a.lo-b.hi,a.hi-b.lo
            lower += 0 if lo<=0<=hi else min(lo*lo,hi*hi)
            upper += max(lo*lo,hi*hi)
        gap = max(lower-Q*Q,Q*Q-upper)
        require(gap > 0, f"same-colour distance could be unit: {i},{j}")
        unit_gap = gap if unit_gap is None else min(unit_gap,gap)
        same += 1
    return {
        "formal_labels":len(points), "all_label_pairs":same+different,
        "same_colour_pairs":same, "different_colour_pairs":different,
        "same_colour_squared_unit_gap_lower_over_Q2":str(Fraction(unit_gap,Q*Q)),
        "different_colour_coordinate_gap_lower_over_Q":str(Fraction(coordinate_gap,Q)),
    }

def verify():
    certificate, geometry = replay_source_geometry()
    closure, included = first_lens_closure(source_intervals(certificate))
    word = (HERE/"four_word.txt").read_text().strip()
    colouring = validate_word(closure, word)
    nodes = three_colour_exhaustion(map(tuple,certificate["edge_equations"]))
    return {
        "status":"EXACT EI19 FIRST LENS CLOSURE FOUR-COLOUR STOP VERIFIED",
        "source_geometry":geometry, "source_vertices":19, "source_edges":35,
        "eligible_source_pairs":len(included), "formal_lens_labels":2*len(included),
        "physical_vertices_upper_bound":len(closure), "colouring":colouring,
        "source_three_colour_exhaustion_nodes":nodes, "chromatic_number":4,
        "record_candidate":False, "next_round_authorized":False,
        "word_sha256":hashlib.sha256((word+"\n").encode()).hexdigest(),
    }

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--check-expected",action="store_true")
    args=parser.parse_args()
    report=verify()
    if args.check_expected:
        require(report==json.loads((HERE/"EXPECTED.json").read_text()),
                "expected output mismatch")
    print(json.dumps(report,indent=2,sort_keys=True))
