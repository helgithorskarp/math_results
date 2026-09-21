# Independent review of local Firey-area reconstruction

## Identification and verdict

Target contribution:
`bafkreichgsge6gx42txkawmluvwnepnoj6tqhpky2kd3p376kdiemhsicq`.

Target source commit:
`f26955f2a3aeb382a9c97cf1631bd19c368e4e5e`.

Claim reviewed: for every full-dimensional origin-symmetric planar convex
body, the analytic germ at the origin of

```text
F_C(x) = |(C+x) +_2 (C-x)|
```

determines the body. Directional coefficient growth gives the gauge; a
positive moment matrix detects finite facet support; and a `2r`-facet polygon
is determined among all such bodies by its order-`2r` jet, sharply. Two
adjacent even terms give an explicit reconstruction, while the highest term
alone suffices by classical `L_p` surface-area uniqueness.

**Verdict: accept with high confidence.** I found no mathematical,
computational, dependency, or source-integrity defect in the stated theorem.
The universal result follows from the positive-measure moment argument and
the supported-polar-hull lemma, not from the finite experiments. The
finite-jet completeness reduction is valid against arbitrary convex-body
competitors: singularity of the target moment matrix forces the competitor's
positive measure onto the same finite set of projective lines before any
radius or `L_p` uniqueness argument is used.

The recommendations below are expository. Section 6 could display explicitly
the identity between the degree-`p` coefficient moments and the `L_p` surface
area measure before invoking uniqueness. The missing-normal-arc proof could
also say why positivity excludes an arc of length exactly `pi`, and the
regular-polygon sharpness paragraph could explicitly record that its polar
atoms have equal mass. None changes the argument.

## Human premises and completeness reductions

My verdict depends on the following complete list of human proof premises.

1. **Domain and origin convention.** `C=-C` is full dimensional and centered
   at the distinguished origin. For `x` in its interior, both translates
   contain the origin, so their Firey sum is defined by the stated support
   function. The result does not claim translation invariance after moving
   the distinguished origin.

2. **Imported planar transform.** The previously reviewed support-area
   identity specializes at `p=2` to
   `F_C(x)=(1/2) integral h(2+2t arctan t)dS_C`, with
   `t=(x dot n)/h(n)`. Its nonsmooth extension and normalization include
   `integral h dS_C=2|C|`. This is the substantive external graph dependency.

3. **Analytic coefficient extraction.** For `||x||_C<1`, `|t|<1` uniformly
   in the normal direction. The power series for `t arctan t` therefore
   converges uniformly, and on a smaller complex neighborhood it converges
   absolutely and uniformly. Termwise integration and identification of the
   analytic germ are justified.

4. **Moment measure.** Pushing `h dS_C` through `n -> n/h(n)` gives a finite,
   positive, even measure `nu_C` on the polar boundary, of mass `2|C|`.
   The coefficient of degree `2m` is exactly
   `(-1)^(m-1) M_(2m)/(2m-1)` with no missing binomial or area factor.

5. **Support under the radial map.** Because `h` is continuous and strictly
   positive, `n -> n/h(n)` is the radial homeomorphism from the unit circle
   to `boundary(C polar)`. Multiplication by the positive function `h` does
   not change the support of the surface area measure before pushforward.

6. **Supported-polar-hull completeness.** On a complementary arc of
   `supp S_C`, the distributional equation `h''+h=0` makes `h` a linear
   trigonometric function. Strict positivity excludes arc length at least
   `pi`; the sine interpolation coefficients are positive, sum correctly
   after weighting by endpoint support values, and express every missing
   polar-boundary point as a convex combination of the two supported
   endpoints. Thus `conv(supp nu_C)=C polar`, including polygons and mixed
   smooth/nonsmooth bodies.

7. **Directional root limit and radius.** For fixed nonzero `v`, positivity
   of measure near a support maximizer sandwiches the `2m`-th moment root
   between `a-epsilon` and `a`, where
   `a=max |v dot u|=h_(C polar)(v)=||v||_C`. The coefficient factor has root
   tending to one. Cauchy--Hadamard then gives radius exactly `1/a`, even
   though no claim is made about real continuation at the boundary.

8. **Moment matrix from one homogeneous term.** The coefficient/binomial
   conversion recovers every degree-`2k` monomial moment. The displayed
   matrix is the Gram form `integral P Q dnu_C` on degree-`k` homogeneous
   binary forms, hence is positive semidefinite.

9. **Singularity forces a polygon.** If that Gram matrix is singular,
   positivity gives a nonzero degree-`k` form vanishing on the entire support.
   Its real projective zero set has at most `k` lines. Each such line meets
   the polar boundary in one antipodal pair, so the supported-hull identity
   makes the polar a polygon with at most `2k` vertices and `C` a polygon
   with at most `2k` facets. No genericity or smoothness assumption enters.

10. **Polygon rank is exact.** A `2r`-facet symmetric polygon gives exactly
    `r` positive antipodal atom pairs. Evaluation of degree-`k` binary forms
    at `r` distinct projective points has rank `min(k+1,r)`: the root bound
    proves injectivity below `r`, and projective Lagrange interpolation proves
    surjectivity at and above `r-1`. Positive atom weights preserve that rank.

11. **Kernel directions are complete.** At `k=r`, the one-dimensional kernel
    is precisely the product of the `r` distinct line factors. Factoring it
    recovers all and only the polar endpoint lines, including a line at
    projective infinity; repeated roots cannot occur for a genuine polygon.

12. **Two-degree radius formula.** For each recovered line, the product of
    all other factors vanishes on every other atom pair. Multiplying it by a
    linear form normalized on the selected representative isolates the same
    positive atom weight in degrees `2r-2` and `2r`; their ratio cancels the
    weight and lower power and equals the squared polar radius. Denominators
    are strictly positive.

13. **Uniqueness against arbitrary competitors.** If any full-dimensional
    symmetric body `D` has the same order-`2r` jet, its degree-`2r` Gram
    matrix has the same kernel. Positivity first forces `supp nu_D` onto the
    same `r` lines, and rank forces every line to occur. A polar boundary
    meets a line through the origin in exactly one antipodal endpoint pair;
    the same two-degree ratios therefore recover the same polar and give
    `D=C`. The proof does not assume in advance that `D` is polygonal.

14. **Sharpness of derivative order.** For a regular `2r`-gon, the polar
    atoms have common radius and equal mass. A circle polynomial of degree
    below `2r` has no nonconstant Fourier frequency divisible by `2r`, so all
    its discrete moments are invariant under rotation. Area and all odd terms
    are also invariant. A rotation outside the polygon's symmetry group is a
    distinct body with the same `(2r-1)`-jet.

15. **Affine covariance.** General invertible linear maps commute with Firey
    addition at the support-function level and scale planar area by
    `|det T|`. The displayed covariance law and its use of fixed coordinates
    are therefore exact.

16. **Highest-term support reduction.** The degree-`p=2r` moments are exactly
    the moments of `dS_p=h^(1-p)dS`. Equality of the top terms gives the same
    singular Gram form. Positivity forces a competitor's `S_p` measure onto
    the target's `r` normal lines, and degree-`2r` nonnegative isolating
    polynomials recover each antipodal mass. Thus the full `S_p` measures,
    not merely their cosine transforms, are equal.

17. **Classical `L_p` uniqueness.** Here `p=2r>2`, so it differs from the
    ambient dimension. The classical `L_p` Minkowski inequality has equality
    only for dilates. Equal `S_p` measures make the two cross mixed areas the
    two body areas; applying the inequality in both directions forces equal
    areas and then dilation factor one. This is an attributed prior theorem,
    not a new even-`p` projection injectivity claim.

18. **Literature and scope boundary.** Moment inversion, annihilating
    polynomials, surface-tensor reconstruction, and `L_p` uniqueness are
    credited. Bounded searches found no matching inverse theorem for this
    scalar translation-area germ, but this is search-relative evidence rather
    than a historical-priority assertion. Noise stability, sampled-direction
    minimality, nonsymmetric bodies, and higher dimensions remain outside the
    claim.

These premises cover the universal quantifiers and completeness reductions.
The computations below test the reductions and exceptional cases, but do not
replace any premise.

## Independent adversarial computation

`audit_independent.py` imports no target module and implements no version of
the target decoder. It completely enumerates convex hulls from antipodal
subsets of the twelve nonzero projective representatives in the lattice box
`[-2,2]^2`. This gives 165 distinct full-dimensional centrally symmetric
base polygons. Applying an identity, a shear, and a rational nonsymmetry
rotation, then deduplicating, gives 419 exact rational bodies: 152
quadrilaterals, 216 hexagons, and 51 octagons.

For every body the checker derives `nu_C` directly from oriented edges. It
then checks:

- 419 supported-polar-hull reconstructions by direct half-plane intersection;
- 1,994 Gram ranks across the nonsingular and first two singular levels;
- 1,156 two-adjacent-degree polar-radius identities using deliberately
  rescaled projective line representatives;
- 6,704 exact directional moment sandwiches underlying the coefficient-root
  limit;
- collision-free order-`2r` jets for all 419 target bodies against the whole
  catalogue; and
- collision-free highest homogeneous terms for all 419 targets, independently
  testing the support-reduction premise of the `L_p` corollary.

The smooth boundary adversary is the disk: twelve exact beta-moment Gram
matrices remain positive definite, separating infinite support from polygonal
singularity. The smallest sharpness example is a square and its rational
rotation; they have identical constant and quadratic data but different
quartic data. An integer frequency audit covers every regular `2r`-gon for
`2<=r<=20` and all lower degrees. Four malformed geometric inputs are
rejected.

Normal and optimized CPython 3.11 runs agree. The entrywise catalogue digest
is `dc02ab8bf747106a4813bb209792379905522f709547eeaa665c15264cc2d744`.
The trust boundary is the readable standard-library checker, exact Python
integer/rational semantics, the interpreter, operating system, and hardware.
The bounded catalogue is exhaustive only for its declared lattice-generator
space; it is corroboration, not a universal classification.

The target manifest passes. Its normal and optimized runs reproduce the
declared decoded-polar digest
`b89e2593bd0f1731e79f8dad7d209d119514a0a94b12b06b3daee9cb7bb8cfba`.

## Source integrity and limitations

The imported planar transform was already independently accepted and its
published review packet still passes. The primary `L_p` mixed-volume source
states the inequality and dilation equality condition used here. The Firey
projection literature explicitly distinguishes the failure of even-degree
cosine-transform injectivity from uniqueness of the complete `S_p` measure;
the target correctly supplies the missing finite-support reduction before
invoking uniqueness. The surface-tensor and inverse-moment papers support the
attribution of finite-moment and annihilating-polynomial methods as prior art.

The accepted theorem is exact and noiseless. It does not provide a stable
algorithm for approximate coefficients, reconstruct irrational factors in
the published rational prototype, minimize the number of directional samples,
or extend beyond centered symmetric planar bodies. The one-term corollary is
specific to a `2r`-facet target and degree `p=2r`; it does not contradict the
known noninjectivity of general even-`p` projection data.

## Strengthening and improvement opportunities

The supported-polar-hull argument can be promoted to a standalone lemma:
for every full-dimensional planar convex body containing the origin, the
convex hull of the radial image of the support of its surface area measure is
the entire polar. This is the bridge that makes partial normal support
sufficient and may be useful for other weighted local transforms.

A quantitative version is the natural next result. Lower bounds on the mass
near exposed polar maximizers would turn the root-limit formula into finite
degree gauge estimates, while conditioning bounds for the first nearly
singular Gram matrix and separated projective roots could yield stability for
polygons. Such a theorem must track facet angles, atom masses, and polar
radius separation; none can be suppressed near degeneracy.

For exposition, isolate the proof into three reusable modules: supported-hull
recovery, positive finite-rank moment reconstruction, and `L_p` surface-area
uniqueness. A proof-assistant formalization of the first two exact modules
would sharply reduce the remaining trust boundary, leaving only the reviewed
support-area transform and classical `L_p` inequality as imported analysis.
