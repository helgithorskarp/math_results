#!/usr/bin/env python3
"""Check covers by direct set intersections; do not import the generator."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED_HASH = "cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d"
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(certificate_path, seed_path=ROOT / "acl69.txt"):
    raw = seed_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SEED_HASH, "wrong seed hash")
    words = raw.decode("ascii").splitlines()
    require(len(words) == 69, "wrong number of seed words")
    for word in words:
        require(len(word) == 18 and set(word) <= set("01") and word.count("1") == 5,
                "malformed seed word")
    seed = [frozenset(i for i, c in enumerate(s) if c == "1") for s in words]
    require(len(set(seed)) == 69, "duplicate seed word")
    distances = {}
    for a, b in itertools.combinations(words, 2):
        d = sum(c != e for c, e in zip(a, b))
        require(d >= 6, "seed violates minimum distance")
        distances[str(d)] = distances.get(str(d), 0) + 1
    certificate = json.loads(certificate_path.read_text())
    require(certificate.get("schema") == "acl69-coordinate-clique-cover-v1", "wrong schema")
    require(certificate.get("seed_sha256") == SEED_HASH, "wrong certificate seed")
    require(certificate.get("alphabet") == ALPHABET, "wrong alphabet")
    require(isinstance(certificate.get("covers"), list), "covers must be a list")
    supports = [(p,) for p in range(18)] + [(p, 17) for p in range(17)]
    require([tuple(c["coordinates"]) for c in certificate["covers"]] == supports,
            "missing, duplicate, extra, or reordered coordinate support")
    universe = [frozenset(b) for b in itertools.combinations(range(18), 5)]
    require(len(universe) == 8568 and len(set(universe)) == 8568, "wrong universe")
    seed_set = set(seed)
    rows = []
    class_checks = 0
    for entry, support in zip(certificate["covers"], supports):
        points = set(support)
        core = [b for b in seed if b.isdisjoint(points)]
        removed = [b for b in seed if not b.isdisjoint(points)]
        # A complete enumeration of new words, independently of triple owners.
        candidates = [b for b in universe if b not in seed_set
                      and all(len(b & old) <= 2 for old in core)]
        labels = entry["colors"]
        require(isinstance(labels, str) and len(labels) == len(candidates),
                f"incomplete residual cover for {support}")
        classes = [[b] for b in removed]
        for candidate, label in zip(candidates, labels):
            require(label in ALPHABET, "unknown color character")
            color = ALPHABET.index(label)
            require(color < len(removed), "color outside claimed cover")
            classes[color].append(candidate)
        all_residual = [b for cl in classes for b in cl]
        require(len(all_residual) == len(set(all_residual)), "duplicated residual word")
        require(set(all_residual) == set(candidates) | set(removed), "residual cover mismatch")
        for cl in classes:
            for a, b in itertools.combinations(cl, 2):
                require(len(a & b) >= 3, f"compatible words share a color for {support}")
                class_checks += 1
        require(len(core) + len(classes) == 69, "incorrect completion bound")
        rows.append({"coordinates": list(support), "core_size": len(core),
                     "new_candidates": len(candidates), "residual_words": len(all_residual),
                     "cover_size": len(classes), "maximum_completion_size": 69})
    return {"seed_words": 69, "universe_words": 8568,
            "seed_distance_histogram": dict(sorted(distances.items())),
            "verified_covers": len(rows), "within_class_pairs_checked": class_checks,
            "new_candidate_occurrences": sum(r["new_candidates"] for r in rows),
            "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
            "results": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=ROOT / "certificates.json")
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    result = verify(args.certificate)
    if args.expect:
        require(result == json.loads(args.expect.read_text()), "expected result differs")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
