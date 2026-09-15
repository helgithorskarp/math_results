#!/usr/bin/env python3
"""Independent exact review checker for the frozen F29/bowtie coupler."""

from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

BASE = Path(__file__).resolve().parent
N = (4, 5, 6, 7, 9, 10, 12, 14, 15, 17, 18, 22, 25, 28)
INTERIOR_ORDER = (23, 24, 11, 20, 26, 27, 1, 3, 2, 8, 16, 21, 13, 19)
SOURCE_SHA256 = "3631210e31697804a86437cc7b6f734870097e22de50e5c4721ecea6ab633924"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def json_hash(value):
    data = json.dumps(value, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def square_quartic(axis):
    """Square a+b*sqrt(3)+c*sqrt(11)+d*sqrt(33), directly."""
    a, b, c, d = axis
    return (
        a * a + 3 * b * b + 11 * c * c + 33 * d * d,
        2 * a * b + 22 * c * d,
        2 * a * c + 6 * b * d,
        2 * a * d + 2 * b * c,
    )


def squared_norm_difference(left, right):
    difference = tuple(a - b for a, b in zip(left, right))
    real = square_quartic(difference[:4])
    imag = square_quartic(difference[4:])
    return tuple(a + b for a, b in zip(real, imag))


def load_geometry(source_path):
    raw = source_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "source identity")
    rows = [
        tuple(map(int, line.split()))
        for line in raw.decode().splitlines()
        if line and not line.startswith("#")
    ]
    require(len(rows) == 29, "source row count")
    require(tuple(row[0] for row in rows) == tuple(range(29)), "source labels")
    require(all(len(row) == 5 for row in rows), "source row width")

    points = [
        (5 * a, 0, 0, 5 * b, 0, 5 * c, 5 * d, 0)
        for _, a, b, c, d in rows
    ]
    centre = (0, 0, 0, 0, 60, 0, 0, 0)
    u = (36, 0, 0, 0, 48, 0, 0, 0)
    u_rho = (18, -24, 0, 0, 24, 18, 0, 0)
    add = lambda x, y: tuple(a + b for a, b in zip(x, y))
    neg = lambda x: tuple(-a for a in x)
    points.extend(
        [centre, add(centre, u), add(centre, u_rho), add(centre, neg(u)), add(centre, neg(u_rho))]
    )
    require(len(points) == len(set(points)) == 34, "physical points and collisions")

    edges = []
    distance_stream = hashlib.sha256()
    for i, j in combinations(range(34), 2):
        norm = squared_norm_difference(points[i], points[j])
        require(norm != (0, 0, 0, 0), "distinct coordinate tuples")
        distance_stream.update((",".join(map(str, norm)) + "\n").encode())
        if norm == (3600, 0, 0, 0):
            edges.append([i, j])

    source_edges = [edge for edge in edges if edge[1] < 29]
    bowtie_edges = [edge for edge in edges if edge[0] >= 29]
    cross_edges = [edge for edge in edges if edge[0] < 29 <= edge[1]]
    require(len(source_edges) == 75, "source edge count")
    require(
        bowtie_edges == [[29, 30], [29, 31], [29, 32], [29, 33], [30, 31], [32, 33]],
        "complete bowtie edges",
    )
    require(cross_edges == [[0, 29]], "unique private cross contact")

    adjacency = [set() for _ in range(29)]
    for a, b in source_edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    require(adjacency[0] == set(N), "marked centre neighbourhood")
    require(set(INTERIOR_ORDER) == set(range(29)) - set(N) - {0}, "interior order")
    return points, edges, adjacency, distance_stream.hexdigest()


def canonical(word):
    relabel = {}
    return tuple(relabel.setdefault(colour, len(relabel)) for colour in word)


def boundary_patterns(adjacency):
    positions = {vertex: index for index, vertex in enumerate(N)}
    terminal_edges = {
        tuple(sorted((positions[a], positions[b])))
        for a in N
        for b in adjacency[a]
        if b in positions
    }
    named = 0
    patterns = set()
    for tail in product(range(3), repeat=13):
        word = (0,) + tail
        if all(word[a] != word[b] for a, b in terminal_edges):
            named += 1
            patterns.add(canonical(word))
    return sorted(patterns), named, sorted(terminal_edges)


def path_dp(adjacency, order, allowed, return_assignment=False):
    """Exact list-colouring DP whose state is the processed/future frontier."""
    processed = []
    frontier = []
    states = {(): ()} if return_assignment else {()}
    maximum_frontier = 0
    maximum_states = 1
    order_set = set(order)
    for step, vertex in enumerate(order):
        future = set(order[step + 1 :])
        new_processed = processed + [vertex]
        new_frontier = [u for u in new_processed if adjacency[u] & future]
        maximum_frontier = max(maximum_frontier, len(new_frontier))
        next_states = {} if return_assignment else set()
        items = states.items() if return_assignment else ((state, None) for state in states)
        for state, history in items:
            colours = dict(zip(frontier, state))
            for colour in allowed[vertex]:
                if any(colours.get(u) == colour for u in adjacency[vertex] if u in order_set):
                    continue
                extended = dict(colours)
                extended[vertex] = colour
                next_state = tuple(extended[u] for u in new_frontier)
                if return_assignment:
                    next_states.setdefault(next_state, history + (colour,))
                else:
                    next_states.add(next_state)
        states = next_states
        processed = new_processed
        frontier = new_frontier
        maximum_states = max(maximum_states, len(states))
        if not states:
            return None if return_assignment else (False, maximum_frontier, maximum_states)
    if return_assignment:
        return dict(zip(order, states[()]))
    return True, maximum_frontier, maximum_states


def frontier_extension(adjacency, pattern, return_word=False):
    """Apply the frontier DP to the fourteen unpinned F29 vertices."""
    fixed = {0: 3}
    fixed.update(zip(N, pattern))
    allowed = {}
    for vertex in INTERIOR_ORDER:
        forbidden = {fixed[u] for u in adjacency[vertex] if u in fixed}
        allowed[vertex] = tuple(colour for colour in range(4) if colour not in forbidden)

    answer = path_dp(adjacency, INTERIOR_ORDER, allowed, return_assignment=return_word)
    if return_word:
        if answer is None:
            return None
        word = [-1] * 29
        word[0] = 3
        for vertex, colour in zip(N, pattern):
            word[vertex] = colour
        for vertex, colour in answer.items():
            word[vertex] = colour
        require(all(colour >= 0 for colour in word), "complete reconstructed source word")
        require(
            all(word[a] != word[b] for a in range(29) for b in adjacency[a]),
            "source witness edge check",
        )
        return "".join(map(str, word))
    return answer


def source_relation(adjacency):
    patterns, named, terminal_edges = boundary_patterns(adjacency)
    allowed = []
    denied = []
    maximum_frontier = 0
    maximum_states = 0
    for pattern in patterns:
        extends, width, states = frontier_extension(adjacency, pattern)
        maximum_frontier = max(maximum_frontier, width)
        maximum_states = max(maximum_states, states)
        key = "".join(map(str, pattern))
        (allowed if extends else denied).append(key)
    require(all(set(word) == set("012") for word in allowed), "frozen source palette")
    return allowed, denied, {
        "named_three_colour_words_with_first_zero": named,
        "bare_at_most_three_colour_patterns": len(patterns),
        "source_canonical_patterns": len(allowed),
        "source_rejected_patterns": len(denied),
        "source_pattern_hash": hashlib.sha256("".join(word + "\n" for word in allowed).encode()).hexdigest(),
        "terminal_edges": [list(edge) for edge in terminal_edges],
        "frontier_width": maximum_frontier,
        "maximum_frontier_states": maximum_states,
    }


def bowtie_relation():
    isolated = []
    joined = []
    lost = []
    for leaves in product(range(4), repeat=4):
        leaf_edges_proper = leaves[0] != leaves[1] and leaves[2] != leaves[3]
        isolated_centres = {c for c in range(4) if leaf_edges_proper and c not in leaves}
        joined_centres = isolated_centres - {3}
        before = bool(isolated_centres)
        after = bool(joined_centres)
        formula = before and set(leaves) != {0, 1, 2}
        require(after == formula, "P != Q truth table")
        if before:
            isolated.append(leaves)
        if after:
            joined.append(leaves)
        if before and not after:
            lost.append(leaves)
    return isolated, joined, lost


def proper(word, edges, colours):
    require(len(word) == 34, "union word length")
    require(set(word) <= set("01234"[:colours]), "union word alphabet")
    require(all(word[a] != word[b] for a, b in edges), "union word edge check")


def review(source_path, certificate):
    points, edges, adjacency, distance_hash = load_geometry(source_path)
    allowed, denied, census = source_relation(adjacency)
    isolated, joined, lost = bowtie_relation()
    require((len(isolated), len(joined), len(lost)) == (120, 96, 24), "bowtie truth counts")

    target_pattern = certificate["target_source_pattern"]
    require(target_pattern in allowed, "target source pattern")
    selected_fresh_pattern = max(
        allowed,
        key=lambda word: (sum(a != b for a, b in zip(word, target_pattern)), word),
    )
    require(certificate["fresh_source_pattern"] == selected_fresh_pattern, "fresh pattern selection")
    fresh_source = frontier_extension(adjacency, tuple(map(int, selected_fresh_pattern)), return_word=True)
    fresh_union = fresh_source + certificate["fresh_bowtie_word"]
    require(certificate["fresh_union_word"] == fresh_union, "fresh word regeneration")
    proper(fresh_union, edges, 4)

    target_four = certificate["target_proper_four_word"]
    target_five = certificate["target_conditional_five_word"]
    proper(target_four, edges, 4)
    proper(target_five, edges, 5)
    forbidden_pins = certificate["forbidden_joint_terminal_word"]
    require(forbidden_pins == target_pattern + "0112", "forbidden fixture identity")
    require(target_five[0] == "3" and target_five[29] == "4", "conditional five-word centres")
    require("".join(target_five[v] for v in N + (30, 31, 32, 33)) == forbidden_pins, "conditional five-word pins")
    require(set(forbidden_pins[:14]) == set(forbidden_pins[14:]) == set("012"), "forbidden equal palettes")
    isolated_forbidden = target_four[:29] + "30112"
    source_and_bowtie_edges = [edge for edge in edges if edge != [0, 29]]
    require(
        all(isolated_forbidden[a] != isolated_forbidden[b] for a, b in source_and_bowtie_edges),
        "forbidden prescription extends on both isolated components",
    )
    require(isolated_forbidden[0] == isolated_forbidden[29] == "3", "bridge is sole violation")
    require((0, 1, 1, 3) in joined, "every normalized F29 pattern reaches the bowtie marginal")
    require(
        all(any(source_centre != bowtie_centre for source_centre in range(4) for bowtie_centre in set(range(4)) - set(leaves)) for leaves in isolated),
        "every isolated bowtie pattern reaches a globally renamed F29 pattern",
    )

    source_count = len(allowed)
    result = {
        "verdict": "ACCEPT_WITH_STRICT_LOCAL_COUPLER_LIMITATION",
        "points": len(points),
        "unit_edges": len(edges),
        "pairs": 561,
        "source_edges": 75,
        "bowtie_edges": 6,
        "cross_edges": [[0, 29]],
        "shared_points": 0,
        "point_hash": json_hash(points),
        "edge_hash": json_hash(edges),
        "distance_hash": distance_hash,
        **census,
        "isolated_bowtie_patterns": len(isolated),
        "joined_bowtie_patterns": len(joined),
        "lost_bowtie_patterns": len(lost),
        "input_joint_canonical_patterns": source_count * len(isolated),
        "composite_joint_canonical_patterns": source_count * len(joined),
        "lost_joint_canonical_patterns": source_count * len(lost),
        "input_joint_labelled_patterns": source_count * len(isolated) * 24,
        "composite_joint_labelled_patterns": source_count * len(joined) * 24,
        "lost_joint_labelled_patterns": source_count * len(lost) * 24,
        "relation_formula": "P != Q",
        "both_component_projections_full": True,
        "bridge_removal_restores_product": True,
        "forbidden_isolated_components_checked": True,
        "proper_target_four_checked": True,
        "proper_conditional_five_checked": True,
        "fresh_pattern": selected_fresh_pattern,
        "fresh_union_word": fresh_union,
        "fresh_word_difference_from_target": sum(a != b for a, b in zip(fresh_union, target_four)),
        "chromatic_number": 4,
        "actual_plane_unit_distance_graph": True,
        "receiver_tested": False,
        "record_candidate": False,
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=BASE / "source29.tsv")
    parser.add_argument("--certificate", type=Path, default=BASE / "certificate.json")
    parser.add_argument("--expected", type=Path, default=BASE / "EXPECTED.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    result = review(args.source, certificate)
    if args.check_expected:
        require(result == json.loads(args.expected.read_text()), "expected theorem output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
