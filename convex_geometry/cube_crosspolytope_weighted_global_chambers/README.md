# Global weighted ray-chamber formula

This directory gives an exact finite formula for every ray-side affine
section of the cube--crosspolytope Minkowski family, with an arbitrary nonzero
normal and at every radius.

For normalized positive active weights \(w_i\in(0,1]\), the proof first
replaces each bounded inactive interval by a fictitious unbounded ray.  The
resulting baseline has a rational two-variable Laplace transform.  Its
partial fractions give a finite truncated-power spline.  A coordinate-specific
signed tail operator then replaces each fictitious tail by the physical
opposite tail.  Expanding over coordinate subsets yields the global formula.

The candidate chamber walls are explicitly contained in

\[
s=B(1/w_i-1)+\frac{2}{w_i}\sum_{j\in J}w_j,
\qquad i\notin J.
\]

Consequently every chamber polynomial and every one-sided derivative can be
computed exactly.  When all weights equal one, the partial-fraction baseline
is the Legendre kernel and the subset formula collapses to the previously
proved diagonal expansion
\(\sum_r\binom Nr\mathcal T^rH_{N-r}\).

See [PROOF.md](PROOF.md) for the theorem and derivation.

## Reproduce

Using CPython 3.11 or later and only its standard library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Expected status: `GLOBAL_WEIGHTED_RAY_CHAMBERS_VERIFIED`.
Expected canonical-output SHA-256:
`6eefd55b8a00cfb253eb4dd354d4744e603e0cc5f3b424a3d848fd2e83f84730`.

The checker uses exact rational arithmetic.  It compares the formula with
direct rational polygons reconstructed from the original 27-halfspace body,
checks the complete partial-fraction identity, verifies the first weighted
chamber, and independently recovers the global equal-weight recurrence.

See [SOURCES.md](SOURCES.md) for dependencies and the bounded novelty search.
