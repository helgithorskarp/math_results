# Full Gaussian majorisation along convex normal rays

The [convex-core theorem](CONVEX_CORES.md) extends the radial result below to
**every nonempty closed convex set C**. Write x=p+ru with p=P_C(x), r=dist(x,C)
and u its outward unit normal. Every common nonnegative 1-Lipschitz profile
rho fixing zero gives

    T(x)=p+rho(r)u,          T(x)=x on C.

This map satisfies full Gaussian majorisation for every bounded law at every
variance, and both ball-volume inequalities for arbitrary individual radii,
in every dimension n>=2. The core can be unbounded, lower dimensional, or
nonsmooth. Distance order along the normal rays may reverse repeatedly.

A geometric consequence reflects the **entire outer collar** of K=C+aB
inward by 2P_K-I, on C+2aB. This includes rounded polytopes with any number
of faces and arbitrary convex cores. Ball radii have no relation to a.
The proof constructs one analytic contracting motion in dimension n+1.

An [independent review](../gaussian_convex_core_review_frontier/REVIEW.md)
accepts the convex-core extension for correctness in the stated scope.
Historical priority remains uncertain. Its classical lift and transfers retain
the attribution below. Full unrestricted R^3 majorisation remains open.
The reviewed proof and checker are preserved at their original source bytes;
the proof's opening status line records its pre-review publication state.

Reproduce its new exact algebra and coordinate checks:

```bash
python3 probability/gaussian_radial_contractions/check_convex_core.py
python3 -O probability/gaussian_radial_contractions/check_convex_core.py
```

Both yield [convex_core_expected.json](convex_core_expected.json), with two
polynomial identities, 66,425 exact lift-coordinate checks over five convex
cores, 120 collar checks, and four deliberate rejections. These are finite
author controls; the arbitrary-core theorem is the written proof.

## Preserved point-core theorem

For **every** nonnegative 1-Lipschitz function rho fixing zero, the map

    T(r u)=rho(r)u,   |u|=1,

preserves full Gaussian majorisation for arbitrary bounded probability laws
in R^3, at every variance and threshold. It also decreases the volume of
unions of balls and increases the volume of intersections, for any number
of centers and arbitrary individual radii. The result holds in every
dimension n>=2.

The profile may reverse radius order any number of times. Examples include
the map fixing the unit ball and inverting its exterior, and profiles with
arbitrarily many radial folds. The input law need not be radially symmetric.

[PROOF.md](PROOF.md) gives a simultaneous contracting motion in dimension
n+1 and the exact distance identity proving its sign. The motion specializes
the **classical Bezdek--Connelly norm-displacement lift**. Its theorem is the
singleton-core case of the independently accepted extension above. That review
does not audit the additional benchmark comparisons below or establish
historical priority. The Gaussian and Kneser--Poulsen transfer theorems are established
inputs, not new results of this note. Full unrestricted R^3 majorisation
remains open.

A ten-site rational restriction has paired rank six, displacement rank three,
and fails the scalar-defect criterion for all unit-vector choices. The full
inversion-fold map is not strong in any separate orthonormal coordinates.
These comparisons concern specified criteria; no exclusion of arbitrary
compositions or indirect applications of known results is claimed.

[SOURCES.md](SOURCES.md) records classical priority and the boundary with the
team's cap, flap, axial, paired-rank and scalar-defect results.

Reproduce the exact checks from the repository root:

```bash
python3 probability/gaussian_radial_contractions/check.py
python3 -O probability/gaussian_radial_contractions/check.py
```

Tested with CPython 3.11.2; Python >=3.10 and the standard library suffice.
Both commands produce [expected.json](expected.json): two exact polynomial
identities, all 45 benchmark pairs, ranks 6 and 3, 36,125 rational derivative
checks, and four intentional rejections. No random input, solver, floating
quadrature, external dataset, or omitted large certificate is required.
The checker validates algebra and the example; the universal theorem and
external transfer steps remain the written analytic proof.
