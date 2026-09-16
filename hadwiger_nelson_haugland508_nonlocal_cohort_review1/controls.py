#!/usr/bin/env python3
"""Negative controls for the reviewer-supplied union word."""

import json

import verify as v


def main() -> None:
    cert = json.loads((v.HERE / "certificate.json").read_text())
    target = v.read_hashed(v.TARGET / "certificate.json", v.TARGET_CERT_SHA256)
    edges, adjacency = v.load_parent()
    supports = [v.frozen_support(r["seed"], r["orientation"], adjacency) for r in target["records"]]
    labels = sorted(set().union(*map(set, supports)))
    actual_edges = v.induced(labels, edges)
    good = cert["union_four_word"]
    v.check_word(labels, actual_edges, good, 4)
    u, w = actual_edges[0]
    corrupted = list(good)
    corrupted[labels.index(w)] = corrupted[labels.index(u)]
    bad = [good[:-1], good + "0", "4" + good[1:], "".join(corrupted)]
    rejected = 0
    for word in bad:
        try:
            v.check_word(labels, actual_edges, word, 4)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("accepted malformed union word")
    v.require(rejected == 4, "all malformed controls")
    print(json.dumps({"invalid_union_words_rejected": rejected, "solver_used": False}, sort_keys=True))


if __name__ == "__main__":
    main()

