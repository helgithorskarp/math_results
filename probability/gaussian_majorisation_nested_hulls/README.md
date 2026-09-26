# Full Gaussian majorisation near a dominant atom under nested hulls

Fix a compact rare law $\nu$ in $\mathbb R^3$ and a contraction $T$ fixing
the origin. If the image support lies in the convex hull of the original
support together with the origin, and its largest distance from the origin
strictly decreases, then

$$
((1-\varepsilon)\delta_0+\varepsilon\nu)*\phi_s
\quad\text{is majorised by}\quad
((1-\varepsilon)\delta_0+\varepsilon T_\#\nu)*\phi_s
$$

for every sufficiently small positive $\varepsilon$, at each **fixed**
variance $s>0$. All hinge thresholds are covered, with strict comparison
below the target maximum. The permitted mass depends on $\nu,T,s$.

This is an author proof awaiting independent review. The unrestricted
dimension-three conjecture remains open. No effective all-threshold mass
bound or new Kneser--Poulsen consequence is claimed.

The [complete proof](PROOF.md) provides a weaker geometric criterion and
the mechanism behind it. At variance one, writing
$C=(2\pi)^{-3/2}$, $R=\sqrt{2\log(C/a)}$ and
$c=\log(1/\varepsilon)/R$, it proves the uniform asymptotic

$$
\frac{H_g(a)-H_f(a)}{aR^2}
=\int_{S^2}[(h_P(\theta)-c)_+-(h_Q(\theta)-c)_+]\,d\sigma(\theta)+o(1).
$$

A shell estimate handles the transition where this leading term may vanish.
The nested-hull and strict-radius conditions then close the entire tail,
extending our [earlier threshold window](../gaussian_majorisation_small_mass/PROOF.md).
The proof here is self-contained. A negative truncated-support coefficient
for any actual contraction would produce Gaussian counterexamples; none
is supplied.

The theorem applies to the classical tetrahedron-flap contraction, with a
dominant origin, **every depth $0<b\le2$ and arbitrary positive rare weights**.
The resulting seventeen-label examples retain the known obstruction to a
continuous contracting motion in dimension five. Their construction and
nonliftability are due to
[Cheng--Tan--Zheng](https://arxiv.org/abs/1107.0140), not this work.

## Reproduce the supplementary exact certificate

From this directory, with CPython 3.11 or later and no external packages:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

The checker fails with a nonzero exit status on any mismatch and compares
its result with [EXPECTED.json](EXPECTED.json). The normal and optimized
outputs are identical. It uses integers and `fractions.Fraction` throughout.
Validated interpreters: CPython 3.11.2 and 3.12.14, in both modes.

The certificate checks:

- All 136 pair inequalities as polynomials in depth, including 54 strict
  inequalities for every positive depth.
- A paired-rank determinant $128b^3$, by direct expansion and a separate
  block factorisation.
- Radius and support-gap identities covering the full depth intervals,
  and a separate barycentric hull certificate for all seventeen images at
  depth one.
- A continuous far-tail region for uniform depth-one rare weights:
  $0<\varepsilon\le1/2$, $R\ge65536$, and $c\le5/2$, where
  $(H_g-H_f)/(4\pi aR^2)>17/24576$.
- Depth-zero equality and a depth-three failure of the nesting hypothesis.

The last positive bound combines the written finite-mixture tail estimate
with an exact spherical-cap calculation. Its large radius is a convenient
sufficient constant, not an optimisation claim. It does not specify the
mass bound needed at all other thresholds.

Expected-output SHA256:
`524b8edc202d0362bf3cd9d95b6fc0c58d070127cd3d63c8c62e241374e6b416`.

Canonical pair and barycentric record SHA256:
`3abcfeb478e55e2a435b70649d73116f1cf45ceec0a3327b8c517a4e16d49817`.

The universal theorem relies on the written analysis, including compact
support, uniform radial boundaries and the outside-tail bound. The code
checks its algebraic application and constants; it is not a formal proof
of those analytic steps. No floating-point sign, quadrature, external data
or solver is trusted. No large generated artifacts are needed.

## Source and team context

The named problem is [Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/abs/2609.07041v2).
Ordinary large-radius mean-width results, such as
[Gorbovickis, arXiv:1006.0531](https://arxiv.org/abs/1006.0531), are background;
they do not directly give the truncated comparison used here.

The team's [symmetric-flap quartic theorem](../gaussian_symmetric_flap_quartics/PROOF.md)
and [degree-independent sparse-energy theorem](../gaussian_replica_curvature_sparse_energies/PROOF.md)
control different classes of energies and parameter ranges. This packet
controls every hinge under its additional geometric and small-mass
hypotheses. It does not assume the instantaneous positivity refuted by the
[local-lift obstruction](../gaussian_majorisation_local_lift_obstruction/PROOF.md).
