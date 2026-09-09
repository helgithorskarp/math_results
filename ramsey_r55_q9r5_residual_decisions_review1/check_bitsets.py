#!/usr/bin/env python3
"""Reviewer-1 definition-level audit of all h4089 residual witnesses.

The submitted CNFs, clause metadata, encoders, and SAT solver are deliberately
ignored.  Each ledger word is decoded as a literal graph, matched to its fixed
blue blocks and graph6 core, and searched for forbidden cliques with a bitset
branching algorithm rather than exhaustive subset enumeration.
"""

from pathlib import Path
import argparse
import csv
import hashlib
from itertools import combinations
import json


N = 23
PAIR_COUNT = N * (N - 1) // 2
FIELDS = [
    "index",
    "task",
    "whole_task_status",
    "residual_status",
    "clauses",
    "cnf_sha256",
    "residual_edgeword",
]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def graph6_core(row):
    need(len(row) == 5 and row[0] == ord("F"), "graph6 order/header")
    payload = [value - 63 for value in row[1:]]
    need(all(0 <= value < 64 for value in payload), "graph6 character")
    need(payload[-1] & 7 == 0, "graph6 padding")

    adjacency = [0] * 7
    bit_index = 0
    for high in range(1, 7):
        for low in range(high):
            value = (payload[bit_index // 6] >> (5 - bit_index % 6)) & 1
            if value:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            bit_index += 1
    need(bit_index == 21, "graph6 edge count")
    return adjacency


def decode_edgeword(word):
    need(type(word) is str and len(word) == 64, "edgeword length")
    need(all(character in "0123456789abcdef" for character in word), "edgeword alphabet")
    integer = int(word, 16)
    need(integer < 1 << PAIR_COUNT, "edgeword padding")
    adjacency = [0] * N
    bit_index = 0
    for low in range(N - 1):
        for high in range(low + 1, N):
            if integer >> bit_index & 1:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            bit_index += 1
    need(bit_index == PAIR_COUNT, "physical pair count")
    return integer, adjacency


def complement(adjacency):
    universe = (1 << len(adjacency)) - 1
    return [universe ^ (1 << vertex) ^ neighbors for vertex, neighbors in enumerate(adjacency)]


def find_clique(adjacency, order):
    """Return one clique via ordered bitset branching, or None."""

    def extend(candidates, remaining, chosen):
        if remaining == 0:
            return chosen
        if candidates.bit_count() < remaining:
            return None
        while candidates:
            lowest = candidates & -candidates
            vertex = lowest.bit_length() - 1
            candidates ^= lowest
            result = extend(candidates & adjacency[vertex], remaining - 1, chosen + (vertex,))
            if result is not None:
                return result
            if candidates.bit_count() < remaining:
                break
        return None

    return extend((1 << len(adjacency)) - 1, order, ())


def clique_algorithm_controls():
    """Compare bitset branching to the definition on every graph of order 5."""
    pairs = list(combinations(range(5), 2))
    comparisons = 0
    for code in range(1 << len(pairs)):
        adjacency = [0] * 5
        for bit, (low, high) in enumerate(pairs):
            if code >> bit & 1:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
        for order in range(2, 6):
            expected = any(
                all(adjacency[low] >> high & 1 for low, high in combinations(vertices, 2))
                for vertices in combinations(range(5), order)
            )
            need((find_clique(adjacency, order) is not None) == expected, "bitset clique control")
            comparisons += 1
    return comparisons


def induced(adjacency, vertices):
    position = {vertex: index for index, vertex in enumerate(vertices)}
    result = [0] * len(vertices)
    for source in vertices:
        for target in vertices:
            if source < target and adjacency[source] >> target & 1:
                i, j = position[source], position[target]
                result[i] |= 1 << j
                result[j] |= 1 << i
    return result


def check_graph(core, word):
    integer, red = decode_edgeword(word)
    for block in range(4):
        vertices = range(4 * block, 4 * block + 4)
        need(all(not (red[u] >> v & 1) for u in vertices for v in vertices if u < v), "fixed block is not blue")

    physical_core = induced(red, range(16, 23))
    need(physical_core == core, "physical graph does not match pinned core")
    need(find_clique(red, 4) is None, "red K4 in residual witness")
    need(find_clique(complement(red), 5) is None, "blue K5 in residual witness")
    return integer.bit_count(), tuple(sorted(neighbors.bit_count() for neighbors in red))


def load_catalogue(path):
    data = Path(path).read_bytes()
    rows = data.splitlines()
    need(len(rows) == len(set(rows)) == 362, "catalogue cardinality/distinctness")
    cores = [graph6_core(row) for row in rows]
    for core in cores:
        need(find_clique(core, 4) is None, "catalogue core has a red K4")
        need(find_clique(complement(core), 4) is None, "catalogue core has a blue K4")
    return data, cores


def load_ledger(path):
    with Path(path).open(newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        need(reader.fieldnames == FIELDS, "ledger header")
        rows = list(reader)
    need(len(rows) == 362, "ledger cardinality")
    return rows


def run(catalogue_path, ledger_path):
    control_comparisons = clique_algorithm_controls()
    catalogue_bytes, cores = load_catalogue(catalogue_path)
    rows = load_ledger(ledger_path)
    red_counts = []
    degree_hash = hashlib.sha256()
    witness_hash = hashlib.sha256()
    distinct_words = set()
    for index, (core, row) in enumerate(zip(cores, rows)):
        need(list(row) == FIELDS, "ledger field order")
        need(row["index"] == str(index), "ledger index")
        need(row["task"] == f"bo1-q9-r5-c{index:06d}", "original task identity")
        need(row["whole_task_status"] == "UNKNOWN", "whole-task status overclaim")
        need(row["residual_status"] == "SAT", "residual status")
        need(row["clauses"].isdigit(), "clause count syntax")
        need(len(row["cnf_sha256"]) == 64 and all(c in "0123456789abcdef" for c in row["cnf_sha256"]), "CNF hash syntax")
        red_edges, degrees = check_graph(core, row["residual_edgeword"])
        red_counts.append(red_edges)
        distinct_words.add(row["residual_edgeword"])
        degree_hash.update(json.dumps([index, degrees], separators=(",", ":")).encode() + b"\n")
        witness_hash.update(f'{index}\t{row["residual_edgeword"]}\n'.encode())

    need(len(distinct_words) == 362, "duplicate residual edgeword")

    # Definition-level corruption controls; none call the target verifier.
    first = int(rows[0]["residual_edgeword"], 16)
    pair_index = {}
    bit = 0
    for low in range(N - 1):
        for high in range(low + 1, N):
            pair_index[low, high] = bit
            bit += 1

    def with_edges(value, vertices, red_value):
        for low in vertices:
            for high in vertices:
                if low < high:
                    mask = 1 << pair_index[low, high]
                    value = value | mask if red_value else value & ~mask
        return f"{value:064x}"

    controls = {
        "padding": f"{first | (1 << PAIR_COUNT):064x}",
        "fixed_blue_edge": f"{first | (1 << pair_index[0, 1]):064x}",
        "red_K4": with_edges(first, (0, 4, 8, 12), True),
        "blue_K5": with_edges(first, (0, 4, 8, 12, 16), False),
        "wrong_core": f"{first ^ (1 << pair_index[16, 17]):064x}",
    }
    rejected = []
    for name, word in controls.items():
        try:
            check_graph(cores[0], word)
        except ValueError:
            rejected.append(name)
        else:
            raise RuntimeError("accepted corrupted witness: " + name)

    return {
        "status": "ALL_362_LITERAL_RESIDUAL_WITNESSES_VALID",
        "catalogue_sha256": hashlib.sha256(catalogue_bytes).hexdigest(),
        "catalogue_cores": len(cores),
        "catalogue_cores_literal_ramsey_4_4": len(cores),
        "ledger_sha256": file_sha256(ledger_path),
        "tasks_checked": len(rows),
        "distinct_residual_edgewords": len(distinct_words),
        "red_edge_range": [min(red_counts), max(red_counts)],
        "degree_stream_sha256": degree_hash.hexdigest(),
        "witness_stream_sha256": witness_hash.hexdigest(),
        "red_K4_found": False,
        "blue_K5_found": False,
        "new_whole_task_exclusions": 0,
        "good43_found": False,
        "cnfs_trusted": False,
        "solver_calls": 0,
        "bitset_clique_control_comparisons": control_comparisons,
        "corruptions_rejected": rejected,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("catalogue", type=Path)
    parser.add_argument("--ledger", type=Path, default=Path(__file__).resolve().parent.parent / "ramsey_r55_q9r5_residual_decisions" / "LEDGER.tsv")
    parser.add_argument("--expected", type=Path)
    args = parser.parse_args()
    result = run(args.catalogue, args.ledger)
    if args.expected:
        need(result == json.loads(args.expected.read_text()), "expected result mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
