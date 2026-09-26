# An extremal-map reduction for Gaussian majorisation

Author proof, 26 September 2026; independent review pending.

The full dimension-three question remains open. This is a reduction of that
question, obtained from classical piecewise-isometric extension, with a
quantitative preservation of strict hinge violations. It supplies neither a
Gaussian counterexample nor a new positive Kneser--Poulsen class.

Write

$$
\gamma_s(x)=(2\pi s)^{-3/2}e^{-|x|^2/(2s)},\qquad
H_f(a)=\int_{\mathbb R^3}(f-a)_+,
$$

and, for a bounded probability law and a contraction on its support, put

$$
D_{\mu,T,s}(a)=H_{T_\#\mu*\gamma_s}(a)-H_{\mu*\gamma_s}(a).
$$

The target is nonnegativity for all such data, all `s>0`, and all `a>0`.
The threshold zero gives equality of masses.

## 1. Statement

**Theorem (rigid mesh reduction).** The full bounded-law question in
dimension three is equivalent to its restriction to the following data:

* a finite tetrahedral triangulation `K` of a full-dimensional convex
  polytope `P` in `R^3`, with vertex set `V`;
* a continuous map `F:P -> R^3` whose restriction to each tetrahedron is
  a Euclidean isometry;
* an arbitrary probability law assigning strictly positive mass to every
  vertex of `K`, with contraction `F|V`.

For these data every mesh edge is a tight distance constraint. Its framework
is infinitesimally rigid in `R^3` at both the input and output configurations:
its rigidity matrix has rank `3|V|-6`. After anchoring one image vertex at
zero, `F|V` is an extreme point of the finite Lipschitz unit ball.

More quantitatively, suppose a finite law `mu` on `X` has
`D_{mu,T,s}(a)=-delta<0`. There is such a mesh with

$$
X\subset V\subset P=\operatorname{conv}X,\qquad F|X=T,
$$

provided `X` spans `R^3`. For every probability law `nu` positive on `V`, set
`mu_epsilon=(1-epsilon)mu+epsilon nu`. Then

$$
\left|D_{\mu_\epsilon,F,s}((1-\epsilon)a)
       -(1-\epsilon)D_{\mu,T,s}(a)\right|\le\epsilon.       \tag{1}
$$

In particular any `0<epsilon<delta/(1+delta)` retains a strict violation.
The original source convex hull is unchanged. No bound on mesh complexity
or on the number of auxiliary vertices is asserted.

The restriction can alternatively require **uniform mass on a finite set
containing all mesh vertices**, with its additional points lying in `P`.
That larger finite set still has a connected tight graph and an
infinitesimally rigid tight framework. This variant is proved in Section 5.

## 2. Classical geometric input

We use Brehm's extension theorem: a contraction between finite subsets of
Euclidean spaces of the same dimension extends to a piecewise distance
preserving map. On any prescribed convex polytope containing the input
points, this gives a finite triangulation on whose cells the extension is
an isometry. The three-dimensional statement is a case of the original
all-dimensional theorem. See [Brehm (1981)](https://link.springer.com/article/10.1007/BF01917587)
and the explicit dimensional discussion in
[Petrunin--Yashinski, Lecture 2 and final remarks](https://arxiv.org/abs/1405.6606).

Apply this with `P=conv X`. Refine the triangulation to make each member
of the finite set `X` a vertex. A finite conforming subdivision inserting
points in their containing simplices has this property; restricting an
isometry to a smaller simplex preserves the property. Denote the resulting
vertex set by `V`.

Such a continuous piecewise-isometric map on a **convex** domain is
1-Lipschitz: partition the segment between two points into its finitely
many cell pieces, preserve the length of each piece, and apply the
triangle inequality to the image polygonal path. Thus all pairs of
vertices contract, not just the mesh edges. If a globally defined map is
required, apply Kirszbraun extension to the finite restriction; only its
values on the probability support enter the comparison.

The finite anchored extremality criterion is also prior work:
[Bredies--Chirinos Rodriguez--Naldi, Theorem 2.2](https://link.springer.com/article/10.1007/s00013-024-01978-y).
For completeness, its short Euclidean argument is as follows. If an
anchored map is the midpoint of two contractions, equality on a tight
edge and strict convexity of the Euclidean ball force their edge vectors
to coincide. Connectivity propagates this equality from the anchor.
Conversely, a disconnected tight component can be translated a sufficiently
small distance in both directions, using the strictly positive minimum
slack on its finitely many cross pairs. This yields two distinct feasible
maps with the original as midpoint.

The one-skeleton of `K` is connected. Consequently this criterion applies
to `F|V`. No concavity of the Gaussian hinge as a function of image sites
is used or claimed. The extension changes the finite domain; it does not
assert that a minimum on the original fixed-domain Lipschitz ball occurs
at an extreme point.

## 3. Rigidity and finite fold choices

Let `q_v=F(v)`. An infinitesimal flex of the mesh framework is a velocity
assignment `z_v` satisfying

$$
(q_v-q_w)\cdot(z_v-z_w)=0
\quad\text{on every mesh edge }vw.                         \tag{2}
$$

On one tetrahedron this velocity field has the form `b+Aq_v` with `A`
skew-symmetric. Indeed, interpolate the velocities by the unique affine
map `b+Bq` on its four affinely independent vertices. With the three edge
vectors from one vertex as a basis, the six edge equations say that the
symmetric part of `B` has zero quadratic form on each basis vector and
each pairwise difference. Polarization makes that symmetric part zero.

Two neighboring tetrahedra share three noncollinear image vertices. The
difference of their infinitesimal rigid motions therefore vanishes on
those three points. A nonzero skew-symmetric `3 x 3` matrix has a
one-dimensional kernel, so it cannot annihilate the two independent
differences of those points. The two motions are identical.

The facet adjacency graph of a triangulation of a convex 3-polytope is
connected: a generic path between two tetrahedron interiors can be chosen
to avoid the edges and vertices and to cross only facets. Propagating
the preceding observation shows that every solution of (2) is one
global infinitesimal rigid motion. These motions have dimension six
because a nondegenerate tetrahedron is present. The claimed rank follows.
The same reasoning applies at the source vertices. Coincident output
vertices in different cells cause no problem: each individual cell remains
nondegenerate, and labels retain their velocities and masses.

There is a useful finite description for a **fixed** mesh with `m`
tetrahedra. Fix the image isometry on one root tetrahedron and choose a
spanning tree of the facet adjacency graph. At each tree step there are
exactly two isometries on the new tetrahedron agreeing on its shared
face: continue the previous isometry, or compose it with reflection in
the source face plane. Thus there are at most `2^(m-1)` candidate maps,
up to a common target isometry. Retain a candidate only if its cell maps
agree at all shared vertices. This is a finite exact consistency test;
agreement at vertices implies agreement on whole shared faces and on
lower-dimensional intersections. The retained map is continuous and is
automatically a contraction by the segment argument above.

Equivalently, relative orientation signs and their compatibility around
mesh cycles encode the maps. The binary choices alone are insufficient:
the checker includes a four-tetrahedron mesh with eight tree choices,
of which four fail the closing consistency condition. This description
does not bound the meshes needed to represent arbitrary contractions.

## 4. Quantitative preservation of a violation

For any probability densities `f,u`, any `a>0`, and `0<epsilon<1`,
pointwise monotonicity and the 1-Lipschitz property of the positive part give

$$
0\le H_{(1-\epsilon)f+\epsilon u}((1-\epsilon)a)
       -(1-\epsilon)H_f(a)\le\epsilon.                    \tag{3}
$$

Apply (3) to the two endpoints. Their two remainders both belong to
`[0,epsilon]`, so their difference belongs to `[-epsilon,epsilon]`.
This proves (1), uniformly in the variance, threshold, geometry, and
number of auxiliary sites. The choice of `epsilon` in the statement
makes `-(1-epsilon)delta+epsilon` strictly negative.

For the passage from an arbitrary bounded-law failure to a finite one,
partition the support into finitely many sets of diameter at most `rho`,
select a point in each nonempty positive-mass piece, and keep its exact
image under `T`. The endpoints are coupled to their original laws with
displacement at most `rho`. Gaussian translates satisfy

$$
\|\gamma_s(\cdot-u)-\gamma_s(\cdot-v)\|_1
\le \sqrt{2/(\pi s)}\,|u-v|,                              \tag{4}
$$

by integration of the directional derivative along the segment.
Also `|H_f(a)-H_g(a)| <= ||f-g||_1`. Thus a sufficiently fine finite
approximation preserves a strict negative gap. This is the same finite
witness step used in the team's
[paired-rank reduction](../gaussian_majorisation_rank_abel/PROOF.md).

The finite source may be assumed to span `R^3`. If it does not, first
extend its map by Kirszbraun, add enough input sites to span `R^3`, and
give their law sufficiently small positive mass. Equation (3) again
preserves the violation. The convex-hull preservation assertion applies
to the resulting full-dimensional finite witness. Apply Section 2 and
then (1). This proves the nontrivial implication of the equivalence;
the reverse implication is immediate because every mesh restriction is
an admissible finite contraction.

## 5. Uniform weights without losing the tight framework

Fix a finite witness and the mesh extension already constructed. Let
the original atoms be `x_1,...,x_n` with masses `w_i>0`, and put
`k=|V\X|`. Choose a large integer `M>k` and positive integers `m_i`
whose sum is `M-k` and for which `m_i/M -> w_i` as `M -> infinity`.

For each `i`, choose `m_i` distinct points in `P`, one of them `x_i`,
all within distance `rho` of `x_i` and all lying in one mesh tetrahedron
incident to it. Choose the other points in that tetrahedron's interior
and avoid all previously chosen sites. This is possible for arbitrarily
large finite `m_i` and arbitrarily small `rho>0`. Include each of the
`k` auxiliary mesh vertices once. Give all `M` distinct input points mass
`1/M` and map them by `F`.

Both convolved laws converge in `L^1` to the original two endpoint laws
as `M -> infinity` and `rho -> 0`. For each endpoint an explicit upper
bound on the error is

$$
\sqrt{2/(\pi s)}\,\rho
+\sum_i|m_i/M-w_i|+k/M.                                  \tag{5}
$$

The hinge gap therefore stays negative for suitable finite choices.
Every extra point preserves its distance to all four vertices of its
containing tetrahedron. This connects it to the original tight graph.
After subtracting the global infinitesimal rigid motion of the mesh,
its velocity is orthogonal to its four displacement vectors to those
vertices; those vectors span `R^3`, so the velocity is zero. The enlarged
tight framework is again infinitesimally rigid, and its anchored map
is extreme. This proves the stated uniform-mass version. It does not
assert rational coordinates or a uniform bound on `M`.

## 6. A necessary adversarial control

Extremality, paired rank six, and full infinitesimal rigidity do **not**
provide the contracting motion in `R^5` used by the known Gaussian
motion argument. The classical simplex-flap example already separates
these conditions. Its construction and nonexistence of such a motion
are due to Belk--Connelly and Cheng--Tan--Zheng; see
[Cheng--Tan--Zheng, Theorem 2.1](https://arxiv.org/abs/1107.0140).

Take the four vectors `v_i` in `{+/-1}^3` with coordinate product `1`.
Fix these four sites and, for each ordered pair `i != j`, send

$$
v_j-v_i\longmapsto v_j+v_i.                              \tag{6}
$$

This is the depth-one outward-to-inward flap contraction, with the
regular simplex scaled by `sqrt(3)`. It has 16 distinct input sites and
10 distinct output sites; keep all 16 labels and add masses at coincident
images. The generated coordinates agree with the team's existing
[flap fixture](../gaussian_majorisation_rank_abel/flap_fixture.json).

The exact checker verifies all 120 pair inequalities, 78 tight pairs,
42 strict pairs, connectedness, paired affine rank six, and rigidity
rank 42 at **both** endpoints. The external theorem, not these rank
checks, supplies nonexistence of an `R^5` contracting motion. No Gaussian
hinge violation is claimed for this control.

In fact, apply Section 2 to this fixture. Any mesh extension retaining
its labels remains nonliftable in `R^5`, since restricting a hypothetical
motion to the original 16 labels would give the prohibited motion.
Thus the rigid-mesh test class itself contains the known obstruction to
the universal five-dimensional-motion strategy.

## 7. Scope and next frontier

This reduction licenses a focus on extreme finite maps **after support
enlargement** and even on rigid folded meshes, without a false Jensen
step for image positions. It does not license restriction to one fixed
atom count, one mesh, bounded fold depth, injective images, or a fixed
lower bound on each atom's mass. The source convex hull can stay fixed,
while mesh complexity and uniform sample size may grow.

The remaining mathematical task is the Gaussian hinge comparison for
arbitrary compatible tetrahedral fold patterns. Rigidity by itself
cannot supply the missing motion. None of the general positive classes
or negative searches inspected in the team refresh settle this class.

The new [common-set transfer and prior localization](../gaussian_prior_localization/PROOF.md)
result concerns optimization over laws on a fixed support. Its diffuse
optimizer example is compatible with Section 5: we approximate a strict
violation while enlarging a finite support, and assert neither exact
finite optimizer attainment nor a uniform atom bound.

The analytic proof uses classical extension and rigidity facts as made
explicit above. The checker establishes the finite controls only; it
does not implement Brehm extension, verify all meshes, integrate a
Gaussian hinge, or independently review the universal reduction.
