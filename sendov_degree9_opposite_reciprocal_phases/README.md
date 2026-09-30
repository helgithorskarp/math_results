# Opposite critical-reciprocal phases in degree nine

Actual author **six-sendov-1**, role **researcher**, 2026-09-30.

For a disk-root degree-nine polynomial with a critical multiset of two
points each of multiplicity four, rotate a marked zero to \(a=|a|\).
If \(U=(a-\zeta_+)^{-1}\) and \(V=(a-\zeta_-)^{-1}\) have positive real
product, the first-power reciprocal sum is at least eight, strictly
at an interior marked zero. Unequal reciprocal radii are permitted.
Boundary equality within this class is precisely the regular family.

[PROOF.md](PROOF.md) proves a global abstract origin minimum
\(B(a)^2\), \(B(a)=\sum_{j=0}^8(1-a)^j\), with a uniform imbalance
penalty. Its new finite ingredient is
\((1-Q)E_Q+8E>7\) on \(0\le b\le c\le1,0\le Q\le1/4\).
Two exact Bernstein cells and a separate dual-integral/interpolation
algorithm agree on every one of the 2448 coefficients.

[LITERATURE.md](LITERATURE.md) positions the claim against the classical
identities, the current quadratic result, earlier collinear and
balanced/collar results, and complementary original-root stability.
Ordinary Sendov is reported resolved; the unrestricted first-power
Tang--Zhang endpoint remains outside this theorem. Independent review
of this new result is pending. No formalization is claimed.

From the repository root, Python3.11+ standard library only:

~~~bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_opposite_reciprocal_phases/verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O sendov_degree9_opposite_reciprocal_phases/verify.py
~~~

The required [expected.json](expected.json) pins the full compact
manifest. The checker regenerates 214 norm monomials,204 derivative
monomials,2448 compared tensor coefficients,1224 direct dual grid values,
434 interpolation inverse identities,23 weak-mean coefficients,
20 Gaussian-rational controls and the balanced reference identity.
Eight corrupted manifest variants are rejected; optimized Python retains
all checks. Missing or altered expected data fails explicitly.

The coefficient ring is characteristic-zero \(\mathbb Q[b,c,Q]\).
There are no third-party packages, floating proof inputs, root-label
assumptions, solvers, large certificates or parent-source imports.
The compact evidence pins hashes; every coefficient is recomputed from
the documented integral, not imported from an opaque corpus.

The full analytic deduction and geometric equality argument are ordinary
written proofs; the code checks their finite algebraic ingredients.
The two algorithms are author validation, not independent peer review.
Python3.11.2 is the measured interpreter. Runtime and memory are recorded
in the research checkpoint after verification.
