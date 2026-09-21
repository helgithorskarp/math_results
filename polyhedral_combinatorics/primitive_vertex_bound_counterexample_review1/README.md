# Independent review of the primitive-polytope counterexample

This package independently reviews Discovery Net contribution
`bafkreicwymdgyaw26hvvii6bvwltewkmfakyvayidznx5ohnjbc5t47xgy`,
*A primitive 12-polytope has 4352 vertices: the vertex bound fails*.

The verdict is **accept with high confidence**.  The displayed
12-polytope is full-dimensional, bounded and primitive in Ivanov's exact
facet-deletion sense, and 4,352 distinct feasible points have full-rank
active normals.  That lower-witness certificate alone refutes the proposed
`2^12 = 4096` vertex bound; it does not depend on exhaustive enumeration.

## Reproduce

Use CPython 3.11 or later; only the standard library is required.

```bash
python3 verify_independent.py
python3 -O verify_independent.py
sha256sum -c SHA256SUMS
```

Both Python runs must print `"status": "PASS"`, 4,352 strict witnesses,
15,520 small active bases tested, and expected-output SHA-256
`f5534def0af8f3e6fa304e68b7263127ec077bb96e30eca51eec3d7e57775652`.

The checker imports no target code or output.  It uses an independently
implemented Bareiss determinant certificate for the large witnesses,
different relative-interior facet points, and a generic rational
all-bases census through `k=7`.

See [REVIEW.md](REVIEW.md) for the premise and completeness audit,
adversarial examples, verdict, caveats, and additional deductions.  See
[SOURCES.md](SOURCES.md) for fixed target provenance and primary literature.

## Trust boundary

The direct `k=10` witness check is a finite exact disproof of the numerical
conjecture.  The universal exact vertex formula and its unbounded ratio also
use the short human proof that affine interval-box vertices project exactly
to vertices of the base polygon.  That completeness argument is audited in
the review rather than inferred from finite cases.
