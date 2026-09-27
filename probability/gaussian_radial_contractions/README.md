# Full Gaussian majorisation for radial contractions

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
the **classical Bezdek--Connelly norm-displacement lift**. The broad profile
application is an author result; independent correctness and priority review
are pending. The Gaussian and Kneser--Poulsen transfer theorems are established
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
