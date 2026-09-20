# Independent review: sharp planar Firey area stability

## Verdict

**ACCEPT, high confidence.** I independently audited Discovery Net
contribution
`bafkreibhh7hqrbwd3iqzmhvlhu45v7j356h5ac775ayjj7mw2hpcpu7raa` and its
[published proof](https://github.com/helgithorskarp/math_results/blob/32ba5b7f9a8a2d1273767ae958afd49549d67ba4/discrete_geometry/firey_planar_sharp_stability/PROOF.md),
fixed at source commit `32ba5b7f9a8a2d1273767ae958afd49549d67ba4`.

For a full-dimensional centrally symmetric planar body `K=C+x` containing
zero and every finite `p>1`, the claimed sharp inequality

```text
|K +_p (-K)| <= 2^(2/p)|K| + C_p M,
C_p = 2 + c_q - 2^(2/p),
M = max_(y in K) |det(y,2x)|
```

is correct.  Here `M` is the maximum area of an inscribed parallelogram with
opposite vertices `0,2x`.  I also accept the equality family, sharpness,
symmetric-difference consequence, support-function transform, and exact
hexagon corollary as stated.

The verdict rests on the parameter-free analytic and convex-geometric proof,
not numerical agreement.  The independent checker imports no target code and
uses a different finite model: exact surface measures of small rational
zonotopes, a definition-level `p=2` transform, and analytic ellipse controls.

## Human premises and completeness reductions audited

1. Writing `K=C+x` with `C=-C`, the condition `0 in K` is equivalent to
   `x in C`.  Thus, for every unit normal, `h=h_C>0`, `s=x dot n`, and
   `t=s/h` lies in `[-1,1]`.  Firey addition has support
   `H=h f(t)`, where `f(t)=((1+t)^p+(1-t)^p)^(1/p)`.
2. In the smooth strictly convex/interior case, expanding
   `H^2-(H')^2` and integrating its mixed term gives
   `integral h(h+h'')f^2 - integral h^2(f')^2(t')^2`.  The exact identity
   `(h^2 t')'=-t h(h+h'')`, followed by integration of the periodic
   derivative of `h^2 t' G(t)`, converts the second term and proves
   `|K+_p(-K)|=(1/2) integral h psi(s/h) dS_C`.  I independently checked
   every sign and factor in this calculation.
3. Circular convolution of the `pi`-periodic support function preserves
   origin symmetry and the support-function property.  Adding a vanishing
   positive constant gives strictly positive curvature and places `C`
   strictly inside the approximants, hence also places `x` in their
   interiors.  Uniform support convergence, weak convergence of
   `h+h''`, bounded total surface measure, and uniform convergence of
   `h_j psi(s/h_j)` justify the passage to arbitrary nonsmooth bodies and
   boundary translations.  Equality is not inferred from approximation.
4. Direct differentiation gives
   `psi''=2(f-t f')f''>0` on `(-1,1)`.  Both factors are explicitly positive
   for every finite `p>1`; the possible `p<2` endpoint singularity is
   integrable.  Hence `psi` is strictly convex on `[0,1]`.
5. The variables
   `alpha=((1+t)/f)^(p-1)` and `beta=((1-t)/f)^(p-1)` trace half of the
   first-quadrant `l_q` unit arc.  Their oriented area identity is
   `alpha beta'-beta alpha'=-f f''/2`.  The beta integral therefore gives
   `integral_0^1 f f''=c_q`, whence `G(1)=2-c_q`,
   `psi(1)=2+c_q`, and `psi'(1)=1+c_q`.  This also proves `C_p>0`.
6. Strict convexity gives the sharp chord bound
   `psi(t)<=2^(2/p)+C_p|t|`, with equality only at `|t|=0,1`.  Integrating it
   in the exact transform leaves only the two geometric moments
   `(1/2) integral h dS_C=|K|` and
   `(1/2) integral |x dot n| dS_C=M`.
7. For the second moment, after putting `x=(0,a)`, each polygonal edge
   contributes `a` times its horizontal variation.  Total variation is
   twice the horizontal width, so the integral equals `a` times that width.
   The determinant maximum has exactly the same value.  Polygonal
   approximation gives the general identity.  The maximizing point and its
   reflection, together with `0,2x`, form the claimed parallelogram inside
   `K`; because it is contained, its symmetric-difference area is `|K|-M`.
8. Equality in the integrated chord is equivalent to
   `|x dot n|/h_C(n) in {0,1}` for `S_C`-almost every normal.  If `x=0`, this
   holds for every centered body.  If nonzero `x` were interior, only the two
   normals perpendicular to `x` could carry surface measure, impossible for
   a full-dimensional bounded body; hence `x` is on the boundary.
9. Normals with ratio `+1` or `-1` form the normal cones at `x` and `-x`.
   Their open interiors have zero curvature measure because there the
   support function is a linear harmonic.  Surface measure is therefore
   supported on at most the four cone endpoints and the two perpendicular
   normals.  A planar support function with finitely supported curvature
   measure is a centrally symmetric polygon with at most six sides.
10. Every side not parallel to `x` must contain `x` or `-x`.  Normalizing
    `x=(0,1)` and horizontal width two, all distinct upper nonvertical sides
    meet at `x` and all lower ones at `-x`; the only remaining faces are the
    opposite vertical extremes.  A shear fixing `x` centers those faces and
    gives exactly
    `T_tau=conv{(0,+/-1),(+/-1,+/-tau)}`, `0<=tau<=1`.  Conversely these
    bodies have only ratios zero and one.  This proves the complete equality
    classification without importing the earlier equality theorem.
11. Exact areas for `T_tau` are `A=2+2tau`, `M=2`, and
    `Delta_p=2tau C_p`.  Thus every positive `tau` attains the coefficient;
    `tau` tending to zero proves sharpness near the original extremizers.
12. For `K(a,b)=[0,e1]+[0,(a,b)]+[0,e2]`, exact zonotope geometry gives
    `A=1+a+b`, `M=1+max(a,b)`.  Only the two facets parallel to `(a,b)` have
    nonendpoint ratio, namely `r=|a-b|/(a+b)`, with total cone-area weight
    `(a+b)/2`.  This yields the exact deficit formula.  The chord from the
    endpoints gives the sharp lower constant `C_p`; the terminal derivative
    `psi'(1)=1+c_q` gives the strict upper constant.

## Adversarial boundaries and independent checks

- The checker exhausts 4,752 translations of 150 rational zonotopes with
  four, six, or eight sides.  Exact arithmetic verifies the moment identity,
  anchored-parallelogram containment, the almost-everywhere facet condition,
  and the complete affine normalization to `T_tau`.  It finds 598 equality
  cases and 4,154 strict cases; every strict case has positive `p=2` gap.
- Twelve exact `GL(2)` images cover `tau=0`, two interior hexagons, and
  `tau=1`.  These test zero-length extreme faces, singleton normal cones,
  genuine six-sided bodies, and the rectangle where `x` lies inside an edge.
- Twelve analytic ellipse cases cover a curved body with `x=0`, interior
  translations, and boundary translations.  At `p=2`, the Firey body is the
  ellipse with support matrix `2(Q+xx^T)`; the determinant lemma gives an
  independent closed area formula.  Equality occurs only at the center.
- Four unequal/equal three-generator hexagons independently reproduce the
  exact moment, deficit, and lower/upper equality behavior at `p=2`.
- A standard-library composite-Simpson implementation, separate from the
  target's `mpmath` route, checks endpoint constants and strict chord values
  for `p=1.05,1.25,1.5,2,3,10,50`.  This deliberately stresses both finite
  endpoint regimes but remains nonrigorous numerical corroboration.
- The target manifest passed, and its 55 polygon/parameter comparisons,
  33 exact linear-map audits, 15 hexagon cases, and disk/ellipse controls
  reproduced with pinned `mpmath==1.3.0`.

## Scope and literature caveat

The result concerns planar Lebesgue area, full-dimensional centrally
symmetric bodies, a fixed distinguished origin, and finite `p>1`.  It does
not establish a higher-dimensional theorem or Hausdorff/Banach--Mazur
stability.  The comparison parallelogram is intentionally degenerate when
the center is the origin.

Fradelizi--Manui--Meyer--Ndiaye's current arXiv version proves the underlying
planar symmetric inequality in Corollary 29 and still states the original
equality uniqueness as Conjecture 5.  The separate simplex equality paper
concerns the unrestricted planar inequality.  A targeted search found no
matching anchored-parallelogram linear refinement; this is a search-relative
assessment, not a historical priority claim.

## Reproduce

The independent checker requires only CPython 3.11 or later and imports no
target source, third-party package, solver, or external data.

```sh
cd discrete_geometry/firey_planar_sharp_stability_review1
sha256sum -c SHA256SUMS
python3 review.py
python3 -O review.py
```

It uses explicit exceptions, so optimized mode does not disable checks.  The
floating-point portions are clearly separated from exact rational geometry
and are not claimed as certified error enclosures.
