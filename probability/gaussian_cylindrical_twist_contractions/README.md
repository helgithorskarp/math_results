# Gaussian majorisation for contractive cylindrical twists

For **every** 1-Lipschitz map on a solid cylinder of the form

```text
T(u,z)=(a Q_theta(z) u,h(z)),        |u|<=R, 0<a<1,
```

with constant transverse scale a and Lipschitz theta,h, the
[author proof](PROOF.md) constructs a continuous contracting motion in R4.
The exact endpoint condition is

```text
h'(z)^2 + R^2 theta'(z)^2/(a^(-2)-1) <= 1 almost everywhere.
```

This gives full Gaussian majorisation for every bounded input law at every
variance, and both Kneser--Poulsen volume comparisons for arbitrary finite
center lists and arbitrary individual ball radii. No rotational symmetry
of the law, atom weights, or center list is required. Independent review
and historical priority are pending; the unrestricted R3 question is open.

The reusable mechanism is a reciprocal-square radial schedule coupled to
the square root of the remaining axial speed. It first unfolds the axial
profile in R3, while adding the entire twist, then performs a one-dimensional
fold in one extra coordinate. It permits arbitrary nonlinear profiles,
changes of twist direction, and axial order reversal. Constant radial
scale and extension to the full solid cylinder are essential hypotheses.

This is the sharp-budget handoff to the geometric lane. R6's concurrent
[twisted-meridian theorem](../gaussian_twisted_meridian_contractions/PROOF.md)
allows broader radial/axial dependence with a sufficient phase bound.
Our proof reaches the exact endpoint bound in the stated cylinder class,
including a nonempty range inaccessible to every C1 phase clock in that
specific meridian interpolation. Neither full theorem subsumes the other.
A saturated example has a seven-site
restriction of paired affine rank six; the whole map fails the
scalar-defect criterion and has nonzero displacement helicity. The earlier
24-site obstruction to universal two-body R5 lifting remains valid: this
theorem does not replace endpoint conditions on disconnected rigid groups
by the cylinder hypothesis.

The proof and [source comparison](SOURCES.md) state the exact scope.
No claim about minimum motion dimension or exclusion of all compositions
of earlier positive maps is made.

With CPython 3.11.2 or later and the standard library, run from this directory:

```sh
python3 -B check.py > /tmp/cylinder-check.json
diff -u EXPECTED.json /tmp/cylinder-check.json
python3 -B -O check.py > /tmp/cylinder-check-opt.json
diff -u EXPECTED.json /tmp/cylinder-check-opt.json
sha256sum -c SHA256SUMS
```

The checker uses exact polynomials and fractions. It checks the differential
square completion, the relative-motion budget, the axial leapfrog identity,
finite parameter controls, the seven-site rank and every endpoint pair,
the scalar-axis obstruction, the strict phase-budget separation, and
rejected schedules/hypotheses. No solver,
numerical Gaussian integration, sampled-angle proof, hidden corpus, or
large external certificate is used. The continuum proof is not inferred
from finite sampling, and the checker is not independent peer review.
