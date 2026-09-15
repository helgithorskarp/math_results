#!/usr/bin/env python3
"""Independent exact review of the fixed native Parts136/A159/B214 union."""
from argparse import ArgumentParser
from copy import deepcopy
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_parts136_mixed_native_transfer_stop"
RECEIVER = HERE.parent / "hadwiger_nelson_parts136_reverse_receiver"
SOURCES = HERE.parent / "hadwiger_nelson_nonmono159_214_lowden2"
INPUT_HASHES = {
    "parts509.tsv": "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "points159.tsv": "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
    "points214.tsv": "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
}
TARGET_HASH = "2714c9bfebc2a88775ad0f512c5cdcbb510f7eb22caddc451d28504608c48cf2"
ONE = (96 * 96,) + (0,) * 7


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(a, b):
    """Subset-mask multiplication in Q(sqrt(3),sqrt(5),sqrt(11))."""
    out = [0] * 8
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            common = i & j
            factor = (3 if common & 1 else 1)
            factor *= (5 if common & 2 else 1)
            factor *= (11 if common & 4 else 1)
            out[i ^ j] += factor * x * y
    return tuple(out)


def norm2(a, b):
    difference = tuple(x-y for x, y in zip(a, b))
    return add(mul(difference[:8], difference[:8]),
               mul(difference[8:], difference[8:]))


def load_table(name, count, scale, provenance):
    raw = (TARGET / name).read_bytes()
    need(hashlib.sha256(raw).hexdigest() == INPUT_HASHES[name], "input hash " + name)
    need(raw == provenance.read_bytes(), "provenance copy " + name)
    rows = [tuple(scale*int(v) for v in line.split())
            for line in raw.decode().splitlines()
            if line and not line.startswith("#")]
    need(len(rows) == len(set(rows)) == count, "table census " + name)
    need(all(len(row) == 16 for row in rows), "table width " + name)
    return raw, rows


def graph(points):
    edges, distance = [], hashlib.sha256()
    for a, b in combinations(range(len(points)), 2):
        squared = norm2(points[a], points[b])
        need(any(squared), "unmerged collision")
        distance.update((",".join(map(str, squared)) + "\n").encode())
        if squared == ONE:
            edges.append((a, b))
    return edges, distance.hexdigest()


def digest(rows):
    return hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()


def build():
    raw_p, parent = load_table(
        "parts509.tsv", 509, 1, RECEIVER / "points.tsv")
    raw_a, source_a = load_table(
        "points159.tsv", 159, 8, SOURCES / "points159.tsv")
    raw_b, source_b = load_table(
        "points214.tsv", 214, 8, SOURCES / "points214.tsv")
    host_labels = [0] + list(range(374, 509))
    host = [parent[i] for i in host_labels]
    need(set(host) & set(source_a) == {parent[0]}, "H/A intersection")
    need(not set(host) & set(source_b), "H/B intersection")
    need(not set(source_a) & set(source_b), "A/B intersection")
    points, positions, maps = [], {}, []
    for block in (host, source_a, source_b):
        current = []
        for point in block:
            if point not in positions:
                positions[point] = len(points)
                points.append(point)
            current.append(positions[point])
        maps.append(current)
    need(len(points) == len(set(points)) == 508, "union census")
    return ((raw_p, raw_a, raw_b), parent, host_labels, host,
            source_a, source_b, points, maps)


def proper(word, edges, n, alphabet="0123"):
    return (isinstance(word, str) and len(word) == n and set(word) <= set(alphabet)
            and all(word[a] != word[b] for a, b in edges))


def component_edges(edges, vertex_map):
    reverse = {v: i for i, v in enumerate(vertex_map)}
    return [(reverse[a], reverse[b]) for a, b in edges if a in reverse and b in reverse]


def source_colour_for_root(word, root, colour, edges):
    old = word[root]
    permutation = {x: x for x in "0123"}
    permutation[old], permutation[colour] = colour, old
    moved = "".join(permutation[x] for x in word)
    need(moved[root] == colour and proper(moved, edges, len(word)),
         "source root permutation")
    return moved


def audit(certificate, target_override=None):
    (raws, parent, host_labels, host, source_a, source_b,
     points, maps) = build()
    edges, distance_hash = graph(points)
    host_map, a_map, b_map = maps
    host_set, a_set, b_set = set(host_map), set(a_map), set(b_map)
    host_edges = {e for e in edges if set(e) <= host_set}
    a_edges = {e for e in edges if set(e) <= a_set}
    b_edges = {e for e in edges if set(e) <= b_set}
    need((len(host_edges), len(a_edges), len(b_edges)) == (564, 646, 977),
         "component edge census")
    need(set(edges) == host_edges | a_edges | b_edges, "additional unit contact")
    need(not (host_edges & a_edges) and not (host_edges & b_edges)
         and not (a_edges & b_edges), "component edge overlap")
    old_new = [e for e in edges if (e[0] < 136) != (e[1] < 136)]
    need({v for e in old_new for v in e if v < 136} == {0}, "host interface")

    target_raw = (TARGET / "certificate.json").read_bytes()
    need(hashlib.sha256(target_raw).hexdigest() == TARGET_HASH, "target hash")
    target = json.loads(target_raw) if target_override is None else target_override
    point_hash = digest(points)
    edge_hash = digest([list(e) for e in edges])
    expected_geometry = {
        "points": 508,
        "edges": 2187,
        "new_points": 372,
        "host_edges": 564,
        "A_edges": 646,
        "B_edges": 977,
        "old_new_edges": 29,
        "new_new_edges": 1594,
        "A_B_contacts": 0,
        "actual_host_boundary_parent_labels": [0],
        "boundary_outside_original_B": [],
        "outside_parent": 238,
        "switching_host_points": 644,
        "outside_switching_host": 238,
        "point_hash": point_hash,
        "edge_hash": edge_hash,
        "distance_hash": distance_hash,
        "all_pairs": 128778,
    }
    need(target["geometry"] == expected_geometry, "target geometry")
    need(proper(target["colour4"], edges, 508), "target four word")
    need(proper(target["colour5"], edges, 508, "01234"), "target five word")
    need(target["colour4"][:136] == target["host_word"], "target host restriction")

    fixtures = json.loads((RECEIVER / "fixtures.json").read_text())["host_rows"]
    need(target["host_word"] == fixtures[0]["witness"], "target source host fixture")
    need(target["boundary_word"] == fixtures[0]["pattern"],
         "target source boundary fixture")
    boundary_labels = [0, 430, 432, 434, 476, 478] + list(range(480, 493))
    boundary_indices = [host_labels.index(v) for v in boundary_labels]
    need("".join(target["host_word"][v] for v in boundary_indices)
         == target["boundary_word"], "target boundary projection")

    need(certificate["schema"] == "hn-parts136-native-transfer-independent-review-v1",
         "review schema")
    need(certificate["target_certificate_sha256"] == TARGET_HASH,
         "review target hash")
    need(certificate["input_sha256"] == [hashlib.sha256(x).hexdigest() for x in raws],
         "review input hashes")
    fresh = certificate["fresh_four_colour_word"]
    need(proper(fresh, edges, 508), "fresh four word")
    fixture_index = certificate["fresh_host_fixture_index"]
    need(fixture_index == 1, "fresh fixture index")
    need(fresh[:136] == fixtures[fixture_index]["witness"], "fresh host fixture")
    fresh_boundary = "".join(fresh[v] for v in boundary_indices)
    need(fresh_boundary == fixtures[fixture_index]["pattern"], "fresh boundary fixture")
    need(certificate["fresh_boundary_pattern"] == fresh_boundary,
         "declared fresh boundary")
    need(certificate["fresh_extra_pins"] == [[136, 0], [294, 0]],
         "fresh extra pins")
    need(all(fresh[v] == str(c) for v, c in certificate["fresh_extra_pins"]),
         "fresh extra pin values")
    different = sum(a != b for a, b in zip(fresh, target["colour4"]))
    difference_by_block = [
        sum(a != b for a, b in zip(fresh[:136], target["colour4"][:136])),
        sum(a != b for a, b in zip(fresh[136:294], target["colour4"][136:294])),
        sum(a != b for a, b in zip(fresh[294:], target["colour4"][294:])),
    ]
    need(certificate["fresh_word_differs_from_target_positions"] == different == 375,
         "fresh word difference")
    need(certificate["fresh_word_difference_by_block"] == difference_by_block
         == [96, 109, 170], "fresh block differences")

    local_a_edges = component_edges(edges, a_map)
    local_b_edges = component_edges(edges, b_map)
    a_word = "".join(fresh[v] for v in a_map)
    b_word = "".join(fresh[v] for v in b_map)
    need(proper(a_word, local_a_edges, 159), "fresh A word")
    need(proper(b_word, local_b_edges, 214), "fresh B word")
    root = a_map.index(0)
    for colour in "0123":
        source_colour_for_root(a_word, root, colour, local_a_edges)

    ids = target["moser_vertices"]
    need(len(ids) == len(set(ids)) == 7 and all(0 <= v < 136 for v in ids),
         "Moser vertices")
    location = {v: i for i, v in enumerate(ids)}
    moser_edges = [(location[a], location[b]) for a, b in edges
                   if a in location and b in location]
    need(len(moser_edges) == 11, "Moser edge census")
    need(not any(all(colours[a] != colours[b] for a, b in moser_edges)
                 for colours in product(range(3), repeat=7)), "Moser three-colouring")

    def sigma5(point):
        return tuple(-x if index % 8 in (2, 3, 6, 7) else x
                     for index, x in enumerate(point))

    switching = set(parent) | {sigma5(point) for point in parent}
    result = {
        "source_points": [len(parent), len(source_a), len(source_b)],
        "physical_points": len(points),
        "new_points_over_host": len(points)-len(host),
        "complete_pair_tests": 508*507//2,
        "complete_edges": len(edges),
        "component_edges": [len(host_edges), len(a_edges), len(b_edges)],
        "host_new_edges": len(old_new),
        "new_new_edges": sum(a >= 136 and b >= 136 for a, b in edges),
        "host_interface_parent_labels": [0],
        "A_B_contacts": 0,
        "outside_parent": len(set(points)-set(parent)),
        "switching_host_points": len(switching),
        "outside_switching_host": len(set(points)-switching),
        "point_sha256": point_hash,
        "edge_sha256": edge_hash,
        "distance_sha256": distance_hash,
        "target_positive_words_checked": 2,
        "fresh_positive_words_checked": 1,
        "fresh_word_differs_from_target_positions": different,
        "fresh_word_difference_by_block": difference_by_block,
        "fresh_boundary_pattern": fresh_boundary,
        "universal_extension_proved_by_one_vertex_sum": True,
        "every_host_four_colouring_extends": True,
        "every_host_projection_unchanged": True,
        "moser_edges": len(moser_edges),
        "moser_three_colour_assignments_exhausted": 3**7,
        "chromatic_number": 4,
        "record_candidate": False,
        "verdict": "ACCEPT_WITH_STRICT_FIXED_FRAME_LIMITATION",
    }
    need(result == json.loads((HERE / "EXPECTED.json").read_text()),
         "EXPECTED mismatch")
    return result


def controls(certificate):
    target = json.loads((TARGET / "certificate.json").read_text())
    rejected = []
    for kind in ("fresh_colour", "fresh_fixture", "input_hash", "target_colour"):
        bad, bad_target = deepcopy(certificate), deepcopy(target)
        if kind == "fresh_colour":
            bad["fresh_four_colour_word"] = "0" * 508
        elif kind == "fresh_fixture":
            bad["fresh_host_fixture_index"] = 0
        elif kind == "input_hash":
            bad["input_sha256"][0] = "0" * 64
        else:
            bad_target["colour4"] = "0" * 508
        try:
            audit(bad, bad_target)
        except ValueError:
            rejected.append(kind)
        else:
            raise ValueError("corruption accepted: " + kind)
    return rejected


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    cert = json.loads((HERE / "certificate.json").read_text())
    output = audit(cert)
    if args.controls:
        output["corruptions_rejected"] = controls(cert)
    print(json.dumps(output, indent=2, sort_keys=True))
