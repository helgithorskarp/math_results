#!/usr/bin/env python3
"""Regenerate a compact positive-word cover of every nonedge pair state."""

from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def find_word(adjacency, pair, want_equal):
    colour = [-1]*len(adjacency)
    colour[0], colour[1] = 0, 1
    nodes = 0

    def visit(left):
        nonlocal nodes
        nodes += 1
        if not left:
            if (colour[pair[0]] == colour[pair[1]]) == want_equal:
                return "".join(map(str, colour))
            return None
        vertex = max(left, key=lambda v: (
            len({colour[w] for w in adjacency[v] if colour[w] >= 0}),
            len(adjacency[v]), -v))
        forbidden = {colour[w] for w in adjacency[vertex] if colour[w] >= 0}
        other = (pair[1] if vertex == pair[0]
                 else pair[0] if vertex == pair[1] else None)
        for value in range(4):
            if value in forbidden:
                continue
            if other is not None and colour[other] >= 0:
                if (value == colour[other]) != want_equal:
                    continue
            colour[vertex] = value
            answer = visit(left-{vertex})
            if answer is not None:
                return answer
        colour[vertex] = -1
        return None

    return visit(set(range(2, len(adjacency)))), nodes


def build(output):
    if output.exists():
        raise FileExistsError(output)
    geometry = json.loads((HERE/"geometry_certificate.json").read_text())
    edges = {tuple(edge) for edge in geometry["source_edges"]}
    edges.add(tuple(geometry["target_contact"]))
    adjacency = [set() for _ in range(23)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    nonedges = [pair for pair in combinations(range(23), 2) if pair not in edges]
    requests = [(pair, want_equal) for pair in nonedges
                for want_equal in (True, False)]
    all_words = []
    search_nodes = 0
    for pair, want_equal in requests:
        word, nodes = find_word(adjacency, pair, want_equal)
        search_nodes += nodes
        if word is None:
            raise RuntimeError(f"no positive word for {pair}, equal={want_equal}")
        if word not in all_words:
            all_words.append(word)

    def covered(word, request):
        pair, want_equal = request
        return (word[pair[0]] == word[pair[1]]) == want_equal

    uncovered = set(requests)
    chosen = []
    while uncovered:
        index = max(range(len(all_words)),
                    key=lambda i: sum(covered(all_words[i], request)
                                      for request in uncovered))
        chosen.append(index)
        uncovered = {request for request in uncovered
                     if not covered(all_words[index], request)}

    # Deterministic inclusion-minimal cleanup of the greedy cover.
    changed = True
    while changed:
        changed = False
        for index in list(chosen):
            trial = [other for other in chosen if other != index]
            if all(any(covered(all_words[other], request) for other in trial)
                   for request in requests):
                chosen = trial
                changed = True
                break

    certificate = {
        "schema": "fish-contact-pair-cover-v1",
        "fixed_edge_colours": {"0": 0, "1": 1},
        "words": [all_words[index] for index in chosen],
        "production": {
            "all_positive_request_search_nodes": search_nodes,
            "raw_unique_words": len(all_words),
            "covered_nonedges": len(nonedges),
            "covered_pair_state_requests": len(requests),
            "cover_is_inclusion_minimal": True,
            "minimum_cardinality_claimed": False,
        },
    }
    output.write_text(json.dumps(certificate, indent=2, sort_keys=True)+"\n")
    return {"output": str(output), "bytes": output.stat().st_size,
            "words": len(certificate["words"]), "search_nodes": search_nodes}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path, help="new output path")
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2, sort_keys=True))
