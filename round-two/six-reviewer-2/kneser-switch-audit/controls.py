#!/usr/bin/env python3
"""Literal published-book checks and rejection of damaged comparison data."""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import audit


def edge(text):
    return audit.EDGE_INDEX[tuple(map(int, text))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-records", type=Path)
    args = parser.parse_args()
    # Root-labeled page lists from six-books-2 PROOF.md, checked using
    # the reviewer's adjacency function, not the author's checker.
    clique = lambda roots: audit.encoded(combinations(roots, 2))
    join = lambda u, h: audit.encoded(list(combinations(u, 2)) +
                                    [(x, y) for x in u for y in h])
    fixtures = [
        (clique((0, 1, 2)), "03", "14", True, "01 25 26 56"),
        (clique((0, 1, 2, 3)), "45", "46", False, "01 02 03 12 13 23 04 14 24 34 56"),
        (clique((0, 1, 2, 3, 4)), "01", "56", False, "02 03 04 12 13 14 25 26 35 36 45 46"),
        (clique((0, 1, 2, 3, 4, 5)), "06", "16", False, "23 24 25 26 34 35 36 45 46 56"),
        (join((3, 4), (0, 1, 2)), "01", "35", True, "03 13 26 46"),
        (join((4, 5), (0, 1, 2, 3)), "06", "45", False, "01 02 03 16 26 36 14 15 24 25 34 35"),
        (join((3, 4, 5), (0, 1, 2)), "06", "34", False, "01 02 16 26 56 23 24 13 14 35 45"),
    ]
    for cut, first, second, color, pages in fixtures:
        i, j = edge(first), edge(second)
        audit.require(audit.red(cut, i, j) == color, "published spine color differs")
        computed = {k for k in range(21) if k not in (i, j)
                    and audit.red(cut, i, k) == color
                    and audit.red(cut, j, k) == color}
        audit.require(computed == {edge(p) for p in pages.split()},
                      "published literal page list differs")
    _, records = audit.audit(run_domain=False)
    rejected = 0
    if args.author_records:
        original = json.loads(args.author_records.read_text())
        audit.compare_author(records, args.author_records)
        damaged = []
        x = deepcopy(original); x["records"].pop(); damaged.append(x)
        x = deepcopy(original); x["records"][1][2] += 1; damaged.append(x)
        x = deepcopy(original); x["cuts_scanned"] -= 1; damaged.append(x)
        x = deepcopy(original); x["record_sha256"] = "0" * 64; damaged.append(x)
        x = deepcopy(original); x["maximum_blue_pages_histogram"]["10"] -= 1; damaged.append(x)
        with TemporaryDirectory() as temporary:
            candidate = Path(temporary) / "damaged.json"
            for record in damaged:
                candidate.write_text(json.dumps(record))
                try:
                    audit.compare_author(records, candidate)
                except RuntimeError:
                    rejected += 1
                else:
                    raise RuntimeError("damaged author comparison was accepted")
        audit.require(rejected == 5, "incomplete corruption controls")
    print(json.dumps({"published_books_checked_independently": len(fixtures),
                      "damaged_author_controls_rejected": rejected,
                      "fixture_only": True}, indent=2))


if __name__ == "__main__":
    main()
