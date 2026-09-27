# Gaussian and ball comparisons for contractions affine on parallel slices

Every 1-Lipschitz map

\[
 T(u,z)=(A(z)u+b(z),h(z))\quad\text{on }K\times I\subset\mathbb R^2\times\mathbb R
\]

admits a simultaneous continuous contracting motion in R5, provided K is
closed and convex with nonempty interior, I is an interval, and A,b,h are
Lipschitz. The endpoint assumption is on the whole prism. Matrices may
change singular values and rank, need not commute, and may reverse
orientation; slice centers may move and the height profile may fold.

This gives full Gaussian-convolution majorisation for **every bounded
probability law, every positive variance, and every threshold**, plus both
Kneser--Poulsen volume inequalities for arbitrary finite selected centers
and independent ball radii. It materially extends the constant-conformal
[cylindrical class](../gaussian_cylindrical_twist_contractions/PROOF.md),
whose stronger ambient R4 bound remains separate.

The key geometric estimate is

\[
 |A(z)u+b(z)-A(w)v-b(w)|^2-|u-v|^2
 \leq\left(\int_w^z\sqrt{1-h'(s)^2}\,ds\right)^2\qquad(z\geq w).
\]

It follows by completing the varying affine slices to horizontal affine
isometries in R4. Combining it with the cylindrical result's unfolded axial
speed gives an explicit R5 contraction. [PROOF.md](PROOF.md) includes a
local matrix criterion, all singular limits, analytic time regularity,
classical Gaussian and ball transfers, and a nonconformal prism example.

**Status:** complete author proof; independent correctness review and
historical priority pending. The unrestricted R3 question is still open.
The theorem does not cover a nonlinear transverse map, a target height
depending on u, or endpoint contractions specified only on a finite set.
The normal-bundle, axial, matrix-path and meridian packages remain intact.
The dependency and priority boundary is in [SOURCES.md](SOURCES.md).

Reproduce the compact exact evidence with Python 3.11 or later (standard
library only):

```sh
python3 probability/gaussian_affine_slice_contractions/verify.py
python3 probability/gaussian_affine_slice_contractions/verify.py --check
cd probability/gaussian_affine_slice_contractions
sha256sum -c SHA256SUMS
```

[EXPECTED.json](EXPECTED.json) records universal 2x2 polynomial identities,
rational moving-frame controls, the exact prism contraction bound, finite
pair/time controls, and rejection of incorrect completion formulas. The
checker corroborates specific algebra; the continuum theorem depends on
the written proof and the stated external results. It uses no floating
point arithmetic, external data, solver, numerical ODE, or Gaussian
quadrature. No large certificate is required.
