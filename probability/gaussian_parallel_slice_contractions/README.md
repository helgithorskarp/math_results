# Gaussian majorisation for arbitrary nonlinear parallel slices

The [author proof](PROOF.md) removes the transverse affinity requirement
from the accepted affine-slice theorem. If

```text
T(u,z) = (f(u,z), h(z)) : K × I -> R² × R
```

is 1-Lipschitz on a whole convex prism, **f may be an arbitrary nonlinear
map**. There is one contracting motion in R⁵ for the whole domain, smooth
on each of three time intervals. Consequently every bounded probability
law on the prism satisfies Gaussian majorisation at **every variance and
threshold**. Every finite selection of centers also satisfies both union
and intersection Kneser--Poulsen inequalities for arbitrary individual
radii. No input-law symmetry, transverse differentiability, affine slices,
or extra contraction margin is required.

This is a complete author argument awaiting independent review. Historical
priority is unresolved, and the unrestricted R³ problem remains open.

The new geometric estimate is

```text
|f(u,z)-f(v,w)|² <= |u-v|² + |A(z)-A(w)|²,
A(z) = integral sqrt(1-h'(q)²) dq.
```

A partition of the height interval allocates the horizontal displacement
in proportion to the available transverse lengths. Refinement proves the
estimate without differentiating f. It also gives the exact factorization
`f(u,z)=G(u,A(z))` with G 1-Lipschitz. Conversely, every such G and h supplies
a map in the class. The R⁵ interpolation and Gaussian/ball transfers use
credited earlier mechanisms; the partition estimate is the new input.

Section 3.1 gives a necessary and sufficient **finite extension test in
prescribed frames**. Target height must be constant on each source-height
level. Adjacent levels determine maximal unused lengths by Pythagoras;
their cumulative sums must satisfy transverse pairwise inequalities.
Kirszbraun extension then supplies the whole-prism map. This test does not
classify all motions or choose favorable coordinate frames.

The nonlinear whole-cube example is not affine on planes, or coordinatewise
strong, in any fixed endpoint frames. It illustrates the larger function
class without claiming exclusion from every earlier composition. General
normal and meridian freedoms remain complementary. The whole-prism
extension hypothesis cannot be replaced by endpoint contraction alone.

## Reproduction

Use CPython 3.11 or later, standard library only. From this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Both Python commands compare their entire record with [EXPECTED.json](EXPECTED.json).
The expected status is `NONLINEAR_PARALLEL_SLICE_EXACT_CONTROLS_PASS`, with
canonical record SHA-256
`6fd418efb87967baee6ee343e234e5ba04dc5a1999175626dd5d836937cc1945`.

The [checker](verify.py) validates 19,278 allocated segments, 6,930 motion
derivative signs, 14,850 axial-fold controls, three finite extension
certificates, zero-budget strata, and 13 deliberately invalid controls.
It uses exact fractions and exact quadratic-surd signs. Its public
`finite_slice_certificate` function accepts rational endpoints and supplied
rational level budgets; it is not a general algebraic-number solver.

Universal dyadic convergence, the nonlinear class theorem, time regularity,
Kirszbraun extension, and the classical transfers are written proofs. The
finite checks are supporting evidence, not an independent review or a
proof by sampling. No numerical quadrature, external dataset, large
certificate, or optional package is required. [INPUTS.json](INPUTS.json)
pins cited source bytes for provenance; the checker needs only this packet
and does not read those older sources. [SOURCES.md](SOURCES.md) separates
antecedents, the present enlargement, and unresolved priority.
