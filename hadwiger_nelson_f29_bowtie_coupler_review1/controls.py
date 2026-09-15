#!/usr/bin/env python3
"""Small exhaustive oracles and semantic corruptions for the review checker."""

from itertools import combinations, product
from pathlib import Path
import copy
import json
import tempfile

import verify as v


def brute_list_colouring(adjacency, domains):
    for word in product(range(3), repeat=len(adjacency)):
        if not all(word[vertex] in domains[vertex] for vertex in range(len(adjacency))):
            continue
        if all(word[a] != word[b] for a in range(len(adjacency)) for b in adjacency[a]):
            return word
    return None


def generic_square(axis):
    radicands = (1, 3, 11, 33)
    output = [0, 0, 0, 0]
    index = {value: position for position, value in enumerate(radicands)}
    for i, left in enumerate(axis):
        for j, right in enumerate(axis):
            common = radicands[i] * radicands[j]
            square_factor = 1
            for prime in (3, 11):
                if common % (prime * prime) == 0:
                    common //= prime * prime
                    square_factor *= prime
            output[index[common]] += left * right * square_factor
    return tuple(output)


def main():
    certificate = json.loads((v.BASE / "certificate.json").read_text())
    expected = json.loads((v.BASE / "EXPECTED.json").read_text())
    v.require(v.review(v.BASE / "source29.tsv", certificate) == expected, "valid baseline")

    arithmetic_cases = 0
    for axis in product(range(-2, 3), repeat=4):
        v.require(v.square_quartic(axis) == generic_square(axis), "quartic-square oracle")
        arithmetic_cases += 1

    pairs = list(combinations(range(4), 2))
    domain_choices = [tuple(c for c in range(3) if mask & (1 << c)) for mask in range(1, 8)]
    orders = ((0, 1, 2, 3), (3, 2, 1, 0), (1, 3, 0, 2))
    list_cases = 0
    dp_order_cases = 0
    for flags in range(1 << len(pairs)):
        adjacency = [set() for _ in range(4)]
        for index, (a, b) in enumerate(pairs):
            if flags & (1 << index):
                adjacency[a].add(b)
                adjacency[b].add(a)
        for choice in product(domain_choices, repeat=4):
            domains = dict(enumerate(choice))
            brute = brute_list_colouring(adjacency, domains)
            for order in orders:
                answer = v.path_dp(adjacency, order, domains, return_assignment=True)
                v.require((answer is None) == (brute is None), "frontier/brute existence")
                if answer is not None:
                    v.require(all(answer[x] in domains[x] for x in range(4)), "frontier domains")
                    v.require(
                        all(answer[a] != answer[b] for a in range(4) for b in adjacency[a]),
                        "frontier edges",
                    )
                dp_order_cases += 1
            list_cases += 1

    raw = (v.BASE / "source29.tsv").read_bytes()
    with tempfile.TemporaryDirectory() as temporary:
        corrupt_source = Path(temporary) / "source29.tsv"
        corrupt_source.write_bytes(raw.replace(b"28 12 0 0 0", b"28 11 0 0 0"))
        try:
            v.review(corrupt_source, certificate)
        except ValueError:
            source_corruption_rejected = True
        else:
            raise ValueError("source corruption accepted")

    corruptions = []
    variants = []
    altered = copy.deepcopy(certificate)
    altered["fresh_union_word"] = "0" + altered["fresh_union_word"][1:]
    variants.append(("fresh union word", altered))
    altered = copy.deepcopy(certificate)
    word = list(altered["target_proper_four_word"])
    word[29] = word[0]
    altered["target_proper_four_word"] = "".join(word)
    variants.append(("private contact colour", altered))
    altered = copy.deepcopy(certificate)
    altered["forbidden_joint_terminal_word"] = altered["forbidden_joint_terminal_word"][:-1] + "3"
    variants.append(("forbidden palette", altered))
    for name, altered in variants:
        try:
            v.review(v.BASE / "source29.tsv", altered)
        except ValueError:
            corruptions.append(name)
        else:
            raise ValueError("semantic corruption accepted: " + name)

    print(
        json.dumps(
            {
                "valid_baseline_passed": True,
                "quartic_square_oracle_cases": arithmetic_cases,
                "four_vertex_list_instances": list_cases,
                "frontier_order_comparisons": dp_order_cases,
                "source_corruption_rejected": source_corruption_rejected,
                "semantic_corruptions_rejected": corruptions,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
