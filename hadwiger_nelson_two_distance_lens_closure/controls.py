#!/usr/bin/env python3
"""Small corruption controls for the exact graph and witness semantics."""
import json

from verify import HERE, ONE, ROOT2_OVER_2, build_graph, mul, proper, word


def main():
    points, edges, source_ids, long_edges, _ = build_graph()
    cert = json.loads((HERE / "certificate.json").read_text())
    four = list(word(cert["four_colouring"], len(points), 4))
    a, b = edges[0]
    four[b] = four[a]
    if proper(four, edges):
        raise ValueError("monochromatic-edge corruption accepted")

    first = cert["long_pair_equal_four_colourings"][0]
    colours = word(first["word"], len(points), 4)
    i, j = long_edges[0]
    if colours[source_ids[i]] != colours[source_ids[j]]:
        raise ValueError("published equality witness is not equal")
    if mul(ROOT2_OVER_2, ROOT2_OVER_2) != tuple(x / 2 for x in ONE):
        raise ValueError("sqrt(2)/2 field identity")

    print(json.dumps({
        "monochromatic_edge_corruption_rejected": True,
        "first_long_pair_equality_checked": True,
        "quadratic_field_identity_checked": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
