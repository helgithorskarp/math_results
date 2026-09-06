#!/usr/bin/env python3
"""Independent exact review of the frozen 544-row H632 transport.

The checker imports no submitted executable code. It rebuilds the exact H632
graph, reinterprets every raw old-colouring recipe, and decides list colouring
with generic DPLL/backtracking plus singleton propagation rather than either
submitted forest/cycle algorithm.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
import os
from pathlib import Path
import sys


DENOMINATOR = 96
EXPECTED_NORM_HASH = "f319dfe814bb9a2259a914b74c79adde9272422e4e761d57dc308fc750a638f7"
EXPECTED_FULL_EDGE_HASH = "b68794133915a87531627c09582dda5eeb959e5ddad03407280ad916d1b9b92e"
EXPECTED_LIBRARY_HASH = "f35fc4fc4d9e42c8d877f05b344de4fa374b17f954bea6b2c00b365d359d52bc"
EXPECTED_CASES_HASH = "1732ba3f438cec81bd83950bf8a54ac728ca6be7136489d9fc60688845fef630"
EXPECTED_LISTS_HASH = "3d7edada6564ae03cf604276dbc58915077a8242132cb2b9861d356628dccb7d"
EXPECTED_SINGLETONS = [11, 39, 48, 51, 81, 105, 142, 145, 168, 179, 199,
                       200, 212, 220, 225, 226, 241, 300, 328, 366, 473, 504]
EXPECTED_CYCLE = [1239, 1370, 1522, 1371]


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def file_record(path: Path) -> dict[str, int | str]:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def verify_sha256s(directory: Path) -> dict[str, dict[str, int | str]]:
    records = {}
    for line in (directory / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        expected, name = line.split(maxsplit=1)
        record = file_record(directory / name)
        require(record["sha256"] == expected, "submitted source hash: " + name)
        records[name] = record
    return records


def scaled_axis(raw: list[object]) -> tuple[int, ...]:
    values = [Fraction(value) * DENOMINATOR for value in raw]
    require(len(values) == 8 and all(value.denominator == 1 for value in values),
            "coordinate axis and denominator")
    return tuple(int(value) for value in values)


def scaled_point(raw: list[list[object]]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    require(isinstance(raw, list) and len(raw) == 2, "point has two axes")
    return scaled_axis(raw[0]), scaled_axis(raw[1])


def ring_product(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * 8
    for left_mask, left_value in enumerate(left):
        for right_mask, right_value in enumerate(right):
            overlap = left_mask & right_mask
            factor = 1
            for bit, prime in enumerate((3, 5, 11)):
                if overlap & (1 << bit):
                    factor *= prime
            result[left_mask ^ right_mask] += left_value * right_value * factor
    return tuple(result)


def exact_squared_distance(left, right) -> tuple[int, ...]:
    result = [0] * 8
    for axis in (0, 1):
        delta = tuple(a - b for a, b in zip(left[axis], right[axis]))
        square = ring_product(delta, delta)
        result = [a + b for a, b in zip(result, square)]
    return tuple(result)


def histogram(values) -> dict[str, int]:
    counts = Counter(values)
    return {str(key): counts[key] for key in sorted(counts)}


def decode_ambient(old, labels, recipe) -> str:
    kind = recipe.get("source")
    if kind == "native":
        colour = recipe["colouring"]
        require(len(colour) == 517, "native H517 source width")
        return colour
    if kind == "forced":
        omitted = [recipe["index"]]
        text = old["forced_witness"][str(recipe["index"])]
    else:
        require(kind == "family", "recognized ambient recipe kind")
        source = old["family"][recipe["index"]]
        omitted = source["D"]
        text = source["witness"]
    retained = [vertex for vertex in range(553) if vertex not in set(omitted)]
    require(len(retained) == len(text), "ambient witness width")
    by_label = dict(zip(retained, text))
    colour = "".join(by_label.get(label, ".") for label in labels) + recipe["extra"]
    require(len(colour) == 517, "decoded H517 source width")
    return colour


def build_source_strings(repository: Path, old, labels, large) -> list[str]:
    prior = load(repository / "hadwiger_nelson_heule517_family_pilot/certificate.json")["rows"]
    small_pilot = load(repository / "hadwiger_nelson_heule517_small_pilot/certificate.json")["rows"]
    small134 = load(repository / "hadwiger_nelson_heule517_small134/certificate.json")
    profiles = load(repository / "hadwiger_nelson_heule517_joint_interface/certificate.json")["rows"]
    large2 = load(repository / "hadwiger_nelson_heule517_large2_pilot/certificate.json")["rows"]
    large3 = load(repository / "hadwiger_nelson_heule517_large3/certificate.json")["rows"]
    large4 = load(repository / "hadwiger_nelson_heule517_large4/certificate.json")["rows"]
    large_order = sorted(large)
    small_order = sorted(set(range(517)) - large)

    def decode_small(row) -> str:
        if row["kind"] == "seed":
            index = row["row"]
            require(type(index) is int and 0 <= index < len(prior), "small seed index")
            require(row["D"] == prior[index]["D"], "small seed omission identity")
            return decode_ambient(old, labels, prior[index])
        require(row["kind"] == "case", "small profile recipe kind")
        index = row["case"]
        require(type(index) is int and 0 <= index < len(profiles), "small profile index")
        left = profiles[index]["colouring"]
        right = row["colouring"]
        require(len(left) == 375 and len(right) == 142, "block-colouring widths")
        output = ["."] * 517
        for vertex, colour in zip(large_order, left):
            output[vertex] = colour
        for vertex, colour in zip(small_order, right):
            output[vertex] = colour
        return "".join(output)

    selected_small = []
    for origin, index in small134["final_rows"]:
        require(origin in ("initial", "new"), "small134 source family")
        pool = small_pilot if origin == "initial" else small134["new_rows"]
        require(type(index) is int and 0 <= index < len(pool), "small134 source index")
        selected_small.append(pool[index])
    require((len(prior), len(selected_small), len(large2), len(large3), len(large4))
            == (526, 202, 86, 108, 33), "historical source-family sizes")

    strings = [decode_ambient(old, labels, row) for row in prior]
    strings.extend(decode_small(row) for row in selected_small)
    strings.extend(row["colouring"] for row in large2)
    strings.extend(row["colouring"] for row in large3)
    strings.extend(row["colouring"] for row in large4)
    strings.extend(row["colouring"] for row in
                   load(repository / "hadwiger_nelson_heule517_whole_decision/certificate.json")["rows"])
    require(len(strings) == 963 and all(len(text) == 517 and set(text) <= set(".0123")
                                         for text in strings), "963 source strings")
    return strings


def decode_interface_recipe(recipe, source_strings: list[str]) -> str:
    require(isinstance(recipe, list) and len(recipe) == 3, "interface recipe shape")
    index, tail, fills = recipe
    require(type(index) is int and 0 <= index < len(source_strings), "interface source index")
    require(len(tail) == 4 and set(tail) <= set(".0123"), "interface tail")
    colour = list(source_strings[index][:510] + tail)
    seen = set()
    for vertex, value in fills:
        require(type(vertex) is int and 0 <= vertex < 510 and vertex not in seen,
                "unique interface fill")
        require(colour[vertex] == "." and value in "0123", "valid interface restoration")
        colour[vertex] = value
        seen.add(vertex)
    return "".join(colour)


def decode_old_library(repository: Path):
    old = load(repository / "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json")
    labels = [index for index, provenance in enumerate(old["provenance"]) if "510" in provenance]
    require(len(labels) == 510 and labels == sorted(set(labels)), "increasing H510 labels")
    points = [scaled_point(old["coordinates"][str(label)]) for label in labels]
    large = {vertex for vertex, point in enumerate(points)
             if all(point[axis][basis] == 0 for axis in (0, 1) for basis in (2, 3, 6, 7))}
    require(len(large) == 375, "old large block")
    source_strings = build_source_strings(repository, old, labels, large)

    interface = load(repository / "hadwiger_nelson_heule514_interface/certificate.json")
    colours = [decode_interface_recipe(recipe, source_strings) for recipe in interface["transport"]]
    colours.extend(row["colouring"] for row in interface["native"])
    require(len(colours) == 516, "interface row count")
    initial = sorted(
        (([vertex for vertex, value in enumerate(colour) if value == "."], colour)
         for colour in colours),
        key=lambda item: (len(item[0]), item[0]),
    )
    rows = [{"group": "interface", "index": index, "full_D": omissions,
             "full_colouring": colour}
            for index, (omissions, colour) in enumerate(initial)]
    for group, path in (
        ("profile", "hadwiger_nelson_heule514_profile_pilot/certificate.json"),
        ("whole", "hadwiger_nelson_heule514_whole_decision/certificate.json"),
    ):
        for record in load(repository / path):
            rows.append({"group": group, "index": record["index"], "full_D": record["D"],
                         "full_colouring": record["colouring"]})
    require(len(rows) == 544, "frozen library row count")
    for row in rows:
        colour = row["full_colouring"]
        require(len(colour) == 514 and set(colour) <= set(".0123"), "H514 colouring domain")
        require(row["full_D"] == [vertex for vertex, value in enumerate(colour) if value == "."],
                "H514 dot set")
        row["tag"] = f'{row["group"]}:{row["index"]}'
        row["old_colouring"] = colour[:510]
        row["old_D"] = [vertex for vertex, value in enumerate(colour[:510]) if value == "."]
    library = "".join(row["tag"] + " " + row["old_colouring"] + "\n" for row in rows).encode("ascii")
    require(sha256(library).hexdigest() == EXPECTED_LIBRARY_HASH, "canonical old-library stream")
    require(histogram(len(row["old_D"]) for row in rows) == {"1": 532, "2": 10, "3": 2},
            "old omission-size census")
    require({row["old_D"][0] for row in rows if len(row["old_D"]) == 1}
            == set(range(510)), "at least one old singleton row per H510 vertex")
    return old, labels, points, rows, library


def reconstruct_h632(repository: Path, old_points):
    fresh_rows = load(repository / "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json")
    ids = [row["centre_index"] for row in fresh_rows]
    require(len(ids) == 122 and ids == sorted(set(ids)), "fixed fresh centre order")
    fresh_points = [scaled_point(row["coordinates"]) for row in fresh_rows]
    require(len(set(old_points + fresh_points)) == 632, "632 distinct exact points")
    unit = (DENOMINATOR * DENOMINATOR,) + (0,) * 7

    old_edges = []
    for left, right in combinations(range(510), 2):
        if exact_squared_distance(old_points[left], old_points[right]) == unit:
            old_edges.append((left, right))
    fresh_edges = []
    norm_stream = sha256()
    for left_position, right_position in combinations(range(122), 2):
        norm = exact_squared_distance(fresh_points[left_position], fresh_points[right_position])
        left, right = ids[left_position], ids[right_position]
        norm_stream.update((f"F {left} {right} " + " ".join(map(str, norm)) + "\n").encode("ascii"))
        if norm == unit:
            fresh_edges.append((left, right))
    attachments = {}
    for position, row in enumerate(fresh_rows):
        centre = ids[position]
        neighbours = []
        for vertex, old_point in enumerate(old_points):
            norm = exact_squared_distance(fresh_points[position], old_point)
            norm_stream.update((f"H {centre} {vertex} " + " ".join(map(str, norm)) + "\n").encode("ascii"))
            if norm == unit:
                neighbours.append(vertex)
        require(neighbours == row["neighbors"] and len(neighbours) == row["degree"],
                "entrywise old attachment")
        attachments[centre] = neighbours
    require(norm_stream.hexdigest() == EXPECTED_NORM_HASH, "fresh/cross norm-stream identity")
    require((len(old_edges), len(fresh_edges), sum(map(len, attachments.values())))
            == (2504, 57, 551), "H632 edge partition")

    structure = load(repository / "hadwiger_nelson_heule_fresh122_incidence/certificate.json")
    require(structure["centre_ids"] == ids and structure["unique_cycle"] == EXPECTED_CYCLE,
            "accepted fresh structure labels")
    require(structure["fresh_edges"] == [list(edge) for edge in fresh_edges],
            "entrywise fresh-edge certificate")
    adjacency = {vertex: set() for vertex in ids}
    for left, right in fresh_edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(ids)
    components = []
    while unseen:
        root = min(unseen)
        queue = deque([root])
        component = {root}
        while queue:
            vertex = queue.popleft()
            for neighbour in sorted(adjacency[vertex] - component):
                component.add(neighbour)
                queue.append(neighbour)
        unseen -= component
        components.append(sorted(component))
    require(components == [record["centres"] for record in structure["components"]],
            "independent component order and membership")

    global_position = {centre: 510 + position for position, centre in enumerate(ids)}
    full_edges = list(old_edges)
    full_edges.extend((old_vertex, global_position[centre])
                      for centre in ids for old_vertex in attachments[centre])
    full_edges.extend((global_position[left], global_position[right])
                      for left, right in fresh_edges)
    require(len(full_edges) == 3112 and len(set(full_edges)) == 3112, "complete H632 edge list")
    edge_stream = "".join(f"{left},{right}\n" for left, right in full_edges).encode("ascii")
    require(sha256(edge_stream).hexdigest() == EXPECTED_FULL_EDGE_HASH,
            "canonical complete H632 edge stream")
    return {
        "fresh_rows": fresh_rows,
        "ids": ids,
        "fresh_edges": fresh_edges,
        "attachments": attachments,
        "adjacency": adjacency,
        "components": components,
        "old_edges": old_edges,
        "full_edges": full_edges,
        "global_position": global_position,
        "norm_stream_sha256": norm_stream.hexdigest(),
        "full_edge_stream_sha256": sha256(edge_stream).hexdigest(),
        "exact_pairs": 632 * 631 // 2,
    }


def check_old_rows(rows, geometry) -> dict[str, int]:
    old_checks = 0
    for row in rows:
        colour = row["old_colouring"]
        for left, right in geometry["old_edges"]:
            if colour[left] == "." or colour[right] == ".":
                continue
            old_checks += 1
            require(colour[left] != colour[right], "old library monochromatic edge")
    require(old_checks == 1356641, "all retained H510-edge checks")

    # The source objects are advertised as H514 colourings.  Check that
    # provenance claim too, even though transport discards and recolours the
    # four H514-tail values.  These labels are fresh-centre identifiers.
    tail = [170, 436, 1239, 1527]
    tail_position = {centre: 510 + position for position, centre in enumerate(tail)}
    h514_edges = list(geometry["old_edges"])
    h514_edges.extend((old_vertex, tail_position[centre])
                      for centre in tail
                      for old_vertex in geometry["attachments"][centre])
    h514_edges.extend((tail_position[left], tail_position[right])
                      for left, right in geometry["fresh_edges"]
                      if left in tail_position and right in tail_position)
    require(len(h514_edges) == 2526 and len(set(h514_edges)) == 2526,
            "reconstructed H514 edge set")
    h514_checks = 0
    for row in rows:
        colour = row["full_colouring"]
        for left, right in h514_edges:
            if colour[left] == "." or colour[right] == ".":
                continue
            h514_checks += 1
            require(colour[left] != colour[right], "H514 library monochromatic edge")
    require(h514_checks == 1368406, "all inherited retained H514-edge checks")
    return {"h510": old_checks, "h514": h514_checks}


def masks_for_row(row, geometry) -> dict[int, int]:
    colour = row["old_colouring"]
    masks = {}
    for centre in geometry["ids"]:
        forbidden = {int(colour[vertex]) for vertex in geometry["attachments"][centre]
                     if colour[vertex] != "."}
        masks[centre] = 15 & ~sum(1 << value for value in forbidden)
    return masks


def component_edges(component: list[int], fresh_edges) -> list[tuple[int, int]]:
    vertices = set(component)
    return [(left, right) for left, right in fresh_edges if left in vertices and right in vertices]


def dpll_colour(vertices: list[int], edges: list[tuple[int, int]], masks: dict[int, int], stats):
    """Definition-level exact four-colour search, independent of graph shape."""
    require(set(masks) == set(vertices), "DPLL mask domain")
    require(all(type(mask) is int and 0 <= mask <= 15 for mask in masks.values()),
            "DPLL list masks")
    index = {vertex: position for position, vertex in enumerate(vertices)}
    adjacency = [[] for _ in vertices]
    for left, right in edges:
        require(left in index and right in index and left != right, "DPLL edge domain")
        adjacency[index[left]].append(index[right])
        adjacency[index[right]].append(index[left])

    def search(domains: list[int]):
        stats["recursive_nodes"] += 1
        queue = deque(position for position, mask in enumerate(domains) if mask.bit_count() == 1)
        while queue:
            position = queue.popleft()
            colour_bit = domains[position]
            if colour_bit == 0 or colour_bit.bit_count() != 1:
                continue
            for neighbour in adjacency[position]:
                if not domains[neighbour] & colour_bit:
                    continue
                if domains[neighbour] == colour_bit:
                    stats["conflicts"] += 1
                    return None
                domains[neighbour] &= ~colour_bit
                stats["domain_deletions"] += 1
                if domains[neighbour].bit_count() == 1:
                    queue.append(neighbour)
        if any(mask == 0 for mask in domains):
            stats["conflicts"] += 1
            return None
        choices = [position for position, mask in enumerate(domains) if mask.bit_count() > 1]
        if not choices:
            return domains
        position = min(choices, key=lambda p: (domains[p].bit_count(), -len(adjacency[p]), p))
        stats["branch_nodes"] += 1
        mask = domains[position]
        while mask:
            bit = mask & -mask
            mask -= bit
            trial = domains.copy()
            trial[position] = bit
            answer = search(trial)
            if answer is not None:
                return answer
        return None

    answer_masks = search([masks[vertex] for vertex in vertices])
    if answer_masks is None:
        return None
    answer = {vertex: answer_masks[position].bit_length() - 1
              for position, vertex in enumerate(vertices)}
    require(all(masks[vertex] & (1 << answer[vertex]) for vertex in vertices),
            "DPLL witness list membership")
    require(all(answer[left] != answer[right] for left, right in edges),
            "DPLL witness edge inequalities")
    return answer


def brute_colour(vertices, edges, masks):
    selected = list(masks)
    domains = [[colour for colour in range(4) if masks[vertex] & (1 << colour)]
               for vertex in selected]
    for values in product(*domains):
        answer = dict(zip(selected, values))
        if all(left not in answer or right not in answer or answer[left] != answer[right]
               for left, right in edges):
            return answer
    return None


def independent_controls() -> dict[str, object]:
    fixtures = [
        ("path4", list(range(4)), [(0, 1), (1, 2), (2, 3)], range(-1, 16)),
        ("cycle4", list(range(4)), [(0, 1), (1, 2), (2, 3), (3, 0)], range(-1, 16)),
        ("cycle4_two_branches", list(range(6)),
         [(2, 3), (3, 4), (4, 5), (5, 2), (2, 1), (1, 0)], range(-1, 4)),
    ]
    expected = {"path4": (83521, 62208), "cycle4": (83521, 60876),
                "cycle4_two_branches": (15625, 1732)}
    records = []
    total = 0
    for name, vertices, edges, states in fixtures:
        count = accepted = 0
        truth = sha256()
        stats = Counter()
        for word in product(states, repeat=len(vertices)):
            masks = {vertex: mask for vertex, mask in zip(vertices, word) if mask >= 0}
            dpll = dpll_colour(list(masks), [(a, b) for a, b in edges
                                             if a in masks and b in masks], masks, stats)
            brute = brute_colour(vertices, edges, masks)
            require((dpll is None) == (brute is None), "DPLL/brute control equality")
            good = dpll is not None
            accepted += good
            count += 1
            truth.update(bytes([good]))
        require((count, accepted) == expected[name], "published control census: " + name)
        records.append({"fixture": name, "cases": count, "colourable": accepted,
                        "truth_sha256": truth.hexdigest(), "search": dict(stats)})
        total += count
    require(total == 182667, "complete independent control domain")
    triangle_masks = {0: 3, 1: 3, 2: 3}
    require(dpll_colour([0, 1, 2], [(0, 1), (1, 2), (0, 2)], triangle_masks,
                        Counter()) is None, "odd-cycle negative control")
    return {"total_cases": total, "fixtures": records,
            "odd_cycle_identical_two_lists_rejected": True}


def check_full_colouring(old_colour: str, fresh_answer: dict[int, int], geometry) -> int:
    require(set(fresh_answer) == set(geometry["ids"]), "all fresh vertices coloured")
    checks = 0
    for left, right in geometry["old_edges"]:
        if old_colour[left] == "." or old_colour[right] == ".":
            continue
        checks += 1
        require(old_colour[left] != old_colour[right], "full witness old edge")
    for centre in geometry["ids"]:
        require(type(fresh_answer[centre]) is int and 0 <= fresh_answer[centre] < 4,
                "fresh witness colour domain")
        for old_vertex in geometry["attachments"][centre]:
            if old_colour[old_vertex] == ".":
                continue
            checks += 1
            require(fresh_answer[centre] != int(old_colour[old_vertex]),
                    "full witness attachment edge")
    for left, right in geometry["fresh_edges"]:
        checks += 1
        require(fresh_answer[left] != fresh_answer[right], "full witness fresh edge")
    return checks


def transport(rows, geometry, target: Path):
    packets = [(component, component_edges(component, geometry["fresh_edges"]))
               for component in geometry["components"]]
    table_lines = []
    list_lines = []
    success_counts = [0] * len(packets)
    failures = Counter()
    row_failure_reasons = Counter()
    empty_histogram = Counter()
    full_rows = []
    reviewer_answers = {}
    nonempty_failures = []
    search_stats = Counter()
    all_mask = (1 << len(packets)) - 1

    for row_index, row in enumerate(rows):
        masks = masks_for_row(row, geometry)
        list_lines.append("".join(format(masks[centre], "x") for centre in geometry["ids"]) + "\n")
        empty_count = sum(mask == 0 for mask in masks.values())
        empty_histogram[empty_count] += 1
        bitmask = 0
        full_answer = {}
        failed_components = []
        for component_index, (vertices, edges) in enumerate(packets):
            local_masks = {vertex: masks[vertex] for vertex in vertices}
            answer = dpll_colour(vertices, edges, local_masks, search_stats)
            if answer is None:
                failed_components.append(component_index)
                failures["empty_list" if 0 in local_masks.values() else "coupled_lists"] += 1
            else:
                bitmask |= 1 << component_index
                success_counts[component_index] += 1
                full_answer.update(answer)
        table_lines.append(f'{row_index}\t{row["tag"]}\t' + ",".join(map(str, row["old_D"]))
                           + f'\t{bitmask:017x}\n')
        if bitmask == all_mask:
            require(len(full_answer) == 122, "complete successful fresh assignment")
            full_rows.append(row_index)
            reviewer_answers[row_index] = full_answer
        elif empty_count:
            row_failure_reasons["empty_list"] += 1
        else:
            row_failure_reasons["coupled_lists"] += 1
            nonempty_failures.append({"index": row_index, "tag": row["tag"],
                                      "failed_components": failed_components})

    table = "".join(table_lines).encode("ascii")
    lists = "".join(list_lines).encode("ascii")
    require(sha256(table).hexdigest() == EXPECTED_CASES_HASH
            and table == (target / "cases.tsv").read_bytes(),
            "entrywise 544-by-66 component truth table")
    require(sha256(lists).hexdigest() == EXPECTED_LISTS_HASH, "canonical list-mask stream")
    require((len(full_rows), row_failure_reasons) == (22, Counter(empty_list=505, coupled_lists=17)),
            "full-row extension census")
    require(failures == Counter(empty_list=1239, coupled_lists=179),
            "component failure-reason census")

    public = load(target / "positive.json")
    require([record["index"] for record in public] == full_rows, "exact 22 successful row indices")
    submitted_checks = reviewer_checks = 0
    reviewer_tail_stream = sha256()
    for record in public:
        row_index = record["index"]
        row = rows[row_index]
        require(record["tag"] == row["tag"] and record["old_omissions"] == row["old_D"],
                "positive witness provenance")
        tail = record["fresh_colouring"]
        require(len(tail) == 122 and set(tail) <= set("0123"), "submitted fresh tail domain")
        submitted_answer = {centre: int(colour) for centre, colour in zip(geometry["ids"], tail)}
        submitted_checks += check_full_colouring(row["old_colouring"], submitted_answer, geometry)
        reviewer_answer = reviewer_answers[row_index]
        reviewer_checks += check_full_colouring(row["old_colouring"], reviewer_answer, geometry)
        reviewer_tail_stream.update((f'{row_index} ' + "".join(str(reviewer_answer[centre])
                                                               for centre in geometry["ids"]) + "\n").encode("ascii"))
    require(submitted_checks == reviewer_checks == 68225, "all 22 full positive edge checks")
    singleton_cuts = sorted(record["old_omissions"][0] for record in public
                            if len(record["old_omissions"]) == 1)
    require(singleton_cuts == EXPECTED_SINGLETONS and len(set(singleton_cuts)) == 22,
            "22 distinct extended old singleton cuts")

    explicit = rows[462]
    explicit_masks = masks_for_row(explicit, geometry)
    require(explicit["tag"] == "interface:462" and explicit["old_D"] == [486],
            "explicit coupled-failure row identity")
    require(explicit_masks[809] == explicit_masks[1041] == 2
            and (809, 1041) in geometry["fresh_edges"], "adjacent forced-colour-one failure")
    require({vertex: explicit["old_colouring"][vertex] for vertex in (396, 405, 427, 433)}
            == {396: "2", 405: "2", 427: "0", 433: "3"}, "centre809 old colours")
    require({vertex: explicit["old_colouring"][vertex] for vertex in (379, 396, 407, 450)}
            == {379: "3", 396: "2", 407: "0", 450: "2"}, "centre1041 old colours")

    return {
        "cases_sha256": sha256(table).hexdigest(),
        "lists_sha256": sha256(lists).hexdigest(),
        "component_success_counts": success_counts,
        "component_failures_by_reason": dict(failures),
        "row_failures_by_reason": dict(row_failure_reasons),
        "empty_centres_per_row_histogram": {str(key): empty_histogram[key]
                                             for key in sorted(empty_histogram)},
        "full_rows": full_rows,
        "singleton_cuts": singleton_cuts,
        "submitted_positive_edge_checks": submitted_checks,
        "reviewer_positive_edge_checks": reviewer_checks,
        "reviewer_positive_tail_sha256": reviewer_tail_stream.hexdigest(),
        "nonempty_list_failed_rows": nonempty_failures,
        "search_stats": dict(search_stats),
        "explicit_failure": {
            "index": 462,
            "tag": explicit["tag"],
            "old_omissions": explicit["old_D"],
            "adjacent_centres": [809, 1041],
            "common_singleton_mask": 2,
        },
    }


def malformed_controls(geometry) -> list[str]:
    rejected = []
    component = geometry["components"][0]
    edges = component_edges(component, geometry["fresh_edges"])
    for name, masks in (("missing_vertex_mask", {}),
                        ("out_of_range_mask",
                         {vertex: (16 if vertex == component[0] else 15)
                          for vertex in component})):
        try:
            dpll_colour(component, edges, masks, Counter())
        except ReviewFailure:
            rejected.append(name)
        else:
            raise ReviewFailure("accepted malformed control: " + name)
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()
    target = (args.target or repository / "hadwiger_nelson_heule632_transport").resolve()

    reviewed_source = verify_sha256s(target)
    plan = load(target / "plan.json")
    for name, expected in plan["input_files"].items():
        require(file_record(repository / name)["sha256"] == expected, "pinned input: " + name)
    old, labels, old_points, rows, library = decode_old_library(repository)
    require(len(labels) == len(old_points) == 510, "old geometry domain")
    geometry = reconstruct_h632(repository, old_points)
    inherited_checks = check_old_rows(rows, geometry)
    controls = independent_controls()
    transport_result = transport(rows, geometry, target)

    submitted = load(target / "result.json")
    require((submitted["old_rows"], submitted["component_tests"], submitted["full_extensions"],
             submitted["failed_extensions"], submitted["component_success_counts"],
             submitted["component_failures_by_reason"], submitted["empty_centres_per_row_histogram"],
             submitted["valid_old_singleton_cuts"], submitted["full_positive_edge_checks"],
             submitted["family_closed_through508"])
            == (544, 35904, 22, 522, transport_result["component_success_counts"],
                transport_result["component_failures_by_reason"],
                transport_result["empty_centres_per_row_histogram"], EXPECTED_SINGLETONS, 68225, False),
            "independent summary matches submitted result")

    result = {
        "all_checks_passed": True,
        "scope": "exact extension classification of the frozen 544 old colourings over all 122 fresh vertices of fixed H632",
        "python": sys.version.split()[0],
        "reviewed_source_commit": "d0bbc427ade0a65514fd1aa7ce7d9c0548bbfe00",
        "reviewed_source": reviewed_source,
        "pinned_input_files": len(plan["input_files"]),
        "geometry": {
            "vertices": 632,
            "exact_pairs_checked": geometry["exact_pairs"],
            "old_edges": len(geometry["old_edges"]),
            "old_fresh_edges": sum(map(len, geometry["attachments"].values())),
            "fresh_edges": len(geometry["fresh_edges"]),
            "full_edges": len(geometry["full_edges"]),
            "fresh_cross_norm_stream_sha256": geometry["norm_stream_sha256"],
            "full_edge_stream_sha256": geometry["full_edge_stream_sha256"],
            "fresh_components": len(geometry["components"]),
        },
        "old_library": {
            "rows": len(rows),
            "stream_sha256": sha256(library).hexdigest(),
            "source_strings_redecoded": 963,
            "omission_size_histogram": histogram(len(row["old_D"]) for row in rows),
            "distinct_singleton_vertices": len({row["old_D"][0] for row in rows
                                                  if len(row["old_D"]) == 1}),
            "retained_H510_edge_checks": inherited_checks["h510"],
            "retained_H514_edge_checks": inherited_checks["h514"],
        },
        "definition_level_controls": controls,
        "transport": transport_result,
        "conclusion": {
            "fixed_544_by_66_decision_complete": True,
            "full_extensions": 22,
            "failed_fixed_old_colourings": 522,
            "valid_H632_singleton_deletion_witnesses": 22,
            "H632_family_closed_through_508": False,
            "failed_row_support_non_four_colourability_proved": False,
            "sub509_five_chromatic_graph_produced": False,
            "record_improvement": False,
            "adaptive_new_colourings_or_solver_calls": 0,
        },
        "negative_controls_rejected": malformed_controls(geometry)
        + ["odd_cycle_identical_two_lists"],
        "trust_boundary": [
            "the pinned coordinate and historical positive-colouring recipe tables",
            "ordinary CPython integer/Fraction arithmetic, JSON decoding, recursion, and exhaustive-loop execution",
            "the standard degree-eight squarefree radical basis used for exact distance equality",
            "SHA-256 collision resistance for source and canonical stream identities",
            "the frozen library is not assumed complete among all H510 colourings, so its 522 failures have no negative graph consequence",
        ],
    }
    atomic_json(args.report, result)
    print(json.dumps({
        "all_checks_passed": True,
        "vertices": 632,
        "edges": len(geometry["full_edges"]),
        "old_rows": len(rows),
        "component_decisions": len(rows) * len(geometry["components"]),
        "full_extensions": len(transport_result["full_rows"]),
        "valid_singleton_cuts": len(transport_result["singleton_cuts"]),
        "family_closed_through_508": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
