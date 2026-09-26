# Order-three control and a sparse Hankel hierarchy

For every bounded probability law in `R^3` supported in a radius-`R` ball
and every 1-Lipschitz map, the analytic author proof establishes positivity
of **every principal 3 by 3 Gaussian moment-gap Hankel block** at variance
`s>=72R^2`. The exponent indices may be arbitrarily large and unevenly spaced.

More generally, every principal `N by N` block is positive semidefinite
at `s>=24 N R^2`, for integers `N>=3`, and positive definite if the expected
squared pair-distance loss is positive. Equivalently, every convex energy
whose curvature is the square of a polynomial with at most `N` monomials
compares in that range. The bound is independent of polynomial degree.

This replaces exponentially growing finite-level variance bounds by a
linear bound in matrix size. The new bridge combines the preceding
signed hinge window with a global bound proportional to the contraction
deficit and a one-sided sparse interpolation estimate. It controls the
entire remaining low-density tail in each of these polynomial tests.

The full majorisation conjecture remains open: the noise bound still grows
with matrix size. No new Kneser--Poulsen case or optimal constant is claimed.
The complete [author proof](PROOF.md) awaits independent review and is not
formalized. [SOURCES.md](SOURCES.md) distinguishes imported identities from
the new estimates and records the team's complementary results.

## Reproduce finite exact audits

From the repository root, with CPython 3.11.2 and the standard library:

```sh
python3 probability/gaussian_sparse_hankel_hierarchy/verify.py > probability/gaussian_sparse_hankel_hierarchy/actual.json
cmp probability/gaussian_sparse_hankel_hierarchy/EXPECTED.json probability/gaussian_sparse_hankel_hierarchy/actual.json
python3 -O probability/gaussian_sparse_hankel_hierarchy/verify.py > probability/gaussian_sparse_hankel_hierarchy/actual-optimized.json
cmp probability/gaussian_sparse_hankel_hierarchy/EXPECTED.json probability/gaussian_sparse_hankel_hierarchy/actual-optimized.json
```

Run `sha256sum -c SHA256SUMS` in this directory for the package manifest.
Generated `actual*.json` and Python caches are ignored.

The checker verifies 54 exact interpolation identities, including 18
nearly coalescing node sets; the coefficient and extrapolation bounds;
the rational tail-margin certificate; and seven actual Gaussian Hankel
blocks. The latter use two equal atoms at `+/-e1` and homotheties, including
`lambda=99/100`, at the variance bound. Three-index controls include
`[0,1,2]`, `[0,5,24]`, and `[100,101,102]`; a four-index control checks the
next matrix size. An exact abstract negative matrix tests the determinant
checker's ability to reject failure, without suggesting a Gaussian counterexample.

All decisions use `Fraction`, outward rational intervals, and bounded
Taylor series. The reused interval primitive is pinned by SHA256.
The binomial replica formula supplies the finite moment integrals exactly;
no spatial quadrature, floating-point eigenvalue, or search dataset enters.
Normal and optimized Python outputs agree. These finite audits corroborate
identities and normalizations; the uniform theorem depends on the written
analytic proof, not on sampling or source publication.
