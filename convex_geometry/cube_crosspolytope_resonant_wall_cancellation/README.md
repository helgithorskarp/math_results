# Infinite resonant wall cancellations

This directory gives exact families of cube--crosspolytope sections in every
dimension with a candidate chamber wall that disappears completely.

For `q = m + 2` active coordinates and a rational parameter
`0 < t <= 1/2`, put

\[
a=t^m,\qquad x=t^{2m+2},\qquad c_+=\frac{a+x}{1-x}.
\]

With active weights \((1,a,c_+,\ldots,c_+)\) and the specified ray offset,
the candidate wall supplied by the weight `a` collides with the wall supplied
by weight one and all `m` copies of `c_+`.  Their two truncated-power terms
have equal magnitude and opposite sign, so the section is one polynomial
across the candidate.  When `m` is even there is a second branch
\(c_-=(a-x)/(1+x)\).

The proof also classifies every cancellation of this displayed collision
pattern inside the three-weight-level ansatz.  See [PROOF.md](PROOF.md).

## Reproduce

Using CPython 3.11 or later and only its standard library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Expected status: `RESONANT_WALL_CANCELLATION_VERIFIED`.
Canonical `EXPECTED.json` SHA-256:
`d59b4b16424324cffc463b2c05c0b20f68a79b709ecffa7d34f4c8a1231dc6d5`.

The checker verifies 60 exact family instances through twelve active
coordinates.  An independent rational polygon engine reconstructs the
original 27-halfspace body and confirms eight missing-wall examples, plus a
nearby resonant control whose wall remains genuine.

See [SOURCES.md](SOURCES.md) for dependencies, literature, and the trust
boundary.
