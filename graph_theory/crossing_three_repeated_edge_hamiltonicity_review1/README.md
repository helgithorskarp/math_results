# Review package: repeated crossed edges at crossing number three

This directory contains an independent high-confidence review of the relative
projective-planar Hamiltonian-path theorem in
[`crossing_three_repeated_edge_hamiltonicity`](../../crossing_three_repeated_edge_hamiltonicity/).

The review audits every human premise and completeness reduction, aligns the
three external Tutte-path inputs with their primary source, and tests the
smallest boundary cases independently.  The verdict and caveats are in
[`REVIEW.md`](REVIEW.md).

## Reproduction

Python 3.11.2 and the standard library are sufficient.

```bash
python3 check_small_graphs.py > actual.json
diff -u EXPECTED_OUTPUT.json actual.json
python3 -O check_small_graphs.py > actual-optimized.json
diff -u EXPECTED_OUTPUT.json actual-optimized.json
sha256sum -c SHA256SUMS
```

The checker enumerates all labelled 4-connected graphs on five and six
vertices and tests the relative claim for every edge.  It also validates an
explicit projective-plane triangulation of `K_6`, the premise making the
census exhaustive over projective-planar graphs at those orders.

No third-party packages, random choices, floating-point arithmetic, solver,
or target implementation are used.
