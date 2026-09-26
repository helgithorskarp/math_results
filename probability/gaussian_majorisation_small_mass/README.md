# Gaussian majorisation near a dominant atom

**Author proof; independent review pending. The full three-dimensional
conjecture remains open.**

Fix a compact probability law `nu` in `B(0,L)`, a contraction `T` fixing the
origin, and Gaussian variance `s>0`. Set

```
mu_e = (1-e) delta_0 + e nu,
f_e  = mu_e * phi_s,
g_e  = T_#mu_e * phi_s,
C    = (2 pi s)^(-3/2).
```

The [proof](PROOF.md) shows that, for this fixed data and all sufficiently
small positive `e`,

```
integral (g_e-a)_+ >= integral (f_e-a)_+
whenever a >= C exp[-s/(32 L^2) (log(1/e))^2].
```

If the map is nonrigid on the support, the gap is strict throughout this
window below `max g_e`. Orthogonal images give equality. The case `L=0`
is trivial. Any dominant atom can be translated to the origin separately
from its image.

Thus a hypothetical failure with `e -> 0`, for **fixed** `nu,T,s`, must have
`a/(C e^m) -> 0` for every fixed positive `m`. This excludes fixed thresholds,
thresholds approaching the density maximum, and all polynomial scales in `e`.
The remaining extremely small thresholds are not controlled. The proof does
not supply an effective numerical value of the allowable `e` for an arbitrary
input, a uniform bound over configurations, full majorisation, or a new
Kneser--Poulsen consequence. The constant `1/32` is not claimed optimal.

The mechanism retains pairwise contraction geometry. Radial norm loss gives
a positive first hinge variation. If all norms are preserved, the second
variation is a positive pairwise sum involving `sinh(z)/z`; equality forces
an orthogonal map. The maximum shifts favorably at the same order, allowing
a uniform local level-set comparison. Radial derivative estimates then
extend the comparison to radii proportional to `log(1/e)`. A separate
reflection argument gives nonnegative first variations for arbitrary fixed
anchor laws, without claiming the same uniform theorem for those laws.

This applies to a dominant origin atom added to the classical simplex-flap
contraction, which retains its prior obstruction to a continuous contraction
in five dimensions. That construction and obstruction are not new.

## Reproduce the supplementary checks

Python 3.11 or later; standard library only. Tested using CPython 3.11.2 and
3.12.14. From this directory run:

```bash
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both executions reproduce [EXPECTED.json](EXPECTED.json), with final status
`SMALL_MASS_GEOMETRY_CHECKS_PASS`. Expected-output SHA256:

```
facac2aa8e4d994f06c5d2c22eb555016909ce0562b6d06b9de1b11c917e4459
```

The exact checks include:

- A rational six-point unit-sphere contraction with the dominant origin
  adjoined, paired affine rank six, and all 15 rare pairs strictly contracted.
  [fixture.json](fixture.json) records the points and two weight choices.
- 504 spherical-moment identities checked by coordinate-monomial integration
  and by polar integration. This audits the spherical kernel normalization.
- Weighted Gram identities, twelve positive power-series coefficients per
  weight choice, and the agreement of the quadratic hinge and moving-mode
  coefficients. An orthogonal map provides an equality control.
- Twelve outward rational enclosures of normalized quadratic variations, and
  the agreement of direct Gaussian overlaps with integrated spherical series
  for the quadratic energy. Internal enclosure widths are below `10^-45`;
  displayed endpoints are rounded outward to 24 decimal places.
- The augmented 17-point simplex-flap contraction: 136 pair constraints,
  54 strict, twelve strict radial losses, and paired rank six. The positive
  first-order maximum coefficient is enclosed as well.

Canonical variation-record SHA256:

```
2418fe879499c10ae641216e76798dd75be1aa69661c112a55121d1d110f3f74
```

The exponential and spherical-kernel enclosures use positive rational Taylor
series with geometric tail bounds. No floating-point sign, random sample,
numerical eigenvalue, external dataset, or solver is trusted. All checks finish
in under a second on the author's environment; no large artifacts are needed.

These computations are finite normalization and implementation audits. The
universal theorem, the uniform moving-mode comparison, and the growing-radius
window are established by the written proof. Repeating this code is not an
independent mathematical review or a proof-assistant verification.

## Source and team context

The sole problem source is [Aishwarya–Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
The source still has version 2 dated 13 September 2026 at our refresh. The
proof derives the needed variations directly and makes no priority claim.
It builds on the research direction isolated by the team's paired-rank,
half-order, Hankel, and energy-class results; [PROOF.md](PROOF.md) gives direct
links and distinguishes that context from mathematical dependencies.
