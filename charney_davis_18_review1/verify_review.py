#!/usr/bin/env python3
"""Independent exact audit for the 18-vertex Charney--Davis reduction.

This checker was written from the displayed identities and proof cases.  It
does not import the target package.  It checks symbolic linear identities,
the complete boundary-profile calculation, and the final max-degree-two
component argument.  It does not recognize homology spheres.
"""

from itertools import product
from math import comb
import json


VARIABLES = ("m", "su", "sv", "tu", "tv", "z")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def const(value):
    return (value,) + (0,) * len(VARIABLES)


def var(name):
    out = [0] * (len(VARIABLES) + 1)
    out[1 + VARIABLES.index(name)] = 1
    return tuple(out)


def add(*terms):
    return tuple(sum(term[i] for term in terms)
                 for i in range(len(VARIABLES) + 1))


def neg(term):
    return tuple(-coefficient for coefficient in term)


def sub(left, right):
    return add(left, neg(right))


def gamma2(d, vertices, edges):
    """Lemma 2.2: gamma_2 for a (d-1)-sphere."""
    return add(edges, const(-(2*d-3)*vertices + 2*d*(d-2)))


def check_link_identities():
    """Prove identities (2) and (3) as equalities of affine forms."""
    a = sub(const(39), var("m"))

    vertex_cases = 0
    for q in range(18):
        remaining = 17-q
        missing = add(var("m"), neg(var("su")), var("tu"))
        link_edges = sub(const(comb(remaining, 2)), missing)
        direct = gamma2(5, remaining, link_edges)
        displayed = add(a, const(8 + q*(q-19)//2),
                        var("su"), neg(var("tu")))
        require(direct == displayed, f"vertex-link identity at q={q}")
        vertex_cases += 1

    edge_cases = 0
    for q, r in product(range(8), repeat=2):
        remaining = 16-q-r
        missing = add(var("m"), neg(var("su")), neg(var("sv")),
                      var("tu"), var("tv"), var("z"))
        link_edges = sub(const(comb(remaining, 2)), missing)
        direct = gamma2(4, remaining, link_edges)
        lu = add(a, const(8 + q*(q-19)//2),
                 var("su"), neg(var("tu")))
        lv = add(a, const(8 + r*(r-19)//2),
                 var("sv"), neg(var("tv")))
        displayed = add(lu, lv, neg(a), const((q-1)*(r-1)),
                        neg(var("z")))
        require(direct == displayed,
                f"edge-link identity at degrees {(q, r)}")
        edge_cases += 1
    return vertex_cases, edge_cases


def enumerate_boundary_profiles():
    """Enumerate all degree moments with at most eight cubic vertices."""
    survivors = []
    no_lower_cubic_survivor = True
    for n3 in range(9):
        for n4 in range(19-n3):
            for n5 in range(19-n3-n4):
                for n6 in range(19-n3-n4-n5):
                    n7 = 18-n3-n4-n5-n6
                    counts = (n3, n4, n5, n6, n7)
                    degree_sum = sum(q*n for q, n in zip(range(3, 8), counts))
                    if degree_sum % 2:
                        continue
                    allowance = 90-8*n4-13*n5-15*n6-14*n7
                    if allowance < 0:
                        continue
                    for triangles in range(allowance//3 + 1):
                        S = allowance-3*triangles
                        require(S >= 0, "moment allowance")
                        if n3 < 8:
                            no_lower_cubic_survivor = False
                        a = 39-degree_sum//2
                        twice_b = (460 + sum(q*(q-11)*n
                                             for q, n in zip(range(3, 8), counts))
                                     - 2*triangles)
                        require(twice_b % 2 == 0, "gamma_3 integrality")
                        survivors.append({
                            "degrees_3_to_7": list(counts),
                            "triangles": triangles,
                            "a": a,
                            "b": twice_b//2,
                            "S": S,
                        })

    require(no_lower_cubic_survivor,
            "a profile with fewer than eight cubic vertices survived")
    expected_keys = [
        ((8, 8, 2, 0, 0), 0),
        ((8, 9, 0, 1, 0), 0),
        ((8, 9, 0, 1, 0), 1),
        ((8, 10, 0, 0, 0), 0),
        ((8, 10, 0, 0, 0), 1),
        ((8, 10, 0, 0, 0), 2),
        ((8, 10, 0, 0, 0), 3),
    ]
    actual_keys = [(tuple(item["degrees_3_to_7"]), item["triangles"])
                   for item in survivors]
    require(actual_keys == expected_keys, "boundary-profile list")
    require(all(item["b"] < 0 for item in survivors),
            "a boundary profile does not force negative gamma_3")
    return survivors


def component_types():
    """Classify the eight-vertex, girth>=5, max-degree-two cases."""
    types = []
    for cycle_counts in product(range(2), repeat=4):
        cycle_vertices = sum((length+5)*count
                             for length, count in enumerate(cycle_counts))
        if cycle_vertices > 8:
            continue
        for path_counts in product(*(range(8//length+1)
                                     for length in range(1, 9))):
            path_vertices = sum(length*path_counts[length-1]
                                for length in range(1, 9))
            if cycle_vertices + path_vertices != 8:
                continue
            edges = cycle_vertices + sum((length-1)*path_counts[length-1]
                                         for length in range(1, 9))
            if edges < 7:
                continue
            description = []
            for offset, count in enumerate(cycle_counts):
                description.extend([f"C{offset+5}"] * count)
            for length, count in enumerate(path_counts, start=1):
                description.extend([f"P{length}"] * count)
            types.append(description)

    types.sort()
    expected = [["C5", "P3"], ["C6", "P2"], ["C7", "P1"],
                ["C8"], ["P8"]]
    require(types == expected, "max-degree-two component classification")

    for description in types:
        adjacency = [set() for _ in range(8)]
        offset = 0
        for component in description:
            kind = component[0]
            size = int(component[1:])
            for i in range(size-1):
                u, v = offset+i, offset+i+1
                adjacency[u].add(v)
                adjacency[v].add(u)
            if kind == "C":
                adjacency[offset].add(offset+size-1)
                adjacency[offset+size-1].add(offset)
            offset += size
        witness = [(u, v) for u in range(8) for v in range(u+1, 8)
                   if len(adjacency[u]) == len(adjacency[v]) == 2
                   and v not in adjacency[u]
                   and adjacency[u].isdisjoint(adjacency[v])]
        require(witness, f"no final edge-link witness for {description}")
    return types


def contradiction_bounds():
    bounds = {
        # q=6: L_v=-25+sum neighbor degrees-t_v, all six <=4.
        "3^8_4^9_6_link_upper": -25 + 6*4,
        # Forced structure gives L_r=L_v=0 and z>=3.
        "3^8_4^8_5^2_edge_link_upper": 0+0-6+(5-1)*(3-1)-3,
        # A triangle component has L_u=0; outside it L_w<=2.
        "3^8_4^10_triangle_edge_link_upper": 0+2-7+(3-1)*(3-1),
        # Four vertices of R would have degree sum 12, versus this maximum.
        "3^8_4^10_degree3_J_max_sum": 2*3+4,
        # Final degree-two witnesses have L_u=L_v=1 and z>=0.
        "3^8_4^10_final_edge_link_upper": 1+1-7+(3-1)*(3-1),
    }
    require(bounds["3^8_4^9_6_link_upper"] == -1, "degree-six case")
    require(bounds["3^8_4^8_5^2_edge_link_upper"] == -1,
            "two-quintic case")
    require(bounds["3^8_4^10_triangle_edge_link_upper"] == -1,
            "triangle case")
    require(bounds["3^8_4^10_degree3_J_max_sum"] == 10,
            "degree-three-in-J case")
    require(bounds["3^8_4^10_final_edge_link_upper"] == -1,
            "final component case")
    return bounds


def sharp_example():
    # The complement of the one-skeleton of C6*C6*C6 has 18 cubic vertices.
    counts = (18, 0, 0, 0, 0)
    degree_sum = 54
    triangles = 6
    a = 39-degree_sum//2
    b = (460 + sum(q*(q-11)*n for q, n in zip(range(3, 8), counts))
         - 2*triangles)//2
    require((a, b) == (12, 8), "C6*C6*C6 gamma-vector check")
    return {"complement_degrees": "3^18", "triangles": triangles,
            "gamma": [1, 6, a, b]}


def main():
    vertex_cases, edge_cases = check_link_identities()
    report = {
        "status": "ACCEPT",
        "symbolic_vertex_link_degree_cases": vertex_cases,
        "symbolic_edge_link_degree_pairs": edge_cases,
        "boundary_profiles": enumerate_boundary_profiles(),
        "contradiction_bounds": contradiction_bounds(),
        "final_component_types": component_types(),
        "sharp_example": sharp_example(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
