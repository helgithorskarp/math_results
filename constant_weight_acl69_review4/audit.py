#!/usr/bin/env python3
"""Independent integer-mask audit of the 35 specified ACL69 core certificates.

No target Python module is imported. The input files are the pinned public
baseline and finite coloring certificate; their discovery is not trusted.
"""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "coding_theory" / "a18_6_5_coordinate_cores"
SEED_SHA = "cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d"
CERT_SHA = "145e6a56e098dd8328f8fed96bfad6f7162e4294f758a12340d0ecf07460861d"
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SUPPORTS = [[p] for p in range(18)] + [[p, 17] for p in range(17)]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def coordinates(mask):
    return [p for p in range(18) if mask & (1 << p)]


def lex_rank(mask):
    # Zero-based lexicographic rank among increasing five-tuples.
    return 8567 - sum(math.comb(17 - p, 5 - i)
                      for i, p in enumerate(coordinates(mask)))


class Universe:
    def __init__(self, raw_seed):
        need(hashlib.sha256(raw_seed).hexdigest() == SEED_SHA, "seed identity")
        words = raw_seed.decode("ascii").splitlines()
        need(len(words) == 69, "seed cardinality")
        need(all(len(w) == 18 and set(w) <= {"0", "1"} and w.count("1") == 5
                 for w in words), "seed word format")
        self.seed = [sum((1 << p) for p in range(18) if w[p] == "1")
                     for w in words]
        self.seed_set = set(self.seed)
        need(len(self.seed_set) == 69, "distinct seed words")
        self.histogram = {}
        for i, a in enumerate(self.seed):
            for b in self.seed[i + 1:]:
                d = (a ^ b).bit_count()
                need(d >= 6, "seed distance")
                self.histogram[str(d)] = self.histogram.get(str(d), 0) + 1
        # Enumerate integers, rather than itertools' increasing subsets.
        self.blocks = [m for m in range(1 << 18) if m.bit_count() == 5]
        need(len(self.blocks) == math.comb(18, 5) == 8568, "complete universe")
        ranks = {lex_rank(m): m for m in self.blocks}
        need(set(ranks) == set(range(8568)), "lex rank is a bijection")
        need(coordinates(ranks[0]) == [0, 1, 2, 3, 4]
             and coordinates(ranks[1]) == [0, 1, 2, 3, 5]
             and coordinates(ranks[8567]) == [13, 14, 15, 16, 17], "rank endpoints")
        self.lex_blocks = [ranks[r] for r in range(8568)]
        self.new = [m for m in self.lex_blocks if m not in self.seed_set]
        # A row bit is set exactly when a new block conflicts with that seed.
        # For weight five, distance < 6 is equivalent to intersection >= 3.
        self.conflicts = {
            m: sum(1 << j for j, b in enumerate(self.seed)
                   if (m ^ b).bit_count() < 6) for m in self.new
        }
        self.distance_comparisons = len(self.new) * len(self.seed)

    def residual(self, support):
        sm = sum(1 << p for p in support)
        core_rows = [j for j, b in enumerate(self.seed) if not b & sm]
        removed = [b for b in self.seed if b & sm]
        core_signature = sum(1 << j for j in core_rows)
        candidates = [m for m in self.new
                      if not self.conflicts[m] & core_signature]
        return core_rows, removed, candidates


def verify(data, universe):
    need(isinstance(data, dict), "certificate object")
    need(data.get("schema") == "acl69-coordinate-clique-cover-v1", "schema")
    need(data.get("seed_sha256") == SEED_SHA, "certificate seed")
    need(data.get("alphabet") == ALPHABET, "alphabet")
    covers = data.get("covers")
    need(isinstance(covers, list) and len(covers) == 35, "complete support cohort")
    supplied_supports = []
    for e in covers:
        need(isinstance(e, dict) and isinstance(e.get("coordinates"), list),
             "support format")
        need(all(type(p) is int for p in e["coordinates"]), "integer coordinates")
        supplied_supports.append(e["coordinates"])
    need(supplied_supports == SUPPORTS, "exact ordered support cohort")
    results = []
    pairs = 0
    cliques = 0
    for support, entry in zip(SUPPORTS, covers):
        core, removed, candidates = universe.residual(support)
        colors = entry.get("colors")
        need(type(colors) is str and len(colors) == len(candidates),
             "complete candidate assignment")
        classes = [[m] for m in removed]
        for m, char in zip(candidates, colors):
            need(char in ALPHABET, "known color")
            index = ALPHABET.index(char)
            need(index < len(classes), "color range")
            classes[index].append(m)
        flattened = [m for group in classes for m in group]
        need(len(flattened) == len(set(flattened))
             and set(flattened) == set(removed) | set(candidates),
             "exact residual partition")
        for group in classes:
            for j, a in enumerate(group):
                for b in group[j + 1:]:
                    need((a ^ b).bit_count() < 6, "non-clique pair")
                    pairs += 1
        need(len(core) + len(classes) == 69, "completion upper bound")
        cliques += len(classes)
        results.append({"coordinates": support, "core_size": len(core),
                        "new_candidates": len(candidates),
                        "cliques": len(classes), "maximum_completion": 69})
    return {"seed_words": 69, "universe_words": 8568,
            "seed_distance_histogram": dict(sorted(universe.histogram.items())),
            "new_to_seed_distance_comparisons": universe.distance_comparisons,
            "supports": 35, "new_candidate_occurrences": sum(
                r["new_candidates"] for r in results),
            "unconditional_clique_inequalities": cliques,
            "within_class_pairs_checked": pairs, "results": results}


def controls(data, universe):
    bad_cases = []

    def add(name, mutate, expected):
        bad = copy.deepcopy(data)
        mutate(bad)
        bad_cases.append((name, bad, expected))

    add("wrong seed declaration", lambda c: c.update(seed_sha256="0" * 64),
        "certificate seed")
    add("missing support", lambda c: c["covers"].pop(), "complete support cohort")
    add("duplicate support", lambda c: c["covers"][1].update(coordinates=[0]),
        "exact ordered support cohort")
    add("truncated candidate list",
        lambda c: c["covers"][0].update(colors=c["covers"][0]["colors"][:-1]),
        "complete candidate assignment")
    add("out of range color", lambda c: c["covers"][0].update(
        colors="Z" + c["covers"][0]["colors"][1:]), "color range")
    add("unknown color", lambda c: c["covers"][0].update(
        colors="!" + c["covers"][0]["colors"][1:]), "known color")
    _, removed, candidates = universe.residual([0])
    wrong = next((k, j) for k, m in enumerate(candidates)
                 for j, b in enumerate(removed) if (m ^ b).bit_count() >= 6)

    def force_compatible(c):
        colors = list(c["covers"][0]["colors"])
        colors[wrong[0]] = ALPHABET[wrong[1]]
        c["covers"][0]["colors"] = "".join(colors)

    add("compatible pair in a class", force_compatible, "non-clique pair")
    rejected = []
    for name, bad, expected in bad_cases:
        try:
            verify(bad, universe)
        except ValueError as e:
            need(str(e) == expected, f"unexpected control failure: {name}: {e}")
            rejected.append(name)
        else:
            raise ValueError(f"accepted malformed certificate: {name}")
    return rejected


def refinement_witness(data, universe):
    """Exact fractional witness against redundancy of one clique inequality."""
    points = [[2, 4, 9, 13, 17], [2, 4, 8, 10, 17], [2, 8, 9, 16, 17]]
    words = [sum(1 << p for p in block) for block in points]
    core, removed, candidates = universe.residual([2])
    colors = data["covers"][2]["colors"]
    group = [removed[12]] + [m for m, c in zip(candidates, colors)
                             if ALPHABET.index(c) == 12]
    need(all(m in group for m in words), "fractional witness class membership")
    need(all((a ^ b).bit_count() == 4 for i, a in enumerate(words)
             for b in words[i + 1:]), "fractional witness pair distances")
    need((words[0] & words[1] & words[2]).bit_count() == 2,
         "fractional witness common intersection")
    # Set each core word to 1, the three displayed words to 1/2, and all
    # other variables to 0. Scale by 2 so every check is integer arithmetic.
    core_words = [universe.seed[j] for j in core]
    triples = [m for m in range(1 << 18) if m.bit_count() == 3]
    need(len(triples) == 816, "complete triple constraints")
    loads = [2 * sum(t & m == t for m in core_words)
             + sum(t & m == t for m in words) for t in triples]
    need(max(loads) <= 2, "fractional triple feasibility")
    need(len(words) == 3 > 2, "strict clique violation")
    return {"coordinates": [2], "class_index": 12, "blocks": points,
            "common_intersection": [2, 17], "block_weight_denominator": 2,
            "core_word_weights": 1, "core_words": len(core),
            "triple_constraints_checked": 816, "max_scaled_triple_load": max(loads),
            "clique_load_numerator": 3, "clique_capacity_numerator": 2}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=Path, default=TARGET / "acl69.txt")
    parser.add_argument("--certificate", type=Path, default=TARGET / "certificates.json")
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == CERT_SHA, "target certificate identity")
    data = json.loads(raw)
    universe = Universe(args.seed.read_bytes())
    result = verify(data, universe)
    result["seed_sha256"] = SEED_SHA
    result["certificate_sha256"] = CERT_SHA
    result["rejected_mutations"] = controls(data, universe)
    result["nontriple_clique_witness"] = refinement_witness(data, universe)
    if args.expect:
        need(result == json.loads(args.expect.read_text()), "expected audit differs")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
