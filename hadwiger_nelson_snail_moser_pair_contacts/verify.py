#!/usr/bin/env python3
"""Standalone exact verification of the Snail--Moser pair-contact census."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
N = 16
ZERO = (Q(0),) * N
ONE = (Q(1),) + (Q(0),) * (N - 1)
FACTORS = tuple(
    (-3 if mask & 1 else 1)
    * (-11 if mask & 2 else 1)
    * (5 if mask & 4 else 1)
    for mask in range(8)
)
MOD = 1_000_000_321
ROOTS = (11_447_578, 70_971_245, 387_152_957, 315_670_077)
SEED_SHA256 = "9d03aaf2233e7b96109484a1fe3c8d311025bb95186b6927d517d716e774f614"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def basis(index):
    return tuple(Q(index == i) for i in range(N))


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def scale(x, scalar):
    return tuple(scalar * a for a in x)


def mul8(x, y):
    out = [Q(0)] * 8
    for i, a in enumerate(x):
        if a:
            for j, b in enumerate(y):
                if b:
                    out[i ^ j] += a * b * FACTORS[i & j]
    return tuple(out)


def mul(x, y):
    # Tower basis A^a B^b C^c E^e, with
    # A^2=-3, B^2=-11, C^2=5, E^2=-3320+632AB.
    low = list(mul8(x[:8], y[:8]))
    high = add(mul8(x[:8], y[8:]), mul8(x[8:], y[:8]))
    for i, coefficient in enumerate(mul8(x[8:], y[8:])):
        low[i] -= 3320 * coefficient
        low[i ^ 3] += 632 * coefficient * FACTORS[i & 3]
    return tuple(low) + high


def bar(x):
    # A, B and E are imaginary; C is real.
    return tuple(-a if (i & 11).bit_count() % 2 else a
                 for i, a in enumerate(x))


def norm(x):
    return mul(x, bar(x))


def inverse(x):
    columns = [mul(x, basis(i)) for i in range(N)]
    rows = [[columns[j][i] for j in range(N)] + [Q(i == 0)]
            for i in range(N)]
    for column in range(N):
        pivot = next((row for row in range(column, N)
                      if rows[row][column]), None)
        need(pivot is not None, "zero divisor in inverse")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        leading = rows[column][column]
        rows[column] = [value / leading for value in rows[column]]
        for row in range(N):
            if row != column and rows[row][column]:
                leading = rows[row][column]
                rows[row] = [a - leading * b
                             for a, b in zip(rows[row], rows[column])]
    answer = tuple(row[-1] for row in rows)
    need(mul(x, answer) == ONE, "inverse identity")
    return answer


def linear(*terms):
    out = ZERO
    for coefficient, value in terms:
        out = add(out, scale(value, Q(coefficient)))
    return out


def source_points(rows):
    need(len(rows) == 27, "source row count")
    need(all(len(row) == 4 and all(type(x) is int for x in row)
             for row in rows), "source row format")
    A, B, C, E = (basis(i) for i in (1, 2, 4, 8))
    w = scale(add(ONE, A), Q(1, 2))
    eta = scale(add(scale(ONE, 5), B), Q(1, 6))
    weta = mul(w, eta)
    p = add(
        linear((3, ONE), (Q(17, 8), w), (Q(-7, 8), eta), (2, weta)),
        mul(C, linear((Q(-1, 4), ONE), (Q(1, 8), w),
                      (Q(-1, 8), eta), (Q(1, 4), weta))),
    )
    q = add(
        linear((Q(11, 4), ONE), (Q(13, 8), w),
               (Q(-1, 8), eta), (2, weta)),
        scale(mul(E, linear((-1, w), (1, eta), (1, weta))), Q(1, 64)),
    )
    snail = (p, q) + tuple(
        linear((a, ONE), (b, w), (c, eta), (d, weta))
        for a, b, c, d in rows
    )
    moser = (ZERO, ONE, w, add(ONE, w), eta, mul(eta, w),
             mul(eta, add(ONE, w)))
    need(len(set(snail)) == 29, "Snail points distinct")
    need(len(set(moser)) == 7, "Moser points distinct")
    return snail, moser


def apply(transform, point):
    translation, multiplier, flip = transform
    return add(translation, mul(multiplier, bar(point) if flip else point))


def distance_classes(points):
    classes = defaultdict(list)
    for i, j in combinations(range(len(points)), 2):
        classes[norm(sub(points[j], points[i]))].append((i, j))
    return classes


def pair_contact_placements(snail, moser):
    snail_classes = distance_classes(snail)
    moser_classes = distance_classes(moser)
    source = {}
    for pair in combinations(range(7), 2):
        x0, x1 = (moser[i] for i in pair)
        for flip in (False, True):
            difference = sub(bar(x1) if flip else x1,
                             bar(x0) if flip else x0)
            source[pair, flip] = (x0, inverse(difference))
    by_transform = {}
    recipe_count = 0
    for distance, moser_pairs in moser_classes.items():
        for mi, mj in moser_pairs:
            for si, sj in snail_classes.get(distance, ()):
                for flip in (False, True):
                    x0, inverse_difference = source[(mi, mj), flip]
                    for swap in (False, True):
                        recipe = (mi, mj, si, sj, int(flip), int(swap))
                        y0, y1 = snail[si], snail[sj]
                        if swap:
                            y0, y1 = y1, y0
                        multiplier = mul(sub(y1, y0), inverse_difference)
                        translation = sub(
                            y0,
                            mul(multiplier, bar(x0) if flip else x0),
                        )
                        transform = (translation, multiplier, flip)
                        need(norm(multiplier) == ONE, "nonisometric recipe")
                        need(apply(transform, moser[mi]) == y0,
                             "first endpoint")
                        need(apply(transform, moser[mj]) == y1,
                             "second endpoint")
                        recipe_count += 1
                        if transform not in by_transform or recipe < by_transform[transform]:
                            by_transform[transform] = recipe
    placements = tuple(sorted(
        ((recipe, transform) for transform, recipe in by_transform.items()),
        key=lambda item: item[0],
    ))
    return recipe_count, placements


def evaluate(x):
    answer = 0
    for index, coefficient in enumerate(x):
        need(coefficient.denominator % MOD != 0, "bad modular denominator")
        value = coefficient.numerator * pow(coefficient.denominator, -1, MOD)
        for bit, root in enumerate(ROOTS):
            if index & (1 << bit):
                value = value * root % MOD
        answer = (answer + value) % MOD
    return answer


def physical_graph(snail, moser, transform):
    addresses = snail + tuple(apply(transform, point) for point in moser)
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
    values = [evaluate(point) for point in points]
    conjugates = [evaluate(bar(point)) for point in points]
    edges = []
    false_modular = 0
    for i, j in combinations(range(len(points)), 2):
        if (values[i] - values[j]) * (conjugates[i] - conjugates[j]) % MOD == 1:
            if norm(sub(points[i], points[j])) == ONE:
                edges.append((i, j))
            else:
                false_modular += 1
    terminals = tuple(class_of[29 + i] for i in range(7))
    need(len(set(terminals)) == 7, "Moser collision")
    return classes, tuple(edges), terminals, false_modular


def canonical_patterns(moser):
    edges = tuple((i, j) for i, j in combinations(range(7), 2)
                  if norm(sub(moser[i], moser[j])) == ONE)
    need(len(edges) == 11, "Moser edge count")
    patterns = []
    for tail in product(range(4), repeat=4):
        pattern = (0, 1, 2) + tail
        if all(pattern[i] != pattern[j] for i, j in edges):
            patterns.append(pattern)
    need(len(patterns) == 16, "canonical Moser pattern count")
    three_colourings = sum(
        all(word[i] != word[j] for i, j in edges)
        for word in product(range(3), repeat=7)
    )
    need(three_colourings == 0, "Moser unexpectedly three-colourable")
    return edges, tuple(patterns)


def find_extension(order, edges, terminals, pattern):
    adjacency = [set() for _ in range(order)]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    colours = [-1] * order
    for vertex, colour in zip(terminals, pattern):
        need(colours[vertex] in (-1, colour), "inconsistent terminal pin")
        colours[vertex] = colour
    need(all(colours[i] != colours[j] or colours[i] == -1
             for i, j in edges), "improper terminal pattern")
    nodes = 0

    def search():
        nonlocal nodes
        nodes += 1
        best_vertex = None
        best_allowed = None
        best_key = None
        for vertex, colour in enumerate(colours):
            if colour != -1:
                continue
            used = {colours[w] for w in adjacency[vertex] if colours[w] != -1}
            allowed = tuple(c for c in range(4) if c not in used)
            if not allowed:
                return False
            key = (len(allowed), -len(adjacency[vertex]), vertex)
            if best_key is None or key < best_key:
                best_vertex, best_allowed, best_key = vertex, allowed, key
        if best_vertex is None:
            return True
        for colour in best_allowed:
            colours[best_vertex] = colour
            if search():
                return True
        colours[best_vertex] = -1
        return False

    need(search(), "nonextending Moser pattern")
    need(all(colours[i] != colours[j] for i, j in edges), "bad extension word")
    need(tuple(colours[v] for v in terminals) == pattern,
         "terminal word mismatch")
    return tuple(colours), nodes


def canonical_line(value):
    return json.dumps(value, separators=(",", ":"), sort_keys=True) + "\n"


def verify():
    roots = ROOTS
    need((roots[0] * roots[0] + 3) % MOD == 0, "A root")
    need((roots[1] * roots[1] + 11) % MOD == 0, "B root")
    need((roots[2] * roots[2] - 5) % MOD == 0, "C root")
    need((roots[3] * roots[3] + 3320 - 632 * roots[0] * roots[1]) % MOD == 0,
         "E root")
    seed_path = ROOT / "hadwiger_nelson_snail_dihedral" / "seed.json"
    need(hashlib.sha256(seed_path.read_bytes()).hexdigest() == SEED_SHA256,
         "source seed hash")
    source = json.loads(seed_path.read_text())
    snail, moser = source_points(source["moser_rows"])
    moser_edges, patterns = canonical_patterns(moser)
    snail_edges = sum(norm(sub(snail[i], snail[j])) == ONE
                      for i, j in combinations(range(29), 2))
    recipe_count, placements = pair_contact_placements(snail, moser)
    need(len(placements) == 1698, "placement count")
    geometry_hash = hashlib.sha256()
    witness_hash = hashlib.sha256()
    recipe_hash = hashlib.sha256()
    order_counts = Counter()
    edge_counts = Counter()
    overlap_counts = Counter()
    relation_sizes = Counter()
    search_nodes = 0
    false_modular = 0
    all_pairs = 0
    for placement_index, (recipe, transform) in enumerate(placements):
        recipe_hash.update(canonical_line(recipe).encode())
        classes, edges, terminals, false = physical_graph(snail, moser, transform)
        false_modular += false
        all_pairs += len(classes) * (len(classes) - 1) // 2
        order_counts[len(classes)] += 1
        edge_counts[len(edges)] += 1
        overlap_counts[36 - len(classes)] += 1
        geometry_hash.update(canonical_line({
            "recipe": recipe,
            "classes": classes,
            "edges": edges,
        }).encode())
        allowed = 0
        for pattern_index, pattern in enumerate(patterns):
            word, nodes = find_extension(len(classes), edges, terminals, pattern)
            search_nodes += nodes
            allowed += 1
            witness_hash.update(
                f"{placement_index}:{pattern_index}:{''.join(map(str, word))}\n".encode()
            )
        relation_sizes[allowed] += 1
    need(relation_sizes == {16: 1698}, "neutral relation census")
    return {
        "verified": True,
        "source_vertices": 29,
        "source_strict_unit_edges": snail_edges,
        "moser_vertices": 7,
        "moser_strict_unit_edges": len(moser_edges),
        "canonical_moser_patterns": len(patterns),
        "ordered_pair_mapping_recipes": recipe_count,
        "distinct_exact_placements": len(placements),
        "physical_order_counts": dict(sorted(order_counts.items())),
        "strict_unit_edge_counts": dict(sorted(edge_counts.items())),
        "overlap_counts": dict(sorted(overlap_counts.items())),
        "relation_size_counts": dict(sorted(relation_sizes.items())),
        "all_physical_pairs_screened": all_pairs,
        "modular_false_positives_checked": false_modular,
        "positive_extension_words_checked": len(placements) * len(patterns),
        "deterministic_search_nodes": search_nodes,
        "fresh_modulus": MOD,
        "canonical_recipe_sha256": recipe_hash.hexdigest(),
        "physical_quotient_graphs_sha256": geometry_hash.hexdigest(),
        "extension_words_sha256": witness_hash.hexdigest(),
        "every_proper_moser_pattern_extends": True,
        "every_union_exactly_four_chromatic": True,
        "record_improvement": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    output = verify()
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        # JSON object keys are strings after decoding; normalize histogram keys.
        need(json.loads(json.dumps(output)) == expected, "EXPECTED.json mismatch")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
