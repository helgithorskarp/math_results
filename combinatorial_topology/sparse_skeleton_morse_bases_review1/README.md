# Independent review: sparse one-skeleton collapse matroid

This directory independently audits the theorem and implementation in
[`../sparse_skeleton_morse_bases`](../sparse_skeleton_morse_bases).  The
review verdict is **accept with high confidence**, subject to the scope and
minor documentation corrections in [`REVIEW.md`](REVIEW.md).

The checker does not import the producer's code.  It exhausts all `2^20`
triangle systems on six labelled vertices.  Exactly 74,558 have triangle
support satisfying the hereditary edge bound.  For every admitted system it
computes boundary ranks over `F2` and `F3`, recursively explores both some and
every maximal free-edge peeling order, and recognizes all minimal dependencies
from vertex links and Euler characteristic.  It separately exhausts 86,276
top-dimensional Morse assignments and 9,561 ternary-weight objectives on five
small adversarial fixtures.  The six-vertex projective plane plus an isolated
vertex is the negative control.

## Reproduce

Python 3.11 or later and the standard library suffice.

```sh
python3 independent_check.py
sha256sum -c SHA256SUMS
```

The first command takes about eleven seconds on the review host and compares
its result with `expected.json`.  It uses explicit failures rather than Python
`assert`, so `python3 -O independent_check.py` checks the same claims.

The finite computation validates the reductions and smallest cases; it does
not prove the universal theorem.  The ordinary proof audit in `REVIEW.md` is
the basis for the universal verdict.
