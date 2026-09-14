#!/usr/bin/env python3
"""Definition-level all-pairs audit in the independent producer basis."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "hadwiger_nelson_snail_mixed_boxes"))
import geometry as G  # noqa: E402

F = G.F
D = F.D
ONE = G.ONE
W = G.q(F.W)
B = G.q(F.B)
ETA = G.scale(G.add(G.scale(ONE, 5), B), Q(1, 6))
MOSER = (
    G.ZERO,
    G.scale(ONE, D),
    G.scale(W, D),
    G.scale(G.add(ONE, W), D),
    G.scale(ETA, D),
    G.scale(G.mul(ETA, W), D),
    G.scale(G.mul(ETA, G.add(ONE, W)), D),
)
SNAIL = G.POINTS
UNIT = G.scale(ONE, D * D)
DEPENDENCIES = {
    ROOT / "hadwiger_nelson_snail_mixed_boxes" / "geometry.py":
        "b029a0c4494006be7a6e47246049030123c4593f057f41478349fbd841e192cd",
    ROOT / "hadwiger_nelson_snail_mixed_boxes" / "field_base.py":
        "2d25983290e6e912bc434f8286e6d2771d893949af83fb16433d1bb74b4bfc0e",
    ROOT / "hadwiger_nelson_snail_mixed_boxes" / "seed.json":
        "9d03aaf2233e7b96109484a1fe3c8d311025bb95186b6927d517d716e774f614",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def distance_classes(points):
    classes = defaultdict(list)
    for i, j in combinations(range(len(points)), 2):
        classes[G.norm(G.sub(points[j], points[i]))].append((i, j))
    return classes


def placements():
    snail_classes = distance_classes(SNAIL)
    moser_classes = distance_classes(MOSER)
    inverses = {}
    for pair in combinations(range(7), 2):
        x0, x1 = (MOSER[i] for i in pair)
        for flip in (False, True):
            difference = G.sub(G.bar(x1) if flip else x1,
                               G.bar(x0) if flip else x0)
            inverses[pair, flip] = (x0, G.inverse(difference))
    by_transform = {}
    recipes = 0
    for distance, moser_pairs in moser_classes.items():
        for mi, mj in moser_pairs:
            for si, sj in snail_classes.get(distance, ()):
                for flip in (False, True):
                    x0, inverse_difference = inverses[(mi, mj), flip]
                    for swap in (False, True):
                        recipe = (mi, mj, si, sj, int(flip), int(swap))
                        y0, y1 = SNAIL[si], SNAIL[sj]
                        if swap:
                            y0, y1 = y1, y0
                        multiplier = G.mul(G.sub(y1, y0), inverse_difference)
                        translation = G.sub(
                            y0,
                            G.mul(multiplier, G.bar(x0) if flip else x0),
                        )
                        transform = (translation, multiplier, flip)
                        need(G.norm(multiplier) == G.ONE, "nonisometry")
                        need(G.apply(transform, MOSER[mi]) == y0, "endpoint 0")
                        need(G.apply(transform, MOSER[mj]) == y1, "endpoint 1")
                        recipes += 1
                        if transform not in by_transform or recipe < by_transform[transform]:
                            by_transform[transform] = recipe
    return recipes, tuple(sorted(
        ((recipe, transform) for transform, recipe in by_transform.items()),
        key=lambda item: item[0],
    ))


def physical_graph(transform):
    addresses = SNAIL + tuple(G.apply(transform, point) for point in MOSER)
    classes_by_point = defaultdict(list)
    for address, point in enumerate(addresses):
        classes_by_point[point].append(address)
    classes = tuple(sorted((tuple(group) for group in classes_by_point.values()),
                           key=lambda group: group[0]))
    points = tuple(addresses[group[0]] for group in classes)
    class_of = {}
    for class_index, group in enumerate(classes):
        for address in group:
            class_of[address] = class_index
    # This audit intentionally performs the exact norm calculation for every
    # physical pair, without the verifier's finite-field rejection filter.
    edges = tuple((i, j) for i, j in combinations(range(len(points)), 2)
                  if G.norm(G.sub(points[i], points[j])) == UNIT)
    terminals = tuple(class_of[29 + i] for i in range(7))
    return classes, edges, terminals


def canonical_patterns():
    moser_edges = tuple((i, j) for i, j in combinations(range(7), 2)
                        if G.norm(G.sub(MOSER[i], MOSER[j])) == UNIT)
    need(len(moser_edges) == 11, "Moser edges")
    patterns = tuple(
        pattern for tail in product(range(4), repeat=4)
        for pattern in ((0, 1, 2) + tail,)
        if all(pattern[i] != pattern[j] for i, j in moser_edges)
    )
    need(len(patterns) == 16, "Moser patterns")
    need(not any(all(word[i] != word[j] for i, j in moser_edges)
                 for word in product(range(3), repeat=7)),
         "Moser three-colouring")
    return moser_edges, patterns


def find_extension(order, edges, terminals, pattern):
    adjacency = [set() for _ in range(order)]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    colours = [-1] * order
    for vertex, colour in zip(terminals, pattern):
        need(colours[vertex] in (-1, colour), "terminal collision")
        colours[vertex] = colour
    need(all(colours[i] != colours[j] or colours[i] == -1
             for i, j in edges), "terminal edge")
    nodes = 0

    def search():
        nonlocal nodes
        nodes += 1
        choice = None
        allowed_choice = None
        key_choice = None
        for vertex, colour in enumerate(colours):
            if colour != -1:
                continue
            used = {colours[w] for w in adjacency[vertex] if colours[w] != -1}
            allowed = tuple(c for c in range(4) if c not in used)
            if not allowed:
                return False
            key = (len(allowed), -len(adjacency[vertex]), vertex)
            if key_choice is None or key < key_choice:
                choice, allowed_choice, key_choice = vertex, allowed, key
        if choice is None:
            return True
        for colour in allowed_choice:
            colours[choice] = colour
            if search():
                return True
        colours[choice] = -1
        return False

    need(search(), "missing extension")
    need(all(colours[i] != colours[j] for i, j in edges), "bad word")
    need(tuple(colours[v] for v in terminals) == pattern, "bad pins")
    return tuple(colours), nodes


def line(value):
    return json.dumps(value, separators=(",", ":"), sort_keys=True) + "\n"


def audit():
    for path, expected_hash in DEPENDENCIES.items():
        need(hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash,
             f"dependency hash: {path.name}")
    moser_edges, patterns = canonical_patterns()
    recipe_count, cohort = placements()
    need(len(cohort) == 1698, "placement count")
    geometry_hash = hashlib.sha256()
    witness_hash = hashlib.sha256()
    recipe_hash = hashlib.sha256()
    orders = Counter()
    edges_histogram = Counter()
    overlaps = Counter()
    relations = Counter()
    nodes = 0
    pair_count = 0
    for placement_index, (recipe, transform) in enumerate(cohort):
        recipe_hash.update(line(recipe).encode())
        classes, edges, terminals = physical_graph(transform)
        orders[len(classes)] += 1
        edges_histogram[len(edges)] += 1
        overlaps[36 - len(classes)] += 1
        pair_count += len(classes) * (len(classes) - 1) // 2
        geometry_hash.update(line({
            "recipe": recipe,
            "classes": classes,
            "edges": edges,
        }).encode())
        allowed = 0
        for pattern_index, pattern in enumerate(patterns):
            word, used_nodes = find_extension(
                len(classes), edges, terminals, pattern
            )
            nodes += used_nodes
            allowed += 1
            witness_hash.update(
                f"{placement_index}:{pattern_index}:{''.join(map(str, word))}\n".encode()
            )
        relations[allowed] += 1
    return {
        "verified": True,
        "method": "exact_all_pairs_in_producer_basis",
        "ordered_pair_mapping_recipes": recipe_count,
        "distinct_exact_placements": len(cohort),
        "physical_order_counts": dict(sorted(orders.items())),
        "strict_unit_edge_counts": dict(sorted(edges_histogram.items())),
        "overlap_counts": dict(sorted(overlaps.items())),
        "relation_size_counts": dict(sorted(relations.items())),
        "all_physical_pairs_checked_exactly": pair_count,
        "positive_extension_words_checked": len(cohort) * len(patterns),
        "deterministic_search_nodes": nodes,
        "canonical_recipe_sha256": recipe_hash.hexdigest(),
        "physical_quotient_graphs_sha256": geometry_hash.hexdigest(),
        "extension_words_sha256": witness_hash.hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    output = audit()
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        mapping = {
            "all_physical_pairs_checked_exactly": "all_physical_pairs_screened",
        }
        for key, value in output.items():
            if key in ("verified", "method"):
                continue
            expected_key = mapping.get(key, key)
            normalized = json.loads(json.dumps(value))
            need(normalized == expected[expected_key], f"EXPECTED mismatch: {key}")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
