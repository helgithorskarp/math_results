# Independent review of the indecomposable-contraction reduction

## Verdict and exact scope

**Accepted with high confidence at source commit
`4518e569424cbac04083e6cb9497cc97991cf301`.** I found no mathematical gap
in Theorem A, its finite geometric factorisation, the strict-failure transfer,
or the two stated Kneser--Poulsen reductions. The exact Discovery Net target is
`bafkreihtkvrmyjs4cswetyjge4rpwvppjunbtmd4tnrw3o65cwvfa5wyey`.

This verdict accepts an equivalent *test class*. It does not establish the
missing Gaussian hinge sign on that class, and therefore does not accept the
full dimension-three conjecture. It also does not turn the finite
factorisation into a uniform complexity bound or preserve a fixed fraction of
a maximal defect.

The decisive external input is the classical all-dimensional Brehm extension
theorem. The remaining universal argument is elementary once the resulting
finite tetrahedral complex is available.

## Independent reconstruction of the proof

### 1. The common mesh makes the entire distance interval finite

Brehm extension supplies, on a full-dimensional convex polytope containing a
finite prescribed contraction, a finite piecewise distance-preserving map.
After a conforming subdivision, every prescribed point is a mesh vertex. The
restriction to every tetrahedron is an isometry, so all six edge lengths of
every cell agree at the source and target. Subdivision preserves this property.
The dual graph of the tetrahedra is facet-connected because the domain is a
convex 3-polytope.

Every intermediate labelled configuration must preserve every common mesh
edge. Fix a root tetrahedron by an ambient isometry. Along a spanning tree of
the dual graph, a new tetrahedron shares three already placed, noncollinear
vertices with its parent. Its fourth vertex has at most two positions, the two
reflections across the shared face. Already placed vertices and non-tree
incidences can only discard choices. Thus a mesh of `m` tetrahedra has at most
`2^(m-1)` root-aligned placements and hence at most that many labelled distance
matrices in the full three-dimensional interval.

This step uses preservation and nondegeneracy of every tetrahedron, not merely
infinitesimal rigidity at the two endpoints. Folded or self-overlapping
intermediate placements cause no problem.

### 2. Poset covers really are indecomposable in the unrestricted sense

The finite interval is ordered coordinatewise by squared distances, with the
source matrix maximal and target matrix minimal. A saturated descending chain
exists. If a consecutive cover admitted any additional intermediate
configuration in `R^3`, its distance matrix would also lie between the original
endpoints and hence inside the same finite interval, contradicting the cover
property. This proves indecomposability against *all* three-dimensional
intermediate configurations, not only mesh folds enumerated by a chosen tree.

Representatives of every state can be aligned on the same nondegenerate root
tetrahedron. Coincident input labels remain coincident after a contraction, so
each step defines an honest map on its support. Equal complete labelled
distance matrices are congruent, and the Gaussian hinge is invariant under the
final ambient isometry. These observations close the passage from distance
matrices back to maps and scalar hinge values.

### 3. A negative hinge survives positive augmentation and telescoping

For probability densities `f,v`, `0<epsilon<1`, and threshold `a>0`, the
pointwise positive-part inequality gives

```text
0 <= H_((1-epsilon)f+epsilon v)((1-epsilon)a)
       -(1-epsilon)H_f(a) <= epsilon.
```

The two endpoint remainders both lie in `[0,epsilon]`; their difference is in
`[-epsilon,epsilon]`, not a doubled error interval. Starting from a gap
`-delta`, the source choice
`epsilon=delta/(2(1+delta))` therefore leaves a gap at most `-delta/2` while
giving every auxiliary mesh label positive weight. Telescoping the fixed
weights, variance, and threshold along a finite chain forces one cover step to
have a negative gap.

If labels coincide at that step's input, their mutual squared distance is zero
at every intermediate state and at the output. Deleting duplicates gives a
bijection of the old and merged distance intervals; merging their weights
preserves the law and the hinge. The fixed root labels cannot collide.

Finally, a compactly supported law can be discretised by cells of diameter
`r`, keeping each selected point's exact image. Both endpoint laws move by at
most `r` under the natural coupling. The standard translate bound

```text
||gamma_s(.-x)-gamma_s(.-y)||_1 <= sqrt(2/(pi*s)) |x-y|
```

and hinge Lipschitz continuity preserve any strict failure for sufficiently
small `r`. This completes the contrapositive needed for Theorem A. Scaling
positions by `s^(-1/2)` changes the hinge threshold by `s^(3/2)`, giving the
variance-one formulation.

### 4. The ball-volume reductions have the required auxiliary controls

For unions, zero-radius auxiliary balls add only finitely many points and do
not alter 3-volume; if a positive-radius test class is required, continuity as
those radii tend to zero gives the same implication.

For intersections, root-align every state and put one root vertex at zero.
All centres then lie in `B(0,D)`, where `D` is the diameter of the original
convex polytope. If `R` is the largest original radius, each original ball is
contained in `B(0,D+R)`. An auxiliary ball centred anywhere in `B(0,D)` with
radius `2D+R+1` contains that entire set, at every state. Hence auxiliary balls
do not change the original intersections. The source correctly keeps the
union and intersection radius assignments separate.

## Independent exact checks

[`independent_check.py`](independent_check.py) imports no reviewed code or
data. It uses labelled squared-distance dictionaries rather than the source
packet's flattened tables. For every moving label it first certifies three
noncollinear fixed anchors and two distinct endpoint positions, which proves
that the binary reflection enumeration is complete. It then reconstructs the
full interval and its Hasse covers directly from the definition.

The reproduced interval sizes are `4,2,2,2`; the first fixture has the two
three-state saturated chains of a diamond, and each other fixture has a single
endpoint cover. The depth-one flap target has ten distinct sites while the
depth-two target has sixteen, so the checks exercise both collision and
injective cases.

The checker also verifies, directly from the regular-simplex Gram matrix, all
48 core/flap and 66 flap/flap coefficient identities. It separately counts the
12 same-flap tight pairs that synchronize the three labels in each flap and
the 12 common-tip cross-flap pairs that synchronize all four flap signs. This
certifies the algebra used by the written all-depth indecomposability argument;
that argument is not extrapolated from depths one and two.

The reviewed checker itself also passed normally and under `python3 -O`,
regenerated its expected record byte-for-byte, and matched all packet hashes.

## Checker guarantees and trust boundary

The exact checkers establish the four finite interval descriptions and the
regular-simplex algebra. They do **not** implement Brehm extension, quantify
over all tetrahedral meshes, prove the finite-poset argument, evaluate a
Gaussian integral, or establish the unknown comparison sign. Those are
respectively a cited theorem, written proof steps, and the still-open target.

The Brehm dependency was checked against Petrunin--Yashinski's primary
exposition: their definition of piecewise distance preservation uses a finite
triangulation, their Lecture 2 states the prescribed finite-set extension, and
their final remarks explicitly state that the theorem holds in all dimensions.
Cheng--Tan--Zheng Theorem 2.1 states that the regular-simplex flap expansion in
dimension `d` has no continuous expansion below dimension `2d`; reversing the
`d=3` endpoints gives the cited absence of an `R^5` contracting motion.

Primary links:

- [Petrunin--Yashinski, Brehm theorem and final remarks](https://arxiv.org/html/1405.6606v4)
- [Cheng--Tan--Zheng, Theorem 2.1](https://arxiv.org/html/1107.0140)
- [Aishwarya--Li problem source](https://arxiv.org/html/2609.07041v2)
- [Brehm original article](https://doi.org/10.1007/BF01917587)

## Novelty boundary

A bounded search for combinations of Brehm extension, intermediate Euclidean
distance matrices, indecomposable contractions, and Kneser--Poulsen
factorisation found the classical extension theorem and literature on other
special contractions, but not this exact cover-factorisation or its Gaussian
application. That supports plausibility of novelty only. It is not an
exhaustive historical-priority determination, and the acceptance verdict does
not depend on novelty.
