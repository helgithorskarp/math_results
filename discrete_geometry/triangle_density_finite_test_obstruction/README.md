# No finite triangle test suite certifies rational-distance density preservation

For **every finite family of noncollinear real triangles**, there is an
irrational homothety arbitrarily close to the identity that preserves all
their rational-distance and rational-squared-distance density statuses,
including negative instances, but fails to preserve density for some other
triangle.

Thus the map-dependent third test in the previously established affine
preserver theorem cannot be replaced by any finite fixed suite. An explicit
countably infinite fixed suite does suffice. The least cardinality is
therefore countably infinite. The underlying preserver group is unchanged.

The mechanism is simultaneous rational congruence of finitely many binary
Gram forms. A norm from the compositum of their imaginary quadratic fields
supplies a common multiplier. A fully explicit polynomial-part bound makes
that multiplier a nonsquare; rational rescaling brings the excluded map
as close to identity as desired.

Read [PROOF.md](PROOF.md) and [SOURCES.md](SOURCES.md). The construction is
an exact geometric testing obstruction, not a solution of the dense pairwise
rational-distance set problem. Classical arithmetic ingredients and the
published triangle-density criteria are explicitly credited.

Reproduce from this directory with CPython 3.11+, standard library only:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both Python commands compare against `expected.json` and print `status: pass`.
`python3 verify.py --emit` regenerates the summary. No solver, floating point,
network, external data or unpublished certificate is required.

`construct.py` takes rational positive-definite Gram matrices and returns
explicit norm and matrix certificates. It does not decide density or
rationality for arbitrary unspecified real coordinates. Runtime grows
exponentially with square-class rank; this is a reproducible construction,
not a complexity bound. The finite audit corroborates the universal proof;
it is not independent peer review or formal verification.
