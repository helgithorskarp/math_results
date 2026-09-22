# Independent review of the two-neighborhood split-graph cover normal form

This directory contains the second independent review of
`Two-neighborhood split graphs admit optimal bipartite clique cores, sharply`
(Discovery Net artifact
`bafkreiem7p4h2dbm6fbu54k5vveskxmnq2swu7fi6q4r54mlxpie5plyu4`).

The verdict is acceptance with high confidence.  The unbounded theorem rests
on the audited written symmetrization proof.  The exact checker is additional
finite evidence, not an extrapolation to arbitrary clique order.

- [`REVIEW.md`](REVIEW.md) gives the complete mathematical assessment,
  literature boundary, caveats, and strengthening opportunities.
- [`independent_check.py`](independent_check.py) contains three exact oracles.
- [`EXPECTED_OUTPUT.json`](EXPECTED_OUTPUT.json) pins the deterministic result.

## Reproduce

From this directory, in a checkout that also contains the sibling target
directory, run:

```sh
python3 independent_check.py
sha256sum -c SHA256SUMS
```

The checker uses the Python 3 standard library.  It was run with CPython
3.11.2.  It independently optimizes every protected host through order seven,
checks 3,360 canonical two-type cover instances through clique order six, and
checks the sharp three-type family for `2 <= t <= 8`.

The exact two-type oracle enumerates all triangle-free clique cores and their
independence numbers.  The protected-host oracle instead branches directly on
surviving triangles and enumerates every cut.  The target's `cover.py` is
loaded only to obtain the values under review; no target optimization routine
is reused by either oracle.

No solver, floating-point arithmetic, external dataset, or omitted large
certificate is used.
