#!/usr/bin/env python3
"""Independent truth-vector coverage and physical five-set verification."""
import argparse
import itertools as it
import json
from collections import Counter
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def words():
    # This obtains the domain from all labeled words, not the producer's
    # combinations-with-replacement iterator.
    return sorted({tuple(sorted(w)) for w in it.product(range(6), repeat=5)})


def verify(cert):
    require(type(cert) is dict and set(cert) == {"schema", "records"}, "schema keys")
    require(cert["schema"] == "r55-two-pentagons-v1", "schema version")
    require(type(cert["records"]) is list, "records must be a list")
    records = {}
    for row in cert["records"]:
        require(type(row) is list and len(row) == 3 and
                all(type(x) is int for x in row), "record format")
        wi, mask, witness = row
        require(0 <= wi < 252 and 0 <= mask < 1024 and
                0 <= witness < 1024 and witness.bit_count() == 5 and
                witness != 31, "record ranges / second five-set")
        require((wi, mask) not in records, "duplicate coverage key")
        records[wi, mask] = witness

    domain = words()
    require(len(domain) == 252, "word domain")
    pairs = list(it.combinations(range(5, 10), 2))
    full = (1 << 1024) - 1
    columns = [sum(1 << m for m in range(1024) if m >> k & 1)
               for k in range(10)]
    found = set()
    per_word = []
    for wi, word in enumerate(domain):
        edge = {}
        for i, j in it.combinations(range(10), 2):
            if j < 5:
                edge[i, j] = full if j - i in (1, 4) else 0
            elif i < 5:
                edge[i, j] = full if word[j - 5] == i + 1 else 0
            else:
                edge[i, j] = columns[pairs.index((i, j))]
        good = full
        for triple in it.combinations(range(10), 3):
            bad = full
            for e in it.combinations(triple, 2):
                bad &= edge[e]
            good &= full ^ bad
        for five in it.combinations(range(10), 5):
            has_edge = 0
            for e in it.combinations(five, 2):
                has_edge |= edge[e]
            good &= has_edge
        per_word.append(good.bit_count())
        while good:
            bit = good & -good
            good ^= bit
            mask = bit.bit_length() - 1
            key = (wi, mask)
            require(key in records, f"missing admissible graph {key}")
            found.add(key)
            s = [v for v in range(10) if records[key] >> v & 1]
            for v in s:
                degree = sum((edge[tuple(sorted((v, u)))] >> mask) & 1
                             for u in s if v != u)
                require(degree == 2, f"invalid pentagon at {key}")
    require(found == set(records), "extra inadmissible graph")

    # Every arbitrary labeling of the five outside stars can be sorted.
    # Its induced map on all ten outside edge coordinates is a bijection,
    # covering all 1024 graphs without imposing an automorphism on a graph.
    normalizations = 0
    ep = list(it.combinations(range(5), 2))
    for w in it.product(range(6), repeat=5):
        order = sorted(range(5), key=lambda i: (w[i], i))
        require(tuple(w[i] for i in order) in domain, "normalization missing")
        moved = [ep.index(tuple(sorted((order[i], order[j])))) for i, j in ep]
        require(sorted(moved) == list(range(10)), "edge coordinates not bijective")
        normalizations += 1

    # For a triangle-free graph, a vertex with two pentagon contacts has
    # a second pentagon. Check the actual six-vertex graph for every star.
    star_cases = Counter()
    for mask in range(32):
        edges = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
        edges |= {(i, 5) for i in range(5) if mask >> i & 1}
        if any(all(e in edges for e in it.combinations(t, 2))
               for t in it.combinations(range(6), 3)):
            star_cases["triangle"] += 1
        elif mask.bit_count() <= 1:
            star_cases["zero_or_one_contact"] += 1
        else:
            require(any(set(s) != set(range(5)) and
                        all(sum(tuple(sorted((i, j))) in edges for j in s if i != j) == 2
                            for i in s) for s in it.combinations(range(6), 5)),
                    "missing second pentagon in one-star case")
            star_cases["second_pentagon"] += 1

    return {"status": "VERIFIED_TWO_PENTAGONS_AT_TEN",
            "normalized_words": len(domain), "outside_graphs_per_word": 1024,
            "physical_normalized_graphs": len(domain) * 1024,
            "admissible_graphs": len(found), "per_word_admissible": per_word,
            "labeled_word_normalizations": normalizations,
            "one_star_cases": dict(sorted(star_cases.items()))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.certificate.read_text())), sort_keys=True))
