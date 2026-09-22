# Review of the sharp simplex orthant-projection theorem

Date: 2026-09-22

Target commit: `b103e916f6efca491e2119e1bc9c2879cbb4e4f7`

Target graph reference: `bafkreiethi6omrbebnho7hld27gxk5qcmo6fuyvjcxu2pdboccrcskjuci`

## Verdict

**Accept, with high confidence in the stated scope.** I found no mathematical
defect in the universal projection-envelope bound, its exact finite
realization for polytopal positive images, the simplex-coordinate formula,
strict placement concavity and optimizer classification, the planar formula,
the certified value `C_3=127/8`, or the exponential growth rate.

The result solves a sharp extremal problem over all finite-dimensional
unconditional lifts whose positive projection is a prescribed simplex. It
does not determine the global constant for arbitrary positive images, the
smallest attaining ambient dimension, an asymptotic prefactor, or the
narrower ball/zonoid conjectures. The acceptance is conditional on the
standard Brunn--Minkowski equality theorem and elementary convex-geometric
premises itemized below; it is not a formal proof or a priority judgment.

## Independent proof audit

### 1. The envelope bound and finite realization

For `z` in an unconditional convex body, sign symmetry and convexity place
`z+`, `z-`, and `|z|` in its positive part. Thus, for `Q=A K+`, the three
points `Az+`, `Az-`, and their sum lie in `Q`, while
`Az=Az+-Az-`. This proves

    A K subset E(Q)={x-y:x,y,x+y in Q}

without interchanging orthant intersection and projection.

For the converse, `E(Q)` is the linear image of a compact polytope. The
construction assigns a centered coordinate segment to every vertex of `Q`
and a centered coordinate square to chosen preimages `(x_v,y_v)` of every
vertex of `E(Q)`. The only delicate set identity is that the positive part of
the convex hull of these centered coordinate boxes equals the convex hull of
their positive boxes. It is valid: that latter hull is coordinatewise
downward closed, while replacing every point in a signed convex combination
by its absolute value produces a dominating point in the positive-box hull.

Every positive segment and parallelogram maps into `Q`, and the vertex
segments recover all of `Q`; every envelope vertex `x_v-y_v` occurs as a
signed corner of its square. Hence both image equalities hold. Each ambient
coordinate occurs in a segment or square, so the constructed body contains
the coordinate crosspolytope and is genuinely full dimensional. Finally,
restricting `A` to its row space multiplies both image volumes by the same
Jacobian `sqrt(det(AA^T))`, correctly converting the linear construction to
an orthogonal-projection example.

### 2. Simplex elimination and normalization

If the origin has barycentric coordinates `c`, the barycentric coordinates
of `x+y` are `lambda+mu-c`. Therefore the three membership conditions are
equivalent to

    lambda,mu>=0,  sum lambda=sum mu=1,  lambda+mu>=c.

Writing `w=lambda-mu` and `a=lambda+mu` leaves precisely

    sum_i max(|w_i|,c_i)<=2,  sum_i w_i=0.

The converse is complete: any slack below two can be distributed among the
`a_i`, after which `(a+w)/2` and `(a-w)/2` are valid probability vectors.
The map from the zero-sum hyperplane to the simplex span is injective even
when some `c_i` vanish, because its one-dimensional kernel is spanned by `c`,
whose coordinate sum is one. The reference simplex volume is
`sqrt(n+1)/n!`, so the normalization of `R_n(c)` is correct.

The identity

    D_c=(product_i[-c_i,c_i]+B_1) intersect H

follows coordinatewise from the distance to the box. At the barycenter,
scaling by `n+1` gives the displayed fixed central-section formula with the
correct `N^-n` factor.

### 3. Strict concavity and all boundary placements

Joint convexity of `max(|w_i|,c_i)` yields the required Minkowski inclusion,
and Brunn--Minkowski gives concavity of the volume root. All `D_c` contain a
fixed full-dimensional crosspolytope in `H`, so the positive-volume equality
criterion applies.

The support value in every coordinate direction is exactly one. At `w_i=1`,
the other coordinates have the stated simplex description with mass `c_i`;
its `(n-1)`-volume is `sqrt(n)c_i^(n-1)/(n-1)!`. This remains meaningful at
`c_i=0`, where the exposed face collapses to one point. If two such bodies
were homothetic, central symmetry removes translation and the common support
values force scale one. The labeled exposed-face volumes then recover every
`c_i`. Distinct parameters are therefore not homothetic, establishing strict
concavity for `n>=2`.

Permutation averaging gives the unique barycentric maximum. Since every
parameter vertex has value `2^n`, strict concavity puts every nonvertex
parameter strictly above it, including points on proper faces of the
parameter simplex. The separate `n=1` calculation correctly gives the
constant value two and avoids applying a false strictness statement there.

### 4. Planar formula and explicit lift

In the zero-sum plane, the difference body is the sixfold-ratio hexagon.
Expanding each maximum leaves exactly the three pairs of additional strip
constraints. Each pair cuts two opposite corner triangles, of relative area
`c_i^2`; the condition `sum c_i=1` makes their interiors disjoint along every
shared edge. Subtracting all six triangles gives
`R_2(c)=6-2 sum c_i^2`, including boundary parameters by continuity.

The displayed nine-dimensional lift is internally consistent. Direct exact
enumeration gives positive image area `27/2`, full image area `72`, and ratio
`16/3`. Every ambient coordinate occurs in a listed square, the map has rank
two, and `det(AA^T)=675`; the projection Jacobian consequently cancels as
claimed.

### 5. Central sections and exponential rate

The volume dissection of
`B_N=[-1,1]^N+N B_1^N` is exact. Choosing the `j` coordinates outside the
cube, their signs, and their nonnegative excesses gives

    V_N=2^N sum_j binom(N,j) N^j/j!.

The supporting hyperplanes parallel to the zero-sum hyperplane lie at
distance `2sqrt(N)`. Central symmetry and Brunn--Minkowski make the central
section maximal, yielding the lower section estimate by integration over the
full width. The two pyramids with common central base and apices
`+/-2(1,...,1)` lie inside the body, have disjoint interiors, and each has the
correct height, yielding the upper estimate. Substitution reproduces exactly
`L_n<=C_n<=(n+1)L_n`.

Uniform factorial estimates give the stated exponent

    f(t)=-2t log t-(1-t)log(1-t)+t.

Its unique maximizer satisfies `1-t=t^2`, hence is
`r=(sqrt(5)-1)/2`, and `f(r)=-2log r+r`. The polynomial section factors do
not affect the root limit, while `(n!/(n+1)^n)^(1/n)` tends to `e^-1`.
This gives `(2/r^2)e^(r-1)` with no missing exponential factor. The proof
appropriately makes no polynomial-prefactor claim.

## Human premises and completeness reductions

The verdict rests on these human-checked premises:

1. The positive part of an unconditional convex body is coordinatewise
   downward closed, and sign symmetry plus convexity gives `z+`, `z-`, and
   `|z|` in that positive part.
2. A linear image of a compact polytope is a polytope, and containing all of
   its vertices contains the whole polytope.
3. The row-space restriction of a surjective matrix has volume Jacobian
   `sqrt(det(AA^T))`.
4. Brunn--Minkowski in the relevant zero-sum subspace, including its equality
   characterization by positive homothety for full-dimensional convex bodies.
5. Central parallel sections of a centrally symmetric convex body are
   maximal; this is the standard sectional consequence of Brunn--Minkowski.
6. The elementary simplex, crosspolytope, pyramid, and Minkowski-sum volume
   calculations used in the normalization and dissection.
7. Uniform Stirling bounds sufficient for the largest-summand root limit.
8. The bounded primary-literature search used to delimit novelty.

The proof covers the required logical branches: arbitrary finite ambient
dimension versus constructed attainment in a possibly larger one; interior
versus boundary origin placements; strictness only for `n>=2`; rational and
irrational simplices; linear images versus orthogonal projections; exact
finite constants versus the all-dimensional asymptotic. It does not assume
the origin is interior, that the simplex is regular, or that the original
body is permutation invariant.

## Adversarial smallest examples

- **Dimension one.** Parameters `(0,1)`, `(2/7,5/7)`, and `(1,0)` all give
  ratio two. This confirms the explicit exception to strict placement
  concavity.
- **Planar vertex.** At `c=(1,0,0)`, the envelope ratio is exactly four, the
  conjectured factor. Moving to the boundary nonvertex `(0,2/5,3/5)` raises
  it to `124/25`; strictness is not limited to interior origins.
- **Off-grid triangle.** At `(1/7,2/7,4/7)`, independent max-inequality
  expansion gives `36/7`, checking the planar formula outside the producer's
  denominator-six grid.
- **Three-dimensional zero coordinate.** For
  `c=(1/2,1/4,1/4,0)`, the fourth coordinate-one exposed face is one point,
  while the other three faces have the exact predicted triangle areas. The
  ratio is `227/16>8`, guarding both the face-degeneration and boundary-
  strictness reductions.
- **Vertex and edge midpoint in dimension three.** The vertex placement has
  ratio eight, while `(1/2,1/2,0,0)` has ratio `25/2`.
- **Nonuniform permutation pair.** The parameters
  `(1/2,1/4,1/8,1/8)` and `(1/4,1/2,1/8,1/8)` both have ratio `1879/128`,
  while their midpoint has the strictly larger ratio `481/32`. All 2,304
  pairs of enumerated endpoint vertices satisfy the claimed Minkowski
  inclusion exactly.
- **Barycentric three-dimensional section.** A separate exact enumeration
  finds 48 vertices and independently reproduces `C_3=127/8`.
- **Projection/intersection trap.** The envelope proof is phrased using
  `Q=A(K intersect orthant)` throughout. It never replaces this by an
  intersection of `AK` with a projected orthant, an invalid operation in
  general.

## Reproduction and source integrity

The producer's ordinary and optimized Python runs matched its committed
`EXPECTED.json` byte-for-byte, and every manifest entry passed. The producer
checks the explicit lift, 28 planar placements by two descriptions, the
three-dimensional section by facet tetrahedra and exact slab integration,
the rational section bounds through dimension twelve, and seven malformed
controls.

This review's standard-library checker uses exact rational arithmetic and a
new parameter surface. Its ordinary and optimized outputs match the committed
expected file. It directly expands the maximum inequality, enumerates active
vertices, and reconstructs volumes from supporting facets. These finite
checks corroborate placement and boundary reductions only; the human audit
of the universal realization and asymptotic controls the verdict.

The live arXiv API on 2026-09-22 listed
[Fradelizi--Manui--Meyer--Ndiaye, arXiv:2607.03582](https://arxiv.org/abs/2607.03582)
only as v1. Its Conjecture 3 is the unconditional-body factor `2^n`, and its
definition requires coordinate sign invariance, not permutation invariance.
The paper proves special cases but not the reviewed simplex-envelope theorem.
The cited [Klain paper](https://arxiv.org/abs/1005.1409) states exactly the
positive-volume homothety equality criterion used here.

Targeted arXiv and web searches for the exact title, orthant/simplex
projection problem, envelope relation, and displayed constants found no
matching primary theorem. This supports the target's restrained scope claim;
it is not a guarantee of historical priority.

## Strengthening and improvement opportunities

1. Promote the positive-part identity for a convex hull of centered
   coordinate boxes to a named lemma. It is correct but is the least standard
   bridge in the realization proof.
2. State explicitly that the kernel of the simplex vertex map is `span(c)`;
   this makes injectivity on the zero-sum hyperplane immediate even when the
   origin lies on the simplex boundary.
3. In the strictness argument, spell out the two inequalities whose equality
   would be needed: containment followed by Brunn--Minkowski. This clarifies
   why nonhomothety alone forces strict concavity despite the initial
   containment.
4. Add a boundary parameter with `c_i=0` and a nonuniform permutation pair to
   the producer checker, as in this review.
5. A proof-assistant formalization of the realization lemma and the strict
   Brunn--Minkowski reduction would reduce the remaining trust surface; it is
   not required for this acceptance.
