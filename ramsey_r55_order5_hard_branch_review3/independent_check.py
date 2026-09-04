#!/usr/bin/env python3
"""Independent audit of the three-case hard order-five Ramsey reduction.

No target code is imported.  Degree profiles are counted by multiplicities,
marked incidences and local graphs are exhaustively rebuilt, and explicit
integer matrices show that none of the three aggregate k_ij systems is
already contradictory.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY/"ramsey_r55_order5_hard_branch"
EXTREMA = dict(zip(range(18, 25), (85, 92, 100, 107, 114, 122, 132)))
WEIGHT = dict(zip(range(18, 25), (21, 12, 3, 0, 3, 12, 21)))
COLUMNS = {0: (0, 1, 2, 3, 5, 5, 6, 6), 1: tuple(range(8))}
EDGES = tuple(combinations(range(8), 2))

# Values are in EDGES lexicographic order.  They are independently found
# witnesses for the complete aggregate systems (not Ramsey graph witnesses).
AGGREGATE_WITNESSES = {
    (0, 4, 1): (4,4,2,4,4,1,0,0,3,3,1,3,5,4,0,0,5,5,3,5,0,0,0,2,4,5,2,1),
    (1, 4, 0): (0,0,2,3,5,5,5,5,5,0,4,1,3,5,0,0,4,4,2,2,1,0,4,4,4,2,0,0),
    (1, 5, 1): (0,2,5,4,0,5,3,5,0,5,3,2,4,5,1,5,0,0,0,0,3,4,4,4,0,1,3,2),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def rotate(vertex):
    if vertex < 3:
        return vertex
    cycle, phase = divmod(vertex-3, 5)
    return 3+5*cycle+(phase+1) % 5


def orbit_histogram(items):
    remaining = set(items)
    histogram = Counter()
    while remaining:
        start = min(remaining)
        orbit = set()
        current = start
        while current not in orbit:
            orbit.add(current)
            current = tuple(sorted(rotate(v) for v in current))
        require(current == start, ("orbit does not return to minimum", start))
        remaining -= orbit
        histogram[len(orbit)] += 1
    return histogram


def multinomial(counts):
    answer = factorial(sum(counts))
    for count in counts:
        answer //= factorial(count)
    return answer


def degree_profile_audit():
    """Count assignments by degree multiplicity rather than a 3^8 product."""
    stages = Counter(total=3**8)
    survivors = set()
    for lows in range(9):
        for highs in range(9-lows):
            central = 8-lows-highs
            labeled = multinomial((lows, central, highs))
            weight = 3+15*(lows+highs)
            if weight > 39:
                continue
            stages["weight"] += labeled
            degree_sum = 62+5*(20*lows+21*central+22*highs)
            if degree_sum % 2:
                continue
            stages["parity"] += labeled
            red_edges = degree_sum//2
            if lows+highs == 0:
                base = comb(22, 2)-red_edges+20*21
                rounded_cap = 5*((EXTREMA[20]-7)//5)+5*((EXTREMA[22]-7)//5)
                require((base, rounded_cap) == (200, 195), "one-defect fixed cap")
                stages["one_defect_rejected"] += labeled
                continue

            require(lows+highs == 2 and weight == 33, "unexpected degree branch")
            red_local = 200+90+5*(lows*(EXTREMA[20]-7)
                                  +central*(EXTREMA[21]-7)
                                  +highs*(EXTREMA[22]-7))
            blue_local = 200+105+5*(lows*(EXTREMA[22]-7)
                                    +central*(EXTREMA[21]-7)
                                    +highs*(EXTREMA[20]-7))
            if red_local % 3 or blue_local % 3:
                stages["triangle_rejected"] += labeled
                continue
            stages["survives"] += labeled
            counts = (0, 0, 1+5*lows, 2+5*central, 5*highs, 0, 0)
            survivors.add((counts, red_edges, red_local//3, blue_local//3))

    require(stages == Counter(total=6561, weight=129, parity=113,
                              one_defect_rejected=1,
                              triangle_rejected=56, survives=56), stages)
    require(survivors == {((0,0,6,32,5,0,0),451,1430,1435)}, survivors)
    return stages


def swap_xy(mask):
    return (mask & 4) | ((mask & 1) << 1) | ((mask & 2) >> 1)


def marked_normal_forms():
    forms = []
    labeled_counts = {}
    for h, columns in COLUMNS.items():
        allowed = []
        for low, high in product(range(8), repeat=2):
            if low == high:
                continue
            low_mask, high_mask = columns[low], columns[high]
            weighted = tuple(5*(bool(high_mask & (1 << bit))
                                -bool(low_mask & (1 << bit))) for bit in range(3))
            if weighted == (0, 0, -5):
                allowed.append((low_mask, high_mask))
        labeled_counts[h] = len(allowed)
        quotient = {min(pair, (swap_xy(pair[0]), swap_xy(pair[1]))) for pair in allowed}
        for low_mask, high_mask in sorted(quotient):
            low = columns.index(low_mask)
            high = columns.index(high_mask)
            excluded = (low_mask & high_mask & 3) == 3
            forms.append((h, low, high, low_mask, high_mask, excluded))
    require(labeled_counts == {0: 4, 1: 4}, labeled_counts)
    require(forms == [(0,4,1,5,1,False), (1,4,0,4,0,False),
                      (1,5,1,5,1,False), (1,7,3,7,3,True)], forms)
    return forms


def local_adjacency(low_mask, high_mask, low_step, high_step, cross_word):
    adjacency = [[False]*13 for _ in range(13)]
    for a, b in combinations(range(13), 2):
        if b < 3:
            red = (a, b) == (0, 1)
        elif a < 3:
            mask = (low_mask, high_mask)[(b-3)//5]
            red = bool(mask & (1 << a))
        else:
            first_cycle, first_phase = divmod(a-3, 5)
            second_cycle, second_phase = divmod(b-3, 5)
            if first_cycle == second_cycle:
                step = (low_step, high_step)[first_cycle]
                separation = min(abs(first_phase-second_phase),
                                 5-abs(first_phase-second_phase))
                red = separation == step
            else:
                red = bool(cross_word & (1 << ((second_phase-first_phase) % 5)))
        adjacency[a][b] = adjacency[b][a] = red
    return adjacency


def forbidden_fives(adjacency):
    answer = []
    for vertices in combinations(range(len(adjacency)), 5):
        red_edges = sum(adjacency[a][b] for a, b in combinations(vertices, 2))
        if red_edges in (0, 10):
            answer.append(vertices)
    return answer


def local_pair_audit(forms):
    domains = {}
    tested = valid = 0
    for h, low, high, low_mask, high_mask, excluded in forms:
        rows = []
        for low_step, high_step in product((1, 2), repeat=2):
            good = []
            for positions in combinations(range(5), 3):
                word = sum(1 << position for position in positions)
                graph = local_adjacency(low_mask, high_mask, low_step, high_step, word)
                bad = forbidden_fives(graph)
                tested += 1
                if not bad:
                    good.append(word)
                    valid += 1
                if excluded:
                    require(any(0 in clique and 1 in clique and
                                all(graph[a][b] for a, b in combinations(clique, 2))
                                for clique in bad),
                            ("missing explicit xy red K5", low_step, high_step, word))
            good.sort()
            expected = (0 if excluded else
                        5 if (low_mask, high_mask) == (5,1) and low_step == high_step
                        else 10)
            require(len(good) == expected,
                    ("local word count", h, low_mask, high_mask, low_step, high_step))
            rows.append([low_step, high_step, good])
        domains[(h, low, high)] = rows
    require((tested, valid) == (160, 100), (tested, valid))
    return domains


def expected_case(h, low, high, domains):
    columns = COLUMNS[h]
    degrees = [21]*8
    degrees[low], degrees[high] = 20, 22
    return {
        "h": h,
        "columns": list(columns),
        "low_cycle": low,
        "high_cycle": high,
        "cycle_red_degrees": degrees,
        "row_sum_targets": [degree-2-mask.bit_count()
                            for degree, mask in zip(degrees, columns)],
        "low_high_red_cross_degree": 3,
        "normal_difference_targets": [[cycle, int(bool(mask & 4))]
            for cycle, mask in enumerate(columns) if cycle not in (low, high)],
        "fixed_cut_targets": {"R_x": 15-h, "R_y": 15-h,
                              "B_x": 16, "B_y": 16, "R_z": 14, "B_z": 17},
        "special_pair_word_domains": domains[(h, low, high)],
    }


def full_invariant_graph(case, values):
    adjacency = [[False]*43 for _ in range(43)]
    for a, b in combinations(range(43), 2):
        if b < 3:
            red = (a, b) == (0, 1)
        elif a < 3:
            red = bool(case["columns"][(b-3)//5] & (1 << a))
        else:
            first_cycle, first_phase = divmod(a-3, 5)
            second_cycle, second_phase = divmod(b-3, 5)
            if first_cycle == second_cycle:
                separation = min(abs(first_phase-second_phase),
                                 5-abs(first_phase-second_phase))
                red = separation == 1
            else:
                pair = tuple(sorted((first_cycle, second_cycle)))
                weight = values[EDGES.index(pair)]
                if first_cycle < second_cycle:
                    shift = (second_phase-first_phase) % 5
                else:
                    shift = (first_phase-second_phase) % 5
                red = shift < weight
        adjacency[a][b] = adjacency[b][a] = red
    return adjacency


def check_aggregate_witness(case, values):
    require(len(values) == 28 and all(0 <= value <= 5 for value in values),
            "aggregate witness box")
    k = dict(zip(EDGES, values))
    incident = lambda cycle: sum(value for edge, value in k.items() if cycle in edge)
    require([incident(i) for i in range(8)] == case["row_sum_targets"], "row sums")
    require(sum(values) == 70, "total cross degree")
    low, high = case["low_cycle"], case["high_cycle"]
    require(k[tuple(sorted((low, high)))] == 3, "exceptional cross degree")
    for cycle, target in case["normal_difference_targets"]:
        difference = (k[tuple(sorted((cycle, high)))]
                      -k[tuple(sorted((cycle, low)))])
        require(difference == target, ("ordinary difference", cycle, difference, target))
    for name, bit, red in (("R_x",1,True), ("R_y",2,True),
                           ("B_x",1,False), ("B_y",2,False),
                           ("R_z",4,True), ("B_z",4,False)):
        selected = [i for i, mask in enumerate(case["columns"])
                    if bool(mask & bit) == red]
        total = sum(k[pair] for pair in combinations(selected, 2))
        require(total == case["fixed_cut_targets"][name],
                ("fixed cut", name, total))

    graph = full_invariant_graph(case, values)
    actual_degrees = [sum(row) for row in graph]
    require(actual_degrees[:3] == [21,21,20], "fixed degrees")
    for cycle, target in enumerate(case["cycle_red_degrees"]):
        require(all(actual_degrees[3+5*cycle+phase] == target for phase in range(5)),
                ("moving degrees", cycle, target))
    expected_pairs = ((100,100), (100,100), (90,105))
    for fixed, expected in enumerate(expected_pairs):
        red = [v for v in range(43) if graph[fixed][v]]
        blue = [v for v in range(43) if v != fixed and not graph[fixed][v]]
        local_red = sum(graph[a][b] for a, b in combinations(red, 2))
        local_blue = sum(not graph[a][b] for a, b in combinations(blue, 2))
        require((local_red, local_blue) == expected,
                ("fixed local counts", fixed, local_red, local_blue))
    bad = forbidden_fives(graph)
    red_bad = sum(all(graph[a][b] for a, b in combinations(vertices, 2))
                  for vertices in bad)
    return red_bad, len(bad)-red_bad


def main():
    for fixed in range(3):
        pairs = combinations((v for v in range(43) if v != fixed), 2)
        require(orbit_histogram(pairs) == Counter({5: 172, 1: 1}),
                ("fixed pair orbit spectrum", fixed))
    require(orbit_histogram(combinations(range(43), 3)) == Counter({5: 2468, 1: 1}),
            "triangle orbit spectrum")

    degree_profile_audit()
    forms = marked_normal_forms()
    domains = local_pair_audit(forms)
    cases = [expected_case(h, low, high, domains)
             for h, low, high, _, _, excluded in forms if not excluded]

    handoff = json.loads((TARGET/"MARKED_CASES.json").read_text())
    require(handoff["cases"] == cases, "marked-case handoff differs")
    require({key: handoff[key] for key in
             ("red_degree_counts_18_to_24", "red_edges", "weight", "excess",
              "red_blue_triangles", "z_local_counts", "other_vertices_local_deficiency",
              "exact_anchor_count", "total_cross_degree_sum")} == {
        "red_degree_counts_18_to_24": [0,0,6,32,5,0,0],
        "red_edges": 451, "weight": 33, "excess": 5,
        "red_blue_triangles": [1430,1435], "z_local_counts": [90,105],
        "other_vertices_local_deficiency": 7, "exact_anchor_count": 32,
        "total_cross_degree_sum": 70,
    }, "global handoff fields")

    bad_counts = []
    for case in cases:
        key = (case["h"], case["low_cycle"], case["high_cycle"])
        bad_counts.append(check_aggregate_witness(case, AGGREGATE_WITNESSES[key]))
    require(bad_counts == [(490,2065), (1275,975), (1210,575)], bad_counts)
    witness_rows = [([*key], list(AGGREGATE_WITNESSES[key]))
                    for key in sorted(AGGREGATE_WITNESSES)]
    witness_digest = sha256(json.dumps(witness_rows, separators=(",", ":")).encode()).hexdigest()

    print("PASS fixed pair/triangle orbit spectra: 172+1 and 2468+1")
    print("PASS multiplicity degree census: 6561 -> 129 weight -> 113 parity")
    print("PASS unique profile after 1+56 rejections: 20^6,21^32,22^5")
    print("PASS m=451 W=33 excess=5; z pair=90,105; triangles=1430,1435")
    print("PASS marked incidence quotient: 8 labeled -> 4 forms -> 3 after xy-K5")
    print("PASS local two-cycle census: 160 assignments, 100 valid")
    print("PASS all three MARKED_CASES.json records independently reconstructed")
    print(f"PASS three full aggregate k_ij systems have explicit integer witnesses: {witness_digest}")
    print("INFO those aggregate witnesses have red/blue K5 counts: 490/2065,1275/975,1210/575")
    print("SCOPE aggregate witnesses are not Ramsey graphs; three global extensions remain unresolved")


if __name__ == "__main__":
    main()
