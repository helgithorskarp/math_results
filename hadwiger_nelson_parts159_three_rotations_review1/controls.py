#!/usr/bin/env python3
"""Fast independent controls for field arithmetic and positive witnesses."""

import json
import independent_audit as A


def main() -> None:
    points = A.read_points()
    edges = A.unit_edges(points)
    extra, extensions, cycles = A.certificate_data(edges)
    rejected = 0
    for word in extra:
        bad = list(word)
        edge = next((i, j) for i, j in edges if bad[i] != bad[j])
        bad[edge[1]] = bad[edge[0]]
        A.require(not A.proper(tuple(bad), edges), "monochromatic corruption accepted")
        rejected += 1

    # Each defining quotient relation is separately exercised.
    tr = A.mul(A.T, (A.Q(0), A.Q(0), A.Q(1), A.Q(0)))
    A.require(A.mul(A.T, A.T) == A.scale(A.ONE, A.Q(-3)), "t relation")
    A.require(A.mul((A.Q(0), A.Q(0), A.Q(1), A.Q(0)),
                    (A.Q(0), A.Q(0), A.Q(1), A.Q(0))) == A.scale(A.ONE, A.Q(-11)),
              "r relation")
    A.require(A.mul(tr, tr) == A.scale(A.ONE, A.Q(33)), "tr relation")
    A.require(A.real_sqrt((A.Q(1), A.Q(0))) == (A.Q(1), A.Q(0)), "square positive")
    A.require(A.real_sqrt((A.Q(2), A.Q(0))) is None, "nonsquare negative control")

    result = {
        "all_controls": True,
        "certificate_rows": len(extensions) + len(cycles),
        "corrupt_component_words_rejected": rejected,
        "internal_edges": len(edges),
        "quotient_relations": 3,
    }
    A.require(result == json.loads((A.HERE / "EXPECTED_CONTROLS.json").read_text()),
              "expected controls mismatch")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
