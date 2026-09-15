#!/usr/bin/env python3
"""Build a compact positive-colouring cover for small E477 core extensions.

This is the certificate producer, not the verifier.  It uses the direct
two-equation unit test and deterministic DSATUR searches only to find proper
colourings.  The independent verifier uses generic radical-field arithmetic
and checks every published word and every claimed extension directly.
"""

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_overlapping_forcing_seed"
OUT = HERE / "certificate.json"
INPUT_HASHES = {
    "certificate.json": "3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237",
    "mandatory_vertices.json": "f0cea2d38b8d43e22bf82cba23ee65fb971cd031918015c9061ee499485cac2d",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def unit(left, right):
    a, b, c, d = (x - y for x, y in zip(left, right))
    return 3 * a * a + 11 * b * b + c * c + 33 * d * d == 1296 and a * b + c * d == 0


def source_data():
    for name, expected in INPUT_HASHES.items():
        require(file_hash(SOURCE / name) == expected, "input hash: " + name)
    equal = json.loads((SOURCE / "certificate.json").read_text())["equal"]
    mandatory = json.loads((SOURCE / "mandatory_vertices.json").read_text())
    require(equal["denominator"] == 1 and len(equal["points"]) == 477, "E477 input")
    points = equal["points"]
    edges = [pair for pair in combinations(range(477), 2) if unit(points[pair[0]], points[pair[1]])]
    require(len(edges) == 2458, "E477 edge census")
    deleted = [row["deleted"] for row in mandatory]
    require(len(deleted) == len(set(deleted)) == 253 and not {0, 1} & set(deleted), "deletion labels")
    core = sorted({0, 1, *deleted})
    optional = sorted(set(range(477)) - set(core))
    adjacency = [set() for _ in range(477)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    return core, optional, adjacency


def solve_extension(core, adjacency, extras, flip=False):
    """Return the core restriction of one positive extension colouring."""
    vertices = core + sorted(extras)
    index = {old: new for new, old in enumerate(vertices)}
    local = [{index[w] for w in adjacency[v] if w in index} for v in vertices]
    colours = [-1] * len(vertices)
    colours[index[0]] = 0
    colours[index[1]] = 1

    def search(done):
        if done == len(vertices):
            return True
        uncoloured = [v for v, colour in enumerate(colours) if colour < 0]
        vertex = max(
            uncoloured,
            key=lambda v: (
                len({colours[w] for w in local[v] if colours[w] >= 0}),
                len(local[v]),
                -v if flip else v,
            ),
        )
        forbidden = {colours[w] for w in local[vertex] if colours[w] >= 0}
        order = (3, 2, 1, 0) if flip else (0, 1, 2, 3)
        for colour in order:
            if colour not in forbidden:
                colours[vertex] = colour
                if search(done + 1):
                    return True
        colours[vertex] = -1
        return False

    require(search(2), "unexpected uncolourable extension")
    return "".join(map(str, colours[: len(core)]))


def allowed_mask(word, vertex, core_index, adjacency):
    mask = 15
    for neighbour in adjacency[vertex]:
        if neighbour in core_index:
            mask &= ~(1 << int(word[core_index[neighbour]]))
    return mask


def covers_pair(word, left, right, core_index, adjacency):
    left_mask = allowed_mask(word, left, core_index, adjacency)
    right_mask = allowed_mask(word, right, core_index, adjacency)
    if not left_mask or not right_mask:
        return False
    if right not in adjacency[left]:
        return True
    return any(
        a != b
        for a in range(4)
        for b in range(4)
        if left_mask & (1 << a) and right_mask & (1 << b)
    )


def main():
    core, optional, adjacency = source_data()
    core_index = {vertex: index for index, vertex in enumerate(core)}
    pairs = list(combinations(optional, 2))

    # One search for each singleton supplies a broad initial bank.  Solve the
    # still-uncovered pairs directly, then retain only a deterministic greedy
    # cover.  Search outcomes are not trusted by the verifier.
    bank = {solve_extension(core, adjacency, {vertex}) for vertex in optional}
    uncovered = [
        pair
        for pair in pairs
        if not any(covers_pair(word, *pair, core_index, adjacency) for word in bank)
    ]
    for index, pair in enumerate(uncovered):
        bank.add(solve_extension(core, adjacency, set(pair), flip=bool(index & 1)))

    words = sorted(bank, key=lambda word: sha256(word.encode()).hexdigest())
    cover_sets = [
        {index for index, pair in enumerate(pairs) if covers_pair(word, *pair, core_index, adjacency)}
        for word in words
    ]
    remaining = set(range(len(pairs)))
    chosen = []
    while remaining:
        choice = max(
            (index for index in range(len(words)) if index not in chosen),
            key=lambda index: (len(cover_sets[index] & remaining), -index),
        )
        require(cover_sets[choice] & remaining, "certificate bank failed to cover a pair")
        chosen.append(choice)
        remaining -= cover_sets[choice]

    # Delete any word made redundant by later choices.
    for choice in list(reversed(chosen)):
        other_cover = set().union(*(cover_sets[index] for index in chosen if index != choice))
        if len(other_cover) == len(pairs):
            chosen.remove(choice)

    certificate = {
        "format": "E477 mandatory-core extension colouring cover v1",
        "input_sha256": INPUT_HASHES,
        "core_vertices": core,
        "optional_vertices": optional,
        "candidate_core_colourings": len(words),
        "covered_optional_pairs": len(pairs),
        "core_colourings": [words[index] for index in chosen],
    }
    OUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "candidate_core_colourings": len(words),
        "certificate_core_colourings": len(chosen),
        "covered_optional_pairs": len(pairs),
        "certificate_sha256": file_hash(OUT),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
