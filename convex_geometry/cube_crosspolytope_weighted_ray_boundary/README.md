# Weighted ray-boundary classification

This directory classifies the first ray chamber of every affine hyperplane
section of the cube--crosspolytope Minkowski family, for an arbitrary nonzero
normal vector.

Let

\[
A_v(b,R)=\int_{\mathbb R^N}\delta(v\mathbin\cdot x-b)
 \mathbf1_{\{\sum_i(|x_i|-1)_+\leq R\}}\,dx.
\]

Put \(M=\|v\|_\infty\), \(h=\|v\|_1\),
\(B=(|b|-h)/M>0\), and \(s=R-B\).  Normalize the \(q\) nonzero absolute
coordinates by \(w_i=|v_i|/M\), let \(k\) be the multiplicity of \(w_i=1\),
and let \(z=N-q\).

The [proof](PROOF.md) gives an explicit rational polynomial for
\(A_v(b,B+s)\) throughout the exact first chamber.  Its coefficients are the
first \(k\) Taylor coefficients of

\[
C_w(t)=\frac{1}{(1-t)^q\prod_iw_i
 \prod_{w_i<1}(1-w_i+w_it)}.
\]

The section vanishes to exactly order \(q-k\) at its first appearance.
Consequently the support-plane section has positive \((N-1)\)-volume if and
only if all nonzero entries of the normal have the same absolute value.  For
full-support normals this singles out the signed diagonals, where the formula
reduces exactly to the Legendre law.  Sparse equal-magnitude normals give an
explicit iterated-integral lift of that law.

## Reproduce

Using CPython 3.11 or later and only its standard library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Expected status: `WEIGHTED_RAY_BOUNDARY_CLASSIFICATION_VERIFIED`.
Expected standard-output SHA-256:

~~~text
9f745c6ba1bfd1e2139b382b94cdafad1c7a5d8275ff7dee2917faabba990f13
~~~

The checker compares the generating-function formula with a separate
coordinate-state enumeration in dimensions through eight.  It also
reconstructs the original three-dimensional sections as exact rational
polygons from all 27 defining halfspaces, tests signed and sparse normals,
checks both activation thresholds and negative controls beyond them, and
recovers the Legendre kernel by an independent recurrence.

See [SOURCES.md](SOURCES.md) for the dependency and novelty boundary.
