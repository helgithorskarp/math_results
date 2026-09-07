#!/usr/bin/env python3
"""Independent audit of the de Grey 1581 terminal-cover certificate.

The reviewed package is treated as data: this program imports none of its
code.  It reuses the separately published SymPy geometry audit, pins that
audit by SHA-256, and independently validates the new colouring DAG and all
511 full-host deletion words.
"""

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_GEOMETRY_AUDIT = (
    HERE.parent / "hadwiger_nelson_degrey1581_residue_sections_review1" / "audit.py"
)
GEOMETRY_AUDIT_SHA256 = (
    "b4992abfcbfca9d91b23765db742cd279b78d45b9b56784bddd3def1daf456f9"
)
CERTIFICATE_SHA256 = (
    "690c34701f671959013e3053e22c60f8f784648e8985e0342e5d138ca1d3f29a"
)
EXPECTED_WORD_SHA256 = (
    "120c1af011ce288286f7f1ad41a9163aa9ce112e4479f4964bd149413a431be3"
)
EXPECTED_COORDINATE_SHA256 = (
    "40b27b53176a846efe80a1f40ce685b7aaf89d6f3988969da112caa9c493c5e3"
)
EXPECTED_EDGE_SHA256 = (
    "a20b27f728af08a9aaacbc60cbaa4ef095f62e4c47ef8ab87dcc0c0233b04675"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_geometry_audit(path):
    raw = path.read_bytes()
    require(sha256(raw) == GEOMETRY_AUDIT_SHA256,
            "unexpected geometry-audit source")
    spec = importlib.util.spec_from_file_location("independent_degrey_geometry", path)
    require(spec is not None and spec.loader is not None,
            "cannot load geometry audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stream_hashes(points, edges):
    coordinate_stream = "".join(
        " ".join(map(str, point)) + "\n" for point in points
    ).encode()
    edge_stream = "".join(f"{u} {v}\n" for u, v in edges).encode()
    return sha256(coordinate_stream), sha256(edge_stream)


def multiply_sqrt7(vector):
    """Multiply a 16-coefficient vector by sqrt(7) in the documented basis."""
    require(len(vector) == 16, "radical vector length")
    return tuple(7 * vector[i + 8] for i in range(8)) + tuple(vector[:8])


def divide_vector(vector, divisor):
    require(all(value % divisor == 0 for value in vector),
            "nonintegral affine image")
    return tuple(value // divisor for value in vector)


def affine_image(point, scale):
    """Apply z -> -2 + ((31+3*i*sqrt(7))/32)*(z+2)."""
    x = list(point[:16])
    y = tuple(point[16:])
    x[0] += 2 * scale
    root7_x = multiply_sqrt7(tuple(x))
    root7_y = multiply_sqrt7(y)
    qx = divide_vector(tuple(31 * a - 3 * b for a, b in zip(x, root7_y)), 32)
    qy = divide_vector(tuple(3 * a + 31 * b for a, b in zip(root7_x, y)), 32)
    qx = list(qx)
    qx[0] -= 2 * scale
    return tuple(qx) + qy


def reconstruct_geometry(target, geometry_audit):
    geometry = load_geometry_audit(geometry_audit)
    points, radicals = geometry.construct(target)
    edges, modular_survivors = geometry.exact_edges(points, radicals)
    coordinate_hash, edge_hash = stream_hashes(points, edges)
    require(coordinate_hash == EXPECTED_COORDINATE_SHA256,
            "coordinate stream digest")
    require(edge_hash == EXPECTED_EDGE_SHA256, "edge stream digest")

    # A coefficient involving sqrt(7) occurs in positions 8..15 of each axis.
    left = tuple(
        vertex for vertex, point in enumerate(points)
        if all(point[i] == 0 for i in range(8, 16))
        and all(point[i] == 0 for i in range(24, 32))
    )
    require(len(left) == 791, "left-half order")
    half_points = tuple(points[vertex] for vertex in left)
    half_label = {point: vertex for vertex, point in enumerate(half_points)}
    require(len(half_label) == len(half_points), "duplicate half point")

    point_label = {point: vertex for vertex, point in enumerate(points)}
    right_points = tuple(affine_image(point, geometry.SCALE)
                         for point in half_points)
    require(all(point in point_label for point in right_points),
            "affine image absent from host")
    right = tuple(point_label[point] for point in right_points)
    require(len(set(right)) == 791, "right-half order")

    inversion = tuple(
        half_label[tuple(-coefficient for coefficient in point)]
        for point in half_points
    )
    minus = (-2 * geometry.SCALE,) + (0,) * 31
    plus = (2 * geometry.SCALE,) + (0,) * 31
    terminals = (half_label[minus], half_label[plus])
    require(terminals == (0, 790), "terminal labels")

    left_set, right_set = set(left), set(right)
    anchor = left[terminals[0]]
    require(left_set & right_set == {anchor}, "half intersection")
    require(left_set | right_set == set(range(len(points))), "half union")

    local_label = {vertex: local for local, vertex in enumerate(left)}
    half_edges = tuple(sorted(
        (local_label[u], local_label[v]) for u, v in edges
        if u in left_set and v in left_set
    ))
    require(len(half_edges) == 3938, "half edge count")
    edge_set = set(edges)
    left_edges = {
        tuple(sorted((left[u], left[v]))) for u, v in half_edges
    }
    right_edges = {
        tuple(sorted((right[u], right[v]))) for u, v in half_edges
    }
    actual_right_edges = {
        edge for edge in edges if edge[0] in right_set and edge[1] in right_set
    }
    require(right_edges == actual_right_edges, "right-half edge image")
    require(left_edges.isdisjoint(right_edges), "halves share an edge")
    bridge = tuple(sorted((left[terminals[1]], right[terminals[1]])))
    require(edge_set - left_edges - right_edges == {bridge},
            "cross-edge census")
    require({tuple(sorted((inversion[u], inversion[v])))
             for u, v in half_edges} == set(half_edges),
            "inversion is not a half automorphism")
    require(inversion[terminals[0]] == terminals[1]
            and inversion[terminals[1]] == terminals[0],
            "inversion does not exchange terminals")

    return {
        "points": points,
        "edges": edges,
        "left": left,
        "right": right,
        "half_edges": half_edges,
        "inversion": inversion,
        "terminals": terminals,
        "bridge": bridge,
        "anchor": anchor,
        "modular_survivors": modular_survivors,
        "coordinate_sha256": coordinate_hash,
        "edge_sha256": edge_hash,
    }


def integer(value, lower, upper, message):
    require(type(value) is int and lower <= value < upper, message)
    return value


def check_word(word, order, edges, deleted=None, separate=None):
    require(type(word) is str and len(word) == order, "colour-word length")
    for vertex, colour in enumerate(word):
        if vertex == deleted:
            require(colour == "-", "deleted vertex is present")
        else:
            require(colour in "0123", "invalid colour or omission")
    if separate is not None:
        require(deleted not in separate, "terminal deletion in separating word")
        require(word[separate[0]] != word[separate[1]],
                "terminals are not separated")
    checks = 0
    for u, v in edges:
        if deleted not in (u, v):
            require(word[u] != word[v], "monochromatic edge")
            checks += 1
    return checks


def decode_certificate(certificate, graph):
    order = len(graph["left"])
    terminals = graph["terminals"]
    require(type(certificate) is dict, "certificate object")
    require(certificate.get("version") == "degrey-terminal-cover-v1",
            "certificate version")
    # This is the producer's historical search threshold, not the proved bound.
    require(type(certificate.get("target")) is int
            and certificate["target"] == 508, "certificate target marker")
    supplied_terminals = certificate.get("terminals")
    require(type(supplied_terminals) is list
            and tuple(supplied_terminals) == terminals
            and all(type(vertex) is int for vertex in supplied_terminals),
            "certificate terminals")
    require(set(certificate) == {"version", "target", "terminals", "baseline", "steps"},
            "certificate fields")

    baseline = certificate.get("baseline")
    half_checks = check_word(baseline, order, graph["half_edges"])
    steps = certificate.get("steps")
    require(type(steps) is list, "steps list")
    words = {}
    kinds = Counter()
    for position, row in enumerate(steps):
        require(type(row) is dict, f"step {position} object")
        deleted = integer(row.get("deleted"), 0, order,
                          f"step {position} deletion")
        require(deleted not in terminals and deleted not in words,
                f"step {position} duplicate or terminal deletion")
        kind = row.get("kind")
        if kind == "seed":
            require(set(row) == {"kind", "deleted", "word"},
                    f"step {position} seed fields")
            word = row.get("word")
        else:
            parent = integer(row.get("parent"), 0, order,
                             f"step {position} parent")
            require(parent in words, f"step {position} forward parent")
            if kind == "inversion":
                require(set(row) == {"kind", "deleted", "parent"},
                        f"step {position} inversion fields")
                require(deleted == graph["inversion"][parent],
                        f"step {position} inversion label")
                word = "".join(
                    words[parent][graph["inversion"][vertex]]
                    for vertex in range(order)
                )
            elif kind == "patch":
                require(set(row) == {"kind", "deleted", "parent", "changes"},
                        f"step {position} patch fields")
                changes = row.get("changes")
                require(type(changes) is list and changes,
                        f"step {position} empty patch")
                edited = list(words[parent])
                changed = set()
                for item in changes:
                    require(type(item) is list and len(item) == 2,
                            f"step {position} patch item")
                    vertex = integer(item[0], 0, order,
                                     f"step {position} patch vertex")
                    colour = item[1]
                    require(vertex not in changed, f"step {position} repeated edit")
                    require(type(colour) is str and len(colour) == 1
                            and colour in "-0123", f"step {position} patch colour")
                    require(edited[vertex] != colour,
                            f"step {position} redundant edit")
                    changed.add(vertex)
                    edited[vertex] = colour
                word = "".join(edited)
            else:
                raise ValueError(f"step {position} kind")
        half_checks += check_word(word, order, graph["half_edges"],
                                  deleted, terminals)
        words[deleted] = word
        kinds[kind] += 1
    require(len(words) == 254, "omission-word count")
    require(kinds == Counter({"inversion": 127, "patch": 93, "seed": 34}),
            "step-kind census")
    return baseline, words, half_checks, dict(sorted(kinds.items()))


def palette_candidates():
    """Generate the 24 bijections by filtering the 4^4 maps."""
    for image in itertools.product("0123", repeat=4):
        if len(set(image)) == 4:
            yield image


def glue_word(graph, left_word, right_word, deleted):
    left, right = graph["left"], graph["right"]
    anchor_terminal, bridge_terminal = graph["terminals"]
    for palette in palette_candidates():
        if (left[anchor_terminal] != deleted
                and left_word[anchor_terminal]
                != palette[int(right_word[anchor_terminal])]):
            continue
        if (deleted not in graph["bridge"]
                and left_word[bridge_terminal]
                == palette[int(right_word[bridge_terminal])]):
            continue
        full_word = [None] * len(graph["points"])
        for local, global_vertex in enumerate(left):
            if global_vertex != deleted:
                full_word[global_vertex] = left_word[local]
        for local, global_vertex in enumerate(right):
            if global_vertex == deleted:
                continue
            colour = palette[int(right_word[local])]
            require(full_word[global_vertex] in (None, colour),
                    "inconsistent anchor colour")
            full_word[global_vertex] = colour
        full_word[deleted] = "-"
        require(all(colour is not None for colour in full_word),
                "uncoloured global vertex")
        return "".join(full_word)
    raise ValueError("no palette gluing")


def verify_cover(certificate, graph):
    baseline, half_words, half_checks, kinds = decode_certificate(certificate, graph)
    terminals = graph["terminals"]
    mandatory_half = tuple(sorted(set(terminals) | set(half_words)))
    require(len(mandatory_half) == 256, "mandatory-half order")
    mandatory_global = tuple(sorted({
        mapping[vertex]
        for mapping in (graph["left"], graph["right"])
        for vertex in mandatory_half
    }))
    require(len(mandatory_global) == 511, "mandatory-global order")
    require(len(mandatory_global) == 2 * len(mandatory_half) - 1,
            "mandatory overlap formula")

    left_lookup = {vertex: local for local, vertex in enumerate(graph["left"])}
    right_lookup = {vertex: local for local, vertex in enumerate(graph["right"])}
    special = {
        graph["left"][terminals[0]],
        graph["left"][terminals[1]],
        graph["right"][terminals[1]],
    }
    word_stream = hashlib.sha256()
    global_checks = 0
    for deleted in mandatory_global:
        left_word = baseline
        right_word = baseline
        if deleted not in special:
            if deleted in left_lookup:
                left_word = half_words[left_lookup[deleted]]
            else:
                require(deleted in right_lookup, "mandatory vertex outside halves")
                right_word = half_words[right_lookup[deleted]]
        full_word = glue_word(graph, left_word, right_word, deleted)
        global_checks += check_word(full_word, len(graph["points"]),
                                    graph["edges"], deleted)
        word_stream.update(f"{deleted} {full_word}\n".encode())

    global_word_sha256 = word_stream.hexdigest()
    require(global_word_sha256 == EXPECTED_WORD_SHA256,
            "global deletion-word stream digest")
    mandatory_stream = (" ".join(map(str, mandatory_global)) + "\n").encode()
    # Pigeonhole step: every graph of order at most 510 omits one of 511
    # certified host vertices, and restriction preserves a proper colouring.
    four_colourable_through = len(mandatory_global) - 1
    require(four_colourable_through == 510, "derived hereditary bound")
    return {
        "accepted": True,
        "arbitrary_target_subsets_classified": True,
        "record_improvement": False,
        "vertices": len(graph["points"]),
        "edges": len(graph["edges"]),
        "half_vertices": len(graph["left"]),
        "half_edges": len(graph["half_edges"]),
        "half_terminals": list(terminals),
        "shared_vertex": graph["anchor"],
        "bridge": list(graph["bridge"]),
        "modular_survivors": graph["modular_survivors"],
        "coordinate_sha256": graph["coordinate_sha256"],
        "edge_sha256": graph["edge_sha256"],
        "certificate_sha256": CERTIFICATE_SHA256,
        "geometry_audit_sha256": GEOMETRY_AUDIT_SHA256,
        "half_omission_words": len(half_words),
        "step_kinds": kinds,
        "required_half_vertices": len(mandatory_half),
        "required_global_vertices": len(mandatory_global),
        "four_colourable_through": four_colourable_through,
        "half_edge_checks": half_checks,
        "global_deletion_edge_checks": global_checks,
        "global_word_sha256": global_word_sha256,
        "mandatory_global_sha256": sha256(mandatory_stream),
        "geometry_engine": "pinned independent SymPy construction and AlgebraicField edge census",
        "certificate_engine": "independent DAG decoder, palette gluing, and direct full-word edge checks",
    }


def run(target, geometry_audit):
    raw = (target / "certificate.json").read_bytes()
    require(sha256(raw) == CERTIFICATE_SHA256, "certificate digest")
    certificate = json.loads(raw)
    graph = reconstruct_geometry(target, geometry_audit)
    return verify_cover(certificate, graph)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--geometry-audit", type=Path,
                        default=DEFAULT_GEOMETRY_AUDIT)
    parser.add_argument("--expected", type=Path)
    arguments = parser.parse_args()
    report = run(arguments.target, arguments.geometry_audit)
    if arguments.expected:
        require(report == json.loads(arguments.expected.read_text()),
                "expected report mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))
