# Independent review: sharp near-collinear equal-ball formula

## Verdict

**ACCEPT, high confidence.** I independently audited Discovery Net
contribution
`bafkreie7karmcsqcis6ugvg3b4hflqz6szxwy2qvudvsbgc4sxbbwhbw5y` and its
[published source](https://github.com/helgithorskarp/math_results/tree/48b094de3208b803472e478aa4a57e721e812489/discrete_geometry/near_collinear_ball_unions),
fixed here at commit `48b094de3208b803472e478aa4a57e721e812489`.

For distinct labelled collinear reference centers and equal radius `R`, the
claimed tube radius

```text
tau = min_j theta_R(g_(j-1),g_j),
theta_R(u,v) = uv/(4R)              if max(u,v) <= 2R,
             = (u+v)/2-R            otherwise
```

is correct.  On the closed tube the union volume is one ball plus the
saturated two-ball increments along the reference path.  Every larger tube
admits strict failure.  The stated adjacent-contraction consequence and
transverse Hessian, including its kernel and the `g=2R` tangency convention,
also follow.

The verdict rests on the written proof, not agreement between programs.  The
review checker deliberately uses a different axial lower-envelope derivation
of the lens maximum and new asymmetric exact witnesses.

## Human premises and completeness reductions audited

1. Normalize any ordered reference triple to outer centers `-u e_1` and
   `v e_1` and middle reference center `0`.  An actual outer intersection is
   contained in the intersection of the radius-`R+epsilon` reference balls;
   this is exactly the triangle inequality and loses no case.
2. At axial coordinate `s`, the largest possible squared norm in that
   expanded lens is the lower envelope of
   `r^2-u^2-2us` and `r^2-v^2+2vs`.  One affine function decreases and the
   other increases, so their crossing is the global maximum
   `r^2-uv`.  This independently recovers the proof's lens calculation.
3. Every possible middle ball contains that lens precisely when its maximum
   norm plus `epsilon` is at most `R`.  In the small-gap regime this reduces
   to `4R epsilon <= uv`; in the long-gap regime the lens is empty until
   `epsilon=(u+v)/2-R`, then is already missable.  The formulas agree at
   `max(u,v)=2R`.
4. `theta_R` is nondecreasing in each gap.  Every nonconsecutive triple has
   left and right separations at least those of a consecutive triple around
   its middle label.  Hence minimizing only over consecutive triples is a
   complete reduction, not a heuristic.
5. Strictly inside the tube, the triple containment for every `i<j<k`
   makes each point's membership labels an interval.  The exact identity
   `number of memberships - number of adjacent double memberships = number
   of label runs` then proves the path inclusion-exclusion formula pointwise.
6. The two-ball lens is two congruent spherical caps.  Substitution in the
   cap integral gives the stated saturated increment `Phi`; no smoothness or
   overlap-graph assumption is being smuggled into this step.
7. At the closed radius, radial scaling of all displacement vectors puts the
   configuration in the strict tube.  Ball and pair-intersection indicators
   converge away from finitely many spheres, a null set, inside a common
   bounded region.  Dominated convergence therefore preserves the *volume*
   identity even when pointwise interval membership fails at the boundary.
8. Above the threshold, moving both outer centers toward an extremal lens
   point and the middle center directly away uses exactly the allowed
   displacement.  A small transverse motion enters both outer balls while
   staying outside the middle ball.  This produces an open set with at least
   two label runs.  Other balls cannot repair the absent middle label, so the
   path expression strictly exceeds union volume.
9. The preceding witness is available for every minimizing consecutive
   triple and every `epsilon>tau`; choosing an intermediate `eta` handles the
   strict displacement requirement.  The construction only needs the plane
   spanned by `e_1,e_2`, so it embeds unchanged in every `d>=2`.
10. In the tube, each adjacent contribution is the nondecreasing function
    `Phi` of that adjacent distance.  It is strictly increasing below `2R`
    and constant from `2R` onward, giving both the contraction inequality and
    the exact clipped-distance equality criterion.
11. With fixed axial coordinates,
    `sqrt(g^2+||Delta y||^2)=g+||Delta y||^2/(2g)+O(||Delta y||^4)` and
    `Phi'(g)=kappa_(d-1)(R^2-g^2/4)^((d-1)/2)` below tangency.  This yields the
    displayed quadratic coefficient and Hessian.  Terms with `g>=2R` are
    locally constant, including `g=2R` because transverse motion only
    increases distance.  Positive edge weights make the kernel precisely
    vectors constant on each strict-overlap path component.
12. For `N<=2` there is no triple obstruction and ordinary two-ball
    inclusion-exclusion is exact for all displacements.  For `N>=3`, the
    finite minimum defining `tau` is positive.  These two cases exhaust all
    allowed `N`.

## Adversarial smallest examples and boundary cases

- The minimal obstruction already has three labels.  Exact asymmetric
  witnesses were checked in both branches: with `R=1`, gaps `(1/7,13/7)`
  have `theta=13/196` and fail at displacement `2/15`; gaps `(1/13,35/13)`
  have `theta=5/13` and fail at displacement `19/20`.  Both witnesses have
  rational extremal coordinates and a rational point strictly inside the two
  outer balls and outside the middle ball.
- At `R=1`, gaps `(1,3)` and displacement `tau=1`, membership at the outer
  tangency point is exactly `101`: set containment fails, but only at a
  zero-volume point.  At every radial scale `alpha<1` the outer balls are
  disjoint.  This confirms why the theorem correctly claims containment only
  in the open tube but volume equality in the closed tube.
- The exact checker tests the branch interface `max(u,v)=2R`, below/equal/
  above-threshold displacements, unequal gaps, long gaps with tube radius
  larger than `R`, and 3,900 small gap sequences.  In 69,275 triples, no
  nonconsecutive triple lowers the consecutive minimum.
- It exhausts all 32,766 nonempty-or-empty membership masks of lengths 1
  through 14, including arbitrary extra labels, and 330,750 rational point
  memberships from 750 independently perturbed three- and four-center
  configurations strictly inside their tubes.
- Cap/Phi identities, contraction equality, Hessian coefficients in odd
  dimensions 3, 5, 7, and 9, and a disconnected weighted-path kernel are
  checked exactly.  These finite calculations corroborate the universal
  proof; they are not presented as exhaustive verification of continuous
  geometry.

## Scope and literature caveats

The theorem is local for a fixed equal radius and fixed distinct collinear
reference configuration.  It neither proves the unrestricted
Kneser--Poulsen conjecture nor covers unequal radii or coincident reference
centers.  Its sharpness concerns this exact path formula, not failure of the
contraction inequality.

The source correctly treats general ball-union inclusion-exclusion and
first-variation methods as classical.  Its comparison with Edelsbrunner's
dual-shape formula, Csikos's volume formula, the planar theorem of
Bezdek--Connelly, and the special-contraction result of Bezdek--Naszodi is
appropriately limited.  My targeted literature check found no matching
published sharp tube radius, but that supports only a search-relative novelty
assessment, not an absolute priority claim.

## Reproduce

Only CPython's standard library is used; no target module, floating point,
solver, or private data is imported.

```sh
cd discrete_geometry/near_collinear_ball_unions_review1
sha256sum -c SHA256SUMS
python3 review.py
python3 -O review.py
```

The expected result is `PASS` followed by the SHA-256 digest of the canonical
JSON summary.  Explicit exceptions are used, so optimized mode does not
disable a check.
