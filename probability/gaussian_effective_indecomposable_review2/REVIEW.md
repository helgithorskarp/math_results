# Independent review of the effective indecomposable bound

## Verdict and scope

**Accepted with high confidence at source commit
[`de9a0bb7af7179ea6e1b2c5b4013f84d6955f981`](https://github.com/helgithorskarp/math_results/tree/de9a0bb7af7179ea6e1b2c5b4013f84d6955f981/probability/gaussian_indecomposable_contractions).**
The exact Discovery Net target is
`bafkreib6l2ras4jqduttk2diybnooir2qrzg6jyin65ms44e45imfe7dkq`.

The explicit bounds

```text
h_N = 512*2^N*(N+6) + 3N + binom(N,3) + 6,
M_N = 12*h_N*[1+h_N+binom(h_N,2)+binom(h_N,3)]
```

are valid.  Every `N`-point contraction in `R^3` has the claimed
piecewise-isometric extension with at most `M_N` tetrahedra and `4M_N`
vertices.  Rational prescribed data give rational mesh data and rational
representatives of the finite interval.  A negative hinge gap `delta` yields
an indecomposable step with at most `4M_N` labels, weight floor
`delta/[8M_N(1+delta)]`, and gap strictly below `-delta*2^(-M_N)`.

This is an effective reduction, not a sign theorem.  It does not prove the
dimension-three Gaussian-majorisation conjecture, give a practical search,
control coordinate bit lengths, or preserve a fixed fraction of the defect.

## Independent proof audit

### Bounded extension

The product triangular fold of `[-4R,4R]^3` has exactly `8^3=512` convex
isometric cubes, maps into `[0,R]^3`, and is globally 1-Lipschitz by splitting
line segments at the finitely many cube faces.  On the outer boundary,
`|a-x|>=3R` while `|b-F(x)|<3R`; consequently every repair region is compactly
contained in the cube.  This is the needed cure for the boundary blind zone
in the usual Brehm construction.

For one repair, on an old piece `Q` with `F=S` the repair region is the cut

```text
Q intersect {|x-a| < |x-S^(-1)b|}.
```

Its boundary section is a convex polygon with at most as many edges as `Q`
has facets.  The standard 1-Lipschitz inequality makes the full repair region
star-shaped about `a`.  Along every ray from `a`, its boundary point is unique:
two boundary points would force a radial segment into a finite union of
bisector planes, none containing `a`.  Hence the cones over the boundary
sections have disjoint interiors and cover the repair closure.

Reflection in each bisector followed by `S` is an isometry, sends `a` to `b`,
and agrees with the old map on the section.  Its radial formula is a convex
combination of `b` and the old boundary image, so the image remains in the
fixed convex cube.  Each old piece contributes at most one retained clip and
one cone; both have at most one more facet.  Thus each repair sends `(c,f)` to
at most `(2c,f+1)`, while previous prescribed points lie outside the strict
repair region.  After `N` repairs the bounds are `c<=512*2^N` and `f<=N+6`.

The construction is a quantitative reworking of the classical Brehm repair.
The primary exposition states the finite-set extension theorem, proves the
same star/bisector mechanism in the plane, and records that it holds in all
dimensions: [Petrunin--Yashinski, Lecture 2 and final
remarks](https://arxiv.org/html/1405.6606v4).  Osinenko's earlier note treats
constructive rational input in dimension two, so no general priority claim is
attached to constructivity here: [Osinenko](https://arxiv.org/abs/1609.00965v2).

### Conforming mesh and rationality

All old facet planes, the facets of the chosen source polytope, and three
coordinate planes through every prescribed source point total at most `h_N`.
Their arrangement has at most
`1+h+binom(h,2)+binom(h,3)` full-dimensional cells and refines all isometric
pieces face-to-face.  The three independent coordinate planes make each
prescribed point a complex vertex.

A convex three-cell with `f<=h_N` facets has `E<=3f-6` edges.  Its barycentric
tetrahedra are the flags vertex--edge--facet--cell, four per edge, so it
contributes at most `12h_N` tetrahedra.  This proves `M_N`; the elementary
vertex bound is then `4M_N`.  The shared barycentric subdivisions are
conforming and nondegenerate.

For rational data, every seed isometry, bisector reflection, plane
intersection, and face barycentre is rational.  After fixing a rational root
tetrahedron, a neighbouring tetrahedron is placed by continuing the current
source isometry or composing it with reflection in its rational source-face
plane.  Thus every candidate placement, and hence every surviving state of
the full distance interval, has a rational representative.  This proves
rationality only; denominators may grow without a stated bound.

### Defect bookkeeping and consumer handoff

With `epsilon=delta/[2(1+delta)]`, scaling the old law and adding an
`epsilon`-mass uniform mesh law changes the endpoint gap by at most one
`epsilon`, leaving at most `-delta/2`.  It also gives every one of at most
`4M_N` vertices mass at least `delta/[8M_N(1+delta)]`.  A mesh of `m`
tetrahedra has at most `2^(m-1)` root-aligned interval states, so a saturated
chain has at most `2^(m-1)-1` steps.  Telescoping therefore produces a step
with gap strictly below `-delta*2^(-m)`, hence below
`-delta*2^(-M_N)`.  The already reviewed collision merge preserves the law
and the whole distance interval.

The handoff to the accepted paired-cubature result is also arithmetically
correct.  If the original defect is `delta`, `k=ceil(6/delta)` makes the
localisation loss `11/(4k)<delta/2`.  Substituting `d=delta/2` in the theorem
gives the stated weight floor `delta/[8M_(A_k)(2+delta)]` and gap magnitude
greater than `delta*2^(-M_(A_k)-1)`.  Root alignment places every centre in a
ball of radius `4k` in the full-dimensional case and below `7k` in the cube
case because `4*sqrt(3)<7`.

## Reproduction and checker boundary

The author's exact checker passed under ordinary and optimized Python with
status `EFFECTIVE_INDECOMPOSABLE_BOUND_CONTROLS_PASS`; the complete submitted
SHA256 manifest matched.  [`independent_check.py`](independent_check.py)
imports no author code or record and passed normally and under `python -O`.
It uses four unrelated signed-permutation/rational repair fixtures and checks
36 Gram entries, 16 bisector boundary agreements, 64 radial identities, and
40 pair distances.  It also reconstructs 81 arrangement orders, the four
displayed large `M_N` values, 315 strict chain/mass inequalities, and five
cubature handoffs.  Its output is:

```text
INDEPENDENT_EFFECTIVE_BOUND_REVIEW_PASS
repair fixtures/Gram/boundary/radial/distance: 4 36 16 64 40
region/flag/displayed-budget checks: 81 3 4
perturbation/chain/handoff checks: 5 315 5
```

These finite controls check algebra, implementation independence, edge cases,
and the displayed constants.  They do not enumerate the universal mesh,
formalize the polyhedral argument, evaluate a Gaussian integral, or establish
the missing hinge sign.  Those boundaries are respectively the written proof,
the previously accepted qualitative reduction, and the still-open headline
problem stated in [Aishwarya--Li, Conjecture
1.1](https://arxiv.org/html/2609.07041v2#S1.SS1.p4).

## Novelty boundary

The Brehm extension and repair are classical, and constructive rational work
already exists in dimension two.  The explicit three-dimensional count and
its Gaussian defect composition may be useful, but this review does not
establish historical priority.  The verdict concerns correctness at the cited
commit, not novelty.
