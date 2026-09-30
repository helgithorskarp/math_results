#!/usr/bin/env python3
"""Independent bit-rotation/XOR audit of the prescribed C5 symmetry maximum.

No researcher module or orbit model is imported. The tree and lower witness
are public, untrusted inputs. Their coordinate/index bridges are explicit.
"""
import argparse
from collections import Counter
import hashlib
from itertools import permutations, product
import json
from math import comb
from pathlib import Path

TARGET = Path(__file__).resolve().parent.parent / "constant_weight_a18_6_5_c5_symmetry"
CERTIFICATE_SHA = "431654bebf14a97458507f14fda4b6732850287a92c2c154f92a1429720b1611"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def fixed_weight(n, weight):
    """Gosper's numeric successor, independent of tuple-combination generation."""
    if weight == 0:
        yield 0
        return
    word = (1 << weight) - 1
    while word < (1 << n):
        yield word
        low = word & -word
        following = word + low
        word = following | (((following ^ word) >> 2) // low)


def rotate(word):
    result = word & (7 << 15)
    for first in (0, 5, 10):
        segment = (word >> first) & 31
        result |= (((segment << 1) & 31) | (segment >> 4)) << first
    return result


def orbit(word):
    images = [word]
    for _ in range(4):
        images.append(rotate(images[-1]))
    require(rotate(images[-1]) == word, "order-five action failed")
    return tuple(sorted(set(images)))


def compatible(first, second):
    # Simultaneous rotation reduces every cross pair to this representative
    # and one of the five relative rotations of the second orbit.
    return all((first[0] ^ other).bit_count() >= 6 for other in second)


def source_key(words):
    """Only the certificate's published ordinal bridge uses point-tuple order."""
    return tuple(sorted(tuple(bits(word)) for word in words))


def model():
    all_words = list(fixed_weight(18, 5))
    require(len(all_words) == comb(18, 5)
            and len(set(all_words)) == len(all_words)
            and all(word.bit_count() == 5 for word in all_words), "Gosper domain")
    raw = {orbit(word) for word in all_words}
    require(set().union(*map(set, raw)) == set(all_words), "raw orbit coverage")
    require(Counter(map(len, raw)) == {1: 3, 5: 1713}, "raw orbit census")
    full = [words for words in raw if len(words) == 5
            and all((words[0] ^ word).bit_count() >= 6 for word in words[1:])]
    full.sort(key=source_key)
    # Verify the relative-rotation shortcut on every within-orbit pair.
    within_checks = 0
    for words in full:
        for i, first in enumerate(words):
            for second in words[i + 1:]:
                require((first ^ second).bit_count() >= 6, "internal distance")
                within_checks += 1
    adjacency = [0] * len(full)
    for i, first in enumerate(full):
        for j in range(i):
            if compatible(first, full[j]):
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
    return {"full": full, "adjacency": adjacency, "raw": raw,
            "within_orbit_distance_checks": within_checks}


def cliques_of_size(adjacency, allowed, size):
    """Exhaust all increasing cliques via recursive deletion/intersection."""
    result = []

    def visit(chosen, candidates):
        if len(chosen) == size:
            result.append(chosen)
            return
        if candidates.bit_count() < size - len(chosen):
            return
        while candidates:
            low = candidates & -candidates
            candidates ^= low
            vertex = low.bit_length() - 1
            visit(chosen + (vertex,), candidates & adjacency[vertex])

    visit((), allowed)
    return result


def all_links(context, point):
    full, adjacency = context["full"], context["adjacency"]
    ids = [i for i, words in enumerate(full) if words[0] & (1 << point)]
    allowed = sum(1 << i for i in ids)
    return ids, cliques_of_size(adjacency, allowed, 4)


def apply(word, permutation):
    return sum(1 << permutation[i] for i in bits(word))


def normalizer(context, representative, links, wanted_link):
    """Enumerate the complete normalizer fixing 17, rather than generator BFS."""
    full = context["full"]
    lookup = {words[0]: i for i, words in enumerate(full)}
    image_counts = Counter()
    point_permutations = set()
    conjugacy_basis_checks = 0
    wanted_permutation = None
    for cycle_permutation in permutations(range(3)):
        for multiplier in range(1, 5):
            for offsets in product(range(5), repeat=3):
                for swap in (False, True):
                    permutation = list(range(18))
                    for block in range(3):
                        for pos in range(5):
                            permutation[5 * block + pos] = (5 * cycle_permutation[block]
                                                           + (multiplier * pos + offsets[block]) % 5)
                    if swap:
                        permutation[15], permutation[16] = 16, 15
                    p = tuple(permutation)
                    require(sorted(p) == list(range(18)) and p[17] == 17,
                            "normalizer permutation")
                    require(p not in point_permutations, "duplicate normalizer parameter")
                    point_permutations.add(p)
                    for i in range(18):
                        left = apply(rotate(1 << i), p)
                        right = 1 << p[i]
                        for _ in range(multiplier):
                            right = rotate(right)
                        require(left == right, "normalizer conjugacy on basis")
                        conjugacy_basis_checks += 1
                    image = tuple(sorted(lookup[orbit(apply(full[i][0], p))[0]]
                                         for i in representative))
                    image_counts[image] += 1
                    if image == wanted_link and wanted_permutation is None:
                        wanted_permutation = p
    require(set(image_counts) == set(links), "complete normalizer link coverage")
    require(set(image_counts.values()) == {60}, "normalizer stabilizer fibers")
    require(wanted_permutation is not None, "lower witness link normalization")
    return ({"fixing_center_order": len(point_permutations),
             "link_orbit_size": len(image_counts), "link_stabilizer_order": 60,
             "conjugacy_basis_checks": conjugacy_basis_checks}, wanted_permutation)


def bound_tree(tree, candidates, target, adjacency, statistics):
    """Derive a clique upper bound bottom-up from a covering case split."""
    require(type(target) is int and target > 0, "completed forbidden clique")
    statistics["nodes"] += 1
    if tree == {"small": True}:
        require(candidates.bit_count() < target, "false cardinality leaf")
        statistics["cardinality_leaves"] += 1
        return candidates.bit_count()
    require(type(tree) is dict and set(tree) == {"colors", "children"}, "node format")
    classes, children = tree["colors"], tree["children"]
    require(type(classes) is list and type(children) is list, "node lists")
    covered = 0
    for color in classes:
        require(type(color) is list and color, "empty or malformed color")
        color_mask = 0
        for vertex in color:
            require(type(vertex) is int and 0 <= vertex < len(adjacency), "vertex range")
            bit = 1 << vertex
            require(not bit & (covered | color_mask), "repeated vertex")
            require(not adjacency[vertex] & color_mask, "color contains compatible pair")
            color_mask |= bit
        covered |= color_mask
    require(covered == candidates, "color partition misses or adds candidate")
    branch_vertices = [v for color in classes[target - 1:] for v in color]
    branch_vertices.reverse()
    require(len(children) == len(branch_vertices), "branch coverage")
    remaining = candidates
    upper = min(len(classes), target - 1)
    for vertex, child in zip(branch_vertices, children):
        branch_upper = 1 + bound_tree(child, remaining & adjacency[vertex],
                                      target - 1, adjacency, statistics)
        require(branch_upper < target, "child fails requested bound")
        upper = max(upper, branch_upper)
        remaining ^= 1 << vertex
        statistics["inclusion_branches"] += 1
    prefix = sum(1 << v for color in classes[:target - 1] for v in color)
    require(remaining == prefix, "residual case coverage")
    return upper


def check_certificate(context, certificate, links):
    require(type(certificate) is dict and set(certificate)
            == {"format", "representative", "residual", "target", "tree"}, "certificate format")
    require(certificate["format"] == "c5-multiway-color-v1"
            and type(certificate["target"]) is int and certificate["target"] == 10,
            "certificate target")
    require(certificate["representative"] == list(min(links)), "representative bridge")
    representative = min(links)
    full, adjacency = context["full"], context["adjacency"]
    remaining = (1 << len(full)) - 1
    for vertex in representative:
        remaining &= adjacency[vertex]
    residual = list(bits(remaining))
    require(certificate["residual"] == residual, "residual domain bridge")
    local_adjacency = []
    for vertex in residual:
        local_adjacency.append(sum(1 << j for j, other in enumerate(residual)
                                   if adjacency[vertex] & (1 << other)))
    statistics = {"nodes": 0, "cardinality_leaves": 0, "inclusion_branches": 0}
    upper = bound_tree(certificate["tree"], (1 << len(residual)) - 1,
                       10, local_adjacency, statistics)
    require(upper <= 9, "root upper bound")
    require(all(not full[i][0] & (1 << 17) for i in residual), "saturated point residual")
    return {"representative": list(representative), "residual_orbits": len(residual),
            "residual_edges": sum(a.bit_count() for a in local_adjacency) // 2,
            "clique_upper_bound": upper, "tree": statistics}, local_adjacency


def saturated_link_geometry(context, links, center):
    """Derive complete affine-plane and pair-replication consequences."""
    omitted = Counter()
    for link in links:
        words = [word for vertex in link for word in context["full"][vertex]]
        lines = [word ^ (1 << center) for word in words]
        support = 0
        for line in lines:
            require(line.bit_count() == 4, "link line rank")
            support |= line
        require(support.bit_count() == 16, "saturated link support")
        missing = list(bits(((1 << 18) - 1) ^ support ^ (1 << center)))
        require(len(missing) == 1 and missing[0] in {15, 16, 17} - {center},
                "link omitted fixed point")
        omitted[missing[0]] += 1
        pair_counts = Counter()
        for pair in fixed_weight(18, 2):
            if pair & support == pair:
                pair_counts[sum(pair & line == pair for line in lines)] += 1
        require(pair_counts == {1: 120}, "affine plane pair coverage")
        require(all(sum(line & (1 << i) != 0 for line in lines) == 5
                    for i in bits(support)), "affine plane replication")
        parallel = cliques_of_size(
            [sum(1 << j for j, other in enumerate(lines) if i != j and not line & other)
             for i, line in enumerate(lines)], (1 << 20) - 1, 4)
        require(len(parallel) == 5 and all(len(set().union(
            *(set(bits(lines[i])) for i in cls))) == 16 for cls in parallel),
            "affine parallel classes")
        require(Counter(i for cls in parallel for i in cls) == {i: 1 for i in range(20)},
                "parallel classes partition lines")
    return {"center": center, "saturated_links": len(links),
            "omitted_fixed_point_counts": {str(k): v for k, v in sorted(omitted.items())},
            "pairs_covered_once_per_link": 120, "parallel_classes_per_link": 5}


def witness(rows):
    require(len(rows) == 68 and all(len(row) == 18 and set(row) <= {"0", "1"}
                                  for row in rows), "witness binary format")
    words = [int(row[::-1], 2) for row in rows]
    require(len(set(words)) == 68 and all(word.bit_count() == 5 for word in words),
            "witness weight and distinctness")
    require(all((first ^ second).bit_count() >= 6 for i, first in enumerate(words)
                for second in words[i + 1:]), "witness distance")
    require({rotate(word) for word in words} == set(words), "witness symmetry")
    support = 0
    for word in words:
        support |= word
    require(support.bit_count() == 17, "classical witness support")
    triples = [triple for triple in fixed_weight(18, 3) if triple & support == triple]
    require(len(triples) == 680
            and all(sum(triple & word == triple for word in words) == 1 for triple in triples),
            "Steiner witness triple coverage")
    return {"words": 68, "pair_distance_checks": comb(68, 2), "used_points": 17,
            "Steiner_triples_checked": 680,
            "fixed_blocks": sum(rotate(word) == word for word in words),
            "point_replications": [sum(word & (1 << i) != 0 for word in words)
                                   for i in range(18)]}


def run(certificate_path, witness_path):
    raw = certificate_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA, "pinned certificate identity")
    certificate = json.loads(raw)
    context = model()
    ids, links = all_links(context, 17)
    tree, _ = check_certificate(context, certificate, links)
    rows = [row.strip() for row in witness_path.read_text().splitlines() if row.strip()]
    witness_result = witness(rows)
    saturated_center = next(i for i in (15, 16, 17)
                            if witness_result["point_replications"][i] == 20)
    center_swap = list(range(18))
    center_swap[saturated_center], center_swap[17] = 17, saturated_center
    moved_words = [apply(int(row[::-1], 2), center_swap) for row in rows]
    lookup = {words[0]: i for i, words in enumerate(context["full"])}
    wanted_link = tuple(sorted({lookup[orbit(word)[0]] for word in moved_words
                                if word & (1 << 17)}))
    normal, mapping = normalizer(context, min(links), links, wanted_link)
    inverse = tuple(mapping.index(i) for i in range(18))
    normalized_words = [apply(word, inverse) for word in moved_words]
    normalized_full = {lookup[orbit(word)[0]] for word in normalized_words
                       if len(orbit(word)) == 5}
    residual_clique = sorted(normalized_full - set(min(links)))
    require(len(normalized_full) == 13 and len(residual_clique) == 9,
            "positive residual clique size")
    require(set(min(links)) <= normalized_full
            and set(residual_clique) <= set(certificate["residual"]),
            "positive residual clique domain")
    require(all(context["adjacency"][i] & (1 << j) for pos, i in enumerate(residual_clique)
                for j in residual_clique[pos + 1:]), "positive nine-clique edges")
    tree["clique_exact_maximum"] = 9
    tree["positive_clique_global_ids"] = residual_clique
    tree["positive_clique_local_ids"] = [certificate["residual"].index(i)
                                          for i in residual_clique]
    geometry = []
    link_sets = {}
    for center in (15, 16, 17):
        _, choices = all_links(context, center)
        link_sets[center] = choices
        geometry.append(saturated_link_geometry(context, choices, center))
    # Consequential bounded refinement: classify compatibility of every pair
    # of saturated fixed-point links, without assuming a 68-word completion.
    pair_statistics = {}
    offsets = {15: 0, 16: len(link_sets[15]),
               17: len(link_sets[15]) + len(link_sets[16])}
    saturated_adjacency = [0] * sum(map(len, link_sets.values()))
    for first, second in ((15, 16), (15, 17), (16, 17)):
        profiles = Counter()
        for i, left in enumerate(link_sets[first]):
            allowed = (1 << len(context["full"])) - 1
            for vertex in left:
                allowed &= context["adjacency"][vertex] | (1 << vertex)
            for j, right in enumerate(link_sets[second]):
                if all(allowed & (1 << v) for v in right):
                    profiles[len(set(left) & set(right)) * 5] += 1
                    a, b = offsets[first] + i, offsets[second] + j
                    saturated_adjacency[a] |= 1 << b
                    saturated_adjacency[b] |= 1 << a
        pair_statistics[f"{first},{second}"] = {str(k): v for k, v in sorted(profiles.items())}
    saturated_triangles = cliques_of_size(saturated_adjacency,
                                         (1 << len(saturated_adjacency)) - 1, 3)
    require(not saturated_triangles, "three compatible saturated fixed-point links")
    result = {"reviewer": "six-reviewer-4", "role": "independent mathematical reviewer",
              "ground_set": 18, "weight": 5, "minimum_distance": 6,
              "cycle_type": "5^3 1^3", "word_domain": comb(18, 5),
              "raw_orbits": {str(k): v for k, v in sorted(Counter(map(len, context["raw"])).items())},
              "admissible_full_orbits": len(context["full"]),
              "within_orbit_distance_checks": context["within_orbit_distance_checks"],
              "full_compatibility_edges": sum(a.bit_count() for a in context["adjacency"]) // 2,
              "through_point17_orbits": len(ids), "degree20_links": len(links),
              "normalizer": normal, "residual_certificate": tree,
              "saturated_link_geometry": geometry, "compatible_saturated_link_pairs": pair_statistics,
              "saturated_link_compatibility_graph": {
                  "vertices": len(saturated_adjacency),
                  "edges": sum(a.bit_count() for a in saturated_adjacency) // 2,
                  "triangles": len(saturated_triangles),
                  "simultaneously_saturated_fixed_points_max": 2},
              "witness": witness_result, "restricted_maximum": 68,
              "certificate_sha256": hashlib.sha256(raw).hexdigest(),
              "source_order_full_orbits_sha256": hashlib.sha256(
                  (json.dumps([source_key(o) for o in context["full"]], separators=(",", ":")) + "\n").encode()).hexdigest(),
              "source_order_links_sha256": hashlib.sha256(
                  (json.dumps(sorted(links), separators=(",", ":")) + "\n").encode()).hexdigest(),
              "external_theorem": "Brouwer (1975), A(17,6,4)<=20, imported from primary paper",
              "general_bounds_improved": False}
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--certificate", type=Path, default=TARGET / "certificate.json")
    p.add_argument("--witness", type=Path, default=TARGET / "witness68.txt")
    p.add_argument("--expect", type=Path)
    args = p.parse_args()
    result = run(args.certificate, args.witness)
    if args.expect:
        require(result == json.loads(args.expect.read_text()), "complete expected output differs")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
