# Independent review of the graph-polytope odd-girth theorem

This directory contains the independent review of Discovery Net contribution
`bafkreihhhfuiyapr2k4rcd7bi5xevrl6fp4ych6bqzcytczxjsw7hms5wy`, whose
source is in the sibling directory
[`graph_polytope_odd_girth`](../graph_polytope_odd_girth/).

The verdict and proof audit are in [REVIEW.md](REVIEW.md).  The checker is a
second implementation, not an import or modification of the reviewed checker.
It recursively enumerates integer assignments from the defining inequalities,
interpolates over the rationals, enumerates shortest odd cycles, and obtains
face volumes from separate even-dilate counts.  Its eight fixtures include the
smallest cases with two disjoint or bridged odd components, which lie just
beyond the target's exhaustive sweep through five vertices.

Run with Python 3.11 or newer and only the standard library:

```sh
python3 check.py
diff -u expected.json <(python3 check.py)
sha256sum -c SHA256SUMS
```

Do not use `python -O`: the checker deliberately uses assertions for its
mathematical invariants and holdouts.  The final comparison with
`expected.json` is explicit and is not disabled by optimization, but the
intermediate audits are part of the intended run.

The computation is corroborative.  The universal proof depends on the
Berline--Vergne local Euler--Maclaurin theorem and on the human completeness
reductions audited in [REVIEW.md](REVIEW.md); finite agreement is not offered
as a replacement for either.
