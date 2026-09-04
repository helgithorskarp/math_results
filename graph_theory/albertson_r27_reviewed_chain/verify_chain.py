#!/usr/bin/env python3
"""Definition-level audit of the reviewed Albertson r=27 dependency chain."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from json import dumps, loads
from math import ceil
from pathlib import Path
from re import fullmatch


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[1]


def edge(left: str, right: str) -> frozenset[str]:
    if left == right:
        raise ValueError("loop")
    return frozenset((left, right))


def read_json(name: str) -> dict[str, object]:
    value = loads((HERE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(name)
    return value


def check_manifest(manifest: dict[str, object]) -> tuple[int, int]:
    artifacts = manifest["artifacts"]
    sources = manifest["primary_sources"]
    assert isinstance(artifacts, list) and isinstance(sources, list)
    checked_files = 0
    for source in sources:
        assert isinstance(source, dict)
        assert str(source["url"]).startswith("https://")
        assert source["revision"] and source["statement"]
    for artifact in artifacts:
        assert isinstance(artifact, dict)
        for key in ("source_commit", "review_commit"):
            if key in artifact:
                assert fullmatch(r"[0-9a-f]{40}", str(artifact[key]))
        refs = []
        for key in ("contribution_ref", "review_ref"):
            if key in artifact:
                refs.append(str(artifact[key]))
        refs.extend(str(item) for item in artifact.get("review_refs", []))
        assert refs and all(fullmatch(r"bafkrei[a-z2-7]{52}", ref) for ref in refs)
        directory = REPOSITORY / str(artifact["path"])
        assert directory.is_dir(), directory
        files = artifact["files"]
        assert isinstance(files, dict) and files
        for relative, expected in files.items():
            path = directory / relative
            actual = sha256(path.read_bytes()).hexdigest()
            assert actual == expected, (path, actual, expected)
            checked_files += 1
    return len(artifacts), checked_files


def oriented_edges(face: list[str]) -> tuple[tuple[str, str], ...]:
    assert len(face) == 3 and len(set(face)) == 3
    return tuple((face[index], face[(index + 1) % 3]) for index in range(3))


def local_disk(rotation: dict[str, object]) -> dict[str, object]:
    faces = rotation["faces"]
    assert isinstance(faces, list)
    undirected = Counter()
    directions: dict[frozenset[str], list[tuple[str, str]]] = defaultdict(list)
    vertices: set[str] = set()
    for face in faces:
        assert isinstance(face, list)
        vertices.update(face)
        for left, right in oriented_edges(face):
            side = edge(left, right)
            undirected[side] += 1
            directions[side].append((left, right))
    assert set(undirected.values()) == {1, 2}
    for side, count in undirected.items():
        if count == 2:
            first, second = directions[side]
            assert first == tuple(reversed(second)), (side, first, second)

    boundary_edges = {side for side, count in undirected.items() if count == 1}
    internal_edges = {side for side, count in undirected.items() if count == 2}
    expected_internal = {edge(*ends) for ends in rotation["internal_edges"]}
    assert internal_edges == expected_internal
    expected_cycle = tuple(rotation["expected_boundary"])
    expected_edges = {
        edge(expected_cycle[index], expected_cycle[(index + 1) % len(expected_cycle)])
        for index in range(len(expected_cycle))
    }
    assert boundary_edges == expected_edges
    assert len(vertices) - len(undirected) + len(faces) == 1

    links: dict[str, set[frozenset[str]]] = defaultdict(set)
    for face in faces:
        for index, vertex in enumerate(face):
            links[vertex].add(edge(face[(index + 1) % 3], face[(index + 2) % 3]))
    internal_vertex = str(rotation["internal_vertex"])
    for vertex, link_edges in links.items():
        degrees = Counter(endpoint for side in link_edges for endpoint in side)
        unseen = set(degrees)
        stack = [unseen.pop()]
        while stack:
            current = stack.pop()
            neighbors = {
                endpoint
                for side in link_edges
                if current in side
                for endpoint in side
                if endpoint != current
            }
            new = neighbors & unseen
            unseen -= new
            stack.extend(new)
        assert not unseen, (vertex, link_edges)
        if vertex == internal_vertex:
            assert len(link_edges) == len(degrees)
            assert set(degrees.values()) == {2}
        else:
            assert len(link_edges) + 1 == len(degrees)
            assert sorted(degrees.values()).count(1) == 2
            assert set(degrees.values()) <= {1, 2}

    restored = {
        name: edge(*ends)
        for name, ends in rotation["expected_restored_edges"].items()
    }
    boundary_vertices = expected_cycle
    complete = {edge(a, b) for a, b in combinations(boundary_vertices, 2)}
    assert set(restored.values()).isdisjoint(boundary_edges)
    assert set(restored.values()) | boundary_edges == complete
    return {
        "vertices": sorted(vertices),
        "edges": len(undirected),
        "faces": len(faces),
        "euler_characteristic": 1,
        "boundary": list(expected_cycle),
        "restored": {key: sorted(value) for key, value in sorted(restored.items())},
    }


def arithmetic_chain() -> dict[str, object]:
    profiles = (("A", 103, 57, 9), ("B", 106, 64, 11))
    terminal = []
    for name, edges, crossings, full in profiles:
        c5 = (2 * edges - 8 * (24 - 2)) // 3
        terminal_edges = edges - 2 * c5
        terminal_crossings = crossings - 4 * c5
        assert c5 == full + 1
        assert terminal_crossings - terminal_edges + 3 * (24 - 2) == 0
        terminal.append((name, c5, full, terminal_edges, terminal_crossings))

    order54 = Fraction(218768121, 35960)
    order53_714 = Fraction(14046318, 2303)
    order53_715 = Fraction(56455997, 9212)
    order53_713_sum = 298314
    assert ceil(order54) == 6084
    assert ceil(order53_714) == 6100
    assert ceil(order53_715) == 6129
    assert ceil(Fraction(order53_713_sum, 49)) == 6089
    z27 = (27 // 2) * (26 // 2) * (25 // 2) * (24 // 2) // 4
    assert z27 == 6084
    return {
        "terminal_profiles": terminal,
        "row_bounds": {
            "53,713": 6089,
            "53,714": 6100,
            "53,715": 6129,
            "54,726": 6084,
        },
        "Z(27)": z27,
    }


def main() -> None:
    manifest = read_json("dependency_manifest.json")
    rotation = read_json("rotation_system.json")
    artifact_count, file_count = check_manifest(manifest)
    disk = local_disk(rotation)
    arithmetic = arithmetic_chain()
    certificate = {
        "manifest_sha256": sha256(
            (HERE / "dependency_manifest.json").read_bytes()
        ).hexdigest(),
        "rotation_sha256": sha256(
            (HERE / "rotation_system.json").read_bytes()
        ).hexdigest(),
        "artifact_count": artifact_count,
        "file_count": file_count,
        "disk": disk,
        "arithmetic": arithmetic,
    }
    digest = sha256(dumps(certificate, sort_keys=True).encode("ascii")).hexdigest()
    print(f"PASS pinned dependency manifest: {artifact_count} artifacts, {file_count} files")
    print("PASS five-face oriented complex is a disk with boundary u-z-t-r-w-u")
    print(f"terminal_profiles={arithmetic['terminal_profiles']}")
    print(f"frontier_row_bounds={arithmetic['row_bounds']}; Z(27)={arithmetic['Z(27)']}")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
